"""
Achievement Profile Builder

Builds the complete achievement profile from
Achievement Engine output.

This becomes part of the Knowledge Profile.
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

        impact = achievement["impact"]

        magnitude = achievement["magnitude"]

        profile = {

            "overall_score": achievement["achievement_score"],

            "achievement_count": achievement["achievement_count"],

            "impact_score": achievement["impact_score"],

            "magnitude_score": achievement["magnitude_score"],

            "top_metrics": self._top_metrics(impact),

            "impact_distribution": self._impact_distribution(impact),

            "magnitude_distribution": self._magnitude_distribution(magnitude),

            "details": achievement,

        }

        return profile

    # -----------------------------------------------------

    def _top_metrics(self, impact):

        metrics = []

        for item in impact["measurements"]:

            metrics.append(

                {

                    "metric": item["metric"],

                    "score": item["score"],

                }

            )

        metrics.sort(

            key=lambda x: x["score"],

            reverse=True,

        )

        return metrics

    # -----------------------------------------------------

    def _impact_distribution(self, impact):

        counter = Counter()

        for item in impact["measurements"]:

            counter[item["metric"]] += 1

        return dict(counter)

    # -----------------------------------------------------

    def _magnitude_distribution(self, magnitude):

        counter = Counter()

        for item in magnitude["measurements"]:

            counter[item["classification"]] += 1

        return dict(counter)