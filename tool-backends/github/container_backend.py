# tool-backend/github/container_backend.py

from .api_backend import GitHubAPIBackend


class GitHubContainerBackend(GitHubAPIBackend):
    """
    Backend for GHCR container registry.
    """

    def list_images(self, owner, package):
        return self.get(f"users/{owner}/packages/container/{package}/versions")
