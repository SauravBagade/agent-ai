# tool-backend/argocd/rollout_backend.py

from .cli_backend import ArgoCDCLIBackend


class ArgoCDRolloutBackend(ArgoCDCLIBackend):
    """
    Progressive deployment backend:
      - stop / resume / rollback deployments
    """

    def rollback(self, name):
        return self._exec(["argocd", "app", "rollback", name])

    def terminate(self, name):
        return self._exec(["argocd", "app", "terminate-op", name])
