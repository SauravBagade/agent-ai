# tool-backend/grafana/alerts_backend.py

import requests


class GrafanaAlertsBackend:
    """
    Alerts backend for Grafana unified alerting.
    """

    def __init__(self, url, token):
        self.url = url.rstrip("/")
        self.token = token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}"
        }

    def list(self):
        r = requests.get(f"{self.url}/api/alerts", headers=self._headers())
        return r.json()
