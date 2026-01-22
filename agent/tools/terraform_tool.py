# agent/tools/terraform_tool.py

import subprocess
import os

class TerraformTool:
    """
    Terraform Tool for running IaC jobs using terraform CLI.

    Supports:
      - terraform init
      - terraform plan
      - terraform apply (auto-approve)
      - terraform destroy (safety blocked by default)
      - terraform validate
      - terraform output

    Works for:
      - AWS
      - GCP
      - Azure
      - K8s cluster provisioning
      - EKS/AKS/GKE modules
    """

    def __init__(self, workdir: str = None):
        # allow user to specify terraform directory
        self.workdir = workdir or os.getcwd()

    # ---- INIT ----

    def init(self):
        cmd = ["terraform", "init"]
        return self._exec(cmd)

    # ---- PLAN ----

    def plan(self):
        cmd = ["terraform", "plan", "-no-color"]
        return self._exec(cmd)

    # ---- APPLY ----

    def apply(self, auto_approve: bool = True):
        cmd = ["terraform", "apply", "-no-color"]
        if auto_approve:
            cmd.append("-auto-approve")
        return self._exec(cmd)

    # ---- DESTROY (DISABLED BY DEFAULT) ----

    def destroy(self, auto_approve: bool = False):
        """
        Destroy is dangerous → safety system will block or require confirmation.
        """
        cmd = ["terraform", "destroy", "-no-color"]
        if auto_approve:
            cmd.append("-auto-approve")
        return self._exec(cmd)

    # ---- VALIDATE ----

    def validate(self):
        cmd = ["terraform", "validate", "-no-color"]
        return self._exec(cmd)

    # ---- OUTPUT ----

    def output(self, name: str = None):
        cmd = ["terraform", "output"]
        if name:
            cmd.append(name)
        return self._exec(cmd)

    # ---- INTERNAL EXEC ----

    def _exec(self, cmd):
        try:
            result = subprocess.check_output(
                cmd,
                stderr=subprocess.STDOUT,
                cwd=self.workdir
            )
            return result.decode("utf-8").strip()

        except subprocess.CalledProcessError as e:
            return f"[terraform-error] {e.output.decode('utf-8').strip()}"

        except FileNotFoundError:
            return "[terraform-not-installed] terraform CLI not found."
