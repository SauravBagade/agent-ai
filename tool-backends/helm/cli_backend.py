# tool-backends/helm/cli_backend.py

import subprocess


class HelmCLIBackend:
    """
    Base Helm backend for CLI execution.

    Supports core operations:
      - install
      - upgrade
      - rollback
      - uninstall
      - list releases
      - get values + manifests
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[helm-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[helm-missing] helm binary not installed."

    def install(self, release, chart, namespace=None, values=None):
        cmd = ["helm", "install", release, chart]
        if namespace:
            cmd += ["-n", namespace]
        if values:
            for file in values:
                cmd += ["-f", file]
        return self._exec(cmd)

    def upgrade(self, release, chart, namespace=None, values=None):
        cmd = ["helm", "upgrade", release, chart]
        if namespace:
            cmd += ["-n", namespace]
        if values:
            for file in values:
                cmd += ["-f", file]
        return self._exec(cmd)

    def rollback(self, release, revision=None, namespace=None):
        cmd = ["helm", "rollback", release]
        if revision:
            cmd.append(str(revision))
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    def uninstall(self, release, namespace=None):
        cmd = ["helm", "uninstall", release]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    def list(self, namespace=None):
        cmd = ["helm", "list", "--all"]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    def get_values(self, release, namespace=None):
        cmd = ["helm", "get", "values", release]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    def get_manifest(self, release, namespace=None):
        cmd = ["helm", "get", "manifest", release]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)
