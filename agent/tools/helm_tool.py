# agent/tools/helm_tool.py

import subprocess


class HelmTool:
    """
    Helm Tool for managing Helm charts on Kubernetes clusters.

    Supports:
      - helm install
      - helm upgrade
      - helm uninstall
      - helm list
      - helm template
      - helm repo add/update
      - helm rollback (future)

    Works with:
      - EKS
      - GKE
      - AKS
      - Minikube
      - K3s
      - Kind
    """

    # ---- INSTALL ----

    def install(self, release: str, chart: str, namespace: str = None, values: str = None):
        cmd = ["helm", "install", release, chart]

        if namespace:
            cmd.extend(["-n", namespace])

        if values:
            cmd.extend(["-f", values])

        return self._exec(cmd)

    # ---- UPGRADE ----

    def upgrade(self, release: str, chart: str, namespace: str = None, values: str = None):
        cmd = ["helm", "upgrade", release, chart]

        if namespace:
            cmd.extend(["-n", namespace])

        if values:
            cmd.extend(["-f", values])

        return self._exec(cmd)

    # ---- UNINSTALL ----

    def uninstall(self, release: str, namespace: str = None):
        cmd = ["helm", "uninstall", release]

        if namespace:
            cmd.extend(["-n", namespace])

        return self._exec(cmd)

    # ---- LIST RELEASES ----

    def list(self, namespace: str = None):
        cmd = ["helm", "list"]

        if namespace:
            cmd.extend(["-n", namespace])

        return self._exec(cmd)

    # ---- TEMPLATE (local rendering) ----

    def template(self, chart: str, values: str = None):
        cmd = ["helm", "template", chart]

        if values:
            cmd.extend(["-f", values])

        return self._exec(cmd)

    # ---- REPO ADD ----

    def repo_add(self, name: str, url: str):
        cmd = ["helm", "repo", "add", name, url]
        return self._exec(cmd)

    # ---- REPO UPDATE ----

    def repo_update(self):
        cmd = ["helm", "repo", "update"]
        return self._exec(cmd)

    # ---- INTERNAL EXECUTE ----

    def _exec(self, cmd):
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return result.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[helm-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[helm-not-installed] helm CLI not found."
