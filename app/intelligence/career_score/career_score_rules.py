"""
Career Score Rules
"""

import json
from pathlib import Path


class CareerScoreRules:

    def __init__(self):

        path = (

            Path(__file__).resolve().parent

            / "cs_knowledge"

            / "data"

            / "career_score_rules.json"

        )

        with open(path, encoding="utf8") as f:

            self.rules = json.load(f)

    @property
    def excellent(self):

        return self.rules["excellent"]

    @property
    def very_good(self):

        return self.rules["very_good"]

    @property
    def good(self):

        return self.rules["good"]

    @property
    def average(self):

        return self.rules["average"]

    @property
    def leadership_weight(self):

        return self.rules["leadership_weight"]

    @property
    def promotion_weight(self):

        return self.rules["promotion_weight"]

    @property
    def stability_weight(self):

        return self.rules["stability_weight"]

    @property
    def trajectory_weight(self):

        return self.rules["trajectory_weight"]

    @property
    def executive_weight(self):

        return self.rules["executive_weight"]

    @property
    def max_score(self):

        return self.rules["max_score"]