"""
Promotion Scorer
"""


class PromotionScorer:

    def __init__(self, rules):

        self.rules = rules

    # -----------------------------------

    def score(self, experiences, levels):

        promotions = 0

        jumps = []

        score = 0

        total_years = 0

        for exp in experiences:

            total_years += exp.duration

        for i in range(1, len(levels)):

            jump = levels[i] - levels[i - 1]

            jumps.append(jump)

            if jump > 0:

                promotions += 1

                score += jump * self.rules.jump_bonus()

        highest = max(levels)

        if highest >= 10:

            score += self.rules.executive_bonus()

        elif highest >= 9:

            score += self.rules.director_bonus()

        elif highest >= 7:

            score += self.rules.manager_bonus()

        velocity = (

            total_years / promotions

            if promotions

            else total_years

        )

        return {

            "promotion_count": promotions,

            "promotion_jumps": jumps,

            "promotion_velocity": round(velocity, 2),

            "promotion_quality": round(score, 1)

        }