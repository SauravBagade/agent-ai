# tool-backends/vault/cli_backend.py

import subprocess


class VaultCLIBackend:
    """
    Low-level wrapper for Vault CLI commands.

    Supports generic actions across backends.
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[vault-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[vault-missing] vault binary not installed."

    def status(self):
        return self._exec(["vault", "status"])

    def login(self, token):
        return self._exec(["vault", "login", token])
