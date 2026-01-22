# tool-backends/helm/lint_backend.py

import subprocess


class HelmLintBackend:
    """
    Lint backend for chart validation.
    Useful for:
      - CI/CD checks
      - PR validation
      - GitOps quality
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[helm-lint-error] {e.output.decode('utf-8').strip()}"

    def lint(self, chart):
        return self._exec(["helm", "lint", chart])
