# tool-backend/prometheus/metrics_backend.py

from .query_backend import PrometheusQueryBackend


class PrometheusMetricsBackend(PrometheusQueryBackend):
    """
    High-level metrics queries for SRE workflows.
    """

    def cpu_usage(self, selector="kubernetes"):
        return self.query(f"sum(rate(container_cpu_usage_seconds_total{{{selector}}}[5m]))")

    def memory_usage(self, selector="kubernetes"):
        return self.query(f"sum(container_memory_usage_bytes{{{selector}}})")

    def node_health(self):
        return self.query("up")
