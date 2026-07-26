"""
Career Stability Profile Builder
"""

from .st_models.stability_profile import StabilityProfile


class StabilityProfileBuilder:

    def build(

        self,

        detector,

        scorer,

        experiences

    ):

        data = detector.detect(experiences)

        result = scorer.score(data)

        profile = StabilityProfile()

        profile.average_tenure = result["average_tenure"]

        profile.longest_tenure = result["longest_tenure"]

        profile.shortest_tenure = result["shortest_tenure"]

        profile.total_companies = data["companies"]

        profile.total_experience = data["total_years"]

        profile.stability_score = result["stability_score"]

        profile.stability_rating = result["stability_rating"]

        profile.employment_risk = result["employment_risk"]

        profile.job_hopper = result["job_hopper"]

        profile.loyalty_rating = result["loyalty_rating"]

        profile.career_consistency = result["career_consistency"]

        profile.evidence = data["evidence"]

        profile.score_breakdown = result["score_breakdown"]

        profile.confidence = 0.95

        return profile