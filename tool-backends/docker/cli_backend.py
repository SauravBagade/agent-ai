# tool-backends/docker/cli_backend.py

import subprocess


class DockerCLIBackend:
    """
    Ultra DevOps Docker CLI Backend

    Provides raw Docker functionality:
      - run / stop / rm / ps
      - build (via CLI)
      - logs
      - inspect
      - exec
      - system prune
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[docker-cli-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[docker-missing] docker binary not installed."

    # ---- RUN CONTAINER ----
    def run(self, image, name=None, ports=None, env=None):
        cmd = ["docker", "run", "-d"]

        if name:
            cmd += ["--name", name]

        if ports:
            for host, container in ports.items():
                cmd += ["-p", f"{host}:{container}"]

        if env:
            for k, v in env.items():
                cmd += ["-e", f"{k}={v}"]

        cmd.append(image)
        return self._exec(cmd)

    # ---- STOP / REMOVE ----
    def stop(self, name):
        return self._exec(["docker", "stop", name])

    def rm(self, name):
        return self._exec(["docker", "rm", name])

    # ---- LOGS ----
    def logs(self, name):
        return self._exec(["docker", "logs", name])

    # ---- INSPECT ----
    def inspect(self, name):
        return self._exec(["docker", "inspect", name])

    # ---- EXEC ----
    def exec(self, name, cmd):
        if isinstance(cmd, str):
            cmd = cmd.split()
        return self._exec(["docker", "exec", name] + cmd)

    # ---- LIST CONTAINERS ----
    def ps(self, all=False):
        cmd = ["docker", "ps"]
        if all:
            cmd.append("-a")
        return self._exec(cmd)

    # ---- IMAGE OPERATIONS ----
    def pull(self, image):
        return self._exec(["docker", "pull", image])

    def tag(self, src, dest):
        return self._exec(["docker", "tag", src, dest])

    def rmi(self, image):
        return self._exec(["docker", "rmi", image])

    # ---- PRUNE ----
    def system_prune(self):
        return self._exec(["docker", "system", "prune", "-f"])
