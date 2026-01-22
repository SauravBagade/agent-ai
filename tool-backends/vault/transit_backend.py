# tool-backends/vault/transit_backend.py

import subprocess


class VaultTransitBackend:
    """
    Transit backend for crypto (encrypt/decrypt/sign/verify)
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8")
        except subprocess.CalledProcessError as e:
            return f"[vault-transit-error] {e.output.decode('utf-8').strip()}"

    def encrypt(self, key, plaintext):
        return self._exec([
            "vault", "write", "-force",
            f"transit/encrypt/{key}",
            f"plaintext={plaintext}"
        ])

    def decrypt(self, key, ciphertext):
        return self._exec([
            "vault", "write", "-force",
            f"transit/decrypt/{key}",
            f"ciphertext={ciphertext}"
        ])
