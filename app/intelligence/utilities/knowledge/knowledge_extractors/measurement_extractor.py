"""
Measurement Extractor

Extracts KPI measurements
from resume achievements.

Repository Driven Version
"""

import re

from app.intelligence.utilities.knowledge.repository.repository import Repository

from app.intelligence.utilities.knowledge.knowledge_extractor_models.measurement_models import (
    MeasurementKnowledge,
)


class MeasurementExtractor:

    def __init__(self):

        self.repository = Repository()

        self.patterns = self.repository.get_measurement_patterns()

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

                unit=metric.preferred_unit or "%",

                operator=self._operator(text),

                direction="",

                effect="",

                business_meaning="",

                confidence=0.98,

                # -------------------------
                # Ontology
                # -------------------------

                entity_id=metric.entity_id,

                business_area=metric.business_area,

                impact_weight=metric.impact_weight,

                source=metric.source,

                metadata=metric.metadata,

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

                multiplier = self.patterns.get(
                    "multipliers",
                    {}
                ).get(
                    suffix.lower(),
                    1,
                )

            normalized = value * multiplier

            return MeasurementKnowledge(

                found=True,

                metric=metric.canonical,

                canonical=metric.canonical,

                category=metric.category,

                value=money.group(1),

                numeric_value=value,

                normalized_value=normalized,

                unit=metric.preferred_unit or "$",

                operator=self._operator(text),

                direction="",

                effect="",

                business_meaning="",

                confidence=0.98,

                # -------------------------
                # Ontology
                # -------------------------

                entity_id=metric.entity_id,

                business_area=metric.business_area,

                impact_weight=metric.impact_weight,

                source=metric.source,

                metadata=metric.metadata,

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

                unit=metric.preferred_unit,

                operator=self._operator(text),

                direction="",

                effect="",

                business_meaning="",

                confidence=0.95,

                # -------------------------
                # Ontology
                # -------------------------

                entity_id=metric.entity_id,

                business_area=metric.business_area,

                impact_weight=metric.impact_weight,

                source=metric.source,

                metadata=metric.metadata,

            )

        # ======================================================

        return MeasurementKnowledge()

    # ----------------------------------------------------------

    def _operator(self, text):

        for op in self.patterns.get("operators", []):

            if f" {op} " in text:
                return op

        return ""