# tool-backend/git/status_backend.py

from .cli_backend import GitCLIBackend


class GitStatusBackend(GitCLIBackend):
    """
    Working tree status inspection.
    """

    def status(self, path):
        return self._exec(["git", "status", "-s"], cwd=path)

