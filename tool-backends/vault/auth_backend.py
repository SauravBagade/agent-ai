# tool-backends/vault/auth_backend.py

import subprocess


class VaultAuthBackend:
    """
    Auth backend for:
      - token
      - approle
      - jwt/oidc
      - aws/gcp
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[vault-auth-error] {e.output.decode('utf-8').strip()}"

    def approle_login(self, role_id, secret_id):
        return self._exec([
            "vault", "write", "auth/approle/login",
            f"role_id={role_id}",
            f"secret_id={secret_id}"
        ])
