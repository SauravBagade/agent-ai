# tool-backend/prometheus/query_backend.py

import requests


class PrometheusQueryBackend:
    """
    Query backend for Prometheus HTTP API.
    """

    def __init__(self, url):
        self.url = url.rstrip("/")

    def query(self, expr):
        r = requests.get(f"{self.url}/api/v1/query", params={"query": expr})
        return r.json()

    def query_range(self, expr, start, end, step="30s"):
        r = requests.get(
            f"{self.url}/api/v1/query_range",
            params={
                "query": expr,
                "start": start,
                "end": end,
                "step": step
            }
        )
        return r.json()
