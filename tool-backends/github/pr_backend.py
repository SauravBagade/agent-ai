# tool-backend/github/pr_backend.py

from .api_backend import GitHubAPIBackend


class GitHubPRBackend(GitHubAPIBackend):
    """
    Pull Request operations:
      - list
      - create
      - merge
      - close
      - reviews (future)
    """

    def list(self, owner, repo):
        return self.get(f"repos/{owner}/{repo}/pulls")

    def create(self, owner, repo, title, head, base):
        return self.post(
            f"repos/{owner}/{repo}/pulls",
            {
                "title": title,
                "head": head,
                "base": base
            }
        )

    def merge(self, owner, repo, pr_number):
        return self.put(f"repos/{owner}/{repo}/pulls/{pr_number}/merge")

    def close(self, owner, repo, pr_number):
        return self.patch(
            f"repos/{owner}/{repo}/pulls/{pr_number}",
            {"state": "closed"}
        )
