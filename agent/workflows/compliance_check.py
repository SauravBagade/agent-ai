# agent/workflows/compliance_check.py

from agent.tools.security_tool import SecurityTool
from agent.tools.helper_tool import HelperTool


class ComplianceCheckWorkflow:
    """
    Compliance Check Workflow for DevSecOps + GRC.

    Supports:
      - CIS Benchmarks (Kubernetes / Linux / Cloud)
      - IaC compliance (Terraform via Checkov)
      - Container policy compliance (image + sbom)
      - SBOM compliance
      - Cluster policy scan (future: Gatekeeper / OPA)
      - Cloud compliance (future: AWS/GCP/Azure)

    Hybrid LLM used for:
      - compliance interpretation
      - rule mapping & mismatch detection
      - remediation guidance
      - severity prioritization
    """

    def __init__(self, context=None, memory=None, llm=None):
        self.context = context
        self.memory = memory
        self.llm = llm

        self.security = SecurityTool()
        self.helper = HelperTool()

    def run(self, plan: dict):
        """
        Example plan:

        {
          "intent": "COMPLIANCE",
          "workflow": "compliance_check",
          "entities": {
            "target": "terraform|cluster|image|sbom",
            "path": "./infra",
            "image": "backend:1.4"
          }
        }
        """
        entities = plan.get("entities", {})
        target = entities.get("target")
        path = entities.get("path")
        image = entities.get("image")

        output = []

        # ---- IaC COMPLIANCE (Terraform) ----
        if target == "terraform" and path:
            check = self.security.check_terraform(path)
            output.append(f"[iac-compliance]\n{check}")
            return self._finish(output)

        # ---- IMAGE POLICY COMPLIANCE ----
        if target == "image" and image:
            scan = self.security.scan_image(image)
            output.append(f"[image-compliance]\n{scan}")
            return self._finish(output)

        # ---- SBOM POLICY COMPLIANCE ----
        if target == "sbom" and path:
            sbom = self.security.scan_sbom(path)
            output.append(f"[sbom]\n{sbom}")
            return self._finish(output)

        # ---- CLUSTER COMPLIANCE (CIS) ----
        if target == "cluster":
            bench = self.security.kube_bench()
            output.append(f"[cluster-cis]\n{bench}")
            return self._finish(output)

        return "[compliance-error] unsupported target or missing entity."

    def _finish(self, output):
        raw = "\n\n".join(output)

        # update context
        if self.context:
            self.context.update({
                "workflow": "compliance_check",
                "status": "ok"
            })

        # LLM interpretation + remediation
        if self.llm:
            return self.llm.explain(
                f"Analyze compliance & recommend remediation:\n{raw}"
            )

        return raw
