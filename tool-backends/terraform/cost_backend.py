# tool-backends/terraform/cost_backend.py

import subprocess


class TerraformCostBackend:
    """
    Cost backend using Infracost:
      - cost estimate
      - diff estimate
    """

    def _exec(self, cmd, cwd=None):
        try:
            out = subprocess.check_output(cmd, cwd=path, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[terraform-cost-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[infracost-missing] infracost not installed."

    def estimate(self, path="."):
        return self._exec(["infracost", "breakdown", "--path", path])

    def diff(self, path="."):
        return self._exec(["infracost", "diff", "--path", path])
