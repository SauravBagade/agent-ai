# tool-backends/helm/release_backend.py

import subprocess


class HelmReleaseBackend:
    """
    Release inspection backend:
      - history
      - status
      - revision
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[helm-release-error] {e.output.decode('utf-8').strip()}"

    def history(self, release, namespace=None):
        cmd = ["helm", "history", release]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    def status(self, release, namespace=None):
        cmd = ["helm", "status", release]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)
