# agent/core/context.py

class Context:
    """
    Manages execution context during a DevOps session.

    Context is different from memory:
      - Memory stores facts (app=nginx, namespace=prod, replicas=3)
      - Context stores execution state (workflow=deploy, phase=completed)

    Used for:
      - chaining multi-step workflows
      - debugging
      - tool responses
      - rollback of actions
      - pipeline analysis
    """

    def __init__(self):
        self.data = {
            "workflow": None,
            "phase": None,
            "last_action": None,
            "last_result": None,
            "status": None,
        }

    def set(self, key: str, value):
        self.data[key] = value

    def update(self, updates: dict):
        for k, v in updates.items():
            self.data[k] = v

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def get_all(self):
        return dict(self.data)

    def clear(self):
        # keeps session but resets context
        self.data = {
            "workflow": None,
            "phase": None,
            "last_action": None,
            "last_result": None,
            "status": None,
        }

    def __repr__(self):
        return f"Context({self.data})"
