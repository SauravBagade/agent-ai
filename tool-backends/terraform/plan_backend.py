# tool-backends/terraform/plan_backend.py

import subprocess


class TerraformPlanBackend:
    """
    Handles Terraform planning:
      - plan dry-run
      - plan file output
      - diff visualization
    """

    def _exec(self, cmd, cwd=None):
        try:
            out = subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[terraform-plan-error] {e.output.decode('utf-8').strip()}"

    def plan(self, path=".", out_file=None):
        cmd = ["terraform", "plan"]
        if out_file:
            cmd += ["-out", out_file]
        return self._exec(cmd, cwd=path)

    def show(self, path=".", plan_file=None):
        cmd = ["terraform", "show"]
        if plan_file:
            cmd.append(plan_file)
        return self._exec(cmd, cwd=path)
