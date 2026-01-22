# agent/core/planner.py

from agent.nlp.intent_classifier import IntentClassifier
from agent.nlp.command_mapper import CommandMapper
from agent.nlp.parser import Parser

class Planner:
    """
    The Planner decides WHAT needs to be done.

    Pipeline:
        user_text → intent → workflow → parsed entities → plan dict

    Example:
        input:  "deploy nginx in prod scaled to 3"
        output:
            {
              "intent": "DEPLOY",
              "workflow": "deploy",
              "entities": {
                  "app": "nginx",
                  "namespace": "prod",
                  "replicas": 3
              },
              "raw": "deploy nginx in prod scaled to 3"
            }
    """

    def __init__(self, model):
        self.model = model
        self.intent = IntentClassifier()
        self.mapper = CommandMapper()
        self.parser = Parser()

    def create_plan(self, user_query: str) -> dict:
        intent = self.intent.classify(user_query)
        workflow = self.mapper.map_intent(intent)
        entities = self.parser.parse(user_query)

        plan = {
            "raw": user_query,
            "intent": intent,
            "workflow": workflow,
            "entities": entities,
        }

        # future: ask cloud model for planning refinement
        # e.g. self.model.plan(plan)

        return plan

