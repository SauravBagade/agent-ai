# tool-backends/vault/pki_backend.py

import subprocess


class VaultPKIBackend:
    """
    PKI backend for certificate issuance.
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8")
        except subprocess.CalledProcessError as e:
            return f"[vault-pki-error] {e.output.decode('utf-8').strip()}"

    def issue_cert(self, role, common_name):
        return self._exec([
            "vault", "write",
            f"pki/issue/{role}",
            f"common_name={common_name}"
        ])
