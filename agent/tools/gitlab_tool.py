# agent/tools/gitlab_tool.py

import os
import requests


class GitLabTool:
    """
    GitLab Tool for interacting with GitLab's REST API.

    Supports:
      - list projects
      - list branches
      - list merge requests
      - pipeline status
      - pipeline logs (future)
      - trigger pipeline (CI/CD)

    Requires:
      GITLAB_TOKEN and optionally GITLAB_HOST
    """

    def __init__(self):
        self.token = os.getenv("GITLAB_TOKEN")
        self.user = os.getenv("GITLAB_USER")
        self.host = os.getenv("GITLAB_HOST", "https://gitlab.com")

        self.headers = {
            "PRIVATE-TOKEN": self.token
        } if self.token else {}

    # ---- LIST PROJECTS ----

    def list_projects(self, user: str = None):
        user = user or self.user
        if not user:
            return "[gitlab-error] No user specified."

        url = f"{self.host}/api/v4/users/{user}/projects"
        return self._get(url)

    # ---- LIST BRANCHES ----

    def list_branches(self, project_id: int):
        url = f"{self.host}/api/v4/projects/{project_id}/repository/branches"
        return self._get(url)

    # ---- LIST MERGE REQUESTS ----

    def list_mrs(self, project_id: int, state="opened"):
        url = f"{self.host}/api/v4/projects/{project_id}/merge_requests?state={state}"
        return self._get(url)

    # ---- MERGE REQUEST DETAILS ----

    def mr_details(self, project_id: int, mr_id: int):
        url = f"{self.host}/api/v4/projects/{project_id}/merge_requests/{mr_id}"
        return self._get(url)

    # ---- PIPELINES ----

    def list_pipelines(self, project_id: int):
        url = f"{self.host}/api/v4/projects/{project_id}/pipelines"
        return self._get(url)

    def pipeline_status(self, project_id: int):
        pipelines = self.list_pipelines(project_id)
        if isinstance(pipelines, str):
            return pipelines

        if pipelines:
            status = pipelines[0].get("status")
            return f"Pipeline status: {status}"
        return "No pipelines found."

    # ---- TRIGGER PIPELINE (CI/CD) ----

    def trigger_pipeline(self, project_id: int, ref="main", token=None):
        token = token or self.token
        if not token:
            return "[gitlab-error] Missing pipeline trigger token."

        url = f"{self.host}/api/v4/projects/{project_id}/trigger/pipeline"
        payload = {
            "ref": ref,
            "token": token
        }
        return self._post(url, payload)

    # ---- INTERNAL HTTP HELPERS ----

    def _get(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
            return f"[gitlab-error:{resp.status_code}] {resp.text}"
        except Exception as e:
            return f"[gitlab-connection-error] {str(e)}"

    def _post(self, url, payload):
        try:
            resp = requests.post(url, headers=self.headers, json=payload)
            if resp.status_code in (200, 201):
                return resp.json()
            elif resp.status_code == 204:
                return "Triggered pipeline."
            return f"[gitlab-error:{resp.status_code}] {resp.text}"
        except Exception as e:
            return f"[gitlab-connection-error] {str(e)}"

