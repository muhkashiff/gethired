"""
GetHired

Production Responsibility Detector

Separates responsibilities from achievements.
"""

import re


class ResponsibilityDetector:

    def __init__(self):

        self.achievement_headers = {

            "key accomplishments",

            "achievements",

            "major achievements",

            "key achievements",

            "highlights",

            "selected achievements",

            "accomplishments"

        }

    # =====================================================
    # Parse Job Content
    # =====================================================

    def parse(self, job_lines):

        responsibilities = []

        achievements = []

        mode = "responsibility"

        # Skip first two header lines
        body = job_lines[2:]

        for line in body:

            text = line.strip()

            if not text:
                continue

            lower = text.lower()

            # -----------------------------
            # Achievement Heading
            # -----------------------------

            if lower in self.achievement_headers:

                mode = "achievement"

                continue

            # -----------------------------
            # Classification
            # -----------------------------

            if mode == "responsibility":

                responsibilities.append(text)

            else:

                achievements.append(text)

        return {

            "responsibilities": responsibilities,

            "achievements": achievements

        }