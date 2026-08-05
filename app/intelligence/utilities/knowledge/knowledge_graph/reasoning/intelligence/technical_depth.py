"""
Enterprise Technical Depth Analyzer

Calculates enterprise technical capability
from capability clusters.

Input

Skill Clusters

Output

TechnicalDepth
"""

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.skill_models import (
    TechnicalDepth,
)


class TechnicalDepthAnalyzer:

    """
    Calculates technical depth from capability clusters.
    """

    def __init__(self):

        self.cluster_weights = {

            "Machine Learning": 12,

            "Data Analytics": 10,

            "Backend Development": 9,

            "Cloud Engineering": 10,

            "Food Safety": 12,

            "Quality Management": 10,

            "Operational Excellence": 8,

            "Leadership": 7,

        }

    # ---------------------------------------------------------

    def analyze(self, clusters):

        depth = TechnicalDepth()

        for cluster in clusters:

            weight = self.cluster_weights.get(

                cluster.name,

                5,

            )

            score = min(

                len(cluster.skills) * weight,

                100,

            )

            if cluster.name == "Machine Learning":

                depth.ai = score

                depth.programming = score

            elif cluster.name == "Data Analytics":

                depth.analytics = score

            elif cluster.name == "Backend Development":

                depth.programming = max(

                    depth.programming,

                    score,

                )

            elif cluster.name == "Cloud Engineering":

                depth.cloud = score

                depth.automation = score

            elif cluster.name == "Food Safety":

                depth.food_safety = score

            elif cluster.name == "Quality Management":

                depth.quality = score

            elif cluster.name == "Operational Excellence":

                depth.operations = score

            elif cluster.name == "Leadership":

                depth.leadership = score

        values = [

            depth.programming,

            depth.analytics,

            depth.quality,

            depth.food_safety,

            depth.operations,

            depth.leadership,

            depth.automation,

            depth.cloud,

            depth.ai,

        ]

        depth.overall = round(

            sum(values) / len(values),

            2,

        )

        return depth