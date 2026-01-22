# agent/llm/hybrid_router.py

from agent.llm.cloud_model import CloudModel
from agent.llm.local_model import LocalModel


class HybridLLM:
    """
    Hybrid AI Router

    Cloud Model = reasoning, planning, summarization, debugging
    Local Model = parsing, execution details, logs, output transforms
    """

    def __init__(self):
        self.cloud = CloudModel()
        self.local = LocalModel()

    # ---------- HIGH LEVEL ----------

    def plan(self, text: str) -> str:
        """
        Use cloud for planning & reasoning.
        e.g:
            - "deploy nginx"
            - "why pod crashing"
            - "explain pipeline failure"
        """
        prompt = f"Plan the following DevOps request: {text}"
        return self.cloud.generate(prompt)

    def explain(self, text: str) -> str:
        """
        Cloud explanation/summarization for logs and CI/CD outputs.
        """
        prompt = f"Explain this in simple language:\n{text}"
        return self.cloud.generate(prompt)

    # ---------- EXECUTION SIDE ----------

    def execute(self, text: str) -> str:
        """
        Local execution-oriented parsing.
        e.g:
            - parsing docker output
            - parsing kubectl describe
            - parsing terraform plan
            - log analysis
        """
        prompt = f"Execute/parse: {text}"
        return self.local.generate(prompt)

    def parse_logs(self, logs: str) -> str:
        prompt = f"Parse logs:\n{logs}"
        return self.local.generate(prompt)

    def parse_error(self, error: str) -> str:
        prompt = f"Parse error message:\n{error}"
        return self.local.generate(prompt)

    # ---------- HYBRID LOOP (AGENT STYLE) ----------

    def think_and_execute(self, user_query: str) -> str:
        """
        Future upgrade: agentic loop (plan → act → reflect)
        """
        plan = self.plan(user_query)
        result = self.execute(plan)
        summary = self.explain(result)
        return summary

