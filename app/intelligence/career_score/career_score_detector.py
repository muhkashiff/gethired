"""
Career Score Detector

Aggregates all Career Intelligence Engines.
"""


class CareerScoreDetector:

    def detect(

        self,

        leadership,

        promotion,

        stability,

        trajectory,

        executive

    ):

        return {

            # ---------------------------------
            # Leadership
            # ---------------------------------

            "leadership_score":

                leadership.overall_score,

            "leadership_strengths":

                leadership.strongest_dimensions,

            # ---------------------------------
            # Promotion
            # ---------------------------------

            "promotion_score":

                promotion.promotion_quality,

            "promotion_count":

                promotion.promotion_count,

            "highest_level":

                promotion.highest_level,

            # ---------------------------------
            # Stability
            # ---------------------------------

            "stability_score":

                stability.stability_score,

            "stability_rating":

                stability.stability_rating,

            # ---------------------------------
            # Trajectory
            # ---------------------------------

            "trajectory_score":

                trajectory.trajectory_score,

            "career_stage":

                trajectory.career_stage,

            "career_trend":

                trajectory.career_trend,

            # ---------------------------------
            # Executive
            # ---------------------------------

            "executive_score":

                executive.executive_score,

            "executive_rating":

                executive.executive_rating,

            "executive_readiness":

                executive.executive_readiness,

            # ---------------------------------
            # Evidence
            # ---------------------------------

            "evidence":

                (

                    leadership.evidence

                    +

                    stability.evidence

                    +

                    trajectory.evidence

                    +

                    executive.evidence

                )

        }