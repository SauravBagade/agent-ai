# tool-backend/git/commit_backend.py

from .cli_backend import GitCLIBackend


class GitCommitBackend(GitCLIBackend):
    """
    Commit operations:
      - add
      - commit
      - amend
    """

    def add(self, path, files="."):
        return self._exec(["git", "add", files], cwd=path)

    def commit(self, path, message):
        return self._exec(["git", "commit", "-m", message], cwd=path)

    def amend(self, path, message=None):
        cmd = ["git", "commit", "--amend"]
        if message:
            cmd += ["-m", message]
        return self._exec(cmd, cwd=path)

