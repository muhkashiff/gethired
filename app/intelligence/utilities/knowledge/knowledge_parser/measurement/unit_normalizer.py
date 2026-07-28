"""
Unit Normalizer

Converts text measurements into normalized
numeric values.

Examples

2.4M  -> 2400000

350K  -> 350000

99%   -> 99

12 hrs -> 12
"""


class UnitNormalizer:

    MULTIPLIERS = {

        "": 1,

        "K": 1_000,

        "M": 1_000_000,

        "B": 1_000_000_000,

    }

    # --------------------------------------------------

    def normalize_value(

        self,

        value,

        magnitude="",

    ):

        if value is None:

            return None

        value = float(value)

        multiplier = self.MULTIPLIERS.get(

            magnitude.upper(),

            1,

        )

        return value * multiplier

    # --------------------------------------------------

    def normalize_unit(

        self,

        unit,

    ):

        if unit is None:

            return ""

        unit = unit.strip().lower()

        mapping = {

            "%": "%",

            "percent": "%",

            "percentage": "%",

            "$": "$",

            "usd": "$",

            "eur": "EUR",

            "pkr": "PKR",

            "hr": "hours",

            "hrs": "hours",

            "hour": "hours",

            "hours": "hours",

            "day": "days",

            "days": "days",

            "kg": "kg",

            "g": "g",

            "ton": "tons",

            "tons": "tons",

            "liter": "liters",

            "liters": "liters",

            "l": "liters",

        }

        return mapping.get(

            unit,

            unit,

        )

    # --------------------------------------------------

    def percent_change(

        self,

        from_value,

        to_value,

    ):

        if from_value in (None, 0):

            return None

        return round(

            ((to_value - from_value) / from_value) * 100,

            2,

        )