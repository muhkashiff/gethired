"""
GetHired

Leadership Weight Engine

Calculates weighted leadership impact.
"""

import re


class LeadershipWeightEngine:

    def __init__(self):

        self.metric_pattern = re.compile(

            r"(\d+(\.\d+)?)\s*%|\$[\d,]+|\d+\+?"

        )

        self.achievement_words = {

            "achieved",
            "improved",
            "reduced",
            "saved",
            "increased",
            "optimized",
            "implemented",
            "developed",
            "established",
            "delivered",
            "created",
            "launched",
            "transformed",
            "enhanced"

        }

    # =====================================================
    # MAIN
    # =====================================================

    def calculate(

        self,

        pattern,

        seniority_level=1,

        years_experience=0

    ):

        score = pattern.weight

        sentence = pattern.text.lower()

        # -----------------------------------------
        # Achievement bonus
        # -----------------------------------------

        for word in self.achievement_words:

            if word in sentence:

                score += 8

                pattern.achievement = True

                pattern.action = word

                break

        # -----------------------------------------
        # Quantified achievement
        # -----------------------------------------

        metrics = self.metric_pattern.findall(sentence)

        if metrics:

            score += 10

            pattern.quantified = True

            pattern.metric = metrics[0][0]

        # -----------------------------------------
        # Seniority
        # -----------------------------------------

        score += seniority_level * 2

        # -----------------------------------------
        # Years experience
        # -----------------------------------------

        score += min(

            years_experience,

            20

        ) * 0.5

        pattern.weight = round(score, 2)

        return pattern