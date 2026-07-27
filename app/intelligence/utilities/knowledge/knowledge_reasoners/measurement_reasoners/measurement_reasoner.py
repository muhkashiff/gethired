"""
Measurement Reasoner

Enriches MeasurementKnowledge with business semantics.

This module determines:

- direction (increase / decrease / neutral)
- effect (positive / negative / neutral)
- business meaning

Unlike earlier versions, this module updates the existing
MeasurementKnowledge object instead of creating a separate
MeasurementReasoning object.
"""

import json
from pathlib import Path


class MeasurementReasoner:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent.parent
            / "knowledge_knowledge"
            / "semantics"
            / "measurement_semantics.json"
        )

        from app.intelligence.utilities.knowledge.repository import repository

        self.rules = repository.get_semantics()

    # ----------------------------------------------------------

    def reason(
        self,
        action,
        measurement,
    ):
        """
        Enrich MeasurementKnowledge with
        direction and business effect.
        """

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
        """
        Determines whether the action has a
        positive or negative business impact.

        Rules are metric-specific.
        """

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