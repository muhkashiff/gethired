"""
Career Trajectory Profile Builder
"""

from .tr_models.trajectory_profile import TrajectoryProfile


class TrajectoryProfileBuilder:

    def build(

        self,

        detector,

        scorer,

        experiences

    ):

        # -----------------------------
        # Detect
        # -----------------------------

        detector_output = detector.detect(experiences)

        # -----------------------------
        # Score
        # -----------------------------

        result = scorer.score(detector_output)

        # -----------------------------
        # Build Profile
        # -----------------------------

        profile = TrajectoryProfile()

        profile.career_stage = result["career_stage"]

        profile.career_trend = result["career_trend"]

        profile.trajectory_score = result["trajectory_score"]

        profile.momentum_score = result["momentum_score"]

        profile.executive_path = result["executive_path"]

        profile.plateau_detected = result["plateau_detected"]

        profile.regression_detected = result["regression_detected"]

        profile.industry_transition = result["industry_transition"]

        # Temporary values (will become intelligent in V2)

        profile.management_growth = result["career_trend"]

        profile.technical_growth = result["career_trend"]

        profile.leadership_growth = result["career_trend"]

        if profile.executive_path:

            profile.future_projection = "Executive Leadership"

        elif profile.career_stage == "Director":

            profile.future_projection = "Executive Candidate"

        elif profile.career_stage == "Management":

            profile.future_projection = "Senior Management"

        else:

            profile.future_projection = "Professional Growth"

        profile.score_breakdown = result["score_breakdown"]

        profile.evidence = detector_output["evidence"]

        profile.confidence = 0.95

        return profile