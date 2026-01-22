# agent/tools/kubernetes_tool.py

import subprocess

class KubernetesTool:
    """
    Kubernetes Tool using kubectl CLI for DevOps actions.

    Supports:
      - deploy yaml
      - get pods/services
      - logs
      - describe
      - scale
      - delete

    Works with:
      - EKS
      - GKE
      - AKS
      - Minikube
      - Kind
      - K3s
    """

    # ---- APPLY YAML ----

    def apply(self, yaml_path: str):
        cmd = ["kubectl", "apply", "-f", yaml_path]
        return self._exec(cmd)

    # ---- GET PODS ----

    def get_pods(self, namespace: str = None):
        cmd = ["kubectl", "get", "pods", "-o", "wide"]
        if namespace:
            cmd.extend(["-n", namespace])
        return self._exec(cmd)

    # ---- GET SERVICES ----

    def get_services(self, namespace: str = None):
        cmd = ["kubectl", "get", "svc"]
        if namespace:
            cmd.extend(["-n", namespace])
        return self._exec(cmd)

    # ---- LOGS ----

    def logs(self, pod: str, namespace: str = None):
        cmd = ["kubectl", "logs", pod]
        if namespace:
            cmd.extend(["-n", namespace])
        return self._exec(cmd)

    # ---- DESCRIBE ----

    def describe(self, pod: str, namespace: str = None):
        cmd = ["kubectl", "describe", "pod", pod]
        if namespace:
            cmd.extend(["-n", namespace])
        return self._exec(cmd)

    # ---- SCALE ----

    def scale(self, deployment: str, replicas: int, namespace: str = None):
        cmd = ["kubectl", "scale", "deployment", deployment, f"--replicas={replicas}"]
        if namespace:
            cmd.extend(["-n", namespace])
        return self._exec(cmd)

    # ---- DELETE ----

    def delete(self, kind: str, name: str, namespace: str = None):
        cmd = ["kubectl", "delete", kind, name]
        if namespace:
            cmd.extend(["-n", namespace])
        return self._exec(cmd)

    # ---- INTERNAL EXEC ----

    def _exec(self, cmd):
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return result.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[kubectl-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[kubectl-not-installed] kubectl CLI not found."
