"""
Enterprise Quantification Analyzer

Enterprise V6

Purpose
-------
Transforms achievement evidence into
quantified business achievements.

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


class QuantificationAnalyzer:

    ####################################################################
    # PUBLIC API
    ####################################################################

    def analyze(

        self,

        achievements,

    ) -> List[QuantifiedAchievement]:

        quantified = []

        for achievement in achievements:

            result = self._extract(

                achievement

            )

            if result:

                quantified.append(result)

        return quantified

    ####################################################################
    # EXTRACTION
    ####################################################################

    def _extract(

        self,

        achievement,

    ):

        measurement = achievement.measurement

        metric = achievement.metric

        if measurement is None:

            return None

        quantified = QuantifiedAchievement()

        ###############################################################
        # Description
        ###############################################################

        quantified.description = self._description(

            achievement

        )

        ###############################################################
        # Metric
        ###############################################################

        if metric:

            quantified.metric = metric.name

        ###############################################################
        # Value
        ###############################################################

        quantified.value = self._extract_number(

            measurement

        )

        ###############################################################
        # Unit
        ###############################################################

        quantified.unit = self._extract_unit(

            measurement

        )

        ###############################################################
        # Direction
        ###############################################################

        quantified.direction = self._infer_direction(

            achievement

        )

        ###############################################################
        # Confidence
        ###############################################################

        quantified.confidence = achievement.confidence

        return quantified

    ####################################################################
    # DESCRIPTION
    ####################################################################

    def _description(

        self,

        achievement,

    ):

        action = ""

        metric = ""

        if achievement.action:

            action = achievement.action.name

        if achievement.metric:

            metric = achievement.metric.name

        return f"{action} {metric}".strip()

    ####################################################################
    # NUMBER
    ####################################################################

    def _extract_number(

        self,

        measurement,

    ):

        text = str(

            getattr(

                measurement,

                "name",

                "",

            )

        )

        match = re.search(

            r"[-+]?\d*\.?\d+",

            text,

        )

        if match:

            return float(

                match.group()

            )

        return 0.0

    ####################################################################
    # UNIT
    ####################################################################

    def _extract_unit(

        self,

        measurement,

    ):

        text = str(

            getattr(

                measurement,

                "name",

                "",

            )

        ).lower()

        if "%" in text:

            return "%"

        if "$" in text:

            return "$"

        if "kg" in text:

            return "kg"

        if "tons" in text:

            return "tons"

        if "hours" in text:

            return "hours"

        if "days" in text:

            return "days"

        return ""

    ####################################################################
    # DIRECTION
    ####################################################################

    def _infer_direction(

        self,

        achievement,

    ):

        action = ""

        if achievement.action:

            action = achievement.action.name.lower()

        if any(

            word in action

            for word in [

                "reduce",

                "decrease",

                "lower",

                "minimize",

            ]

        ):

            return "decrease"

        if any(

            word in action

            for word in [

                "increase",

                "improve",

                "grow",

                "maximize",

            ]

        ):

            return "increase"

        return "neutral"