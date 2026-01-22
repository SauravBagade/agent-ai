# tool-backends/terraform/state_backend.py

import subprocess


class TerraformStateBackend:
    """
    State backend for:
      - state list
      - state show
      - state rm
      - remote state operations (future)
    """

    def _exec(self, cmd, cwd=None):
        try:
            out = subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[terraform-state-error] {e.output.decode('utf-8').strip()}"

    def list(self, path="."):
        return self._exec(["terraform", "state", "list"], cwd=path)

    def show(self, resource, path="."):
        return self._exec(["terraform", "state", "show", resource], cwd=path)

    def rm(self, resource, path="."):
        return self._exec(["terraform", "state", "rm", resource], cwd=path)
