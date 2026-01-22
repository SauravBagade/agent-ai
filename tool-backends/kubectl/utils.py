# tool-backends/kubectl/utils.py

class KubectlUtils:
    """
    Utility helpers for Kubernetes naming, parsing, & selectors.
    """

    def normalize_namespace(self, ns):
        return ns or "default"

    def is_fqdn(self, name):
        return "." in name

    def resource_key(self, namespace, pod):
        return f"{namespace}/{pod}" if namespace else pod

    def pod_selector(self, app):
        """
        Most common selector for pods
        """
        return f"-l app={app}"
