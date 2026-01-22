# tool-backend/grafana/datasource_backend.py

import requests
import json


class GrafanaDatasourceBackend:
    """
    Datasource provisioning backend.
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
        r = requests.get(f"{self.url}/api/datasources", headers=self._headers())
        return r.json()
