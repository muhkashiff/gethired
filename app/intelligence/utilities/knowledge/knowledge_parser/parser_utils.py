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
        modifiers

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
        measurement

    ):

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
            "transform"

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

        mapping = {

            "leadership": "leadership",

            "food_safety": "food_safety",

            "quality_management": "quality",

            "quality_improvement": "quality",

            "quality_excellence": "quality",

            "operational_excellence": "operations",

            "finance": "finance",

            "supply_chain": "supply_chain",

            "manufacturing": "manufacturing",

            "compliance": "compliance",

            "continuous_improvement": "continuous_improvement"

        }

        return mapping.get(

            getattr(domain, "domain", ""),

            "general"

        )

    # ----------------------------------------------------------
    # Business Area
    # ----------------------------------------------------------

    @staticmethod
    def business_area(domain):

        mapping = {

            "leadership": "Leadership",

            "food_safety": "Food Safety",

            "quality_management": "Quality",

            "quality_improvement": "Quality",

            "quality_excellence": "Quality",

            "operational_excellence": "Operations",

            "finance": "Finance",

            "manufacturing": "Manufacturing",

            "supply_chain": "Supply Chain",

            "compliance": "Compliance",

            "continuous_improvement": "Continuous Improvement"

        }

        return mapping.get(

            getattr(domain, "domain", ""),

            "General"

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

        interpretation

    ):

        if not interpretation.domain.found:

            return False

        executive_domains = {

            "leadership",
            "strategy",
            "operational_excellence",
            "quality_excellence"

        }

        if interpretation.domain.domain in executive_domains:

            return True

        if interpretation.measurement.effect == "positive":

            return True

        return False