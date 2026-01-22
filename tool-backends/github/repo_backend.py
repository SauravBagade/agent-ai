# tool-backend/github/repo_backend.py

from .api_backend import GitHubAPIBackend


class GitHubRepoBackend(GitHubAPIBackend):
    """
    Repository operations:
      - get repo info
      - list branches
      - list files
    """

    def info(self, owner, repo):
        return self.get(f"repos/{owner}/{repo}")

    def branches(self, owner, repo):
        return self.get(f"repos/{owner}/{repo}/branches")

    def contents(self, owner, repo, path=""):
        return self.get(f"repos/{owner}/{repo}/contents/{path}")
