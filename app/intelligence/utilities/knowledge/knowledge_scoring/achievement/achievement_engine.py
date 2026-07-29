"""
Achievement Engine

Combines multiple scoring engines into a unified
achievement intelligence model.

Current Inputs

- Impact Engine
- Magnitude Engine

Future Inputs

- Business Value
- Innovation
- Complexity
- Executive Visibility
"""


from app.intelligence.utilities.knowledge.knowledge_scoring.impact.impact_engine import (
    ImpactEngine,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.magnitude.magnitude_engine import (
    MagnitudeEngine,
)


class AchievementEngine:

    def __init__(self):

        self.impact_engine = ImpactEngine()

        self.magnitude_engine = MagnitudeEngine()

    # -----------------------------------------------------

    def score(self, graph):

        impact = self.impact_engine.score(graph)

        magnitude = self.magnitude_engine.score(graph)

        achievements = []

        total_score = 0

        # -------------------------------------------------
        # Merge Impact + Magnitude
        # -------------------------------------------------

        for impact_item in impact["measurements"]:

            metric = impact_item["metric"]

            magnitude_item = next(

                (
                    item
                    for item in magnitude["measurements"]

                    if (
                        item.get("metric") == metric
                    )
                ),

                None,

            )

            if magnitude_item is None:

                magnitude_item = {

                    "metric": metric,

                    "measurement_type": "absolute",

                    "classification": "Unknown",

                    "score": 0,

                    "start_value": None,

                    "end_value": None,

                    "change_value": None,

                    "percent_change": None,

                    "direction": impact_item["direction"],

                }
            achievement_score = (

                impact_item["score"]

                + magnitude_item["score"]

            )

            total_score += achievement_score

            achievements.append(

                {

                    "metric": metric,

                    "action": impact_item["action"],

                    "measurement_type": magnitude_item["measurement_type"],

                    "from_value": magnitude_item["start"],

                    "to_value": magnitude_item["end"],

                    "change_value": magnitude_item["change"],

                    "percent_change": magnitude_item["percent_change"],

                    "direction": impact_item["direction"],

                    "classification": magnitude_item["classification"],

                    "impact_score": impact_item["score"],

                    "magnitude_score": magnitude_item["score"],

                    "overall_score": round(achievement_score, 2),

                    "business_value": self._business_value(

                        achievement_score

                    ),

                    "executive_ready": achievement_score >= 20,

                }

            )

        # -------------------------------------------------

        return {

            "achievement_score": round(total_score, 2),

            "achievement_count": len(achievements),

            "impact_score": impact["score"],

            "magnitude_score": magnitude["score"],

            "impact": impact,

            "magnitude": magnitude,

            "achievements": achievements,

        }

    # -----------------------------------------------------

    def _business_value(self, score):

        if score >= 25:

            return "Exceptional"

        if score >= 20:

            return "High"

        if score >= 12:

            return "Moderate"

        return "Low"