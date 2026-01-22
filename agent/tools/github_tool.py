# agent/tools/github_tool.py

import os
import requests


class GitHubTool:
    """
    GitHub Tool for interacting with GitHub REST API.

    Supports:
      - list repositories
      - list branches
      - list pull requests
      - get pull request details
      - get workflow runs (CI/CD)
      - get workflow status
      - trigger workflow dispatch (optional)

    Requires:
      GITHUB_TOKEN in environment
    """

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.user = os.getenv("GITHUB_USER")  # optional

        self.headers = {
            "Accept": "application/vnd.github+json",
        }

        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

        self.base = "https://api.github.com"

    # ---- LIST REPOS ----

    def list_repos(self, user: str = None):
        user = user or self.user
        if not user:
            return "[github-error] No user specified."

        url = f"{self.base}/users/{user}/repos"
        return self._get(url)

    # ---- LIST BRANCHES ----

    def list_branches(self, repo: str, user: str = None):
        user = user or self.user
        if not user:
            return "[github-error] No user specified."

        url = f"{self.base}/repos/{user}/{repo}/branches"
        return self._get(url)

    # ---- LIST PULL REQUESTS ----

    def list_prs(self, repo: str, user: str = None, state="open"):
        user = user or self.user
        if not user:
            return "[github-error] No user specified."

        url = f"{self.base}/repos/{user}/{repo}/pulls?state={state}"
        return self._get(url)

    # ---- PR DETAILS ----

    def pr_details(self, repo: str, pr_number: int, user: str = None):
        user = user or self.user
        if not user:
            return "[github-error] No user specified."

        url = f"{self.base}/repos/{user}/{repo}/pulls/{pr_number}"
        return self._get(url)

    # ---- WORKFLOW RUNS (CI/CD) ----

    def get_workflow_runs(self, repo: str, user: str = None):
        user = user or self.user
        if not user:
            return "[github-error] No user specified."

        url = f"{self.base}/repos/{user}/{repo}/actions/runs"
        return self._get(url)

    # ---- WORKFLOW STATUS (CI/CD) ----

    def check_workflow_status(self, repo: str, user: str = None):
        runs = self.get_workflow_runs(repo, user)
        if isinstance(runs, str):
            return runs

        if "workflow_runs" in runs and runs["workflow_runs"]:
            latest = runs["workflow_runs"][0]
            status = latest.get("conclusion") or latest.get("status")
            return f"Workflow status: {status}"
        return "No workflow runs found."

    # ---- TRIGGER WORKFLOW (Optional) ----

    def trigger_workflow(self, repo: str, workflow: str, ref="main", user: str = None):
        user = user or self.user
        if not user:
            return "[github-error] No user specified."

        url = f"{self.base}/repos/{user}/{repo}/actions/workflows/{workflow}/dispatches"
        payload = {"ref": ref}
        return self._post(url, payload)

    # ---- INTERNAL HTTP HELPERS ----

    def _get(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
            return f"[github-error:{resp.status_code}] {resp.text}"
        except Exception as e:
            return f"[github-connection-error] {str(e)}"

    def _post(self, url, payload):
        try:
            resp = requests.post(url, headers=self.headers, json=payload)
            if resp.status_code in (200, 201, 204):
                return "Triggered workflow successfully."
            return f"[github-error:{resp.status_code}] {resp.text}"
        except Exception as e:
            return f"[github-connection-error] {str(e)}"
