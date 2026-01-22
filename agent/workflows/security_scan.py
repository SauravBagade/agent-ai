# agent/workflows/security_scan.py

from agent.tools.security_tool import SecurityTool
from agent.tools.helper_tool import HelperTool


class SecurityScanWorkflow:
    """
    Security Scan Workflow for DevSecOps operations.

    Supports:
      - image scan (Trivy/Grype)
      - filesystem scan
      - SBOM generation
      - Terraform IaC security (Checkov)
      - Kubernetes benchmark (kube-bench)

    Uses Hybrid LLM for:
      - summarizing vulnerability data
      - prioritizing CVE by severity
      - remediation suggestions
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
          "intent": "SECURITY",
          "workflow": "security_scan",
          "entities": {
            "target": "image|fs|sbom|terraform|cluster",
            "image": "nginx:1.25",
            "path": "./infra",
            "cluster": "eks-prod"
          }
        }
        """

        entities = plan.get("entities", {})
        target = entities.get("target")

        output = []

        # ---- IMAGE VULN SCAN ----
        if target == "image":
            image = entities.get("image")
            if not image:
                return "[security-scan-error] missing image name."
            scan = self.security.scan_image(image)
            output.append(f"[image-scan]\n{scan}")
            return self._finish(output)

        # ---- FILESYSTEM SCAN ----
        if target == "fs":
            path = entities.get("path") or "."
            scan = self.security.scan_filesystem(path)
            output.append(f"[filesystem-scan]\n{scan}")
            return self._finish(output)

        # ---- SBOM ----
        if target == "sbom":
            path = entities.get("path") or "."
            sbom = self.security.scan_sbom(path)
            output.append(f"[sbom]\n{sbom}")
            return self._finish(output)

        # ---- TERRAFORM SECURITY ----
        if target == "terraform":
            path = entities.get("path")
            if not path:
                return "[security-scan-error] terraform requires path."
            check = self.security.check_terraform(path)
            output.append(f"[terraform-security]\n{check}")
            return self._finish(output)

        # ---- CLUSTER CIS ----
        if target == "cluster":
            bench = self.security.kube_bench()
            output.append(f"[cluster-benchmark]\n{bench}")
            return self._finish(output)

        return f"[security-scan-error] unsupported target '{target}'"

    def _finish(self, output):
        raw = "\n\n".join(output)

        if self.context:
            self.context.update({
                "workflow": "security_scan",
                "status": "ok"
            })

        # Hybrid LLM adds remediation & prioritization
        if self.llm:
            return self.llm.explain(
                f"Analyze vulnerabilities & suggest remediation:\n{raw}"
            )

        return raw
