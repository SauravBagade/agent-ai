# agent/tools/helper_tool.py

import time
import json
import datetime
import re


class HelperTool:
    """
    Helper utility functions for DevOps Agent.

    Provides:
      - JSON parsing
      - text matching
      - time formatting
      - retry helper
      - shell output cleaner
      - simple mapping utilities
      - name normalization

    These helpers improve reliability & reduce duplication across workflows.
    """

    # ---- JSON PARSER ----

    def parse_json(self, text: str):
        try:
            return json.loads(text)
        except Exception:
            return None

    # ---- CLEAN TEXT (LOGS / CLI OUTPUT) ----

    def clean_output(self, text: str):
        if not text:
            return text
        # remove ANSI colors + whitespace noise
        ansi = re.compile(r"\x1B\[[0-9;]*[a-zA-Z]")
        text = ansi.sub("", text)
        return text.strip()

    # ---- SIMPLE RETRY LOOP ----

    def retry(self, func, attempts: int = 3, delay: float = 1.0):
        last = None
        for _ in range(attempts):
            try:
                return func()
            except Exception as e:
                last = str(e)
                time.sleep(delay)
        return f"[retry-failed] {last}"

    # ---- TIME UTILS ----

    def now(self):
        return datetime.datetime.utcnow().isoformat() + "Z"

    def since_seconds(self, ts: float):
        return round(time.time() - ts, 2)

    # ---- NORMALIZATION ----

    def normalize_app(self, app: str):
        """
        Convert app name variations into canonical form.
        e.g:
          apache -> httpd
          nginx -> nginx
        """
        mapping = {
            "apache": "httpd",
            "httpd": "httpd",
            "nginx": "nginx",
            "redis": "redis",
            "mysql": "mysql"
        }
        return mapping.get(app.lower(), app.lower())

    # ---- SAFE CONVERT ----

    def safe_int(self, x, default=None):
        try:
            return int(x)
        except:
            return default

    def safe_float(self, x, default=None):
        try:
            return float(x)
        except:
            return default

    # ---- DICTIONARY MERGE ----

    def merge(self, a: dict, b: dict):
        out = dict(a or {})
        out.update(b or {})
        return out
