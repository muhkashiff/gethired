"""
Measurement Reasoner

Ontology Driven Version

Enriches MeasurementKnowledge using ontology semantics.

Determines

- direction
- effect
- business meaning

Repository Driven
"""

from app.intelligence.utilities.knowledge.repository.repository import Repository


class MeasurementReasoner:

    def __init__(self):

        self.repository = Repository()

        self.rules = self.repository.measurement_semantics()

    # ----------------------------------------------------------

    def reason(
        self,
        action,
        measurement,
    ):

        if not measurement.found:
            return measurement

        verb = action.base.lower()

        direction = self._direction(verb)

        effect = self._effect(
            measurement.canonical,
            verb,
        )

        measurement.direction = direction

        measurement.effect = effect

        measurement.business_meaning = (
            f"{verb} {measurement.canonical}"
        )

        measurement.confidence = max(
            measurement.confidence,
            0.97,
        )

        return measurement

    # ----------------------------------------------------------

    def _direction(self, verb):

        increase = {

            "increase",
            "improve",
            "grow",
            "raise",
            "maximize",
            "achieve",
            "optimize",
            "boost",
            "enhance",

        }

        decrease = {

            "reduce",
            "decrease",
            "drop",
            "eliminate",
            "prevent",
            "minimize",
            "lower",
            "cut",

        }

        if verb in increase:
            return "increase"

        if verb in decrease:
            return "decrease"

        return "neutral"

    # ----------------------------------------------------------

    def _effect(
        self,
        canonical_metric,
        verb,
    ):

        rule = self.rules.get(canonical_metric)

        if rule is None:
            return "neutral"

        positive = [

            v.lower()

            for v in rule.get("positive", [])

        ]

        negative = [

            v.lower()

            for v in rule.get("negative", [])

        ]

        if verb in positive:
            return "positive"

        if verb in negative:
            return "negative"

        return "neutral"