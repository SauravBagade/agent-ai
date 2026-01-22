# tool-backends/docker/compose_backend.py

import subprocess
import os


class DockerComposeBackend:
    """
    Docker Compose Backend for multi-service orchestration.

    Supports:
      - compose up/down
      - logs
      - ps/services
      - scale
      - stop/start
      - build (compose build)
      - env & multiple compose files (future)

    Use cases:
      - local microservice dev
      - testing pipelines
      - hybrid CI workflows
      - ephemeral environments
    """

    def __init__(self, compose_file="docker-compose.yml"):
        self.compose_file = compose_file

    def _exec(self, cmd, cwd=None):
        env = os.environ.copy()
        try:
            out = subprocess.check_output(
                cmd,
                stderr=subprocess.STDOUT,
                cwd=cwd,
                env=env
            )
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[compose-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[compose-missing] docker compose not installed (v2.x)"

    def up(self, detach=True, cwd=None):
        cmd = ["docker", "compose", "-f", self.compose_file, "up"]
        if detach:
            cmd.append("-d")
        return self._exec(cmd, cwd=cwd)

    def down(self, cwd=None):
        cmd = ["docker", "compose", "-f", self.compose_file, "down"]
        return self._exec(cmd, cwd=cwd)

    def ps(self, cwd=None):
        cmd = ["docker", "compose", "-f", self.compose_file, "ps"]
        return self._exec(cmd, cwd=cwd)

    def logs(self, service=None, tail=200, cwd=None):
        cmd = ["docker", "compose", "-f", self.compose_file, "logs", f"--tail={tail}"]
        if service:
            cmd.append(service)
        return self._exec(cmd, cwd=cwd)

    def build(self, service=None, cwd=None):
        cmd = ["docker", "compose", "-f", self.compose_file, "build"]
        if service:
            cmd.append(service)
        return self._exec(cmd, cwd=cwd)

    def stop(self, service=None, cwd=None):
        cmd = ["docker", "compose", "-f", self.compose_file, "stop"]
        if service:
            cmd.append(service)
        return self._exec(cmd, cwd=cwd)

    def start(self, service=None, cwd=None):
        cmd = ["docker", "compose", "-f", self.compose_file, "start"]
        if service:
            cmd.append(service)
        return self._exec(cmd, cwd=cwd)

    def restart(self, service=None, cwd=None):
        cmd = ["docker", "compose", "-f", self.compose_file, "restart"]
        if service:
            cmd.append(service)
        return self._exec(cmd, cwd=cwd)

    def scale(self, service, replicas, cwd=None):
        cmd = ["docker", "compose", "-f", self.compose_file, "up", "-d", "--scale", f"{service}={replicas}"]
        return self._exec(cmd, cwd=cwd)

    # ---- Future Enhancements ----

    def up_profile(self, profile, cwd=None):
        return self._exec(
            ["docker", "compose", "-f", self.compose_file, "--profile", profile, "up", "-d"],
            cwd=cwd
        )

    def env_file(self, env_file):
        self.env_file = env_file
