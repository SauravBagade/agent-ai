# tool-backend/argocd/utils.py

class ArgoCDUtils:
    """
    Helpers for application naming, repo paths, etc.
    """

    def normalize_name(self, name):
        return name.lower().replace("_", "-")
