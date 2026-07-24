"""
GetHired
Experience Pattern Library

Centralized regular expressions for extracting
employment periods from resumes and job descriptions.
"""

import re


# ----------------------------------------------------
# Example:
# 2015 - 2020
# 2015–2020
# 2015 — Present
# ----------------------------------------------------

YEAR_RANGE = re.compile(
    r"(?P<start>\d{4})\s*[-–—]\s*(?P<end>\d{4}|Present|Current)",
    re.IGNORECASE,
)


# ----------------------------------------------------
# Example:
# Jan 2015 - Mar 2020
# April 2010 – Present
# ----------------------------------------------------

MONTH_YEAR_RANGE = re.compile(
    r"(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|Sept|September|Oct|October|Nov|November|Dec|December)"
    r"\s+"
    r"(?P<start>\d{4})"
    r"\s*[-–—]\s*"
    r"((Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|Sept|September|Oct|October|Nov|November|Dec|December)"
    r"\s+)?"
    r"(?P<end>\d{4}|Present|Current)",
    re.IGNORECASE,
)