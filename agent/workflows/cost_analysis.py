# agent/workflows/cost_analysis.py

from agent.tools.cost_tool import CostTool
from agent.tools.helper_tool import HelperTool


class CostAnalysisWorkflow:
    """
    Cost Analysis Workflow for FinOps automation.

    Supports:
      - namespace cost (Kubecost)
      - service cost (Kubecost)
      - terraform infra cost & diff (Infracost)

    Uses hybrid LLM for:
      - analyzing cost components
      - identifying expensive workloads
      - recommending optimization strategies
    """

    def __init__(self, context=None, memory=None, llm=None):
        self.context = context
        self.memory = memory
        self.llm = llm

        self.cost = CostTool()
        self.helper = HelperTool()

    def run(self, plan: dict):
        """
        Example plan:
        {
          "intent": "COST",
          "workflow": "cost_analysis",
          "entities": {
            "target": "namespace|service|terraform",
            "namespace": "prod",
            "service": "backend",
            "path": "infra/eks-cluster"
          }
        }
        """
        entities = plan.get("entities", {})
        target = entities.get("target")
        namespace = entities.get("namespace")
        service = entities.get("service")
        path = entities.get("path")

        output = []

        # ---- K8s Namespace Cost ----
        if target == "namespace" and namespace:
            ns_cost = self.cost.namespace_cost(namespace)
            output.append(f"[namespace-cost]\n{ns_cost}")
            return self._finish(output)

        # ---- K8s Service Cost ----
        if target == "service" and service:
            svc_cost = self.cost.service_cost(service)
            output.append(f"[service-cost]\n{svc_cost}")
            return self._finish(output)

        # ---- Terraform Infra Cost ----
        if target == "terraform" and path:
            breakdown = self.cost.terraform_cost(path)
            diff = self.cost.terraform_diff(path)
            output.append(f"[infra-cost-breakdown]\n{breakdown}")
            output.append(f"[infra-cost-diff]\n{diff}")
            return self._finish(output)

        return "[cost-analysis-error] missing target or required entities."

    # ---- Finalization with optional LLM explanation ----

    def _finish(self, output):
        raw = "\n\n".join(output)

        # update context for traceability
        if self.context:
            self.context.update({
                "workflow": "cost_analysis",
                "status": "ok"
            })

        # LLM Explanation + Recommendations
        if self.llm:
            return self.llm.explain(
                f"Analyze and explain cost data for FinOps context:\n{raw}"
            )

        return raw
