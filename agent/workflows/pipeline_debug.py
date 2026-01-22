# agent/workflows/pipeline_debug.py

from agent.tools.cicd_tool import CICDTool
from agent.tools.logging_tool import LoggingTool
from agent.tools.monitoring_tool import MonitoringTool
from agent.tools.helper_tool import HelperTool


class PipelineDebugWorkflow:
    """
    Pipeline Debug Workflow for CI/CD troubleshooting.

    Uses:
      - CICD status
      - CICD runs
      - logs (future: job logs)
      - anomaly & failure pattern analysis via Hybrid LLM

    Supports CI/CD providers:
      - GitHub Actions
      - GitLab CI
      - future: Jenkins / ArgoCD / Tekton / Bitbucket
    """

    def __init__(self, context=None, memory=None, llm=None):
        self.context = context
        self.memory = memory
        self.llm = llm

        self.cicd = CICDTool()
        self.logging = LoggingTool()
        self.monitor = MonitoringTool()
        self.helper = HelperTool()

    def run(self, plan: dict):
        """
        Example plan:

        {
          "intent": "DEBUG",
          "workflow": "pipeline_debug",
          "entities": {
            "provider": "github|gitlab",
            "repo": "backend",
            "project_id": 123,       (gitlab)
            "branch": "main",
            "namespace": "prod"
          }
        }
        """
        entities = plan.get("entities", {})
        provider = entities.get("provider")
        repo = entities.get("repo")
        project_id = entities.get("project_id")
        branch = entities.get("branch")
        namespace = entities.get("namespace")

        output = []

        # ---- PIPELINE STATUS ----
        if provider and repo:
            status = self.cicd.status(provider, repo)
            output.append(f"[pipeline-status]\n{status}")

            runs = self.cicd.list_runs(provider, repo)
            output.append(f"[pipeline-runs]\n{runs}")

        elif provider and project_id:
            status = self.cicd.status(provider, str(project_id))
            output.append(f"[pipeline-status]\n{status}")

            runs = self.cicd.list_runs(provider, str(project_id))
            output.append(f"[pipeline-runs]\n{runs}")

        else:
            return "[pipeline-debug-error] missing provider + repo/project_id"

        # ---- ALERT / METRICS CONTEXT (Optional) ----
        alerts = self.monitor.list_alerts()
        output.append(f"[alerts]\n{alerts}")

        # Future: fetch pipeline logs (GH/GitLab artifacts)

        raw_output = "\n\n".join(output)

        # ---- EXPLANATION VIA LLM ----
        if self.llm:
            explanation = self.llm.explain(
                f"Pipeline debug info: {raw_output}"
            )
            self._update_context(provider, repo or project_id)
            return explanation

        self._update_context(provider, repo or project_id)
        return raw_output

    def _update_context(self, provider, repo):
        if self.context:
            self.context.update({
                "workflow": "pipeline_debug",
                "provider": provider,
                "repo": repo,
                "status": "ok"
            })
