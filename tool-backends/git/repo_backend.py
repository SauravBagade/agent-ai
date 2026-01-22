# tool-backend/git/repo_backend.py

from .cli_backend import GitCLIBackend


class GitRepoBackend(GitCLIBackend):
    """
    Repository-level backend:
      - clone
      - init
      - fetch
    """

    def clone(self, url, path):
        return self._exec(["git", "clone", url, path])

    def init(self, path):
        return self._exec(["git", "init"], cwd=path)

    def fetch(self, path):
        return self._exec(["git", "fetch"], cwd=path)
