"""
Evidence Engine

Computes semantic evidence from a clause.
"""

from app.intelligence.utilities.knowledge.evidence.evidence_models import (
    ClauseEvidence,
)

from app.intelligence.utilities.knowledge.evidence import (
    evidence_weights as W,
)


class EvidenceEngine:

    def score(self, clause):

        evidence = ClauseEvidence()

        # ------------------------------------
        # Leadership
        # ------------------------------------

        if clause.domain.domain == "leadership":

            evidence.leadership = W.LEADERSHIP

        # ------------------------------------
        # Achievement
        # ------------------------------------

        if clause.achievement:

            evidence.achievement = W.ACHIEVEMENT

        # ------------------------------------
        # Quantified
        # ------------------------------------

        if clause.quantified:

            evidence.quantified = W.QUANTIFIED

        # ------------------------------------
        # Business Impact
        # ------------------------------------

        if clause.measurement.effect == "positive":

            evidence.business_impact = W.BUSINESS_IMPACT

        # ------------------------------------
        # Executive Modifier
        # ------------------------------------

        for modifier in clause.modifiers:

            if modifier.category == "achievement":

                evidence.executive = W.EXECUTIVE

                break

        # ------------------------------------
        # Certification
        # ------------------------------------

        if "ISO" in clause.text.upper():

            evidence.certification = W.CERTIFICATION

        if "FSSC" in clause.text.upper():

            evidence.certification = W.CERTIFICATION

        # ------------------------------------
        # Continuous Improvement
        # ------------------------------------

        if clause.action.base in {

            "improve",

            "optimize",

            "reduce",

            "increase",

        }:

            evidence.improvement = W.CONTINUOUS_IMPROVEMENT

        # ------------------------------------
        # Final Score
        # ------------------------------------

        evidence.score = min(

            W.MAX_SCORE,

            evidence.leadership

            + evidence.achievement

            + evidence.quantified

            + evidence.business_impact

            + evidence.executive

            + evidence.certification

            + evidence.improvement,

        )

        evidence.confidence = clause.confidence

        return evidence