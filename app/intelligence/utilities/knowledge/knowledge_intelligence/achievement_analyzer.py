"""
Achievement Analyzer

Evaluates the strength of KnowledgeFacts.

Input
-----
KnowledgeDocument

Output
------
AchievementAnalysis objects
"""

from app.intelligence.utilities.knowledge.knowledge_intelligence.achievement_models import (
    AchievementAnalysis,
)


class AchievementAnalyzer:

    def __init__(self):
        pass

    # --------------------------------------------------------

    def analyze(self, document):

        analyses = []

        for fact in document.facts:

            analyses.append(

                self._analyze_fact(fact)

            )

        return analyses

    # --------------------------------------------------------

    def _analyze_fact(self, fact):

        interpretation = fact.interpretation

        analysis = AchievementAnalysis()

        analysis.found = fact.achievement

        if not fact.achievement:
            return analysis

        # -----------------------------------------
        # Title
        # -----------------------------------------

        analysis.title = fact.text

        # -----------------------------------------
        # Category
        # -----------------------------------------

        analysis.category = interpretation.domain.domain

        # -----------------------------------------
        # Quantified
        # -----------------------------------------

        analysis.quantified = interpretation.quantified

        # -----------------------------------------
        # Leadership
        # -----------------------------------------

        leadership_domains = {

            "leadership",
            "management",
            "people",

        }

        if interpretation.action.base in {

            "lead",
            "manage",
            "coach",
            "train",

        }:

            analysis.leadership = True

        if interpretation.domain.domain in leadership_domains:

            analysis.leadership = True

        # -----------------------------------------
        # Executive
        # -----------------------------------------

        analysis.executive = getattr(
                    fact,
                    "executive_signal",
                    False,
                )

        # -----------------------------------------
        # Business Impact
        # -----------------------------------------

        if interpretation.measurement.found:

            if interpretation.measurement.effect == "positive":

                analysis.business_impact = True

        # -----------------------------------------
        # Score
        # -----------------------------------------

        score = 0

        if analysis.quantified:
            score += 30

        if analysis.business_impact:
            score += 30

        if analysis.leadership:
            score += 20

        if analysis.executive:
            score += 20

        analysis.score = score

        # -----------------------------------------
        # Confidence
        # -----------------------------------------

        analysis.confidence = interpretation.confidence

        # -----------------------------------------
        # Recommendation
        # -----------------------------------------

        if score >= 90:

            analysis.recommendation = "Exceptional achievement."

        elif score >= 70:

            analysis.recommendation = "Strong achievement."

        elif score >= 50:

            analysis.recommendation = "Moderate achievement."

        else:

            analysis.recommendation = (
                "Consider adding measurable business impact."
            )

        return analysis