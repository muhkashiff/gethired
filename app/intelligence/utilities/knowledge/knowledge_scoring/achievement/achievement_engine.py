"""
Achievement Engine

Combines multiple scoring engines into a single
achievement score.

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

        total = (

            impact["score"]

            + magnitude["score"]

        )

        return {

            "achievement_score": round(total, 2),

            "impact_score": impact["score"],

            "magnitude_score": magnitude["score"],

            "achievement_count": max(

                impact["count"],

                magnitude["count"],

            ),

            "impact": impact,

            "magnitude": magnitude,

        }