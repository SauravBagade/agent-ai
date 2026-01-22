# agent/tools/security_tool.py

import subprocess


class SecurityTool:
    """
    Security Tool abstraction for DevSecOps tasks.

    Supports (initial):
      - Trivy (container & IaC scanning)
      - Grype (container vulnerability scanning)
      - Checkov (Terraform policy checks)
      - Kube-bench (Kubernetes CIS benchmark)

    Use cases:
      - scan docker images
      - scan terraform modules
      - scan K8s manifests
      - check cluster security posture
      - detect secrets
    """

    # ---- TRIVY ----

    def scan_image(self, image: str):
        """
        Scan container image for vulnerabilities.
        """
        cmd = ["trivy", "image", "--quiet", "--format", "json", image]
        return self._exec(cmd)

    def scan_filesystem(self, path: str):
        """
        Scan local directory for vulnerabilities / secrets.
        """
        cmd = ["trivy", "fs", "--quiet", "--format", "json", path]
        return self._exec(cmd)

    def scan_sbom(self, path: str):
        """
        Generate SBOM (software bill of materials).
        """
        cmd = ["trivy", "sbom", "--quiet", "--format", "json", path]
        return self._exec(cmd)

    # ---- GRYPE ----

    def grype_scan(self, image: str):
        """
        Alternative container scanner (Anchore).
        """
        cmd = ["grype", "-o", "json", image]
        return self._exec(cmd)

    # ---- CHECKOV (Terraform + IaC) ----

    def check_terraform(self, path: str):
        """
        Check Terraform IaC security policy.
        """
        cmd = ["checkov", "-d", path, "-o", "json"]
        return self._exec(cmd)

    # ---- KUBE-BENCH ----

    def kube_bench(self):
        """
        Kubernetes CIS benchmark scan.
        """
        cmd = ["kube-bench", "--json"]
        return self._exec(cmd)

    # ---- INTERNAL EXEC ----

    def _exec(self, cmd):
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return result.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[security-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return f"[security-tool-missing] {cmd[0]} not installed."
