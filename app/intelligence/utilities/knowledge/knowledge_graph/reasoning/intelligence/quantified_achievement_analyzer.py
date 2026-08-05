"""
Enterprise Quantified Achievement Analyzer

Enterprise V6

Purpose
-------
Converts achievement evidence into measurable
business achievements.

Input
-----
AchievementEvidence

Output
------
QuantifiedAchievement
"""

import re
from typing import List

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.achievement_models import (
    QuantifiedAchievement,
)


class QuantifiedAchievementAnalyzer:

    def analyze(self, achievements) -> List[QuantifiedAchievement]:

        results = []

        for achievement in achievements:

            quantified = self._analyze_single(achievement)

            if quantified:

                results.append(quantified)

        return results

    # ----------------------------------------------------------

    def _analyze_single(self, achievement):

        if achievement.measurement is None:
            return None

        quantified = QuantifiedAchievement()

        quantified.description = self._description(achievement)

        if achievement.metric:
            quantified.metric = getattr(
                achievement.metric,
                "name",
                "",
            )

        measurement_text = getattr(
            achievement.measurement,
            "name",
            "",
        )

        (
            quantified.value,
            quantified.unit,
        ) = self._extract_measurement(measurement_text)

        quantified.direction = self._direction(achievement)

        quantified.confidence = achievement.confidence

        return quantified

    # ----------------------------------------------------------

    def _description(self, achievement):

        action = ""

        metric = ""

        if achievement.action:
            action = achievement.action.name

        if achievement.metric:
            metric = achievement.metric.name

        return f"{action} {metric}".strip()

    # ----------------------------------------------------------

    def _extract_measurement(self, text):

        if not text:
            return 0.0, ""

        numbers = re.findall(

            r"\d+(?:\.\d+)?",

            text,

        )

        value = 0.0

        if numbers:
            value = float(numbers[-1])

        unit = ""

        text_lower = text.lower()

        if "%" in text:
            unit = "%"

        elif "kg" in text_lower:
            unit = "kg"

        elif "ton" in text_lower:
            unit = "tons"

        elif "day" in text_lower:
            unit = "days"

        elif "hour" in text_lower:
            unit = "hours"

        elif "$" in text or "usd" in text_lower:
            unit = "USD"

        elif "pkr" in text_lower:
            unit = "PKR"

        elif "million" in text_lower:
            unit = "million"

        return value, unit

    # ----------------------------------------------------------

    def _direction(self, achievement):

        if achievement.action is None:
            return "neutral"

        action = achievement.action.name.lower()

        decrease = {

            "reduce",

            "decrease",

            "lower",

            "minimize",

            "cut",

        }

        increase = {

            "increase",

            "improve",

            "grow",

            "maximize",

            "boost",

            "raise",

        }

        for word in decrease:

            if word in action:
                return "decrease"

        for word in increase:

            if word in action:
                return "increase"

        return "neutral"