"""
Leadership Analyzer

Graph-based Leadership Analyzer

Consumes the KnowledgeGraph instead of raw resume experiences.
"""

from app.intelligence.eng_models.leadership import Leadership


class LeadershipAnalyzer:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def analyze(self, graph):

        leadership = Leadership()

        actions = graph.actions()
        domains = graph.domains()
        metrics = graph.metrics()

        score = 0
        evidence = []

        # ---------------------------------------------
        # Leadership Actions
        # ---------------------------------------------

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

        }

        for action in actions:

            if action.label.lower() in leadership_actions:

                score += 15
                evidence.append(action.label)

        # ---------------------------------------------
        # Leadership Domains
        # ---------------------------------------------

        for domain in domains:

            if domain.label.lower() == "leadership":

                score += 20
                evidence.append(domain.label)

        # ---------------------------------------------
        # Operational KPIs increase leadership
        # ---------------------------------------------

        for metric in metrics:

            if metric.category in (

                "operations",
                "quality",
                "people",

            ):

                score += 5

        # ---------------------------------------------
        # Populate Model
        # ---------------------------------------------

        leadership.people_management = min(score, 100)

        leadership.operational_leadership = min(score, 100)

        leadership.change_management = min(int(score * 0.8), 100)

        leadership.technical_leadership = min(int(score * 0.7), 100)

        leadership.project_management = min(int(score * 0.6), 100)

        leadership.strategic_leadership = min(int(score * 0.5), 100)

        leadership.financial_leadership = min(int(score * 0.4), 100)

        leadership.commercial_leadership = min(int(score * 0.3), 100)

        leadership.stakeholder_management = min(int(score * 0.5), 100)

        leadership.continuous_improvement = min(

            int(

                (
                    leadership.change_management
                    + leadership.operational_leadership
                    + leadership.technical_leadership
                ) / 3
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

        leadership.strengths = evidence

        leadership.evidence = evidence

        leadership.confidence = 0.95

        return leadership