# agent/workflows/upgrade.py

from agent.tools.helm_tool import HelmTool
from agent.tools.kubernetes_tool import KubernetesTool
from agent.tools.docker_tool import DockerTool
from agent.tools.terraform_tool import TerraformTool
from agent.tools.helper_tool import HelperTool


class UpgradeWorkflow:
    """
    Upgrade Workflow for progressive deployments.

    Supports:
      - Helm upgrade
      - Kubernetes apply upgrade
      - Docker image upgrade
      - Terraform infra upgrade (plan + apply with safety)

    Upgrade features:
      - version / chart / tag aware
      - memory can store previous version (for rollback)
      - context tracks upgrade phase
    """

    def __init__(self, context=None, memory=None, safety=None, llm=None):
        self.context = context
        self.memory = memory
        self.safety = safety
        self.llm = llm

        self.helm = HelmTool()
        self.k8s = KubernetesTool()
        self.docker = DockerTool()
        self.tf = TerraformTool()
        self.helper = HelperTool()

    def run(self, plan: dict):
        """
        Example plan:
        {
          "intent": "UPGRADE",
          "workflow": "upgrade",
          "entities": {
            "app": "backend",
            "target": "helm|k8s|docker|terraform",
            "version": "1.2.3",
            "namespace": "prod",
            "chart": "backend/chart"
          }
        }
        """

        entities = plan.get("entities", {})
        app = entities.get("app")
        target = entities.get("target") or "helm"
        namespace = entities.get("namespace")
        version = entities.get("version")
        chart = entities.get("chart")

        # ---- HELM UPGRADE ----
        if target == "helm":
            if not chart:
                return "[upgrade-error] helm requires chart"
            result = self.helm.upgrade(app, chart, namespace)
            self._store_memory(app, version, target)
            self._update_context("helm-upgrade", namespace, version)
            return result

        # ---- K8S MANIFEST UPGRADE ----
        if target == "k8s":
            manifest = entities.get("manifest")
            if not manifest:
                return "[upgrade-error] k8s requires manifest"
            result = self.k8s.apply(manifest)
            self._store_memory(app, version, target)
            self._update_context("k8s-upgrade", namespace, version)
            return result

        # ---- DOCKER UPGRADE ----
        if target == "docker":
            image = f"{app}:{version}" if version else app
            # stop → remove → run new
            self.docker.stop_container(app)
            self.docker.remove_container(app)
            result = self.docker.run_container(image)
            self._store_memory(app, version, target)
            self._update_context("docker-upgrade", namespace, version)
            return result

        # ---- TERRAFORM UPGRADE (plan + apply) ----
        if target == "terraform":
            path = entities.get("path")
            if not path:
                return "[upgrade-error] terraform requires path"
            init = self.tf.init()
            plan = self.tf.plan()
            if self.safety and not self.safety.approve_upgrade(plan):
                return "[upgrade-blocked] safety denied terraform apply"
            apply = self.tf.apply()
            self._store_memory(app, version, target)
            self._update_context("terraform-upgrade", namespace, version)
            return f"{init}\n{plan}\n{apply}"

        return f"[upgrade-error] unsupported target '{target}'"

    # ---- MEMORY + CONTEXT ----

    def _store_memory(self, app, version, target):
        if not self.memory:
            return
        previous = self.memory.get(f"{app}.version")
        self.memory[f"{app}.version"] = version or previous or "latest"
        self.memory[f"{app}.target"] = target

    def _update_context(self, action, namespace, version):
        if self.context:
            self.context.update({
                "workflow": "upgrade",
                "last_action": action,
                "namespace": namespace,
                "version": version,
                "status": "ok"
            })
