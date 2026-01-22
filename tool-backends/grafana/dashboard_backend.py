# tool-backend/grafana/dashboard_backend.py

import requests
import json


class GrafanaDashboardBackend:
    """
    Dashboard backend for Grafana HTTP API.
    """

    def __init__(self, url, token):
        self.url = url.rstrip("/")
        self.token = token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def list(self):
        r = requests.get(f"{self.url}/api/search", headers=self._headers())
        return r.json()

    def get(self, uid):
        r = requests.get(f"{self.url}/api/dashboards/uid/{uid}", headers=self._headers())
        return r.json()

    def import_dashboard(self, payload):
        r = requests.post(
            f"{self.url}/api/dashboards/db",
            headers=self._headers(),
            data=json.dumps(payload)
        )
        return r.json()
