# tool-backend/git/remote_backend.py

from .cli_backend import GitCLIBackend


class GitRemoteBackend(GitCLIBackend):
    """
    Remote backend:
      - add remote
      - push
      - pull
      - fetch
    """

    def add(self, path, name, url):
        return self._exec(["git", "remote", "add", name, url], cwd=path)

    def push(self, path, remote="origin", branch="main"):
        return self._exec(["git", "push", remote, branch], cwd=path)

    def pull(self, path, remote="origin", branch="main"):
        return self._exec(["git", "pull", remote, branch], cwd=path)

    def fetch(self, path, remote="origin"):
        return self._exec(["git", "fetch", remote], cwd=path)
