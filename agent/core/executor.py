# agent/core/executor.py

from agent.workflows.deploy import DeployWorkflow
from agent.workflows.rollback import RollbackWorkflow
from agent.workflows.debug import DebugWorkflow
from agent.workflows.scale import ScaleWorkflow
from agent.workflows.logs import LogsWorkflow
from agent.workflows.cost_analysis import CostWorkflow
from agent.workflows.pipeline_debug import PipelineDebugWorkflow
from agent.workflows.cluster_health import ClusterHealthWorkflow


class Executor:
    """
    Executor is the action engine.
    It receives a plan from the Planner and executes the associated workflow.
    """

    def __init__(self, model):
        self.model = model

        # workflow lookup table
        self.workflows = {
            "deploy": DeployWorkflow,
            "rollback": RollbackWorkflow,
            "debug": DebugWorkflow,
            "scale": ScaleWorkflow,
            "logs": LogsWorkflow,
            "cost_analysis": CostWorkflow,
            "pipeline_debug": PipelineDebugWorkflow,
            "cluster_health": ClusterHealthWorkflow,
        }

    def run(self, plan: dict):
        workflow_name = plan.get("workflow")
        intent = plan.get("intent")

        # safety fallback
        if workflow_name is None or workflow_name == "unknown":
            return f"❓ Unknown intent: {intent}"

        workflow_cls = self.workflows.get(workflow_name)

        if workflow_cls is None:
            return f"❌ Workflow not implemented: {workflow_name}"

        try:
            workflow = workflow_cls()
            result = workflow.run(plan)
            return result
        except Exception as e:
            return f"💥 Execution error: {str(e)}"

