"""
Absolute Detector

Detects standalone measurements such as

    99%
    $450000
    2.4M
    12 hours

This detector is intentionally executed LAST because
range and delta detectors are more specific.
"""

from app.intelligence.utilities.knowledge.knowledge_parser.measurement.measurement_patterns import (
    MeasurementPatterns,
)

from app.intelligence.utilities.knowledge.knowledge_parser.measurement.unit_normalizer import (
    UnitNormalizer,
)


class AbsoluteDetector:

    def __init__(self):

        self.normalizer = UnitNormalizer()

    # ---------------------------------------------------------

    def detect(self, text):

        matches = list(

            MeasurementPatterns.ABSOLUTE_PATTERN.finditer(text)

        )

        if not matches:

            return None

        # Last numeric match is usually the KPI value
        match = matches[-1]

        value = self.normalizer.normalize_value(

            match.group("value"),

            match.group("magnitude") or "",

        )

        unit = self.normalizer.normalize_unit(

            (match.group("currency") or "")
            + (match.group("unit") or "")

        )

        return {

            "measurement_type": "absolute",

            "from_value": None,

            "to_value": None,

            "change_value": None,

            "percent_change": None,

            "numeric_value": value,

            "unit": unit,

        }