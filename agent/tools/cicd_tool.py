# agent/tools/cicd_tool.py

from agent.tools.github_tool import GitHubTool
from agent.tools.gitlab_tool import GitLabTool


class CICDTool:
    """
    Unified CI/CD abstraction layer for:
      - GitHub Actions
      - GitLab CI
      - (future) Jenkins
      - (future) ArgoCD
      - (future) Tekton

    Supports:
      - check pipeline status
      - list pipeline runs
      - correlate failures
      - trigger pipelines

    Workflows will not need to know whether CI/CD is GitHub or GitLab.
    """

    def __init__(self):
        self.github = GitHubTool()
        self.gitlab = GitLabTool()

    # ---- UNIFIED STATUS ----

    def status(self, provider: str, repo_or_id: str):
        """
        provider: github | gitlab
        repo_or_id:
          - for GitHub: repo name
          - for GitLab: project_id
        """

        provider = provider.lower()

        if provider == "github":
            return self.github.check_workflow_status(repo_or_id)

        if provider == "gitlab":
            try:
                project_id = int(repo_or_id)
                return self.gitlab.pipeline_status(project_id)
            except ValueError:
                return "[cicd-error] GitLab requires project_id integer"

        return f"[cicd-error] unknown provider '{provider}'"

    # ---- LIST RUNS ----

    def list_runs(self, provider: str, repo_or_id: str):
        provider = provider.lower()

        if provider == "github":
            return self.github.get_workflow_runs(repo_or_id)

        if provider == "gitlab":
            try:
                project_id = int(repo_or_id)
                return self.gitlab.list_pipelines(project_id)
            except ValueError:
                return "[cicd-error] GitLab requires project_id integer"

        return f"[cicd-error] unknown provider '{provider}'"

    # ---- TRIGGER ----

    def trigger(self, provider: str, repo_or_id: str, ref: str = "main"):
        provider = provider.lower()

        if provider == "github":
            # need workflow filename for GH dispatch
            return "[cicd-info] GitHub trigger requires workflow filename."

        if provider == "gitlab":
            try:
                project_id = int(repo_or_id)
                return self.gitlab.trigger_pipeline(project_id, ref)
            except ValueError:
                return "[cicd-error] GitLab requires project_id integer"

        return f"[cicd-error] unknown provider '{provider}'"

    # ---- CORRELATE FAILURE (HYBRID LLM) ----

    def analyze_failure(self, provider: str, repo_or_id: str, llm=None):
        """
        High-level failure reasoning using hybrid LLM.
        """

        runs = self.list_runs(provider, repo_or_id)

        if isinstance(runs, str):
            return runs

        if not runs:
            return "No pipeline runs found."

        # extract latest run from provider-specific format
        if provider == "github":
            latest = runs.get("workflow_runs", [{}])[0]
            info = f"status={latest.get('conclusion')}, head={latest.get('head_branch')}"
        elif provider == "gitlab":
            latest = runs[0]
            info = f"status={latest.get('status')}, ref={latest.get('ref')}"
        else:
            return f"[cicd-error] unknown provider '{provider}'"

        if llm:
            # cloud LLM gives explanation
            return llm.explain(f"pipeline failed info: {info}")

        return info
