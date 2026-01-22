# agent/tools/git_tool.py

import subprocess
import os


class GitTool:
    """
    Git Tool using git CLI for repo operations.

    Supports:
      - clone repo
      - pull updates
      - checkout branch
      - create branch
      - add/commit/push
      - get status
      - get log
      - tag (future)
      - diff (future)

    Works with:
      - GitHub
      - GitLab
      - Bitbucket
      - Self-hosted Git
    """

    def __init__(self, workdir: str = None):
        self.workdir = workdir or os.getcwd()

    # ---- CLONE ----

    def clone(self, repo_url: str, dest: str = None):
        dest = dest or "."
        cmd = ["git", "clone", repo_url, dest]
        return self._exec(cmd)

    # ---- PULL ----

    def pull(self):
        cmd = ["git", "pull"]
        return self._exec(cmd)

    # ---- CHECKOUT ----

    def checkout(self, branch: str):
        cmd = ["git", "checkout", branch]
        return self._exec(cmd)

    # ---- CREATE BRANCH ----

    def create_branch(self, branch: str):
        cmd = ["git", "checkout", "-b", branch]
        return self._exec(cmd)

    # ---- ADD ----

    def add(self, path: str = "."):
        cmd = ["git", "add", path]
        return self._exec(cmd)

    # ---- COMMIT ----

    def commit(self, message: str):
        cmd = ["git", "commit", "-m", message]
        return self._exec(cmd)

    # ---- PUSH ----

    def push(self, branch: str = None):
        cmd = ["git", "push"]
        if branch:
            cmd.append("origin")
            cmd.append(branch)
        return self._exec(cmd)

    # ---- STATUS ----

    def status(self):
        cmd = ["git", "status", "-s"]
        return self._exec(cmd)

    # ---- LOG ----

    def log(self, n: int = 10):
        cmd = ["git", "log", f"-{n}", "--oneline"]
        return self._exec(cmd)

    # ---- DIFF ----

    def diff(self, target: str = "HEAD"):
        cmd = ["git", "diff", target]
        return self._exec(cmd)

    # ---- INTERNAL EXEC ----

    def _exec(self, cmd):
        try:
            result = subprocess.check_output(
                cmd,
                stderr=subprocess.STDOUT,
                cwd=self.workdir
            )
            return result.decode("utf-8").strip()

        except subprocess.CalledProcessError as e:
            return f"[git-error] {e.output.decode('utf-8').strip()}"

        except FileNotFoundError:
            return "[git-not-installed] git CLI not found."
