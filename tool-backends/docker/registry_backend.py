# tool-backends/docker/registry_backend.py

import subprocess
import os


class DockerRegistryBackend:
    """
    Docker Registry Backend for image distribution
    and CI/CD supply chain operations.

    Supports:
      - docker login/logout
      - push/pull
      - tag & retag
      - registry abstraction
      - cloud integration (future)
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[registry-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[docker-missing] docker binary not installed."

    # ---- LOGIN ----
    def login(self, registry, username=None, password=None):
        """
        docker login example:
          docker login -u USER --password-stdin registry
        """
        cmd = ["docker", "login", registry]
        if username:
            cmd += ["-u", username]
        if password:
            # using password-stdin is better for security
            p = subprocess.Popen(
                cmd + ["--password-stdin"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out, err = p.communicate(password.encode())
            return out.decode("utf-8").strip() or err.decode("utf-8").strip()
        return self._exec(cmd)

    # ---- LOGOUT ----
    def logout(self, registry):
        return self._exec(["docker", "logout", registry])

    # ---- TAG ----
    def tag(self, source, target):
        return self._exec(["docker", "tag", source, target])

    # ---- PUSH ----
    def push(self, image):
        return self._exec(["docker", "push", image])

    # ---- PULL ----
    def pull(self, image):
        return self._exec(["docker", "pull", image])

    # ---- CLOUD REGISTRY HELPERS (FUTURE) ----

    def login_ecr(self, region, repo, aws_cli="aws"):
        """
        AWS ECR Login — future expansion
        will convert:
          aws ecr get-login-password | docker login ...
        """
        return "[ecr-login-future]"

    def login_gcr(self, gcloud_cli="gcloud"):
        return "[gcr-login-future]"

    def login_acr(self, azure_cli="az"):
        return "[acr-login-future]"

    def login_ghcr(self):
        """
        GitHub Container Registry (GHCR)
        stores token in GHCR_PAT env var (future)
        """
        return "[ghcr-login-future]"
