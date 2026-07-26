"""
Career Stability Scorer
"""


class StabilityScorer:

    def __init__(self, rules):

        self.rules = rules

    # -----------------------------------------------------

    def score(self, detector_output):

        durations = detector_output["durations"]

        average = sum(durations) / len(durations)

        longest = max(durations)

        shortest = min(durations)

        score = 0

        average_score = 0
        bonus = 0
        penalty = 0

        # -------------------------------------------------
        # Average Tenure Score
        # -------------------------------------------------

        if average >= self.rules.excellent_average:

            average_score = 40
            score += average_score

            loyalty = "Excellent"
            consistency = "High"
            risk = "Low"

        elif average >= self.rules.good_average:

            average_score = 30
            score += average_score

            loyalty = "Good"
            consistency = "Good"
            risk = "Low"

        elif average >= self.rules.acceptable_average:

            average_score = 20
            score += average_score

            loyalty = "Average"
            consistency = "Moderate"
            risk = "Medium"

        else:

            average_score = 10
            score += average_score

            loyalty = "Poor"
            consistency = "Low"
            risk = "High"

        # -------------------------------------------------
        # Job Hopper Penalty
        # -------------------------------------------------

        hopper = shortest < self.rules.hopper_limit

        if hopper:

            penalty = 15
            score -= penalty

        # -------------------------------------------------
        # Long Tenure Bonus
        # -------------------------------------------------

        if longest >= 7:

            bonus = 15
            score += bonus

        elif longest >= 5:

            bonus = 10
            score += bonus

        # -------------------------------------------------
        # Clamp Score
        # -------------------------------------------------

        score = max(0, min(score, self.rules.max_score))

        # -------------------------------------------------
        # Stability Rating
        # -------------------------------------------------

        if score >= 90:

            rating = "Outstanding"

        elif score >= 75:

            rating = "Excellent"

        elif score >= 60:

            rating = "Good"

        elif score >= 40:

            rating = "Moderate"

        else:

            rating = "Weak"

        # -------------------------------------------------
        # Explainability Breakdown
        # -------------------------------------------------

        score_breakdown = {

            "average_tenure_score": average_score,

            "longest_tenure_bonus": bonus,

            "job_hopper_penalty": penalty,

            "final_score": score

        }

        # -------------------------------------------------
        # Return
        # -------------------------------------------------

        return {

            "average_tenure": round(average, 2),

            "longest_tenure": longest,

            "shortest_tenure": shortest,

            "stability_score": score,

            "stability_rating": rating,

            "employment_risk": risk,

            "job_hopper": hopper,

            "loyalty_rating": loyalty,

            "career_consistency": consistency,

            "score_breakdown": score_breakdown

        }