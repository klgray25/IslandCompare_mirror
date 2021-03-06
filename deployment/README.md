# IslandCompare deployment

Example deployments are provided in this folder for various destinations. For production use, it is recommended to create your own deployment recipe
using terraform modules provided in `../desinations`. Terraform is the deployment manager software used for all deployment destinations.

To install Terraform, check that your system's package manager provides it or download it [here](https://www.terraform.io/downloads.html).

## Run local

If you are running Docker on OSX (Mac), first see the [related subheading below](#osx-peculiarities). Ensure that you are running the most recent version of docker and that docker can
be [run without root privileges](https://docs.docker.com/engine/install/linux-postinstall/). Change the current working directory to `./docker`.
Modify `./changeme.auto.tfvars` with your custom values. You must at least set the `docker_gid` variable to a group id with write access
to `/var/run/docker.sock`. Run `stat /var/run/docker.sock` to show the owning group id.

Run the following to start an instance on your local computer using docker:

```shell script
terraform init
./deploy.sh
```

To run an analysis, download the [IslandCompare-CLI](https://raw.githubusercontent.com/brinkmanlab/islandcompare-cli/master/islandcompare.py) tool.
Terraform will have generated `./env.sh`; run `source ./env.sh` to configure the CLI tool. See
the [CLI ReadMe](https://github.com/brinkmanlab/islandcompare-cli/blob/master/README.md) for instructions on its use. The instructions will include
command line arguments for configuring host and api key, which can be ommitted as `./env.sh` configured them globally.

To visualize your data you can access it locally at http://localhost:8000/plugins/visualizations/islandcompare/static/index.html

Browse to http://localhost:8000/ to access the Galaxy deployment directly. When logging in, use the username "admin" and locate your admin password by running `terraform output -json` and identifying the value under "galaxy_admin_password".

To shut down this instance, run `./destroy.sh`. This will delete the instance, all of its data, and the container images. Docker may fail to unmount
CVMFS during shutdown; run `sudo fusermount -u ./microbedb/mount` if you encounter `transport endpoint is not connected` errors.

### OSX Peculiarities

OSX does not natively support Docker, it runs Docker within a Linux virtual machine. Due to this, mounting MicrobeDB via CVMFS following the instructions above will fail with an error.

To work around this CVMFS must be installed and configured manually. First ensure that [FUSE](http://osxfuse.github.io/) is enabled by
running `kextstat | grep -i fuse`. Download the [CVMFS package](https://ecsft.cern.ch/dist/cvmfs/cvmfs-2.8.0/cvmfs-2.8.0.pkg). Install the pkg and
reboot. Copy [../destinations/docker/cvmfs.config](../destinations/docker/cvmfs.config) to `/etc/cvmfs/default.local`.
Copy [./microbedb.brinkmanlab.ca.pub](./microbedb.brinkmanlab.ca.pub) to `/etc/cvmfs/keys/microbedb.brinkmanlab.ca.pub`. Ensure everything is
configured properly by running `sudo cvmfs_config chksetup`. You **MUST** mount the CVMFS repository under a shared folder as configured in your
Docker settings. By default, `/tmp` should be included as a shared folder, and you can mount the repository to `/tmp/microbedb`. Ensure `/tmp/microbedb`
exists and run `sudo mount -t cvmfs microbedb.brinkmanlab.ca /tmp/microbedb`.

Once CVMFS is configured and you can see the database files in the location you chose to mount the repository, add the following
to `changeme.auto.tfvars`:

```hcl
docker_gid = 0
microbedb_mount_path = "/tmp/microbedb"
docker_socket_path = "/run/host-services/docker.proxy.sock"
enable_CVMFS = false
```

The last modification you need to make is to allow group write access to the docker socket within containers. To do this, run the following:
```shell
docker run --rm -v /run/host-services/docker.proxy.sock:/run/host-services/docker.proxy.sock alpine chmod g+w /run/host-services/docker.proxy.sock
```

Mounting CVMFS and the above command need to be run any time you restart your system before you can run deploy.sh or submit analyses.
See https://github.com/docker/for-mac/issues/3431 for more information about the issue.

Appropriate resources [must be allocated](https://stackoverflow.com/a/50770267/15446750) to the Docker VM or OSX will randomly kill the application and tools during an analysis.
A minimum of 8GB of RAM and 16GB of swap space is required. It is recommended to provide as much swap space as possible to avoid out of memory issues.

## Deploy to cloud

Several terraform destinations have been configured. Select one from the `./destinations/` folder that you plan to use.
Modify `./changeme.auto.tfvars` with any custom values you like. Ensure you are authenticated with your cloud provider and that the required
environment variables are set for the respective terraform provider. Review the relevant cloud provider section below for additional configuration.
Once fully prepared, run `./deploy.sh` to deploy the application to the cloud.

### AWS

Select the region deployed to by exporting `export AWS_DEFAULT_REGION='us-west-2'` or creating an aws provider configuration block in the terraform
definitions. See [supported regions for EKS](https://docs.aws.amazon.com/general/latest/gr/eks.html) as not all regions support deployment. This
step is independent of the default region setting in the next step.

Install the [AWS CLI tool](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
and [aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html). Configure the aws cli tool by
running `aws configure` and fill in the requested info. Proceed with deployment.

Additionally:
Galaxy is deployed into an AWS EKS cluster. Run `aws-iam-authenticator token -i islandcompare --token-only` to get the required token for the
dashboard. Configure `kubectl` by running `aws eks --region us-west-2 update-kubeconfig --name islandcompare`. `--name` must match the value
of `instance` in changeme.auto.tfvars. Refer to the Kubernetes section for the remaining information.

### Azure

TODO

### Google Cloud

TODO

### OpenStack

TODO

### Kubernetes

All cloud deployments include a dashboard server that provides administrative control of the cluster. To access
it, [install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) and run `kubectl proxy` in a separate terminal.
Visit [here](http://localhost:8001/api/v1/namespaces/kube-system/services/https:dashboard-chart-kubernetes-dashboard:https/proxy/#/login) to access
the dashboard.

To check the state of the cluster run `kubectl describe node`.

### Existing Kubernetes cluster

Configure the Kubernetes terraform provider and deploy the `./destinations/k8s` module.

### Existing Nomad cluster

Configure the Nomad terraform provider and deploy the `./destinations/nomad` module.