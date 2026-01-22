# agent/tools/logging_tool.py

import requests
import os


class LoggingTool:
    """
    Logging Tool abstraction for DevOps agent.

    Supports:
      - Loki queries
      - Elasticsearch search (ELK stack)
      - error correlation (future)
      - log filtering & parsing (via LLM hybrid)

    Use cases:
      - debug crashing pods
      - CI/CD job logs
      - microservice tracing
      - SRE troubleshooting
    """

    def __init__(self):
        self.loki_url = os.getenv("LOKI_URL", "http://localhost:3100")
        self.elastic_url = os.getenv("ELASTIC_URL", "http://localhost:9200")

    # ---- LOKI QUERY ----

    def loki_query(self, query: str):
        params = {"query": query}
        url = f"{self.loki_url}/loki/api/v1/query"

        try:
            resp = requests.get(url, params=params)
            if resp.status_code == 200:
                return resp.json()
            return f"[loki-error:{resp.status_code}] {resp.text}"
        except Exception as e:
            return f"[loki-connection-error] {str(e)}"

    # ---- LOKI STREAM (TAIL) ----

    def loki_tail(self, query: str):
        url = f"{self.loki_url}/loki/api/v1/tail"

        params = {"query": query}

        try:
            resp = requests.get(url, params=params, stream=True)
            if resp.status_code == 200:
                return "[loki-streaming] (not parsed yet)"
            return f"[loki-error:{resp.status_code}] {resp.text}"
        except Exception as e:
            return f"[loki-connection-error] {str(e)}"

    # ---- ELASTICSEARCH SEARCH ----

    def elastic_search(self, index: str, query: dict):
        url = f"{self.elastic_url}/{index}/_search"

        try:
            resp = requests.post(url, json=query)
            if resp.status_code == 200:
                return resp.json()
            return f"[elastic-error:{resp.status_code}] {resp.text}"
        except Exception as e:
            return f"[elastic-connection-error] {str(e)}"

    # ---- HIGH-LEVEL HELPERS ----

    def error_logs(self, app: str, namespace: str = None):
        """
        Loki high-level helper for app logs.
        Works for K8s with promtail or agent-based logging.
        """
        query = f'{{app="{app}"}} |= "error"'
        if namespace:
            query = f'{{app="{app}", namespace="{namespace}"}} |= "error"'
        return self.loki_query(query)

    def service_logs(self, app: str, namespace: str = None):
        query = f'{{app="{app}"}}'
        if namespace:
            query = f'{{app="{app}", namespace="{namespace}"}}'
        return self.loki_query(query)

    # ---- FUTURE: CORRELATION ----

    def correlate(self, app: str, llm=None):
        """
        Correlates logs via LLM reasoning (future upgrade).
        """
        logs = self.service_logs(app)
        if llm:
            return llm.explain(f"analyze logs: {logs}")
        return logs
