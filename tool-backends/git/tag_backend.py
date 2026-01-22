# tool-backend/git/tag_backend.py

from .cli_backend import GitCLIBackend


class GitTagBackend(GitCLIBackend):
    """
    Tag backend for release automation + semver.
    """

    def list(self, path):
        return self._exec(["git", "tag", "-l"], cwd=path)

    def create(self, path, tag):
        return self._exec(["git", "tag", tag], cwd=path)

    def delete(self, path, tag):
        return self._exec(["git", "tag", "-d", tag], cwd=path)
 
