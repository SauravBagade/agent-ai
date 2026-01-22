# tool-backends/helm/repo_backend.py

import subprocess


class HelmRepoBackend:
    """
    Manages Helm repositories:
      - add/remove
      - update
      - list
      - search
    """

    def _exec(self, cmd):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return out.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[helm-repo-error] {e.output.decode('utf-8').strip()}"

    def add(self, name, url):
        return self._exec(["helm", "repo", "add", name, url])

    def update(self):
        return self._exec(["helm", "repo", "update"])

    def list(self):
        return self._exec(["helm", "repo", "list"])

    def search(self, name):
        return self._exec(["helm", "search", "repo", name])
