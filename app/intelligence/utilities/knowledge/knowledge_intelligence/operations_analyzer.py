"""
Operations Analyzer

Analyzes operational excellence evidence
from the semantic knowledge document.
"""

from app.intelligence.utilities.knowledge.knowledge_intelligence.intelligence_models import (
    IntelligenceResult,
)


class OperationsAnalyzer:

    def analyze(self, document):

        result = IntelligenceResult()

        result.title = "Operations"

        score = 0

        # -------------------------------------------------
        # Traverse Document
        # -------------------------------------------------

        for sentence in document.sentences:

            for clause in sentence.clauses:

                for fact in clause.facts:

                    interp = fact.interpretation

                    # -------------------------------------
                    # Operations Domain
                    # -------------------------------------

                    if (
                        interp.domain.found
                        and interp.domain.domain == "operational_excellence"
                    ):

                        score += 20

                        result.findings.append(fact)

                        result.strengths.append(fact.text)

                        # ---------------------------------
                        # Measurement Present
                        # ---------------------------------

                        if interp.measurement.found:

                            score += 15

                        # ---------------------------------
                        # Quantified Result
                        # ---------------------------------

                        if interp.quantified:

                            score += 10

                        # ---------------------------------
                        # Achievement Bonus
                        # ---------------------------------

                        if interp.achievement:

                            score += 10

                        # ---------------------------------
                        # KPI Bonus
                        # ---------------------------------

                        if interp.metric.found:

                            score += 10

                        # ---------------------------------
                        # Positive Business Effect
                        # ---------------------------------

                        if (
                            interp.measurement.found
                            and interp.measurement.effect == "positive"
                        ):

                            score += 5

        # -------------------------------------------------
        # Final Score
        # -------------------------------------------------

        result.score = min(score, 100)

        result.confidence = 0.95

        # -------------------------------------------------
        # Recommendations
        # -------------------------------------------------

        if result.score < 50:

            result.recommendations.append(
                "Include quantified operational improvements demonstrating measurable business impact."
            )

        return result