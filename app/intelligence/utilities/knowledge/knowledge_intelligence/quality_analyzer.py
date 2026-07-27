"""
Quality Analyzer

Analyzes quality-related evidence
from the semantic knowledge document.
"""

from app.intelligence.utilities.knowledge.knowledge_intelligence.intelligence_models import (
    IntelligenceResult,
)


class QualityAnalyzer:

    def analyze(self, document):

        result = IntelligenceResult()

        result.title = "Quality"

        score = 0

        # -------------------------------------------------
        # Traverse Document
        # -------------------------------------------------

        for sentence in document.sentences:

            for clause in sentence.clauses:

                for fact in clause.facts:

                    interp = fact.interpretation

                    # -------------------------------------
                    # Quality Domain
                    # -------------------------------------

                    if (
                        interp.domain.found
                        and interp.domain.domain == "quality"
                    ):

                        score += 20

                        result.findings.append(fact)

                        result.strengths.append(fact.text)

                        # -----------------------------
                        # Quantified achievement
                        # -----------------------------

                        if interp.quantified:

                            score += 15

                        # -----------------------------
                        # Achievement bonus
                        # -----------------------------

                        if interp.achievement:

                            score += 10

                        # -----------------------------
                        # Business KPI bonus
                        # -----------------------------

                        if interp.metric.found:

                            score += 10

        # -------------------------------------------------
        # Final Score
        # -------------------------------------------------

        result.score = min(score, 100)

        result.confidence = 0.95

        # -------------------------------------------------
        # Recommendation
        # -------------------------------------------------

        if result.score < 50:

            result.recommendations.append(
                "Include measurable quality improvements with quantified business impact."
            )

        return result