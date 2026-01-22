# tool-backends/helm/template_backend.py

import subprocess


class HelmTemplateBackend:
    """
    Templating backend for dry-run / manifest preview / CI checks.

    Useful for:
      - GitOps validation
      - CI/CD merges
      - testing values overrides
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[helm-template-error] {e.output.decode('utf-8').strip()}"

    def template(self, chart, namespace=None, values=None, set_vars=None):
        cmd = ["helm", "template", chart]

        if namespace:
            cmd += ["-n", namespace]

        if values:
            for file in values:
                cmd += ["-f", file]

        if set_vars:
            for k, v in set_vars.items():
                cmd += ["--set", f"{k}={v}"]

        return self._exec(cmd)
