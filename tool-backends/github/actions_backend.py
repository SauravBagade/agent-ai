# tool-backend/github/actions_backend.py

from .api_backend import GitHubAPIBackend


class GitHubActionsBackend(GitHubAPIBackend):
    """
    GitHub Actions CI/CD backend:
      - workflow runs
      - job logs
      - re-run workflows
      - cancel runs
    """

    def workflows(self, owner, repo):
        return self.get(f"repos/{owner}/{repo}/actions/workflows")

    def runs(self, owner, repo):
        return self.get(f"repos/{owner}/{repo}/actions/runs")

    def rerun(self, owner, repo, run_id):
        return self.post(f"repos/{owner}/{repo}/actions/runs/{run_id}/rerun", {})

    def cancel(self, owner, repo, run_id):
        return self.post(f"repos/{owner}/{repo}/actions/runs/{run_id}/cancel", {})
