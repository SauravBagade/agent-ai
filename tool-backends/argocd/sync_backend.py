# tool-backend/argocd/sync_backend.py

from .cli_backend import ArgoCDCLIBackend


class ArgoCDSyncBackend(ArgoCDCLIBackend):
    """
    Sync backend:
      - sync app (GitOps reconciliation)
      - refresh app
    """

    def sync(self, name, prune=False):
        cmd = ["argocd", "app", "sync", name]
        if prune:
            cmd.append("--prune")
        return self._exec(cmd)

    def refresh(self, name):
        return self._exec(["argocd", "app", "refresh", name])
