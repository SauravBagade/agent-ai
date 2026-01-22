# agent/nlp/intent_classifier.py

class IntentClassifier:
    """
    Classifies natural language into DevOps intents.
    Example:
        "deploy nginx"      → DEPLOY
        "rollback release"  → ROLLBACK
        "why pipeline fail" → DEBUG
        "show logs for api" → LOGS
        "scale app to 5"    → SCALE
        "how much cost"     → COST
    """

    def classify(self, query: str) -> str:
        text = query.lower()

        # ---- DEPLOY ----
        if any(word in text for word in [
            "deploy", "launch", "start", "release", "create deployment", "apply"
        ]):
            return "DEPLOY"

        # ---- ROLLBACK ----
        if any(word in text for word in [
            "rollback", "undo", "revert", "previous version"
        ]):
            return "ROLLBACK"

        # ---- DEBUG ----
        if any(word in text for word in [
            "debug", "fix", "fail", "error", "why", "troubleshoot", "issue"
        ]):
            return "DEBUG"

        # ---- SCALE ----
        if any(word in text for word in [
            "scale", "increase", "decrease", "replicas", "autoscale"
        ]):
            return "SCALE"

        # ---- BUILD (Docker CI) ----
        if any(word in text for word in [
            "build", "image", "docker build", "container build"
        ]):
            return "BUILD"

        # ---- LOGS ----
        if any(word in text for word in [
            "logs", "error logs", "kubectl logs", "tail logs"
        ]):
            return "LOGS"

        # ---- COST / FINOPS ----
        if any(word in text for word in [
            "cost", "price", "bill", "billing", "how much", "finops"
        ]):
            return "COST"

        # ---- PIPELINE / CI/CD ----
        if any(word in text for word in [
            "pipeline", "cicd", "github actions", "jenkins", "gitlab ci", "workflow"
        ]):
            return "PIPELINE"

        # ---- STATUS / HEALTH / SRE ----
        if any(word in text for word in [
            "status", "health", "slo", "sli", "uptime"
        ]):
            return "STATUS"

        # ---- DEFAULT ----
        return "UNKNOWN"

