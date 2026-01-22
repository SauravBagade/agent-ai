# tool-backend/git/utils.py

import re


class GitUtils:
    """
    Helpers for parsing versions, branches, commit IDs, etc.
    """

    def is_semver(self, tag):
        return bool(re.match(r"^\d+\.\d+\.\d+$", tag))

    def normalize_branch(self, name):
        return name.replace("_", "-").lower()
