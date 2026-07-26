"""
Executive Profile Builder
"""

from .ep_models.executive_profile import ExecutiveProfile


class ExecutiveProfileBuilder:

    def build(

        self,

        detector,

        scorer,

        leadership,

        promotion,

        stability,

        trajectory

    ):

        detector_output = detector.detect(

            leadership,

            promotion,

            stability,

            trajectory

        )

        result = scorer.score(

            detector_output

        )

        profile = ExecutiveProfile()

        profile.executive_score = result["executive_score"]

        profile.executive_rating = result["executive_rating"]

        profile.executive_readiness = result["executive_readiness"]

        profile.leadership_maturity = result["leadership_maturity"]

        profile.people_leadership = result["people_leadership"]

        profile.strategic_leadership = result["strategic_leadership"]

        profile.operational_leadership = result["operational_leadership"]

        profile.promotion_maturity = result["promotion_maturity"]

        profile.career_maturity = result["career_maturity"]

        profile.stability_maturity = result["stability_maturity"]

        profile.trajectory_maturity = result["trajectory_maturity"]

        profile.business_acumen = result["business_acumen"]

        profile.commercial_exposure = result["commercial_exposure"]

        profile.change_leadership = result["change_leadership"]

        profile.executive_presence = result["executive_presence"]

        profile.next_role = result["next_role"]

        profile.future_roles = result["future_roles"]

        profile.strengths = result["strengths"]

        profile.development_areas = result["development_areas"]

        profile.score_breakdown = result["score_breakdown"]

        profile.evidence = detector_output["evidence"]

        profile.confidence = 0.95

        return profile