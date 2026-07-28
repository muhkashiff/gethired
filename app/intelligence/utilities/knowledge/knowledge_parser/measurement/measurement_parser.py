"""
Measurement Parser

Master orchestrator for measurement extraction.

Priority

1. Range
2. Delta
3. Absolute

Returns one normalized measurement object.
"""

import re

from app.intelligence.utilities.knowledge.knowledge_parser.measurement.range_detector import (
    RangeDetector,
)

from app.intelligence.utilities.knowledge.knowledge_parser.measurement.delta_detector import (
    DeltaDetector,
)

from app.intelligence.utilities.knowledge.knowledge_parser.measurement.absolute_detector import (
    AbsoluteDetector,
)


class MeasurementParser:

    def __init__(self):

        self.range_detector = RangeDetector()

        self.delta_detector = DeltaDetector()

        self.absolute_detector = AbsoluteDetector()

    # ---------------------------------------------------------

    def _extract_raw_value(self, text):

        """
        Preserve the original measurement exactly as it
        appeared in the resume.

        Examples

            99%
            $2.4M
            15 hrs
            350K
        """

        pattern = re.compile(

            r"(\$?\d+(?:\.\d+)?(?:K|M|B)?\s*(?:%|USD|EUR|PKR|hrs?|hours?|days?|kg|g|tons?|liters?|l)?)",

            re.IGNORECASE,

        )

        matches = pattern.findall(text)

        if matches:

            return matches[-1].strip()

        return ""

    # ---------------------------------------------------------

    def _finalize(self, result, text):

        """
        Add fields common to every detector.
        """

        if result is None:
            return None

        result["raw_value"] = self._extract_raw_value(text)

        return result

    # ---------------------------------------------------------

    def parse(

        self,

        text,

        direction=None,

    ):

        # -----------------------------------------
        # Range
        # -----------------------------------------

        result = self.range_detector.detect(text)

        if result:

            return self._finalize(result, text)

        # -----------------------------------------
        # Delta
        # -----------------------------------------

        result = self.delta_detector.detect(

            text,

            direction,

        )

        if result:

            return self._finalize(result, text)

        # -----------------------------------------
        # Absolute
        # -----------------------------------------

        result = self.absolute_detector.detect(text)

        if result:

            return self._finalize(result, text)

        return None