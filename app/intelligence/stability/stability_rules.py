"""
Career Stability Rules
"""

import json
from pathlib import Path


class StabilityRules:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent
            / "st_knowledge"
            / "data"
            / "stability_rules.json"
        )

        with open(path, encoding="utf8") as f:

            self.rules = json.load(f)

    # -----------------------------------------

    @property
    def excellent_average(self):

        return self.rules["excellent_average_tenure"]

    @property
    def good_average(self):

        return self.rules["good_average_tenure"]

    @property
    def acceptable_average(self):

        return self.rules["acceptable_average_tenure"]

    @property
    def hopper_limit(self):

        return self.rules["job_hopper_limit"]

    @property
    def excellent_score(self):

        return self.rules["excellent_score"]

    @property
    def good_score(self):

        return self.rules["good_score"]

    @property
    def average_score(self):

        return self.rules["average_score"]

    @property
    def max_score(self):

        return self.rules["max_score"]