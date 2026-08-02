"""
Enterprise Leadership Analyzer

KnowledgeGraph V5 Compatible

Consumes only KnowledgeGraph.

No dependency on old graph.actions(),
graph.domains(), etc.

GETHIRED Enterprise V5
"""

from app.intelligence.eng_models.leadership import Leadership


class LeadershipAnalyzer:

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _nodes(self, graph, entity_type):
        """
        Returns all nodes of a given entity type.
        Compatible with KnowledgeGraph V5.
        """

        return [
            node
            for node in graph.nodes.values()
            if getattr(node, "entity_type", "").lower() == entity_type.lower()
        ]

    # ---------------------------------------------------------

    def analyze(self, graph):

        leadership = Leadership()

        actions = self._nodes(graph, "action")
        domains = self._nodes(graph, "domain")
        metrics = self._nodes(graph, "metric")

        score = 0
        evidence = []

        # --------------------------------------------------
        # Leadership verbs
        # --------------------------------------------------

        leadership_actions = {
            "lead",
            "manage",
            "mentor",
            "coach",
            "develop",
            "direct",
            "supervise",
            "coordinate",
            "guide",
            "train",
            "build",
            "implement",
            "drive",
            "improve",
            "optimize",
        }

        for action in actions:

            label = getattr(action, "label", "").lower()

            if label in leadership_actions:
                score += 15
                evidence.append(action.label)

        # --------------------------------------------------
        # Leadership domains
        # --------------------------------------------------

        for domain in domains:

            label = getattr(domain, "label", "").lower()

            if label in {
                "leadership",
                "management",
                "operations",
                "quality management",
                "food safety",
            }:
                score += 20
                evidence.append(domain.label)

        # --------------------------------------------------
        # Operational metrics
        # --------------------------------------------------

        for metric in metrics:

            category = getattr(metric, "category", "").lower()

            if category in {
                "operations",
                "quality",
                "people",
                "food safety",
                "performance",
            }:
                score += 5

        # --------------------------------------------------
        # Normalize score
        # --------------------------------------------------

        score = min(score, 100)

        leadership.people_management = score
        leadership.operational_leadership = score
        leadership.change_management = min(int(score * 0.80), 100)
        leadership.technical_leadership = min(int(score * 0.70), 100)
        leadership.project_management = min(int(score * 0.60), 100)
        leadership.strategic_leadership = min(int(score * 0.50), 100)
        leadership.financial_leadership = min(int(score * 0.40), 100)
        leadership.commercial_leadership = min(int(score * 0.30), 100)
        leadership.stakeholder_management = min(int(score * 0.50), 100)

        leadership.continuous_improvement = min(
            int(
                (
                    leadership.change_management
                    + leadership.operational_leadership
                    + leadership.technical_leadership
                )
                / 3
            ),
            100,
        )

        values = [
            leadership.people_management,
            leadership.strategic_leadership,
            leadership.operational_leadership,
            leadership.technical_leadership,
            leadership.financial_leadership,
            leadership.commercial_leadership,
            leadership.change_management,
            leadership.stakeholder_management,
            leadership.project_management,
            leadership.continuous_improvement,
        ]

        leadership.overall_score = round(
            sum(values) / len(values),
            2,
        )

        leadership.strengths = sorted(set(evidence))
        leadership.evidence = sorted(set(evidence))
        leadership.confidence = 0.95

        return leadership