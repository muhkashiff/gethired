"""
Achievement Profile Builder

Builds the complete AchievementProfile object from
Achievement Engine output.

Produces

• Overall score
• Impact score
• Magnitude score
• Top achievements
• KPI distributions
• Detailed achievement cards
"""

from collections import Counter

from app.intelligence.utilities.knowledge.knowledge_scoring.achievement.achievement_engine import (
    AchievementEngine,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import (
    AchievementProfile,
)


class AchievementProfileBuilder:

    def __init__(self):

        self.engine = AchievementEngine()

    # -----------------------------------------------------

    def build(self, graph):

        engine_result = self.engine.score(graph)

        achievements = engine_result["achievements"]

        profile = AchievementProfile()

        # -------------------------------------------------
        # Overall Scores
        # -------------------------------------------------

        profile.overall_score = engine_result.get(
            "achievement_score",
            0,
        )

        profile.achievement_count = engine_result.get(
            "achievement_count",
            0,
        )

        profile.impact_score = engine_result.get(
            "impact_score",
            0,
        )

        profile.magnitude_score = engine_result.get(
            "magnitude_score",
            0,
        )

        # -------------------------------------------------
        # Executive Views
        # -------------------------------------------------

        profile.top_metrics = self._top_metrics(
            achievements
        )

        profile.top_achievements = achievements

        # -------------------------------------------------
        # Distributions
        # -------------------------------------------------

        profile.impact_distribution = (
            self._impact_distribution(
                achievements
            )
        )

        profile.magnitude_distribution = (
            self._magnitude_distribution(
                achievements
            )
        )

        # -------------------------------------------------
        # Raw Engine Output
        # -------------------------------------------------

        profile.details = engine_result

        return profile

    # -----------------------------------------------------

    def _top_metrics(self, achievements):

        metrics = []

        for item in achievements:

            metrics.append(

                {

                    "metric": item.get("metric"),

                    "overall_score": item.get(
                        "overall_score",
                        0,
                    ),

                    "impact_score": item.get(
                        "impact_score",
                        0,
                    ),

                    "magnitude_score": item.get(
                        "magnitude_score",
                        0,
                    ),

                    "business_value": item.get(
                        "business_value",
                        "",
                    ),

                }

            )

        metrics.sort(

            key=lambda x: x["overall_score"],

            reverse=True,

        )

        return metrics

    # -----------------------------------------------------

    def _top_achievements(self, impact, magnitude):

        mag_lookup = {}

        for m in magnitude.measurements:

            metric = getattr(m, "metric", None)

            if metric:

                mag_lookup[metric] = m

        cards = []

        for item in impact.measurements:

            metric = getattr(item, "metric", None)

            mag = mag_lookup.get(metric)

            cards.append(

                {

                    "metric": metric,

                    "action": getattr(item, "action", ""),

                    "measurement": getattr(
                        item,
                        "measurement",
                        "",
                    ),

                    "measurement_type": getattr(
                        item,
                        "measurement_type",
                        "",
                    ),

                    "start_value": getattr(
                        item,
                        "start_value",
                        None,
                    ),

                    "end_value": getattr(
                        item,
                        "end_value",
                        None,
                    ),

                    "change_value": getattr(
                        item,
                        "change_value",
                        None,
                    ),

                    "percent_change": getattr(
                        item,
                        "percent_change",
                        None,
                    ),

                    "unit": getattr(
                        item,
                        "unit",
                        "",
                    ),

                    "direction": getattr(
                        item,
                        "direction",
                        "",
                    ),

                    "effect": getattr(
                        item,
                        "effect",
                        "",
                    ),

                    "business_meaning": getattr(
                        item,
                        "business_meaning",
                        "",
                    ),

                    "business_value": getattr(
                        item,
                        "business_value",
                        "",
                    ),

                    "business_area": getattr(
                        item,
                        "business_area",
                        "",
                    ),

                    "impact_score": getattr(
                        item,
                        "score",
                        0,
                    ),

                    "magnitude_score": getattr(
                        mag,
                        "score",
                        0,
                    )
                    if mag
                    else 0,

                    "classification": getattr(
                        mag,
                        "classification",
                        "Unknown",
                    )
                    if mag
                    else "Unknown",

                }

            )

        cards.sort(

            key=lambda x: (

                x["impact_score"],

                x["magnitude_score"],

            ),

            reverse=True,

        )

        return cards

    # -----------------------------------------------------

    def _impact_distribution(self, achievements):

        counter = Counter()

        for item in achievements:

            metric = item.get("metric")

            if metric:

                counter[metric] += 1

        return dict(counter)

    # -----------------------------------------------------

    def _magnitude_distribution(self, achievements):

        counter = Counter()

        for item in achievements:

            classification = item.get(
                "classification"
            )

            if classification:

                counter[classification] += 1

        return dict(counter)