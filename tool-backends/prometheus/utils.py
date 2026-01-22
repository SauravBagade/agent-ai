# tool-backend/prometheus/utils.py

class PrometheusUtils:
    """
    Helpers for query normalization.
    """

    def normalize_selector(self, kv):
        return ",".join(f"{k}='{v}'" for k, v in kv.items())
