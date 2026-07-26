"""
Promotion Profile Builder
"""

from .pm_models.promotion_profile import PromotionProfile


class PromotionProfileBuilder:

    def build(

        self,

        detector,

        scorer,

        experiences

    ):

        data = detector.detect(experiences)

        result = scorer.score(

            experiences,

            data["levels"]

        )

        profile = PromotionProfile()

        profile.title_history = data["titles"]

        profile.level_history = data["levels"]

        profile.promotion_count = result["promotion_count"]

        profile.promotion_velocity = result["promotion_velocity"]

        profile.promotion_quality = result["promotion_quality"]

        profile.promotion_jumps = result["promotion_jumps"]

        highest_level = max(data["levels"])

        profile.highest_level_score = highest_level

        for name, value in detector.levels.items():

                if value == highest_level:

                    profile.highest_level = name

                    break

        profile.confidence = 0.95

        return profile