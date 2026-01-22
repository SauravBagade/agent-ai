# tool-backends/helm/utils.py

class HelmUtils:
    """
    Utility helpers for Helm charts & release names.
    """

    def normalize_release(self, name):
        return name.lower().replace("_", "-")

    def namespace_or_default(self, ns):
        return ns or "default"
