# tool-backend/argocd/diff_backend.py

from .cli_backend import ArgoCDCLIBackend


class ArgoCDDiffBackend(ArgoCDCLIBackend):
    """
    Diff backend (Git vs Deployed cluster)
    """

    def diff(self, name):
        return self._exec(["argocd", "app", "diff", name])
