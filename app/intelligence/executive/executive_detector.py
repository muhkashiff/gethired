"""
Executive Detector

Collects intelligence from all
Career Intelligence Engines.
"""


class ExecutiveDetector:

    def detect(

        self,

        leadership,

        promotion,

        stability,

        trajectory

    ):

        return {

            # ------------------------
            # Leadership
            # ------------------------

            "leadership_score":

                leadership.overall_score,

            "leadership_strengths":

                leadership.strongest_dimensions,

            "leadership_summary":

                leadership.summary,

            # ------------------------
            # Promotion
            # ------------------------

            "promotion_score":

                promotion.promotion_quality,

            "promotion_count":

                promotion.promotion_count,

            "highest_level":

                promotion.highest_level,

            # ------------------------
            # Stability
            # ------------------------

            "stability_score":

                stability.stability_score,

            "stability_rating":

                stability.stability_rating,

            # ------------------------
            # Trajectory
            # ------------------------

            "trajectory_score":

                trajectory.trajectory_score,

            "career_stage":

                trajectory.career_stage,

            "career_trend":

                trajectory.career_trend,

            "executive_path":

                trajectory.executive_path,

            # ------------------------
            # Evidence
            # ------------------------

            "evidence":

                (

                    leadership.evidence

                    +

                    stability.evidence

                    +

                    trajectory.evidence

                )

        }