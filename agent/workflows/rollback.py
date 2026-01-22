# agent/workflows/rollback.py

from agent.tools.docker_tool import DockerTool
from agent.tools.kubernetes_tool import KubernetesTool
from agent.tools.helm_tool import HelmTool
from agent.tools.terraform_tool import TerraformTool
from agent.tools.helper_tool import HelperTool


class RollbackWorkflow:
    """
    Rollback Workflow for DevOps agent.

    Supports rollback types:
      - Docker container revert (manual stop/remove/re-run)
      - Helm rollback
      - Kubernetes undo via kubectl rollout
      - Terraform destroy (optional, safety enforced)
      - Git-based rollback (future)
      - CI/CD rollback (future)

    Rollback requires:
      - execution context
      - last successful deployment info
      - memory of version/tag/commit
    """

    def __init__(self, context=None, memory=None, safety=None, llm=None):
        self.context = context
        self.memory = memory
        self.safety = safety
        self.llm = llm

        self.docker = DockerTool()
        self.k8s = KubernetesTool()
        self.helm = HelmTool()
        self.tf = TerraformTool()
        self.helper = HelperTool()

    def run(self, plan: dict):
        """
        Plan example:
        {
          "intent": "ROLLBACK",
          "workflow": "rollback",
          "entities": {
            "target": "helm|k8s|docker|terraform",
            "release": "backend",
            "app": "backend",
            "namespace": "prod",
            "revision": 2
          }
        }
        """
        entities = plan.get("entities", {})
        target = entities.get("target") or "helm"
        app = entities.get("app")
        release = entities.get("release") or app
        namespace = entities.get("namespace")
        revision = entities.get("revision")

        # ---- DOCKER ROLLBACK (basic restart logic) ----
        if target == "docker":
            self.docker.stop_container(app)
            self.docker.remove_container(app)
            # Re-run using memory (image tag)
            image = None
            if self.memory:
                image = self.memory.get("image", app)
            result = self.docker.run_container(image or app)
            self._update_context("docker-rollback", namespace)
            return result

        # ---- KUBERNETES ROLLBACK ----
        if target == "k8s":
            # kubectl rollout undo deployment backend
            cmd = f"kubectl rollout undo deployment/{app}"
            result = self._shell(cmd)
            self._update_context("k8s-rollout", namespace)
            return result

        # ---- HELM ROLLBACK ----
        if target == "helm":
            if not revision:
                return "[rollback-error] no revision provided for helm."
            cmd_result = self.helm._exec(
                ["helm", "rollback", release, str(revision)] +
                (["-n", namespace] if namespace else [])
            )
            self._update_context("helm-rollback", namespace)
            return cmd_result

        # ---- TERRAFORM ROLLBACK (dangerous) ----
        if target == "terraform":
            if self.safety and not self.safety.approve_rollback():
                return "[rollback-blocked] safety denied terraform destroy"
            destroy = self.tf.destroy()
            self._update_context("terraform-destroy", namespace)
            return destroy

        return f"[rollback-error] unsupported target '{target}'"

    # ---- internal helpers ----

    def _update_context(self, action, namespace):
        if self.context:
            self.context.update({
                "workflow": "rollback",
                "last_action": action,
                "namespace": namespace,
                "status": "ok"
            })

    def _shell(self, cmd):
        import subprocess
        try:
            out = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except Exception as e:
            return f"[rollback-shell-error] {str(e)}"
