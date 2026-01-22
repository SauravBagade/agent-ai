# tool-backends/vault/lease_backend.py

import subprocess


class VaultLeaseBackend:
    """
    Lease backend for dynamic credentials (DB, Cloud)
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8")
        except subprocess.CalledProcessError as e:
            return f"[vault-lease-error] {e.output.decode('utf-8').strip()}"

    def renew(self, lease_id):
        return self._exec(["vault", "lease", "renew", lease_id])

    def revoke(self, lease_id):
        return self._exec(["vault", "lease", "revoke", lease_id])
