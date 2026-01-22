# agent/workflows/scale.py

from agent.tools.kubernetes_tool import KubernetesTool
from agent.tools.docker_tool import DockerTool
from agent.tools.helper_tool import HelperTool


class ScaleWorkflow:
    """
    Scale Workflow for operational DevOps/SRE use.

    Supports:
      - Kubernetes deployment scaling
      - Docker container scaling (simple multi-run)
      - future: HPA autoscaling
      - future: cost-aware scaling
      - future: metric-based scaling
    """

    def __init__(self, context=None, memory=None, llm=None):
        self.context = context
        self.memory = memory
        self.llm = llm

        self.k8s = KubernetesTool()
        self.docker = DockerTool()
        self.helper = HelperTool()

    def run(self, plan: dict):
        """
        Example plan:
        {
          "intent": "SCALE",
          "workflow": "scale",
          "entities": {
            "app": "backend",
            "namespace": "prod",
            "replicas": 3,
            "target": "k8s|docker"
          }
        }
        """
        entities = plan.get("entities", {})
        app = entities.get("app")
        namespace = entities.get("namespace")
        replicas = self.helper.safe_int(entities.get("replicas"), default=1)
        target = entities.get("target") or "k8s"

        # ---- KUBERNETES SCALE ----
        if target == "k8s":
            result = self.k8s.scale(app, replicas, namespace)
            self._update_context("k8s-scale", namespace, replicas)
            return result

        # ---- DOCKER SCALE (manual multi-run) ----
        if target == "docker":
            # stop existing container
            self.docker.stop_container(app)
            self.docker.remove_container(app)
            out = []
            for i in range(replicas):
                name = f"{app}-{i+1}"
                out.append(self.docker.run_container(name))
            self._update_context("docker-scale", namespace, replicas)
            return "\n".join(out)

        return f"[scale-error] unsupported target '{target}'"

    def _update_context(self, action, namespace, replicas):
        if self.context:
            self.context.update({
                "workflow": "scale",
                "last_action": action,
                "namespace": namespace,
                "replicas": replicas,
                "status": "ok"
            })
