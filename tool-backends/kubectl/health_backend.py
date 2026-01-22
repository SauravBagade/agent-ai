# tool-backends/kubectl/health_backend.py

import subprocess


class KubectlHealthBackend:
    """
    Health backend for Kubernetes SRE diagnostics.

    Supports:
      - node health
      - pod readiness/liveness
      - restart counts (future)
      - events (future)
      - condition checks (future)
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[health-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[kubectl-missing]"

    def nodes(self):
        return self._exec(["kubectl", "get", "nodes", "-o", "wide"])

    def pods(self, namespace=None):
        cmd = ["kubectl", "get", "pods", "-o", "wide"]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)
