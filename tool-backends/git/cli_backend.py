# tool-backend/git/cli_backend.py

import subprocess


class GitCLIBackend:
    """
    Thin wrapper over git CLI.
    """

    def _exec(self, cmd, cwd=None):
        try:
            out = subprocess.check_output(cmd, cwd=cwd, stderr=subprocess.STDOUT)
            return out.decode().strip()
        except subprocess.CalledProcessError as e:
            return f"[git-error] {e.output.decode().strip()}"
        except FileNotFoundError:
            return "[git-missing] git not installed."
