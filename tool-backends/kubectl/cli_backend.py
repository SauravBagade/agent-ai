# tool-backends/kubectl/cli_backend.py

import subprocess


class KubectlCLIBackend:
    """
    Low-level kubectl backend for DevOps/SRE operations.

    Supports:
      - apply
      - get/describe
      - delete
      - logs
      - exec
      - rollout
      - scale
      - namespaces
      - contexts

    Higher-level tools (KubernetesTool) call into this backend.
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[kubectl-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[kubectl-missing] kubectl not installed."

    # ---- APPLY ----
    def apply(self, manifest):
        return self._exec(["kubectl", "apply", "-f", manifest])

    # ---- DELETE ----
    def delete(self, manifest):
        return self._exec(["kubectl", "delete", "-f", manifest])

    # ---- GET ----
    def get(self, resource, namespace=None):
        cmd = ["kubectl", "get", resource]
        if namespace:
            cmd += ["-n", namespace]
        cmd += ["-o", "wide"]
        return self._exec(cmd)

    # ---- DESCRIBE ----
    def describe(self, resource, name, namespace=None):
        cmd = ["kubectl", "describe", resource, name]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    # ---- LOGS ----
    def logs(self, pod, container=None, namespace=None):
        cmd = ["kubectl", "logs", pod]
        if container:
            cmd.append(container)
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    # ---- EXEC ----
    def exec(self, pod, command, namespace=None):
        if isinstance(command, str):
            command = command.split()
        cmd = ["kubectl", "exec", "-it", pod]
        if namespace:
            cmd += ["-n", namespace]
        cmd += ["--"] + command
        return self._exec(cmd)

    # ---- ROLLOUT (UNDO/STATUS) ----
    def rollout(self, action, deployment, namespace=None):
        cmd = ["kubectl", "rollout", action, deployment]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    # ---- SCALE ----
    def scale(self, deployment, replicas, namespace=None):
        cmd = [
            "kubectl", "scale",
            f"deployment/{deployment}",
            f"--replicas={replicas}"
        ]
        if namespace:
            cmd += ["-n", namespace]
        return self._exec(cmd)

    # ---- NAMESPACE OPS ----
    def get_namespaces(self):
        return self._exec(["kubectl", "get", "ns"])

    # ---- CONTEXT OPS ----
    def get_contexts(self):
        return self._exec(["kubectl", "config", "get-contexts"])

    def use_context(self, ctx):
        return self._exec(["kubectl", "config", "use-context", ctx])
