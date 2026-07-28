"""
Range Detector

Detects measurements expressed as:

    from 70% to 99%
    from 5 to 2
    from $2M to $5M

Produces

    from_value
    to_value
    change_value
    percent_change
"""

from app.intelligence.utilities.knowledge.knowledge_parser.measurement.measurement_patterns import (
    MeasurementPatterns,
)

from app.intelligence.utilities.knowledge.knowledge_parser.measurement.unit_normalizer import (
    UnitNormalizer,
)


class RangeDetector:

    def __init__(self):

        self.normalizer = UnitNormalizer()

    # ---------------------------------------------------------

    def detect(self, text):

        match = MeasurementPatterns.RANGE_PATTERN.search(text)

        if not match:
            return None

        # --------------------------------------------------
        # Preserve original strings
        # --------------------------------------------------

        raw_from = match.group("from")

        raw_to = match.group("to")

        from_unit = match.group("from_unit") or ""

        to_unit = match.group("to_unit") or ""

        raw_from_value = f"{raw_from}{from_unit}".strip()

        raw_to_value = f"{raw_to}{to_unit}".strip()

        # --------------------------------------------------
        # Normalize
        # --------------------------------------------------

        from_value = self.normalizer.normalize_value(raw_from)

        to_value = self.normalizer.normalize_value(raw_to)

        unit = self.normalizer.normalize_unit(

            to_unit or from_unit

        )

        # --------------------------------------------------
        # Calculations
        # --------------------------------------------------

        change = round(

            to_value - from_value,

            2,

        )

        percent_change = self.normalizer.percent_change(

            from_value,

            to_value,

        )

        # --------------------------------------------------

        return {

            "measurement_type": "range",

            "raw_from_value": raw_from_value,

            "raw_to_value": raw_to_value,

            "raw_value": raw_to_value,

            "from_value": from_value,

            "to_value": to_value,

            "change_value": change,

            "percent_change": percent_change,

            "numeric_value": to_value,

            "unit": unit,

        }