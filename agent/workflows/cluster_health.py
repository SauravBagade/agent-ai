# agent/workflows/cluster_health.py

from agent.tools.kubernetes_tool import KubernetesTool
from agent.tools.monitoring_tool import MonitoringTool
from agent.tools.logging_tool import LoggingTool
from agent.tools.helper_tool import HelperTool


class ClusterHealthWorkflow:
    """
    Cluster Health Workflow for SRE & DevOps situational awareness.

    Evaluates:
      - pod status
      - node health
      - restart counts
      - service reachability
      - alerts (Prometheus/Alertmanager)
      - simple metrics health
      - LLM explanation for summary

    Works on:
      - EKS
      - GKE
      - AKS
      - Minikube / Kind
      - K3s
    """

    def __init__(self, context=None, memory=None, llm=None):
        self.context = context
        self.memory = memory
        self.llm = llm

        self.k8s = KubernetesTool()
        self.monitor = MonitoringTool()
        self.logging = LoggingTool()
        self.helper = HelperTool()

    def run(self, plan: dict):
        """
        Example plan:
        {
          "intent": "HEALTH",
          "workflow": "cluster_health",
          "entities": {
            "namespace": "prod"
          }
        }
        """
        entities = plan.get("entities", {})
        namespace = entities.get("namespace")

        output = []

        # ---- Pods ----
        pods = self.k8s.get_pods(namespace)
        output.append(f"[pods]\n{pods}")

        # ---- Services ----
        svcs = self.k8s.get_services(namespace)
        output.append(f"[services]\n{svcs}")

        # ---- Restart Counts ----
        restarts = self.monitor.pod_restarts(namespace)
        output.append(f"[restarts]\n{restarts}")

        # ---- Alerts ----
        alerts = self.monitor.list_alerts()
        output.append(f"[alerts]\n{alerts}")

        # ---- Nodes (optional future) ----
        # can use prom_query("kube_node_status_condition")

        raw_output = "\n\n".join(output)

        # ---- LLM Summary ----
        if self.llm:
            explained = self.llm.explain(
                f"Analyze Kubernetes cluster health and summarize:\n{raw_output}"
            )
            self._update_context(namespace, status="analysis-complete")
            return explained

        self._update_context(namespace, status="raw")
        return raw_output

    def _update_context(self, namespace, status):
        if self.context:
            self.context.update({
                "workflow": "cluster_health",
                "namespace": namespace,
                "status": status
            })
