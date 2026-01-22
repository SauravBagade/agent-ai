# tool-backend/git/diff_backend.py

from .cli_backend import GitCLIBackend


class GitDiffBackend(GitCLIBackend):
    """
    Diff backend used for CI/CD + pipelines + approvals.
    """

    def diff(self, path, staged=False):
        cmd = ["git", "diff"]
        if staged:
            cmd.append("--staged")
        return self._exec(cmd, cwd=path)

    def diff_commits(self, path, commit_a, commit_b):
        return self._exec(["git", "diff", commit_a, commit_b], cwd=path)
