# tool-backend/github/utils.py

class GitHubUtils:
    """
    Helpers for GitHub formatting + identifiers.
    """

    def parse_repo(self, s):
        return s.split("/")
