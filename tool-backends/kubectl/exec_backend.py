# tool-backends/kubectl/exec_backend.py

import subprocess


class KubectlExecBackend:
    """
    Exec backend for executing commands inside pods.

    Use cases:
      - debug pod
      - inspect runtime
      - shell access
      - test connectivity
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[exec-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[kubectl-missing]"

    def exec(self, pod, command, namespace=None):
        if isinstance(command, str):
            command = command.split()

        cmd = ["kubectl", "exec", "-it", pod]

        if namespace:
            cmd += ["-n", namespace]

        cmd += ["--"] + command
        return self._exec(cmd)
