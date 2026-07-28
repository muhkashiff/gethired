"""
Delta Detector

Detects

    by 20%
    by 15
    by $250000
"""

from app.intelligence.utilities.knowledge.knowledge_parser.measurement.measurement_patterns import (
    MeasurementPatterns,
)

from app.intelligence.utilities.knowledge.knowledge_parser.measurement.unit_normalizer import (
    UnitNormalizer,
)


class DeltaDetector:

    def __init__(self):

        self.normalizer = UnitNormalizer()

    # ---------------------------------------------------------

    def detect(

        self,

        text,

        direction=None,

    ):

        match = MeasurementPatterns.DELTA_PATTERN.search(text)

        if not match:
            return None

        value = self.normalizer.normalize_value(

            match.group("value")

        )

        unit = self.normalizer.normalize_unit(

            match.group("unit")

        )

        if direction:

            direction = direction.lower()

            if direction in [

                "decrease",

                "reduction",

                "reduce",

                "lower",

                "negative",

            ]:

                value = -value

        return {

            "measurement_type": "delta",

            "from_value": None,

            "to_value": None,

            "change_value": value,

            "percent_change": value if unit == "%" else None,

            "numeric_value": abs(value),

            "unit": unit,

        }