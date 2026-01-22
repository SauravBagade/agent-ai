# tool-backend/github/artifacts_backend.py

from .api_backend import GitHubAPIBackend


class GitHubArtifactsBackend(GitHubAPIBackend):
    """
    Build artifact backend for CI pipelines.
    """

    def list(self, owner, repo):
        return self.get(f"repos/{owner}/{repo}/actions/artifacts")
