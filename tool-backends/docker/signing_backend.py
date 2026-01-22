# tool-backends/docker/signing_backend.py

import subprocess


class DockerSigningBackend:
    """
    Signing Backend using Cosign (Sigstore)

    Supports:
      - container image signing
      - attestation (future: SBOM + provenance)
      - verification
      - keyless signing (OIDC)
      - registry transparency + trust

    Ecosystem:
      - Cosign: signing/verification
      - Rekor: transparency log
      - Fulcio: certificates (OIDC)
      - SBOM: synergy with syft backend
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[signing-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[cosign-missing] cosign binary not installed."

    # ---- IMAGE SIGN (KEYLESS) ----
    def sign(self, image):
        """
        Cosign keyless signing:
          cosign sign <image>

        Requires:
          - OIDC login (GitHub Actions, GCP, Azure, etc.)
        """
        cmd = ["cosign", "sign", image]
        return self._exec(cmd)

    # ---- IMAGE SIGN (KEYED) ----
    def sign_with_key(self, image, key, password=None):
        """
        Cosign key signing:
          cosign sign --key cosign.key <image>
        """
        cmd = ["cosign", "sign", "--key", key, image]

        if password:
            p = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out, err = p.communicate(password.encode())
            return out.decode("utf-8").strip() or err.decode("utf-8").strip()

        return self._exec(cmd)

    # ---- VERIFY SIGNATURE ----
    def verify(self, image, key=None):
        """
        Cosign signature verification:
          cosign verify <image>
        """
        cmd = ["cosign", "verify", image]
        if key:
            cmd += ["--key", key]
        return self._exec(cmd)

    # ---- ATTESTATION (FUTURE) ----
    def attest(self, image, predicate, keyless=True):
        """
        Attach SBOM / Provenance / Metadata via:
          cosign attest
        """
        return f"[attestation-future] attach {predicate} to {image}"

    # ---- VERIFY ATTESTATION (FUTURE) ----
    def verify_attestation(self, image):
        return "[verify-attestation-future]"

    # ---- SIGN SBOM (FUTURE) ----
    def sign_sbom(self, sbom_path):
        return "[sbom-signing-future]"

    # ---- KEYLESS OIDC (FUTURE) ----
    def oidc_sign(self, image):
        return "[oidc-sign-future]"
