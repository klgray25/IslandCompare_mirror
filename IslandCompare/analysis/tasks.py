from __future__ import absolute_import, unicode_literals
from celery import shared_task
from analysis.models import AnalysisComponent
from analysis import components
from analysis.pipeline import PipelineSerializer
import logging


class PipelineComponentFactory(object):
    @staticmethod
    def create_component(name):
        if name == "setup_gbk":
            return components.SetupGbkPipelineComponent()
        if name == "gbk_metadata":
            return components.GbkMetadataComponent()
        if name == "parsnp":
            return components.ParsnpPipelineComponent()
        if name == "mauve":
            return components.MauvePipelineComponent()
        if name == "sigi":
            return components.SigiHMMPipelineComponent()
        if name == "islandpath":
            return components.IslandPathPipelineComponent()
        raise(RuntimeError("Given component does not exist: {}".format(name)))


logger = logging.getLogger(__name__)


def run_pipeline_wrapper(self, pipeline):
    task = run_pipeline.s(PipelineSerializer.serialize(pipeline)).apply_async()
    logger.info("Job scheduled with celery task id: {}".format(task.task_id))
    return task


@shared_task(bind=True)
def run_pipeline(self, serialized_pipeline):
    logger.info("Begin scheduling of pipeline components with celery task id: {}".format(self.request.id))
    pipeline = PipelineSerializer.deserialize(serialized_pipeline, PipelineComponentFactory())
    pipeline.analysis.celery_task_id = self.request.id
    pipeline.analysis.save()

    task_chain = None

    for component in pipeline.pipeline_components:
        if task_chain is None:
            task_chain = run_pipeline_component.s(serialized_pipeline, pipeline.analysis.id, component.name)
        else:
            task_chain.link(run_pipeline_component.s(pipeline.analysis.id, component.name))

    logger.info("End scheduling of pipeline components with celery task id: {}".format(self.request.id))
    return task_chain.apply_async()


@shared_task(bind=True)
def run_pipeline_component(self, report, analysis_id, pipeline_component_name):
    pipeline_component = PipelineComponentFactory.create_component(pipeline_component_name)
    logger.info("Attempting to run component: {} for analysis with id: {}".format(pipeline_component_name,
                                                                                   analysis_id))

    analysis_component = AnalysisComponent.objects.get(analysis__id=analysis_id,
                                                       type__name=pipeline_component.name)
    analysis_component.celery_task_id = self.request.id
    analysis_component.save()

    return pipeline_component.run(report)
