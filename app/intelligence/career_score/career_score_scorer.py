"""
Career Score Scorer
"""


class CareerScoreScorer:

    def __init__(self, rules):

        self.rules = rules

    # -------------------------------------------------------------

    def score(self, detector_output):

        # ==========================================================
        # Raw Engine Scores
        # ==========================================================

        leadership = detector_output["leadership_score"]

        promotion = detector_output["promotion_score"]

        stability = detector_output["stability_score"]

        trajectory = detector_output["trajectory_score"]

        executive = detector_output["executive_score"]

        # ==========================================================
        # MASTER INDEX 1
        # Leadership Index
        # ==========================================================

        leadership_index = (

            leadership * 0.70

            +

            executive * 0.30

        )

        # ==========================================================
        # MASTER INDEX 2
        # Career Health Index
        # ==========================================================

        career_health = (

            promotion * 0.35

            +

            stability * 0.30

            +

            trajectory * 0.35

        )

        # ==========================================================
        # MASTER INDEX 3
        # Market Readiness Index
        # ==========================================================

        market_readiness = (

            executive * 0.40

            +

            leadership * 0.30

            +

            trajectory * 0.30

        )

        # ==========================================================
        # Overall Career Score
        # ==========================================================

        overall = (

            leadership_index * 0.35

            +

            career_health * 0.35

            +

            market_readiness * 0.30

        )

        overall = round(overall, 1)

        # ==========================================================
        # Recruiter Readiness
        # ==========================================================

        if overall >= 90:

            recruiter = "Excellent"

        elif overall >= 80:

            recruiter = "Very Strong"

        elif overall >= 70:

            recruiter = "Strong"

        elif overall >= 60:

            recruiter = "Competitive"

        else:

            recruiter = "Needs Improvement"

        # ==========================================================
        # ATS Strength
        # ==========================================================

        if leadership >= 85 and trajectory >= 80:

            ats = "Excellent"

        elif leadership >= 75:

            ats = "Very Good"

        elif leadership >= 65:

            ats = "Good"

        else:

            ats = "Average"

        # ==========================================================
        # Career Grade
        # ==========================================================

        if overall >= 95:

            grade = "A+"

        elif overall >= 90:

            grade = "A"

        elif overall >= 85:

            grade = "A-"

        elif overall >= 80:

            grade = "B+"

        elif overall >= 75:

            grade = "B"

        elif overall >= 70:

            grade = "B-"

        elif overall >= 65:

            grade = "C+"

        else:

            grade = "C"

        # ==========================================================
        # Market Position
        # ==========================================================

        if overall >= 95:

            position = "Top 1%"

        elif overall >= 90:

            position = "Top 5%"

        elif overall >= 85:

            position = "Top 10%"

        elif overall >= 80:

            position = "Top 20%"

        elif overall >= 70:

            position = "Top 35%"

        else:

            position = "Average"

        # ==========================================================
        # Career Risk
        # ==========================================================

        # ==========================================================
        # Career Risk
        # ==========================================================

        if career_health >= 85:

            risk = "Low"

        elif career_health >= 70:

            risk = "Medium"

        else:

            risk = "High"

        # ==========================================================
        # Growth Index
        # ==========================================================

        growth = (

            promotion * 0.50

            +

            trajectory * 0.50

        )

        # ==========================================================
        # Strengths
        # ==========================================================

        strengths = []

        if leadership_index >= 85:

            strengths.append("Leadership")

        if career_health >= 80:

            strengths.append("Career Health")

        if market_readiness >= 85:

            strengths.append("Market Readiness")

        if executive >= 80:

            strengths.append("Executive Potential")

        # ==========================================================
        # Development Areas
        # ==========================================================

        development = []

        if promotion < 70:

            development.append("Promotion Readiness")

        if stability < 70:

            development.append("Career Stability")

        if executive < 80:

            development.append("Executive Presence")

        # ==========================================================
        # Return
        # ==========================================================

        return {

            "overall_score": overall,

            "leadership_index": round(leadership_index, 1),

            "career_health_index": round(career_health, 1),

            "market_readiness_index": round(market_readiness, 1),

            "growth_index": round(growth, 1),

            "promotion_index": promotion,

            "stability_index": stability,

            "trajectory_index": trajectory,

            "executive_index": executive,

            "overall_rating": recruiter,

            "career_grade": grade,

            "market_position": position,

            "career_risk": risk,

            "ats_strength": ats,

            "recruiter_readiness": recruiter,

            "strengths": strengths,

            "development_areas": development,

            "score_breakdown": {

                "leadership_index": round(leadership_index, 1),

                "career_health_index": round(career_health, 1),

                "market_readiness_index": round(market_readiness, 1),

                "overall_score": overall

            }

        }