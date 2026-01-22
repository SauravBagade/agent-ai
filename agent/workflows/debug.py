# agent/workflows/debug.py

from agent.tools.kubernetes_tool import KubernetesTool
from agent.tools.logging_tool import LoggingTool
from agent.tools.monitoring_tool import MonitoringTool
from agent.tools.cicd_tool import CICDTool
from agent.tools.helper_tool import HelperTool


class DebugWorkflow:
    """
    Debugging Workflow for SRE + DevOps troubleshooting.

    Performs multi-signal debugging:
      - kubectl describe
      - kubectl logs
      - metrics (Prometheus)
      - alerts (Alertmanager)
      - pipeline status (CI/CD)
      - correlation with hybrid LLM

    Outputs can be explained via cloud LLM for human clarity.
    """

    def __init__(self, context=None, memory=None, llm=None):
        self.context = context
        self.memory = memory
        self.llm = llm

        self.k8s = KubernetesTool()
        self.logging = LoggingTool()
        self.monitor = MonitoringTool()
        self.cicd = CICDTool()
        self.helper = HelperTool()

    def run(self, plan: dict):
        """
        Example plan:
        {
          "intent": "DEBUG",
          "workflow": "debug",
          "entities": {
            "app": "backend",
            "namespace": "prod",
            "provider": "github|gitlab",
            "repo": "my-app"
          }
        }
        """
        entities = plan.get("entities", {})
        app = entities.get("app")
        namespace = entities.get("namespace")
        provider = entities.get("provider")
        repo = entities.get("repo")

        output = []

        # ---- KUBERNETES DEBUG ----
        if app:
            pods = self.k8s.get_pods(namespace)
            output.append(f"[pods]\n{pods}")

            # logs from app
            logs = self.logging.service_logs(app, namespace)
            output.append(f"[logs]\n{logs}")

            # restarts
            restarts = self.monitor.pod_restarts(namespace)
            output.append(f"[restarts]\n{restarts}")

        # ---- PIPELINE DEBUG (CI/CD) ----
        if provider and repo:
            status = self.cicd.status(provider, repo)
            output.append(f"[pipeline]\n{status}")

        # ---- ALERTS ----
        alerts = self.monitor.list_alerts()
        output.append(f"[alerts]\n{alerts}")

        full_output = "\n\n".join(output)

        # ---- Hybrid LLM Explanation ----
        if self.llm:
            explained = self.llm.explain(f"debug results: {full_output}")
            self._update_context(status="analysis-complete", app=app, namespace=namespace)
            return explained

        self._update_context(status="raw-debug", app=app, namespace=namespace)
        return full_output

    def _update_context(self, status, app, namespace):
        if self.context:
            self.context.update({
                "workflow": "debug",
                "app": app,
                "namespace": namespace,
                "status": status
            })
