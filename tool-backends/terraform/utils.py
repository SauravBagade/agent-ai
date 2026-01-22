# tool-backends/terraform/utils.py

class TerraformUtils:
    """
    Utility helpers for env/workspace normalization.
    """

    def workspace_or_default(self, ws):
        return ws or "default"

    def validate_path(self, path):
        return path or "."
