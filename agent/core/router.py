# agent/core/router.py

from agent.core.planner import Planner
from agent.core.executor import Executor


class Router:
    """
    Router handles full high-level pipeline:

        user_input
           ↓
        Planner    (what to do)
           ↓
        Executor   (run the workflow)
           ↓
        result

    This is the agent control loop for DevOps tasks.
    """

    def __init__(self, model):
        self.model = model
        self.planner = Planner(model)
        self.executor = Executor(model)

    def process(self, user_query: str):
        if not user_query or not isinstance(user_query, str):
            return "❌ Invalid query."

        try:
            # 1) create execution plan
            plan = self.planner.create_plan(user_query)

            # 2) execute workflow based on plan
            result = self.executor.run(plan)

            return result

        except Exception as e:
            return f"💥 Router error: {str(e)}"

