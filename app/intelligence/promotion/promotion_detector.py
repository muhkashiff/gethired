"""
Promotion Detector

Extracts promotion history
from Experience objects.
"""

import json
from pathlib import Path


class PromotionDetector:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent
            / "pm_knowledge"
            / "data"
            / "title_hierarchy.json"
        )

        with open(path, encoding="utf8") as f:
            self.levels = json.load(f)

        # DEBUG
        print("Hierarchy Loaded")
        print(self.levels)

    # ---------------------------------------

    def detect(self, experiences):

        titles = []

        level_history = []

        for exp in experiences:

            titles.append(exp.title)

            level = self.levels.get(
                exp.seniority,
                1
            )

            level_history.append(level)

        return {

            "titles": titles,

            "levels": level_history

        }