"""
Experience Analyzer

Calculates experience directly from parsed resume.
"""

import re
from datetime import datetime


class ExperienceAnalyzer:

    def __init__(self):

        self.current_year = datetime.now().year

    # -------------------------------------------------
    # Calculate total years
    # -------------------------------------------------

    def total_years(self, experiences):

        periods = []

        for exp in experiences:

            start = exp.start_year
            end = exp.end_year

            if not start:
                continue

            if not end:
                end = self.current_year

            periods.append((start, end))

        if not periods:
            return 0

        # Merge overlapping ranges
        periods.sort()

        merged = []

        s, e = periods[0]

        for ns, ne in periods[1:]:

            if ns <= e:
                e = max(e, ne)

            else:
                merged.append((s, e))
                s, e = ns, ne

        merged.append((s, e))

        total = 0

        for s, e in merged:
            total += (e - s)

        return total

    # -------------------------------------------------
    # Category experience
    # -------------------------------------------------

    def category_years(self, experiences):

        manufacturing = 0
        retail = 0
        management = 0
        qa = 0

        for exp in experiences:

            years = exp.duration()

            text = (
                exp.job_title +
                " " +
                exp.company
            ).lower()

            if any(x in text for x in [
                "chemist",
                "quality",
                "production",
                "manufacturing",
                "factory"
            ]):
                manufacturing += years
                qa += years

            if any(x in text for x in [
                "retail",
                "store",
                "shell"
            ]):
                retail += years

            if any(x in text for x in [
                "manager",
                "director",
                "lead",
                "head"
            ]):
                management += years

        return {

            "manufacturing": manufacturing,

            "retail": retail,

            "management": management,

            "qa": qa

        }

    # -------------------------------------------------
    # Main
    # -------------------------------------------------

    def analyze(self, resume):

        total = self.total_years(resume.experience)

        categories = self.category_years(
            resume.experience
        )

        return {

            "total_years": total,

            **categories

        }