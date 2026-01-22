# tool-backend/argocd/app_backend.py

from .cli_backend import ArgoCDCLIBackend


class ArgoCDAppBackend(ArgoCDCLIBackend):
    """
    Application management backend:
      - list apps
      - create app
      - delete app
      - show app details
    """

    def list(self):
        return self._exec(["argocd", "app", "list"])

    def create(self, name, repo, path, dest_server, dest_ns):
        return self._exec([
            "argocd", "app", "create", name,
            "--repo", repo,
            "--path", path,
            "--dest-server", dest_server,
            "--dest-namespace", dest_ns
        ])

    def delete(self, name):
        return self._exec(["argocd", "app", "delete", name, "--yes"])

    def get(self, name):
        return self._exec(["argocd", "app", "get", name])
