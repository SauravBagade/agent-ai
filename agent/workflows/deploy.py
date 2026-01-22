# agent/workflows/deploy.py

from agent.tools.docker_tool import DockerTool
from agent.tools.kubernetes_tool import KubernetesTool
from agent.tools.helm_tool import HelmTool
from agent.tools.terraform_tool import TerraformTool
from agent.tools.aws_tool import AWSTool
from agent.tools.helper_tool import HelperTool


class DeployWorkflow:
    """
    Deployment Workflow for multiple DevOps scenarios:

      Simple:
        - deploy nginx (docker)
        - deploy apache

      Kubernetes:
        - deploy nginx to prod namespace
        - deploy backend service

      Helm:
        - deploy chart
        - upgrade chart

      Terraform:
        - create eks cluster
        - apply infra modules

      Cloud:
        - bootstrap cluster with AWS + kubeconfig
    """

    def __init__(self, context=None, memory=None, llm=None):
        self.context = context
        self.memory = memory
        self.llm = llm

        self.docker = DockerTool()
        self.k8s = KubernetesTool()
        self.helm = HelmTool()
        self.tf = TerraformTool()
        self.aws = AWSTool()
        self.helper = HelperTool()

    def run(self, plan: dict):
        """
        plan dict structure (example):
        {
          "intent": "DEPLOY",
          "workflow": "deploy",
          "entities": {
            "app": "nginx",
            "namespace": "prod",
            "target": "docker|k8s|helm|terraform|cloud"
          }
        }
        """
        entities = plan.get("entities", {})
        app = entities.get("app")
        namespace = entities.get("namespace")
        target = entities.get("target") or "docker"

        # ---- DOCKER DEPLOY ----
        if target == "docker":
            app_norm = self.helper.normalize_app(app or "app")
            result = self.docker.run_container(app_norm)
            if self.context:
                self.context.update({
                    "workflow": "deploy",
                    "last_action": "docker-run",
                    "status": "ok"
                })
            return result

        # ---- KUBERNETES DEPLOY (YAML) ----
        elif target == "k8s":
            yaml_path = entities.get("manifest")
            if not yaml_path:
                return "[deploy-error] no k8s manifest provided."
            result = self.k8s.apply(yaml_path)
            if self.context:
                self.context.update({
                    "workflow": "deploy",
                    "last_action": "k8s-apply",
                    "namespace": namespace,
                    "status": "ok"
                })
            return result

        # ---- HELM DEPLOY ----
        elif target == "helm":
            chart = entities.get("chart")
            release = entities.get("release") or app or "app"
            if not chart:
                return "[deploy-error] no helm chart provided."
            result = self.helm.install(release, chart, namespace)
            if self.context:
                self.context.update({
                    "workflow": "deploy",
                    "last_action": "helm-install",
                    "namespace": namespace,
                    "status": "ok"
                })
            return result

        # ---- TERRAFORM DEPLOY ----
        elif target == "terraform":
            path = entities.get("path")
            if not path:
                return "[deploy-error] no terraform path provided."
            init = self.tf.init()
            plan = self.tf.plan()
            apply = self.tf.apply()
            return f"{init}\n{plan}\n{apply}"

        # ---- CLOUD BOOTSTRAP (EKS) ----
        elif target == "cloud":
            cloud = entities.get("cloud") or "aws"
            if cloud == "aws":
                cluster = entities.get("cluster") or "eks"
                # Update kubeconfig
                kube = self.aws.get_eks_kubeconfig(cluster)
                if self.context:
                    self.context.update({
                        "workflow": "deploy",
                        "cluster": cluster,
                        "cloud": "aws",
                        "status": "ok"
                    })
                return kube

        return f"[deploy-error] unsupported target '{target}'"
