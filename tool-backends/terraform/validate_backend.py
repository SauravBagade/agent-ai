# tool-backends/terraform/validate_backend.py

import subprocess


class TerraformValidateBackend:
    """
    Validation backend:
      - syntax checks
      - configuration validation
    Useful in CI/CD pipelines
    """

    def _exec(self, cmd, cwd=None):
        try:
            out = subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[terraform-validate-error] {e.output.decode('utf-8').strip()}"

    def validate(self, path="."):
        return self._exec(["terraform", "validate"], cwd=path)
