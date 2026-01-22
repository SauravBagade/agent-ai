# agent/core/memory.py

class Memory:
    """
    Simple in-memory store for DevOps agent context.
    Handles:
      - last app (nginx, api, backend)
      - last namespace (prod, dev)
      - last replicas
      - last cluster (eks, aks, gke)
      - last provider (aws, gcp, azure)
      - last workflow (deploy, scale, logs, etc.)

    Future upgrades:
      - persistent memory
      - vector memory (LLM embeddings)
      - per-user session memory
      - hierarchical context
      - cloud state caching
      - multi-agent shared memory
    """

    def __init__(self):
        self.store = {}

    def update(self, data: dict):
        """
        Update memory from parsed entities or workflow results.
        Example:
            memory.update({"app": "nginx", "namespace": "prod"})
        """
        for k, v in data.items():
            if v is not None:
                self.store[k] = v

    def get(self, key: str, default=None):
        return self.store.get(key, default)

    def get_context(self):
        """
        Return all memory (useful for planner/executor).
        """
        return dict(self.store)

    def clear(self, keys: list = None):
        if keys is None:
            self.store.clear()
        else:
            for k in keys:
                self.store.pop(k, None)

    def __repr__(self):
        return f"Memory({self.store})"
