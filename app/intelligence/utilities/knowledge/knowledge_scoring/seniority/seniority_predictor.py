"""
Seniority Predictor

Predicts candidate seniority
from the Knowledge Graph.

This engine NEVER reads resume text.

It only analyses Graph Nodes.
"""
from app.intelligence.utilities.knowledge.knowledge_scoring.engines.leadership_engine import (
    LeadershipEngine,
)
from collections import Counter


class SeniorityPredictor:

    def __init__(self):

        self.weights = {

            "leadership": 3,
            "management": 3,
            "strategy": 4,
            "implementation": 1,
            "optimization": 1,
            "analysis": 1,
            "operations": 1,

        }

    # ----------------------------------------------------------

    def predict(self, graph):

        score = 0

        domains = Counter()

        actions = Counter()

        for node in graph.nodes:

            if node.node_type == "Action":

                category = node.category.lower()

                actions[category] += 1

                score += self.weights.get(category, 0)

            elif node.node_type == "Domain":

                domains[node.label.lower()] += 1

        # ----------------------------------------
        # Executive domains
        # ----------------------------------------

        if domains["leadership"]:

            score += 4

        if domains["strategy"]:

            score += 5

        if domains["operations"]:

            score += 2

        if domains["quality"]:

            score += 2

        # ----------------------------------------
        # Predict level
        # ----------------------------------------

        if score >= 20:

            level = "Executive"

        elif score >= 14:

            level = "Director"

        elif score >= 9:

            level = "Manager"

        elif score >= 5:

            level = "Senior Professional"

        else:

            level = "Professional"

        return {

            "level": level,

            "score": score,

            "actions": dict(actions),

            "domains": dict(domains),

        }