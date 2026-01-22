# tool-backends/vault/utils.py

class VaultUtils:
    """
    Utils for normalization + secret resolution.
    """

    def normalize_path(self, path):
        return path.strip("/")
