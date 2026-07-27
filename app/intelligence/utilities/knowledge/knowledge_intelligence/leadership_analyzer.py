"""
Leadership Analyzer

Analyzes leadership-related evidence
from the semantic knowledge document.
"""

from app.intelligence.utilities.knowledge.knowledge_intelligence.intelligence_models import (
    IntelligenceResult,
)


class LeadershipAnalyzer:

    def analyze(self, document):

        result = IntelligenceResult()

        result.title = "Leadership"

        score = 0

        # -------------------------------------------------
        # Traverse Document
        # -------------------------------------------------

        for sentence in document.sentences:

            for clause in sentence.clauses:

                for fact in clause.facts:

                    interp = fact.interpretation

                    # -------------------------------------
                    # Leadership Domain
                    # -------------------------------------

                    if (
                        interp.domain.found
                        and interp.domain.domain == "leadership"
                    ):

                        score += 20

                        result.findings.append(fact)

                        result.strengths.append(fact.text)

                        # -----------------------------
                        # Quantified achievement
                        # -----------------------------

                        if interp.quantified:

                            score += 10

                        # -----------------------------
                        # Achievement bonus
                        # -----------------------------

                        if interp.achievement:

                            score += 10

        # -------------------------------------------------
        # Final Score
        # -------------------------------------------------

        result.score = min(score, 100)

        result.confidence = 0.95

        # -------------------------------------------------
        # Recommendation
        # -------------------------------------------------

        if result.score < 40:

            result.recommendations.append(
                "Add more leadership accomplishments."
            )

        return result