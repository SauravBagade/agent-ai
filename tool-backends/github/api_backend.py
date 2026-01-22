# tool-backend/github/api_backend.py

import requests
import os


class GitHubAPIBackend:
    """
    Generic GitHub API backend using REST.
    Supports simple auth via token.
    """

    def __init__(self, token=None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"

        if not self.token:
            raise ValueError("GitHub token not provided or missing in env (GITHUB_TOKEN).")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

    def get(self, endpoint):
        r = requests.get(f"{self.base_url}/{endpoint}", headers=self._headers())
        return r.json()

    def post(self, endpoint, data):
        r = requests.post(f"{self.base_url}/{endpoint}", headers=self._headers(), json=data)
        return r.json()

    def patch(self, endpoint, data):
        r = requests.patch(f"{self.base_url}/{endpoint}", headers=self._headers(), json=data)
        return r.json()
