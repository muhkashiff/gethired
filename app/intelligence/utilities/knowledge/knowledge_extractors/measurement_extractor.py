"""
Measurement Extractor

Extracts KPI measurements
from resume achievements.
"""

import json
import re
from pathlib import Path

from app.intelligence.utilities.knowledge.knowledge_extractor_models.measurement_models import (
    MeasurementKnowledge,
)


class MeasurementExtractor:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent.parent
            / "knowledge_knowledge"
            / "config"
            / "measurement_patterns.json"
        )

        with open(path, encoding="utf8") as f:
            self.patterns = json.load(f)

    # ----------------------------------------------------------

    def extract(self, sentence, metric):

        if not metric.found:
            return MeasurementKnowledge()

        text = sentence.lower()

        # ======================================================
        # Percentage
        # ======================================================

        percent = re.search(r"(\d+(?:\.\d+)?)\s*%", text)

        if percent:

            value = float(percent.group(1))

            return MeasurementKnowledge(

                found=True,

                metric=metric.canonical,

                canonical=metric.canonical,

                category=metric.category,

                value=percent.group(1),

                numeric_value=value,

                normalized_value=value,

                unit="%",

                operator=self._operator(text),

                direction="",

                effect="",

                business_meaning="",

                confidence=0.98

            )

        # ======================================================
        # Currency
        # ======================================================

        money = re.search(r"\$(\d+(?:\.\d+)?)([kmb])?", text)

        if money:

            value = float(money.group(1))

            suffix = money.group(2)

            multiplier = 1

            if suffix:
                multiplier = self.patterns["multipliers"][suffix.lower()]

            normalized = value * multiplier

            return MeasurementKnowledge(

                found=True,

                metric=metric.canonical,

                canonical=metric.canonical,

                category=metric.category,

                value=money.group(1),

                numeric_value=value,

                normalized_value=normalized,

                unit="$",

                operator=self._operator(text),

                direction="",

                effect="",

                business_meaning="",

                confidence=0.98

            )

        # ======================================================
        # Plain Number
        # ======================================================

        integer = re.search(r"\b(\d+)\b", text)

        if integer:

            value = float(integer.group(1))

            return MeasurementKnowledge(

                found=True,

                metric=metric.canonical,

                canonical=metric.canonical,

                category=metric.category,

                value=integer.group(1),

                numeric_value=value,

                normalized_value=value,

                unit=metric.unit,

                operator=self._operator(text),

                direction="",

                effect="",

                business_meaning="",

                confidence=0.95

            )

        # ======================================================

        return MeasurementKnowledge()

    # ----------------------------------------------------------

    def _operator(self, text):

        for op in self.patterns["operators"]:

            if f" {op} " in text:
                return op

        return ""