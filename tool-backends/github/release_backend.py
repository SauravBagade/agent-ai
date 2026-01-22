# tool-backend/github/release_backend.py

from .api_backend import GitHubAPIBackend


class GitHubReleaseBackend(GitHubAPIBackend):
    """
    Release backend for semantic release automation.
    """

    def list(self, owner, repo):
        return self.get(f"repos/{owner}/{repo}/releases")

    def create(self, owner, repo, tag, body=""):
        return self.post(
            f"repos/{owner}/{repo}/releases",
            {"tag_name": tag, "body": body}
        )
