# agent/nlp/command_mapper.py

class CommandMapper:
    """
    Maps classified intent to a workflow name.
    Example:
        DEPLOY   → deploy
        ROLLBACK → rollback
        DEBUG    → debug
        LOGS     → logs
        COST     → cost
        BUILD    → build
        PIPELINE → pipeline_debug
        STATUS   → cluster_health
    """

    def __init__(self):
        # mapping intent → workflow file name (without .py)
        self.table = {
            "DEPLOY": "deploy",
            "ROLLBACK": "rollback",
            "DEBUG": "debug",
            "BUILD": "build",
            "LOGS": "logs",
            "COST": "cost_analysis",
            "PIPELINE": "pipeline_debug",
            "SCALE": "scale",
            "STATUS": "cluster_health",
        }

    def map_intent(self, intent: str) -> str:
        # fallback if unknown
        return self.table.get(intent, "unknown")

