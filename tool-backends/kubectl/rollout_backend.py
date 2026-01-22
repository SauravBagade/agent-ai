# tool-backends/kubectl/rollout_backend.py

import subprocess


class KubectlRolloutBackend:
    """
    Handles Kubernetes rollout operations:
      - status
      - history
      - undo (rollback)
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[rollout-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[kubectl-missing]"

    def status(self, deployment, namespace=None):
        cmd = ["kubectl", "rollout", "status", f"deployment/{deployment}"]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    def undo(self, deployment, namespace=None):
        cmd = ["kubectl", "rollout", "undo", f"deployment/{deployment}"]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    def history(self, deployment, namespace=None):
        cmd = ["kubectl", "rollout", "history", f"deployment/{deployment}"]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)
