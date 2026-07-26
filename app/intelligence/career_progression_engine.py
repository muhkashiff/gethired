"""
Career Progression Engine

Evaluates career growth,
promotion history,
executive progression.
"""

import json
from pathlib import Path

from app.intelligence.eng_models.career_progression import CareerProgression


class CareerProgressionEngine:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent
            / "eng_knowledge"
            / "data"
            / "career_levels.json"
        )

        with open(path, encoding="utf8") as f:

            self.levels = json.load(f)

    # ---------------------------------------------------

    def evaluate(self, experiences):

        profile = CareerProgression()

        if not experiences:

            return profile

        titles = []

        levels = []

        total_years = 0

        for exp in experiences:

            titles.append(exp.title)

            total_years += exp.duration

            level = self.levels.get(exp.seniority, 1)

            levels.append(level)

        profile.title_history = titles

        profile.years_experience = round(total_years, 1)

        profile.highest_level = max(

            [e.seniority for e in experiences],

            key=lambda x: self.levels.get(x, 0)

        )

        # ------------------------------

        promotions = 0

        for i in range(1, len(levels)):

            if levels[i] > levels[i - 1]:

                promotions += 1

        profile.promotion_count = promotions

        # ------------------------------

        if promotions:

            profile.promotion_velocity = round(

                total_years / promotions,

                2

            )

        else:

            profile.promotion_velocity = total_years

        # ------------------------------

        max_level = max(levels)

        growth = (

            max_level / 10

        ) * 100

        profile.career_growth_score = round(growth, 1)

        # ------------------------------

        if promotions >= 3:

            profile.trend = "Rapid Growth"

        elif promotions == 2:

            profile.trend = "Strong Growth"

        elif promotions == 1:

            profile.trend = "Steady Growth"

        else:

            profile.trend = "Stable"

        # ------------------------------

        profile.confidence = 0.95

        return profile