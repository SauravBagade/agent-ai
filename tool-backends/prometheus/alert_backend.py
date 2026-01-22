# tool-backend/prometheus/alert_backend.py

import requests


class PrometheusAlertBackend:
    """
    Alertmanager backend.
    """

    def __init__(self, alert_url):
        self.url = alert_url.rstrip("/")

    def alerts(self):
        r = requests.get(f"{self.url}/api/v2/alerts")
        return r.json()

    def silences(self):
        r = requests.get(f"{self.url}/api/v2/silences")
        return r.json()
