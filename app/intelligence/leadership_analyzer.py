"""
GetHired

Leadership Analyzer

Analyzes responsibilities and achievements
to produce leadership intelligence.
"""

import re

from app.intelligence.eng_models.leadership import Leadership
from app.intelligence.eng_knowledge.leadership_loader import (
    LeadershipKnowledge,
)


class LeadershipAnalyzer:

    def __init__(self):

        self.knowledge = LeadershipKnowledge()

    # ======================================================
    # MAIN
    # ======================================================

    def analyze(self, experiences):

        leadership = Leadership()

        dimensions = self.knowledge.get_dimensions()

        evidence = []

        strengths = []

        scores = {}

        # initialize scores

        for item in dimensions:

            scores[item["dimension"]] = 0

        # ------------------------------------------
        # Analyze each experience
        # ------------------------------------------

        for job in experiences:

            text = []

            text.extend(job.responsibilities)

            text.extend(job.achievements)

            for sentence in text:

                lower = sentence.lower()

                for item in dimensions:

                    matched = False

                    for keyword in item["keywords"]:

                        if keyword.lower() in lower:

                            scores[item["dimension"]] += item["weight"]

                            evidence.append(sentence)

                            matched = True

                            break

                    if matched:
                        continue

        # ------------------------------------------
        # Normalize (0-100)
        # ------------------------------------------

        for item in dimensions:

            dimension = item["dimension"]

            value = min(scores[dimension], 100)

            setattr(leadership, dimension, value)

            if value >= 70:

                strengths.append(dimension.replace("_", " ").title())

        leadership.strengths = strengths

        leadership.evidence = evidence

        # ------------------------------------------
        # Continuous Improvement bonus
        # ------------------------------------------

        ci = leadership.change_management

        op = leadership.operational_leadership

        tech = leadership.technical_leadership

        leadership.continuous_improvement = min(
            100,
            int((ci + op + tech) / 3)
        )

        # ------------------------------------------
        # Overall Leadership Score
        # ------------------------------------------

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

            leadership.continuous_improvement

        ]

        leadership.overall_score = round(
            sum(values) / len(values),
            2
        )

        leadership.confidence = 0.95

        return leadership