"""
Base Intelligence Analyzer

Reusable scoring engine for all resume intelligence modules.

Used by:

- Leadership Analyzer
- Quality Analyzer
- Operations Analyzer
- Manufacturing Analyzer
- Food Safety Analyzer
- Supply Chain Analyzer

Architecture:

KnowledgeDocument
        |
        ↓
KnowledgeFact
        |
        ↓
KnowledgeInterpretation
        |
        ↓
BaseAnalyzer
        |
        ↓
IntelligenceResult
"""

from app.intelligence.utilities.knowledge.knowledge_intelligence.intelligence_models import (
    IntelligenceResult,
)


class BaseAnalyzer:
    """
    Generic intelligence scoring engine.
    """


    def __init__(self):

        pass


    # ---------------------------------------------------------
    # Main Analyzer
    # ---------------------------------------------------------

    def analyze(
        self,
        document,
        accepted_domains,
        title,
        recommendation,
    ):

        result = IntelligenceResult()

        result.title = title


        score = 0


        for fact in document.facts:


            interpretation = fact.interpretation


            domain = (
                interpretation.domain.domain
                if interpretation.domain
                else ""
            )


            if domain not in accepted_domains:

                continue


            # ---------------------------------------------
            # Add finding
            # ---------------------------------------------

            result.findings.append(
                fact
            )


            result.strengths.append(
                fact.text
            )


            # ---------------------------------------------
            # Base achievement score
            # ---------------------------------------------

            fact_score = 20



            # ---------------------------------------------
            # Quantified achievement
            # ---------------------------------------------

            if interpretation.quantified:

                fact_score += 15



            # ---------------------------------------------
            # Positive business impact
            # ---------------------------------------------

            measurement = interpretation.measurement


            if measurement:

                if measurement.effect == "positive":

                    fact_score += 15



            # ---------------------------------------------
            # KPI impact weight
            # ---------------------------------------------

            kpi_weight = self.get_kpi_weight(
                interpretation
            )


            if kpi_weight:

                fact_score += int(
                    kpi_weight / 5
                )



            # ---------------------------------------------
            # Leadership signal
            # ---------------------------------------------

            if self.is_leadership_signal(
                interpretation
            ):

                fact_score += 10



            score += fact_score



        # -------------------------------------------------
        # Final score
        # -------------------------------------------------

        result.score = min(
            score,
            100
        )


        result.confidence = 0.95



        if result.score < 50:

            result.recommendations.append(
                recommendation
            )


        return result



    # ---------------------------------------------------------
    # KPI Weight Resolver
    # ---------------------------------------------------------

    def get_kpi_weight(
        self,
        interpretation,
    ):

        """
        Reads impact_weight from ontology.

        Example:

        Customer Complaints

        impact_weight = 95
        """


        try:

            entity = (
                interpretation.metric.entity_id
            )


            if not entity:

                entity = (
                    interpretation.object.entity_id
                )


            if not entity:

                return 0



            # Future repository integration point

            return getattr(
                interpretation.metric,
                "impact_weight",
                0
            )


        except Exception:

            return 0



    # ---------------------------------------------------------
    # Leadership Detection
    # ---------------------------------------------------------

    def is_leadership_signal(
        self,
        interpretation,
    ):


        action = (
            interpretation.action.base.lower()
            if interpretation.action
            else ""
        )


        leadership_actions = {

            "lead",
            "manage",
            "train",
            "coach",
            "mentor",
            "supervise",

        }


        return action in leadership_actions