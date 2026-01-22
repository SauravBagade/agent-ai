# tool-backends/kubectl/logs_backend.py

import subprocess


class KubectlLogsBackend:
    """
    Logs backend for pod/service logs.

    Supports:
      - tail logs
      - container logs
      - namespace logs
      - previous logs (for CrashLoop)
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[logs-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[kubectl-missing]"

    def logs(self, pod, container=None, namespace=None, tail=None, previous=False):
        cmd = ["kubectl", "logs", pod]

        if container:
            cmd.append(container)

        if namespace:
            cmd += ["-n", namespace]

        if tail:
            cmd += ["--tail", str(tail)]

        if previous:
            cmd.append("--previous")

        return self._exec(cmd)
