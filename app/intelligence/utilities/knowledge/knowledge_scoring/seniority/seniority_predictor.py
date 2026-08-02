"""
Enterprise Seniority Predictor

KnowledgeGraph V5 Compatible

Uses only KnowledgeGraph.

No dependency on parser output.

GETHIRED Enterprise V5
"""

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
            "quality": 2,
            "food safety": 2,
        }

    # ----------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------

    def _nodes(self, graph, entity_type):

        return [
            node
            for node in graph.nodes.values()
            if getattr(node, "entity_type", "").lower() == entity_type.lower()
        ]

    # ----------------------------------------------------------

    def predict(self, graph):

        score = 0

        domains = Counter()
        actions = Counter()
        business_areas = Counter()

        action_nodes = self._nodes(graph, "action")
        domain_nodes = self._nodes(graph, "domain")

        # ------------------------------------------------------
        # Action Analysis
        # ------------------------------------------------------

        for node in action_nodes:

            category = getattr(node, "category", "").lower()

            actions[category] += 1

            score += self.weights.get(category, 0)

            score += getattr(node, "impact_weight", 1)

            area = getattr(node, "business_area", "").lower()

            if area:
                business_areas[area] += 1

        # ------------------------------------------------------
        # Domain Analysis
        # ------------------------------------------------------

        executive_domains = {
            "leadership": 4,
            "strategy": 5,
            "operations": 2,
            "quality": 2,
            "food safety": 2,
            "business excellence": 3,
        }

        for node in domain_nodes:

            label = getattr(node, "label", "").lower()

            domains[label] += 1

            score += executive_domains.get(label, 0)

        # ------------------------------------------------------
        # Breadth Bonus
        # ------------------------------------------------------

        score += len(domains)

        score += min(len(actions), 5)

        # ------------------------------------------------------
        # Normalize
        # ------------------------------------------------------

        score = round(score, 2)

        # ------------------------------------------------------
        # Level Prediction
        # ------------------------------------------------------

        if score >= 35:
            level = "Executive"

        elif score >= 25:
            level = "Director"

        elif score >= 16:
            level = "Manager"

        elif score >= 8:
            level = "Senior Professional"

        else:
            level = "Professional"

        # ------------------------------------------------------

        return {

            "level": level,

            "score": score,

            "actions": dict(actions),

            "domains": dict(domains),

            "business_areas": dict(business_areas),

        }