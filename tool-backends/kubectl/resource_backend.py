# tool-backends/kubectl/resource_backend.py

import subprocess


class KubectlResourceBackend:
    """
    Resource backend for typical kubectl get/describe ops.

    Supports:
      - get (pods, services, deployments, nodes)
      - describe
      - delete
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[resource-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[kubectl-missing]"

    def get(self, resource, namespace=None, wide=True):
        cmd = ["kubectl", "get", resource]
        if namespace:
            cmd += ["-n", namespace]
        if wide:
            cmd += ["-o", "wide"]
        return self._exec(cmd)

    def describe(self, resource, name, namespace=None):
        cmd = ["kubectl", "describe", resource, name]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    def delete(self, resource, name, namespace=None):
        cmd = ["kubectl", "delete", resource, name]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)
