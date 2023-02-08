from prefect.filesystems import GitHub
from my_project.flows import my_flow
from prefect.deployments import Deployment

deployment = Deployment.build_from_flow(
    flow=github_flow_green,
    name="example-deployment", 
    version=1, 
    work_queue_name="demo",
)
deployment.apply()

github_block = GitHub.load("zoom-git")
