"""
Parser Utilities

Shared helper functions used by the
Knowledge Parser.

Keeps SentenceParser lightweight while
centralising parser intelligence.
"""

from statistics import mean


class ParserUtils:

    # ----------------------------------------------------------
    # Confidence
    # ----------------------------------------------------------

    @staticmethod
    def calculate_confidence(
        action,
        obj,
        domain,
        metric,
        measurement,
        modifiers,
    ):

        scores = []

        if getattr(action, "found", False):
            scores.append(action.confidence)

        if getattr(obj, "found", False):
            scores.append(obj.confidence)

        if getattr(domain, "found", False):
            scores.append(domain.confidence)

        if getattr(metric, "found", False):
            scores.append(metric.confidence)

        if getattr(measurement, "found", False):
            scores.append(measurement.confidence)

        for modifier in modifiers:

            if getattr(modifier, "found", False):
                scores.append(modifier.confidence)

        if not scores:
            return 0.0

        return round(mean(scores), 2)

    # ----------------------------------------------------------
    # Achievement
    # ----------------------------------------------------------

    @staticmethod
    def is_achievement(
        action,
        measurement,
    ):
        """
        Temporary implementation.

        Later this should become ontology-driven by reading
        action.metadata["is_achievement"] or similar.
        """

        achievement_verbs = {

            "lead",
            "implement",
            "improve",
            "increase",
            "reduce",
            "optimize",
            "develop",
            "manage",
            "deliver",
            "achieve",
            "create",
            "build",
            "launch",
            "establish",
            "design",
            "transform",

        }

        if getattr(action, "base", "").lower() in achievement_verbs:
            return True

        if getattr(measurement, "found", False):
            return True

        return False

    # ----------------------------------------------------------
    # Semantic Type
    # ----------------------------------------------------------

    @staticmethod
    def semantic_type(domain):
        """
        Ontology driven.

        No hardcoded mapping required.
        """

        if not getattr(domain, "found", False):
            return "general"

        return getattr(
            domain,
            "business_area",
            "general",
        )

    # ----------------------------------------------------------
    # Business Area
    # ----------------------------------------------------------

    @staticmethod
    def business_area(domain):
        """
        Ontology driven.

        Returns the business area directly from DomainKnowledge.
        """

        if not getattr(domain, "found", False):
            return "General"

        return getattr(
            domain,
            "business_area",
            "General",
        )

    # ----------------------------------------------------------
    # Resume Strength
    # ----------------------------------------------------------

    @staticmethod
    def resume_strength(confidence):

        if confidence >= 0.95:
            return "Exceptional"

        if confidence >= 0.90:
            return "Very Strong"

        if confidence >= 0.80:
            return "Strong"

        if confidence >= 0.70:
            return "Moderate"

        return "Weak"

    # ----------------------------------------------------------
    # Executive Signal
    # ----------------------------------------------------------

    @staticmethod
    def executive_signal(
        interpretation,
    ):

        if not interpretation.domain.found:
            return False

        executive_domains = {

            "leadership",
            "strategy",
            "operational_excellence",
            "quality_excellence",

        }

        if interpretation.domain.domain in executive_domains:
            return True

        if interpretation.measurement.effect == "positive":
            return True

        return False