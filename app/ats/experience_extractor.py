"""
GetHired

Experience Extractor

Extracts employment periods from resume text.
"""

from datetime import datetime

from .experience_patterns import (
    YEAR_RANGE,
    MONTH_YEAR_RANGE,
)


class ExperienceExtractor:

    def __init__(self):

        self.current_year = datetime.now().year

    def extract(self, lines):

        positions = []

        current_title = ""

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # -----------------------------
            # Detect Job Title
            # -----------------------------

            if "|" in line:

                current_title = line

            # -----------------------------
            # Year Range
            # -----------------------------

            for match in YEAR_RANGE.finditer(line):

                start = int(match.group("start"))

                end = match.group("end")

                if end.lower() in ("present", "current"):

                    end = self.current_year

                else:

                    end = int(end)

                positions.append(

                    {
                        "title": current_title,
                        "start": start,
                        "end": end,
                        "text": line,
                    }

                )

            # -----------------------------
            # Month-Year Range
            # -----------------------------

            for match in MONTH_YEAR_RANGE.finditer(line):

                start = int(match.group("start"))

                end = match.group("end")

                if end.lower() in ("present", "current"):

                    end = self.current_year

                else:

                    end = int(end)

                positions.append(

                    {
                        "title": current_title,
                        "start": start,
                        "end": end,
                        "text": line,
                    }

                )

        return positions