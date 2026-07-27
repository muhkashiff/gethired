"""
Achievement Analyzer

Evaluates the strength of extracted KnowledgeFacts.

Input
-----
KnowledgeDocument

Output
------
List[AchievementAnalysis]
"""

from app.intelligence.utilities.knowledge.knowledge_intelligence.achievement_models import (
    AchievementAnalysis,
)


class AchievementAnalyzer:

    def __init__(self):
        pass

    # --------------------------------------------------------
    # Public
    # --------------------------------------------------------

    def analyze(self, document):

        analyses = []

        # Traverse complete hierarchy
        for sentence in document.sentences:

            for clause in sentence.clauses:

                for fact in clause.facts:

                    analyses.append(

                        self._analyze_fact(fact)

                    )

        return analyses

    # --------------------------------------------------------
    # Private
    # --------------------------------------------------------

    def _analyze_fact(self, fact):

        interpretation = fact.interpretation

        analysis = AchievementAnalysis()

        # --------------------------------------------------
        # Is this an achievement?
        # --------------------------------------------------

        analysis.found = interpretation.achievement

        if not interpretation.achievement:

            return analysis

        # --------------------------------------------------
        # Basic Information
        # --------------------------------------------------

        analysis.title = fact.text

        if interpretation.domain.found:

            analysis.category = interpretation.domain.domain

        else:

            analysis.category = "general"

        # --------------------------------------------------
        # Quantified
        # --------------------------------------------------

        analysis.quantified = interpretation.quantified

        # --------------------------------------------------
        # Leadership Detection
        # --------------------------------------------------

        leadership_actions = {

            "lead",
            "manage",
            "coach",
            "mentor",
            "train",
            "direct",
            "supervise",
            "coordinate",
            "guide",

        }

        leadership_domains = {

            "leadership",
            "management",
            "people",

        }

        if (
            interpretation.action.found
            and interpretation.action.base in leadership_actions
        ):

            analysis.leadership = True

        if (
            interpretation.domain.found
            and interpretation.domain.domain in leadership_domains
        ):

            analysis.leadership = True

        # --------------------------------------------------
        # Executive Signal
        # --------------------------------------------------

        analysis.executive = getattr(

            fact,

            "executive_signal",

            False,

        )

        # --------------------------------------------------
        # Business Impact
        # --------------------------------------------------

        if interpretation.measurement.found:

            if interpretation.measurement.effect == "positive":

                analysis.business_impact = True

        if interpretation.metric.found:

            analysis.business_impact = True

        # --------------------------------------------------
        # Certification Achievement
        # --------------------------------------------------

        analysis.certification = False

        if interpretation.object.found:

            if interpretation.object.category in {

                "certification",

                "food_safety",

                "quality",

            }:

                analysis.certification = True

        # --------------------------------------------------
        # Improvement Achievement
        # --------------------------------------------------

        analysis.improvement = False

        if interpretation.action.found:

            if interpretation.action.base in {

                "improve",

                "reduce",

                "increase",

                "optimize",

                "enhance",

                "implement",

            }:

                analysis.improvement = True

        # --------------------------------------------------
        # Score
        # --------------------------------------------------

        score = 0

        if analysis.quantified:
            score += 25

        if analysis.business_impact:
            score += 25

        if analysis.leadership:
            score += 15

        if analysis.executive:
            score += 10

        if analysis.certification:
            score += 15

        if analysis.improvement:
            score += 10

        analysis.score = min(score, 100)

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        analysis.confidence = interpretation.confidence

        # --------------------------------------------------
        # Recommendation
        # --------------------------------------------------

        if analysis.score >= 90:

            analysis.recommendation = (
                "Exceptional executive-level achievement."
            )

        elif analysis.score >= 75:

            analysis.recommendation = (
                "Strong measurable achievement."
            )

        elif analysis.score >= 60:

            analysis.recommendation = (
                "Good achievement. Add more quantified business impact."
            )

        else:

            analysis.recommendation = (
                "Add measurable KPIs, business impact and quantified improvements."
            )

        return analysis