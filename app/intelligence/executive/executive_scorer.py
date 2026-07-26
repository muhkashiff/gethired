"""
Executive Potential Scorer
"""


class ExecutiveScorer:

    def __init__(self, rules):

        self.rules = rules

    # ---------------------------------------------------------

    def score(self, detector_output):

        # ---------------------------------------
        # Raw Scores
        # ---------------------------------------

        leadership = detector_output["leadership_score"]

        promotion = detector_output["promotion_score"]

        stability = detector_output["stability_score"]

        trajectory = detector_output["trajectory_score"]

        # ---------------------------------------
        # Leadership Maturity
        # ---------------------------------------

        leadership_maturity = leadership

        people_leadership = leadership

        strategic = leadership * 0.95

        operational = leadership * 0.90

        # ---------------------------------------
        # Career Maturity
        # ---------------------------------------

        promotion_maturity = promotion

        career_maturity = (

            promotion +

            trajectory

        ) / 2

        stability_maturity = stability

        trajectory_maturity = trajectory

        # ---------------------------------------
        # Business Acumen
        # ---------------------------------------

        business = (

            trajectory +

            leadership

        ) / 2

        commercial = (

            business * 0.90

        )

        change = (

            leadership * 0.90

        )

        executive_presence = (

            trajectory +

            promotion

        ) / 2

        # ---------------------------------------
        # Final Executive Score
        # ---------------------------------------

        final_score = (

            leadership * self.rules.leadership_weight +

            promotion * self.rules.promotion_weight +

            stability * self.rules.stability_weight +

            trajectory * self.rules.trajectory_weight +

            business * self.rules.business_weight

        )

        final_score = round(final_score, 2)

        # ---------------------------------------
        # Readiness
        # ---------------------------------------

        if final_score >= self.rules.executive_ready:

            readiness = "Executive Ready"

            rating = "Outstanding"

            next_role = "Vice President / COO"

        elif final_score >= self.rules.director_ready:

            readiness = "Director Ready"

            rating = "Excellent"

            next_role = "Director"

        elif final_score >= self.rules.senior_manager_ready:

            readiness = "Senior Manager Ready"

            rating = "Very Good"

            next_role = "Senior Manager"

        elif final_score >= self.rules.manager_ready:

            readiness = "Management Ready"

            rating = "Good"

            next_role = "Manager"

        else:

            readiness = "Developing"

            rating = "Developing"

            next_role = "Professional"

        # ---------------------------------------
        # Future Roles
        # ---------------------------------------

        future_roles = []

        if readiness == "Executive Ready":

            future_roles.extend([

                "Vice President",

                "Chief Operating Officer",

                "Chief Executive Officer"

            ])

        elif readiness == "Director Ready":

            future_roles.extend([

                "Plant Director",

                "Regional Director",

                "Operations Director"

            ])

        elif readiness == "Senior Manager Ready":

            future_roles.extend([

                "Senior Manager",

                "Plant Manager",

                "Operations Manager"

            ])

        else:

            future_roles.extend([

                "Team Lead",

                "Supervisor",

                "Manager"

            ])

        # ---------------------------------------
        # Strengths
        # ---------------------------------------

        strengths = []

        if leadership > 80:

            strengths.append("Leadership")

        if trajectory > 80:

            strengths.append("Career Growth")

        if stability > 70:

            strengths.append("Career Stability")

        # ---------------------------------------
        # Development
        # ---------------------------------------

        development = []

        if promotion < 70:

            development.append(

                "Accelerate promotion readiness"

            )

        if stability < 60:

            development.append(

                "Increase career stability"

            )

        if leadership < 75:

            development.append(

                "Strengthen strategic leadership"

            )

        # ---------------------------------------
        # Score Breakdown
        # ---------------------------------------

        breakdown = {

            "leadership":

                round(

                    leadership *

                    self.rules.leadership_weight,

                    2

                ),

            "promotion":

                round(

                    promotion *

                    self.rules.promotion_weight,

                    2

                ),

            "stability":

                round(

                    stability *

                    self.rules.stability_weight,

                    2

                ),

            "trajectory":

                round(

                    trajectory *

                    self.rules.trajectory_weight,

                    2

                ),

            "business":

                round(

                    business *

                    self.rules.business_weight,

                    2

                ),

            "final_score":

                final_score

        }

        return {

            "executive_score": final_score,

            "executive_rating": rating,

            "executive_readiness": readiness,

            "leadership_maturity": leadership_maturity,

            "people_leadership": people_leadership,

            "strategic_leadership": strategic,

            "operational_leadership": operational,

            "promotion_maturity": promotion_maturity,

            "career_maturity": career_maturity,

            "stability_maturity": stability_maturity,

            "trajectory_maturity": trajectory_maturity,

            "business_acumen": business,

            "commercial_exposure": commercial,

            "change_leadership": change,

            "executive_presence": executive_presence,

            "next_role": next_role,

            "future_roles": future_roles,

            "strengths": strengths,

            "development_areas": development,

            "score_breakdown": breakdown

        }