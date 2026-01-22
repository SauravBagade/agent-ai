# agent/tools/monitoring_tool.py

import requests
import os


class MonitoringTool:
    """
    Monitoring Tool abstraction for cluster & service observability.

    Supports:
      - Prometheus queries
      - Grafana dashboards (future)
      - Alertmanager status (future)
      - SLO/SLI checks (future)

    This tool enables the agent to perform:
      - cluster health checks
      - performance diagnosis
      - auto-debug SRE issues
      - metrics-based decisions
    """

    def __init__(self):
        self.prom_url = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
        self.grafana_url = os.getenv("GRAFANA_URL", "http://localhost:3000")
        self.alert_url = os.getenv("ALERTMANAGER_URL", "http://localhost:9093")

    # ---- PROMETHEUS QUERY ----

    def prom_query(self, query: str):
        """
        Prometheus API:
        GET /api/v1/query?query=<expr>
        """
        url = f"{self.prom_url}/api/v1/query"
        params = {"query": query}
        try:
            resp = requests.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "success":
                    return data.get("data", {}).get("result", [])
                return f"[prometheus-error] {data}"
            return f"[prometheus-http-error:{resp.status_code}] {resp.text}"
        except Exception as e:
            return f"[prometheus-connection-error] {str(e)}"

    # ---- SIMPLE HEALTH CHECKS ----

    def node_cpu(self):
        return self.prom_query("node_cpu_seconds_total")

    def node_memory(self):
        return self.prom_query("node_memory_MemAvailable_bytes")

    def pod_restarts(self, namespace: str = None):
        q = "sum(kube_pod_container_status_restarts_total)"
        if namespace:
            q += f"{{namespace=\"{namespace}\"}}"
        return self.prom_query(q)

    def http_requests(self, service: str = None):
        q = "sum(rate(http_requests_total[5m]))"
        if service:
            q += f"{{service=\"{service}\"}}"
        return self.prom_query(q)

    # ---- ALERTMANAGER ----

    def list_alerts(self):
        url = f"{self.alert_url}/api/v2/alerts"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                return resp.json()
            return f"[alertmanager-error:{resp.status_code}] {resp.text}"
        except Exception as e:
            return f"[alertmanager-connection-error] {str(e)}"

    # ---- FUTURE: GRAFANA DASHBOARDS ----

    def grafana_dashboards(self):
        return "[grafana-integration-pending]"
