"""
Measurement Patterns

Central regex repository for measurement parsing.

Every detector imports patterns from here.

This keeps regexes in one place and makes future
maintenance much easier.
"""

import re


class MeasurementPatterns:
    """
    Shared measurement regex patterns.
    """

    # --------------------------------------------------
    # Numeric values
    # --------------------------------------------------

    NUMBER = r"\d+(?:\.\d+)?"

    MAGNITUDE = r"(?:K|M|B)?"

    UNIT = r"(?:%|\$|USD|EUR|PKR|hrs?|hours?|days?|kg|g|tons?|liters?|l)?"

    # --------------------------------------------------
    # FROM → TO
    # --------------------------------------------------

    RANGE_PATTERN = re.compile(

        rf"""
        from\s+
        (?P<from>{NUMBER})
        \s*
        (?P<from_unit>{UNIT})
        \s+
        to\s+
        (?P<to>{NUMBER})
        \s*
        (?P<to_unit>{UNIT})
        """,

        re.IGNORECASE | re.VERBOSE,

    )

    # --------------------------------------------------
    # BY
    # --------------------------------------------------

    DELTA_PATTERN = re.compile(

        rf"""
        by
        \s+
        (?P<value>{NUMBER})
        \s*
        (?P<unit>{UNIT})
        """,

        re.IGNORECASE | re.VERBOSE,

    )

    # --------------------------------------------------
    # Absolute values
    # --------------------------------------------------

    ABSOLUTE_PATTERN = re.compile(

        rf"""
        (?P<currency>\$|USD|EUR|PKR)?
        \s*
        (?P<value>{NUMBER})
        \s*
        (?P<magnitude>{MAGNITUDE})
        \s*
        (?P<unit>{UNIT})
        """,

        re.IGNORECASE | re.VERBOSE,

    )