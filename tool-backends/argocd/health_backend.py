# tool-backend/argocd/health_backend.py

from .cli_backend import ArgoCDCLIBackend


class ArgoCDHealthBackend(ArgoCDCLIBackend):
    """
    Health backend for rollout & reconciliation status.
    """

    def health(self, name):
        return self._exec(["argocd", "app", "get", name, "--health"])
