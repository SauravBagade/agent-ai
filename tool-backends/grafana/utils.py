# tool-backend/grafana/utils.py

class GrafanaUtils:
    """
    Helpers for dashboard + datasource identifiers.
    """

    def normalize_uid(self, uid):
        return uid.lower()
