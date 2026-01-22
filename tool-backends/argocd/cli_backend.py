# tool-backend/argocd/cli_backend.py

import subprocess


class ArgoCDCLIBackend:
    """
    Low-level wrapper around `argocd` CLI.
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode().strip()
        except subprocess.CalledProcessError as e:
            return f"[argocd-error] {e.output.decode().strip()}"
        except FileNotFoundError:
            return "[argocd-missing] argocd binary not installed."

    def login(self, server, username, password, insecure=True):
        cmd = ["argocd", "login", server, "--username", username, "--password", password]
        if insecure:
            cmd.append("--insecure")
        return self._exec(cmd)
