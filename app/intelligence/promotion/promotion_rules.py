"""
Promotion Rules
"""

import json
from pathlib import Path


class PromotionRules:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent
            / "pm_knowledge"
            / "data"
            / "promotion_rules.json"
        )

        with open(path, encoding="utf8") as f:

            self.rules = json.load(f)

    # ----------------------------

    def jump_bonus(self):

        return self.rules["promotion_jump_bonus"]

    def manager_bonus(self):

        return self.rules["manager_bonus"]

    def director_bonus(self):

        return self.rules["director_bonus"]

    def executive_bonus(self):

        return self.rules["executive_bonus"]

    def fast_track_years(self):

        return self.rules["fast_track_years"]