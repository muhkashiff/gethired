"""
Career Trajectory Scorer
"""


class TrajectoryScorer:

    def __init__(self, rules):

        self.rules = rules

    # --------------------------------------------------

    def score(self, detector_output):

        levels = detector_output["levels"]

        industries = detector_output["industries"]

        score = 0

        momentum = 0

        growth_points = 0

        executive_path = False

        plateau = False

        regression = False

        # ---------------------------------------
        # Promotion Momentum
        # ---------------------------------------

        jumps = []

        for i in range(1, len(levels)):

            jump = levels[i] - levels[i - 1]

            jumps.append(jump)

        positive_jumps = [j for j in jumps if j > 0]

        negative_jumps = [j for j in jumps if j < 0]

        if positive_jumps:

            growth_points = sum(positive_jumps)

            momentum = growth_points * 10

            score += momentum

        if negative_jumps:

            regression = True

            score -= abs(sum(negative_jumps)) * 10

        # ---------------------------------------
        # Executive Path
        # ---------------------------------------

        if max(levels) >= self.rules.executive_level:

            executive_path = True

            score += 20

        elif max(levels) >= self.rules.director_level:

            score += 15

        elif max(levels) >= self.rules.manager_level:

            score += 10

        # ---------------------------------------
        # Industry Progression
        # ---------------------------------------

        unique_industries = len(set(industries))

        if unique_industries == 1:

            industry_growth = "Deep Specialist"

            score += 10

        elif unique_industries == 2:

            industry_growth = "Cross Industry"

            score += 8

        else:

            industry_growth = "Diverse"

            score += 5

        # ---------------------------------------
        # Career Trend
        # ---------------------------------------

        if growth_points >= self.rules.rapid_growth:

            trend = "Rapid Growth"

        elif growth_points >= self.rules.steady_growth:

            trend = "Steady Growth"

        else:

            trend = "Slow Growth"

        # ---------------------------------------
        # Career Stage
        # ---------------------------------------

        highest = max(levels)

        if highest >= 10:

            stage = "Executive"

        elif highest >= 9:

            stage = "Director"

        elif highest >= 7:

            stage = "Management"

        else:

            stage = "Professional"

        score = max(0, min(score, self.rules.max_score))

        breakdown = {

            "promotion_momentum": momentum,

            "executive_bonus": 20 if executive_path else 0,

            "industry_bonus": 10 if unique_industries == 1 else 8 if unique_industries == 2 else 5,

            "final_score": score

        }

        return {

            "career_stage": stage,

            "career_trend": trend,

            "trajectory_score": score,

            "momentum_score": momentum,

            "executive_path": executive_path,

            "plateau_detected": plateau,

            "regression_detected": regression,

            "industry_transition": industry_growth,

            "score_breakdown": breakdown

        }