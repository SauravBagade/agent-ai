# agent/tools/cost_tool.py

import requests
import os
import subprocess


class CostTool:
    """
    Cost Tool for DevOps FinOps automation.

    Supports:
      - Kubecost API (K8s cost model)
      - Infracost (Terraform cost diff)
      - Cloud optimization insights (future)

    Enables:
      - namespace cost visibility
      - service cost visibility
      - infra cost planning
      - cost-aware deployments
    """

    def __init__(self):
        self.kubecost_url = os.getenv("KUBECOST_URL", "http://localhost:9090")
        self.infracost_bin = os.getenv("INFRACOST_BIN", "infracost")

    # ---- KUBECOST (K8s Cost) ----

    def namespace_cost(self, namespace: str):
        url = f"{self.kubecost_url}/model/namespaces"
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                return f"[kubecost-error:{resp.status_code}] {resp.text}"

            data = resp.json()
            for item in data:
                if item.get("namespace") == namespace:
                    return {
                        "namespace": namespace,
                        "cpu_cost": item.get("cpuCost"),
                        "ram_cost": item.get("ramCost"),
                        "total_cost": item.get("totalCost"),
                    }
            return f"[kubecost] namespace '{namespace}' not found"
        except Exception as e:
            return f"[kubecost-connection-error] {str(e)}"

    def service_cost(self, service: str):
        url = f"{self.kubecost_url}/model/services"
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                return f"[kubecost-error:{resp.status_code}] {resp.text}"

            data = resp.json()
            for item in data:
                if item.get("service") == service:
                    return {
                        "service": service,
                        "cpu_cost": item.get("cpuCost"),
                        "ram_cost": item.get("ramCost"),
                        "total_cost": item.get("totalCost"),
                    }
            return f"[kubecost] service '{service}' not found"
        except Exception as e:
            return f"[kubecost-connection-error] {str(e)}"

    # ---- INFRACOST (TERRAFORM COST) ----

    def terraform_cost(self, path: str, breakdown: bool = True):
        """
        Infracost CLI: cost estimation for Terraform.

        Example:
          infracost breakdown --path infra/eks
        """
        cmd = [self.infracost_bin, "breakdown", f"--path={path}", "--format=json"]
        return self._exec(cmd)

    def terraform_diff(self, path: str):
        """
        Infracost diff:
          - compare cost before/after change
        """
        cmd = [self.infracost_bin, "diff", f"--path={path}", "--format=json"]
        return self._exec(cmd)

    # ---- INTERNAL EXEC ----

    def _exec(self, cmd):
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return result.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[infracost-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[infracost-not-installed] Infracost CLI not found."

