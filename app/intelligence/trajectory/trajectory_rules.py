"""
Career Trajectory Rules
"""

import json
from pathlib import Path


class TrajectoryRules:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent
            / "tr_knowledge"
            / "data"
            / "trajectory_rules.json"
        )

        with open(path, encoding="utf8") as f:

            self.rules = json.load(f)

    @property
    def rapid_growth(self):
        return self.rules["rapid_growth"]

    @property
    def steady_growth(self):
        return self.rules["steady_growth"]

    @property
    def plateau_years(self):
        return self.rules["plateau_years"]

    @property
    def executive_level(self):
        return self.rules["executive_level"]

    @property
    def director_level(self):
        return self.rules["director_level"]

    @property
    def manager_level(self):
        return self.rules["manager_level"]

    @property
    def professional_level(self):
        return self.rules["professional_level"]

    @property
    def max_score(self):
        return self.rules["max_score"]