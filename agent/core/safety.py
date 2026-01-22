# agent/core/safety.py

class Safety:
    """
    Safety system to prevent dangerous DevOps operations.

    Example blocked actions:
      - delete cluster
      - destroy infra
      - remove namespace
      - kubectl delete all
      - terraform destroy
    
    TODO (future):
      - RBAC permissions
      - approvals
      - audit logs
      - dry-run enforcement
    """

    def __init__(self):
        # patterns considered destructive
        self.dangerous_words = [
            "destroy",
            "delete",
            "remove",
            "wipe",
            "kill",
            "shutdown",
            "terminate"
        ]

        # protected cloud resources
        self.protected_resources = [
            "cluster",
            "eks",
            "gke",
            "aks",
            "namespace",
            "project"
        ]

        # intents that require approval
        self.approval_required = [
            "DESTROY",
            "DELETE",
            "REMOVE",
            "WIPE"
        ]

    def check(self, plan: dict) -> (bool, str):
        raw = (plan.get("raw") or "").lower()

        # block dangerous patterns
        for word in self.dangerous_words:
            if word in raw:
                # check if tied to protected resource
                for resource in self.protected_resources:
                    if resource in raw:
                        return False, f"⛔ Safety blocked: destructive action '{word} {resource}'"
                return False, f"⚠ Safety blocked: destructive keyword '{word}' detected"

        # allow all other actions
        return True, "✔ Safe to execute"
