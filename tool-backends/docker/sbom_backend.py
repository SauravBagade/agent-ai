# tool-backends/docker/sbom_backend.py

import subprocess


class DockerSBOMBackend:
    """
    SBOM Backend using Syft for supply chain visibility.

    Supports:
      - image-based SBOM
      - filesystem SBOM
      - SPDX format
      - CycloneDX format
      - JSON format (for LLM parsing)
      - dependency graphing (future)

    Tools required (externally):
      syft: https://github.com/anchore/syft
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[sbom-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[syft-missing] syft binary not installed."

    # ---- IMAGE SBOM ----

    def sbom_image(self, image, fmt="json"):
        """
        Example:
          syft nginx:latest -o json
          syft ubuntu -o spdx-json
          syft python:3.10 -o cyclonedx-json
        """
        cmd = ["syft", image, "-o", self._format(fmt)]
        return self._exec(cmd)

    # ---- FILESYSTEM SBOM ----

    def sbom_fs(self, path, fmt="json"):
        """
        Example:
          syft dir/ -o json
          syft . -o cyclonedx-json
        """
        cmd = ["syft", path, "-o", self._format(fmt)]
        return self._exec(cmd)

    # ---- OUTPUT FORMAT HANDLER ----

    def _format(self, fmt):
        fmt = fmt.lower()
        if fmt in ("json", "spdx", "cyclonedx"):
            if fmt == "spdx":
                return "spdx-json"
            if fmt == "cyclonedx":
                return "cyclonedx-json"
            return "json"
        return "json"

    # ---- FUTURE: DEPENDENCY GRAPH ----

    def dependency_graph(self, target):
        return "[sbom-dependency-graph-future]"

    # ---- FUTURE: ATTESTATION (for cosign) ----

    def attestation(self, target):
        return "[sbom-attestation-future]"

    # ---- FUTURE: SBOM DIFF ----

    def diff(self, old, new):
        return "[sbom-diff-future]"
