# tool-backends/docker/build_backend.py

import subprocess
import os


class DockerBuildBackend:
    """
    Docker Build Backend for CI/CD & DevOps pipelines.

    Supports:
      - docker build
      - build args
      - multi-stage builds (via Dockerfile)
      - tagging
      - local context builds
      - build directory selection

    Future features:
      - buildx / multi-arch
      - caching / registry cache
      - remote dockerfile
      - sbom + signing integration
    """

    def _exec(self, cmd, cwd=None):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, cwd=cwd)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[docker-build-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[docker-missing] docker binary not installed."

    def build(self, context=".", dockerfile="Dockerfile", tag=None, build_args=None):
        """
        Build container image using docker build.

        Args:
          context (str): build context path
          dockerfile (str): Dockerfile path
          tag (str): image tag e.g. backend:1.2
          build_args (dict): build-time args for Dockerfile

        Example:
          build(context=".", dockerfile="Dockerfile", tag="backend:1.2",
                build_args={"ENV": "prod"})
        """
        cmd = ["docker", "build", "-f", dockerfile]

        if tag:
            cmd += ["-t", tag]

        if build_args:
            for k, v in build_args.items():
                cmd += ["--build-arg", f"{k}={v}"]

        cmd.append(context)
        return self._exec(cmd)

    def build_no_cache(self, context=".", dockerfile="Dockerfile", tag=None):
        cmd = ["docker", "build", "--no-cache", "-f", dockerfile]
        if tag:
            cmd += ["-t", tag]
        cmd.append(context)
        return self._exec(cmd)

    def build_pull(self, context=".", dockerfile="Dockerfile", tag=None):
        cmd = ["docker", "build", "--pull", "-f", dockerfile]
        if tag:
            cmd += ["-t", tag]
        cmd.append(context)
        return self._exec(cmd)

    # ---- FUTURE: MULTI-ARCH VIA BUILDX ----
    def build_multiarch(self, context=".", tag=None, platforms=None):
        """
        Buildx multi-arch builds (future)
        e.g. linux/amd64, linux/arm64
        """
        if not platforms:
            platforms = ["linux/amd64", "linux/arm64"]

        cmd = [
            "docker", "buildx", "build",
            "--push",
            "--platform", ",".join(platforms)
        ]
        if tag:
            cmd += ["-t", tag]
        cmd.append(context)

        return self._exec(cmd)

    # ---- FUTURE: CACHE + EXPORT ----
    def build_with_cache(self, context=".", dockerfile="Dockerfile", tag=None, cache_from=None, cache_to=None):
        cmd = ["docker", "build", "-f", dockerfile]

        if tag:
            cmd += ["-t", tag]

        if cache_from:
            cmd += ["--cache-from", cache_from]

        if cache_to:
            cmd += ["--cache-to", cache_to]

        cmd.append(context)
        return self._exec(cmd)
