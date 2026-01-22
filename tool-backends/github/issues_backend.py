# tool-backend/github/issues_backend.py

from .api_backend import GitHubAPIBackend


class GitHubIssuesBackend(GitHubAPIBackend):
    """
    Issue backend for lightweight project mgmt.
    """

    def list(self, owner, repo):
        return self.get(f"repos/{owner}/{repo}/issues")

    def create(self, owner, repo, title, body=""):
        return self.post(
            f"repos/{owner}/{repo}/issues",
            {"title": title, "body": body}
        )
