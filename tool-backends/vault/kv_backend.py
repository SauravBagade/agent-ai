# tool-backends/vault/kv_backend.py

import subprocess


class VaultKVBackend:
    """
    KV backend for secret storage (v1 + v2)
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[vault-kv-error] {e.output.decode('utf-8').strip()}"

    def read(self, path):
        return self._exec(["vault", "kv", "get", path])

    def write(self, path, **kwargs):
        cmd = ["vault", "kv", "put", path]
        for k, v in kwargs.items():
            cmd.append(f"{k}={v}")
        return self._exec(cmd)

    def delete(self, path):
        return self._exec(["vault", "kv", "delete", path])
