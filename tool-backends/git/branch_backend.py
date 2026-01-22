# tool-backend/git/branch_backend.py

from .cli_backend import GitCLIBackend


class GitBranchBackend(GitCLIBackend):
    """
    Branch operations:
      - create
      - list
      - switch
      - delete
    """

    def create(self, path, name):
        return self._exec(["git", "branch", name], cwd=path)

    def list(self, path):
        return self._exec(["git", "branch", "-a"], cwd=path)

    def switch(self, path, name):
        return self._exec(["git", "checkout", name], cwd=path)

    def delete(self, path, name, force=False):
        cmd = ["git", "branch", "-D" if force else "-d", name]
        return self._exec(cmd, cwd=path)
