"""
GetHired

Production Header Parser
"""

import re


class HeaderParser:

    def __init__(self):
        pass

    # =====================================================
    # Parse Header
    # =====================================================

    def parse(self, job_lines):

        result = {

            "title": "",

            "company": "",

            "location": "",

            "start_year": 0,

            "end_year": 0,

            "current_job": False,

            "confidence": 1.0

        }

        if not job_lines:
            return result

        # ----------------------------------------
        # First line
        # ----------------------------------------

        first = job_lines[0].strip()

        result["raw_header"] = first

        # ----------------------------------------
        # Split title/company
        # ----------------------------------------

        if "|" in first:

            parts = first.split("|", 1)

            left = parts[0].strip()

            right = parts[1].strip()

            # ------------------------------------
            # Right side contains year
            # ------------------------------------

            if re.search(r"(19|20)\d{2}", right):

                title_company = right

                year_match = re.search(

                    r"((19|20)\d{2})\s*[-–]\s*((19|20)\d{2}|Present|Current)",

                    right,

                    re.I

                )

                if year_match:

                    result["start_year"] = int(
                        year_match.group(1)
                    )

                    if year_match.group(3).lower() in [

                        "present",

                        "current"

                    ]:

                        result["current_job"] = True

                    else:

                        result["end_year"] = int(
                            year_match.group(3)
                        )

                before_year = right.split(
                    str(result["start_year"])
                )[0]

                result["title"] = left

                result["company"] = before_year.strip()

            else:

                result["title"] = left

                result["company"] = right

        else:

            result["title"] = first

        # ----------------------------------------
        # Second line
        # ----------------------------------------

        if len(job_lines) > 1:

            second = job_lines[1]

            # Date line

            if re.search(r"(19|20)\d{2}", second):

                year_match = re.search(

                    r"((19|20)\d{2})\s*[-–]\s*((19|20)\d{2}|Present|Current)",

                    second,

                    re.I

                )

                if year_match:

                    result["start_year"] = int(
                        year_match.group(1)
                    )

                    if year_match.group(3).lower() in [

                        "present",

                        "current"

                    ]:

                        result["current_job"] = True

                    else:

                        result["end_year"] = int(
                            year_match.group(3)
                        )

                if "|" in second:

                    result["location"] = second.split("|")[-1].strip()

        return result