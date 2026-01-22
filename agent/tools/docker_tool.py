# agent/tools/docker_tool.py

import subprocess

class DockerTool:
    """
    Docker Tool for running containers through Docker CLI.

    Supports basic operations:
      - run container
      - stop container
      - remove container
      - list containers
      - show logs

    Future:
      - build image
      - push to registry
      - inspect container
      - exec commands
      - stats / health checks
    """

    # ---- RUN CONTAINER ----

    def run_container(self, app: str, port: int = 80):
        """
        Run container by app name.
        Maps common DevOps app names to images.
        """

        image_map = {
            "nginx": "nginx",
            "apache": "httpd",
            "httpd": "httpd",
            "redis": "redis",
            "mysql": "mysql",
        }

        image = image_map.get(app, app)

        cmd = ["docker", "run", "-d", "--name", app, "-p", f"{port}:{port}", image]

        return self._exec(cmd)

    # ---- STOP ----

    def stop_container(self, app: str):
        cmd = ["docker", "stop", app]
        return self._exec(cmd)

    # ---- REMOVE ----

    def remove_container(self, app: str):
        cmd = ["docker", "rm", "-f", app]
        return self._exec(cmd)

    # ---- LIST ----

    def list_containers(self):
        cmd = ["docker", "ps", "-a"]
        return self._exec(cmd)

    # ---- LOGS ----

    def logs(self, app: str):
        cmd = ["docker", "logs", app]
        return self._exec(cmd)

    # ---- PRIVATE EXEC HELPER ----

    def _exec(self, cmd):
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return result.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[docker-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[docker-not-installed] Docker CLI not found."
