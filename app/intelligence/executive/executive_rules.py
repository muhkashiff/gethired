"""
Executive Rules Loader
"""

import json
from pathlib import Path


class ExecutiveRules:

    def __init__(self):

        path = (

            Path(__file__).resolve().parent

            / "ep_knowledge"

            / "data"

            / "executive_rules.json"

        )

        with open(path, encoding="utf8") as f:

            self.rules = json.load(f)

    @property
    def executive_ready(self):

        return self.rules["executive_ready"]

    @property
    def director_ready(self):

        return self.rules["director_ready"]

    @property
    def senior_manager_ready(self):

        return self.rules["senior_manager_ready"]

    @property
    def manager_ready(self):

        return self.rules["manager_ready"]

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
    def business_weight(self):

        return self.rules["business_weight"]

    @property
    def max_score(self):

        return self.rules["max_score"]