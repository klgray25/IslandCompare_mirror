from analysis.pipeline import PipelineComponent
from analysis.models import Analysis
from tempfile import mkdtemp, NamedTemporaryFile
from shutil import rmtree
from Bio import SeqIO, Phylo
import os
from django.conf import settings
import subprocess
from io import StringIO
import csv


class SetupGbkPipelineComponent(PipelineComponent):
    name = "setup_gbk"
    result_types = ["gbk_paths"]

    def analysis(self, report):
        analysis_entry = Analysis.objects.get(id=report['analysis'])
        genomes = analysis_entry.genomes

        report['gbk_paths'] = dict()
        for genome in genomes.all():
            report['gbk_paths'][genome.id] = genome.gbk.path


class ParsnpPipelineComponent(PipelineComponent):
    name = "parsnp"
    dependencies = ["gbk_paths"]
    result_types = ["newick"]
    temp_dir_path = None
    output_dir = "temp/parsnp/"
    temp_results_dir = None
    PARSNP_PATH = settings.PARSNP_PATH

    @staticmethod
    def convert_gbk_to_fna(input_path, output_path):
        input_handle = open(input_path, "r")
        output_handle = open(output_path, "w")

        for seq_record in SeqIO.parse(input_handle, "genbank"):
            output_handle.write(">%s %s\n%s\n" % (
                seq_record.id,
                seq_record.description,
                seq_record.seq))

        output_handle.close()
        input_handle.close()

    @staticmethod
    def parse_newick(input_path):
        tree = Phylo.read(input_path, 'newick')
        terminals = tree.get_terminals()

        for leaf in terminals:
            leaf.name = leaf.name.split('.')[0]

        processed_tree = StringIO()
        Phylo.write(tree, processed_tree, "newick")
        output = processed_tree.getvalue()
        processed_tree.close()

        return output

    def setup(self, report):
        self.temp_dir_path = mkdtemp()
        for gbk_id in report["gbk_paths"]:
            gbk_path = report["gbk_paths"][gbk_id]
            self.convert_gbk_to_fna(gbk_path,
                                    self.temp_dir_path+"/"+str(gbk_id)+".fna")

    def analysis(self, report):
        self.temp_results_dir = self.output_dir + str(report["analysis"])
        script_file = NamedTemporaryFile(delete=True)
        with open(script_file.name, 'w') as script:
            script.write("#!/bin/bash\n")
            script.write(self.PARSNP_PATH + " -r ! -d " + self.temp_dir_path +
                         " -o " + self.temp_results_dir + " -c YES")
            script.close()

        os.chmod(script_file.name, 0o0777)
        script_file.file.close()
        os.mkdir(self.temp_results_dir, 0o777)
        with open(self.temp_results_dir+"/logs", 'w') as logs:
            subprocess.check_call(script_file.name, stdout=logs)
        script_file.close()

        report["newick"] = self.parse_newick(self.temp_results_dir + "/parsnp.tree")

    def cleanup(self):
        if self.temp_dir_path is not None and os.path.exists(self.temp_dir_path):
            rmtree(self.temp_dir_path)
        if self.temp_results_dir is not None and os.path.exists(self.temp_results_dir):
            rmtree(self.temp_results_dir)


class MauvePipelineComponent(PipelineComponent):
    name = "mauve"
    dependencies = ["newick", "gbk_paths"]
    result_types = ["alignment"]
    MAUVE_PATH = settings.MAUVE_PATH
    output_dir = "temp/mauve/"
    temp_dir_path = None
    backbone_file_name = "pairwise.backbone"
    minimum_homologous_region_size = 50

    def parse_mauve_pairwise_backbone(self, backbone_file):
        homologous_regions = []

        with open(backbone_file) as backbone:
            tsv_reader = csv.reader(backbone, delimiter='\t')
            next(tsv_reader)
            for row in tsv_reader:
                top_start = int(row[0])
                top_end = int(row[1])
                bottom_start = int(row[2])
                bottom_end = int(row[3])

                if abs(top_start - top_end) >= self.minimum_homologous_region_size \
                        and abs(bottom_start - bottom_end) >= self.minimum_homologous_region_size:
                    homologous_regions.append([top_start, top_end, bottom_start, bottom_end])

        return homologous_regions

    def mauve_subprocess(self, working_dir, gbk_list):
        absolute_working_dir = os.path.abspath(working_dir)
        scratch_path1 = absolute_working_dir + "/temp1"
        scratch_path2 = absolute_working_dir + "/temp2"
        os.mkdir(scratch_path1)
        os.mkdir(scratch_path2)

        script_file = NamedTemporaryFile(delete=True)
        mauve_absolute_path = os.path.abspath(self.MAUVE_PATH)

        with open(script_file.name, 'w') as script:
            script.write("#!/bin/bash\n")
            script.write(mauve_absolute_path + " --output=/dev/null  --scratch-path-1=" + scratch_path1
                         + " --scratch-path-2=" + scratch_path2 + " --backbone-output="
                         + absolute_working_dir + "/" + self.backbone_file_name + " ")

            for sequence in gbk_list:
                script.write(sequence+" ")
            script.close()

        os.chmod(script_file.name, 0o0755)
        script_file.file.close()

        with open(working_dir + "/logs", 'w') as logs:
            subprocess.check_call(script_file.name, cwd=working_dir, stdout=logs)
        script_file.close()

    def retrieve_mauve_results(self, backbone_list):
        merged_mauve_results = []

        for backbone in backbone_list:
            merged_mauve_results.append(self.parse_mauve_pairwise_backbone(backbone))

        return merged_mauve_results

    def setup(self, report):
        self.temp_dir_path = self.output_dir + str(report["analysis"])
        os.mkdir(self.temp_dir_path, 0o777)

    def analysis(self, report):
        tree = Phylo.read(StringIO(report["newick"]), 'newick')
        ordered_genome_ids = [int(clade.name) for clade in tree.get_terminals(order='preorder')]
        results_list = []

        for sequence_counter in range(len(ordered_genome_ids) - 1):
            first_genome_id = ordered_genome_ids[sequence_counter]
            second_genome_id = ordered_genome_ids[sequence_counter + 1]

            first_gbk_path = report["gbk_paths"][first_genome_id]
            second_gbk_path = report["gbk_paths"][second_genome_id]

            sub_results_dir = self.temp_dir_path + "/" + str(sequence_counter) + "/"
            os.mkdir(sub_results_dir, 0o777)
            results_list.append(sub_results_dir + self.backbone_file_name)

            self.mauve_subprocess(sub_results_dir,
                                  [first_gbk_path, second_gbk_path])

        report["alignment"] = self.retrieve_mauve_results(results_list)

    def cleanup(self):
        if self.temp_dir_path is not None and os.path.exists(self.temp_dir_path):
            rmtree(self.temp_dir_path)
