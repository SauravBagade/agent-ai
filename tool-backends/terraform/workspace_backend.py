# tool-backends/terraform/workspace_backend.py

import subprocess


class TerraformWorkspaceBackend:
    """
    Multi-env workspace support for:
      - dev
      - stage
      - prod
      - preview
    """

    def _exec(self, cmd, cwd=None):
        try:
            out = subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[terraform-workspace-error] {e.output.decode('utf-8').strip()}"

    def list(self, path="."):
        return self._exec(["terraform", "workspace", "list"], cwd=path)

    def select(self, name, path="."):
        return self._exec(["terraform", "workspace", "select", name], cwd=path)

    def new(self, name, path="."):
        return self._exec(["terraform", "workspace", "new", name], cwd=path)
