# tool-backends/terraform/cli_backend.py

import subprocess
import os


class TerraformCLIBackend:
    """
    Core Terraform command backend.

    Supports:
      - init
      - apply
      - destroy
      - fmt
      - providers
      - output
    """

    def _exec(self, cmd, cwd=None):
        try:
            out = subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[terraform-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[terraform-missing] terraform binary not installed."

    def init(self, path="."):
        return self._exec(["terraform", "init"], cwd=path)

    def apply(self, path=".", auto_approve=True):
        cmd = ["terraform", "apply"]
        if auto_approve:
            cmd.append("-auto-approve")
        return self._exec(cmd, cwd=path)

    def destroy(self, path=".", auto_approve=True):
        cmd = ["terraform", "destroy"]
        if auto_approve:
            cmd.append("-auto-approve")
        return self._exec(cmd, cwd=path)

    def fmt(self, path="."):
        return self._exec(["terraform", "fmt"], cwd=path)

    def providers(self, path="."):
        return self._exec(["terraform", "providers"], cwd=path)

    def output(self, path="."):
        return self._exec(["terraform", "output"], cwd=path)
