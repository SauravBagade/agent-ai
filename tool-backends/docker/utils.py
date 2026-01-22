# tool-backends/docker/utils.py

import re


class DockerUtils:
    """
    Utility helpers for Docker & OCI image operations.

    Provides:
      - image parsing (registry/repo/tag/digest)
      - tag normalization
      - digest extraction
      - registry URL helpers
      - version helpers (semver-aware future)
    """

    # ---- IMAGE PARSING ----

    def parse_image(self, image: str):
        """
        Parses OCI image references.

        Example:
          nginx:latest
          ghcr.io/user/app:1.2.0
          registry.azurecr.io/backend@sha256:xxxx

        Returns:
          {
            "registry": str | None,
            "repo": str,
            "tag": str | None,
            "digest": str | None
          }
        """

        digest = None
        tag = None
        registry = None

        if "@" in image:
            image, digest = image.split("@", 1)

        if ":" in image:
            image, tag = image.rsplit(":", 1)

        # registry detection (simple heuristic)
        parts = image.split("/")
        if "." in parts[0] or ":" in parts[0]:
            registry = parts[0]
            repo = "/".join(parts[1:])
        else:
            repo = image

        return {
            "registry": registry,
            "repo": repo,
            "tag": tag,
            "digest": digest
        }

    # ---- TAG HELPERS ----

    def normalize_tag(self, tag: str):
        """
        Ensures tags are lower-case, semantic & safe.
        """
        if not tag:
            return "latest"
        return tag.lower()

    def latest_if_none(self, tag):
        return tag or "latest"

    # ---- VERSION CHECKS (FUTURE) ----

    def is_semver(self, tag):
        pattern = r"^\d+\.\d+\.\d+(-[a-z0-9]+)?$"
        return bool(re.match(pattern, tag.lower()))

    def bump_patch(self, tag):
        if not self.is_semver(tag):
            return tag
        major, minor, patch = tag.split(".")
        return f"{major}.{minor}.{int(patch)+1}"

    # ---- REGISTRY URL HELPERS ----

    def to_registry_url(self, registry):
        if not registry:
            return None
        if not registry.startswith("https://"):
            return f"https://{registry}"
        return registry

    # ---- DIGEST EXTRACTOR ----

    def extract_digest(self, ref):
        """
        Extract sha256 digest if present
        """
        if "@" in ref:
            return ref.split("@", 1)[1]
        return None
