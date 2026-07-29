"""
Achievement Profile Builder

Builds the complete achievement profile from
Achievement Engine output.

Produces a richer profile including:

• Overall score
• Top achievements
• KPI distribution
• Magnitude distribution
• Detailed measurement cards
"""

from collections import Counter

from app.intelligence.utilities.knowledge.knowledge_scoring.achievement.achievement_engine import (
    AchievementEngine,
)


class AchievementProfileBuilder:

    def __init__(self):

        self.engine = AchievementEngine()

    # -----------------------------------------------------

    def build(self, graph):

        achievement = self.engine.score(graph)

        achievement_cards = achievement["achievements"]

        profile = {

            "overall_score": achievement["achievement_score"],

            "achievement_count": achievement["achievement_count"],

            "impact_score": achievement["impact_score"],

            "magnitude_score": achievement["magnitude_score"],

            # Executive summaries
            "top_metrics": self._top_metrics(achievement_cards),

            "top_achievements": achievement_cards,

            # Distributions
            "impact_distribution": self._impact_distribution(
                achievement["achievements"]
            ),

            "magnitude_distribution": self._magnitude_distribution(
                achievement["achievements"]
            ),

            # Full engine output
            "details": achievement,

        }

        return profile

    # -----------------------------------------------------

    def _top_metrics(self, achievements):

        metrics = []

        for item in achievements:

            metrics.append(
                {

                    "metric": item["metric"],

                    "overall_score": item["overall_score"],

                    "impact_score": item["impact_score"],

                    "magnitude_score": item["magnitude_score"],

                    "business_value": item["business_value"],

                }

            )

        metrics.sort(

            key=lambda x: x["overall_score"],

            reverse=True,

        )

        return metrics

    # -----------------------------------------------------

    def _top_achievements(self, impact, magnitude):

        # -----------------------------------------------------
        # Build lookup from Magnitude Engine
        # -----------------------------------------------------

        mag_lookup = {}

        for m in magnitude.get("measurements", []):

            metric = m.get("metric")

            if metric:

                mag_lookup[metric] = m

        # -----------------------------------------------------
        # Merge Impact + Magnitude
        # -----------------------------------------------------

        cards = []

        for item in impact.get("measurements", []):

            metric = item.get("metric")

            mag = mag_lookup.get(metric, {})

            cards.append(

                {

                    # -----------------------------------
                    # KPI
                    # -----------------------------------

                    "metric": metric,

                    "action": item.get("action"),

                    "measurement": item.get("measurement"),

                    "measurement_type": item.get("measurement_type"),

                    # -----------------------------------
                    # Values
                    # -----------------------------------

                    "start_value": item.get("start_value"),

                    "end_value": item.get("end_value"),

                    "change_value": item.get("change_value"),

                    "percent_change": item.get("percent_change"),

                    "unit": item.get("unit"),

                    # -----------------------------------
                    # Business Interpretation
                    # -----------------------------------

                    "direction": item.get("direction"),

                    "effect": item.get("effect"),

                    "business_meaning": item.get("business_meaning"),

                    "business_value": item.get("business_value"),

                    "business_area": item.get("business_area"),

                    # -----------------------------------
                    # Scores
                    # -----------------------------------

                    "impact_score": item.get("score", 0),

                    "magnitude_score": mag.get("score", 0),

                    "classification": mag.get("classification", "Unknown"),

                }

            )

        # -----------------------------------------------------
        # Highest impact first
        # -----------------------------------------------------

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

            classification = item.get("classification")

            if classification:

                counter[classification] += 1

        return dict(counter)