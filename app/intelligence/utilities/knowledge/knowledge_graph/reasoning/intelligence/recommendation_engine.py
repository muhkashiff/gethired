"""
Enterprise Skill Recommendation Engine

Enterprise V6

Purpose
-------
Transforms skill intelligence into actionable recommendations.

Inputs
------
Technical Depth
Business Breadth
Future Readiness
Skill Clusters

Output
------
Ordered recommendations with priority and rationale.
"""

from typing import List

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.skill_models import (
    SkillRecommendation,
)


class RecommendationEngine:

    def __init__(self):

        self._weights = {

            "critical": 100,
            "high": 80,
            "medium": 60,
            "low": 40,

        }

    # =========================================================

    def generate(

        self,

        technical_depth,

        business_breadth,

        future_readiness,

        clusters,

    ) -> List[SkillRecommendation]:

        recommendations = []

        # ---------------------------------------------
        # AI Readiness
        # ---------------------------------------------

        if future_readiness.ai_ready < 60:

            recommendations.append(

                SkillRecommendation(

                    title="Develop AI Capability",

                    priority="critical",

                    score=self._weights["critical"],

                    rationale=(
                        "Machine Learning / AI capability is below enterprise expectations."
                    ),

                    suggested_skills=[

                        "Machine Learning",

                        "Deep Learning",

                        "LLMs",

                        "Prompt Engineering",

                    ],

                )

            )

        # ---------------------------------------------
        # Cloud
        # ---------------------------------------------

        if future_readiness.cloud_ready < 60:

            recommendations.append(

                SkillRecommendation(

                    title="Strengthen Cloud Engineering",

                    priority="high",

                    score=self._weights["high"],

                    rationale=(
                        "Modern enterprise roles increasingly require cloud deployment skills."
                    ),

                    suggested_skills=[

                        "Azure",

                        "AWS",

                        "Docker",

                        "Kubernetes",

                    ],

                )

            )

        # ---------------------------------------------
        # Analytics
        # ---------------------------------------------

        if technical_depth.analytics < 50:

            recommendations.append(

                SkillRecommendation(

                    title="Improve Analytics Depth",

                    priority="high",

                    score=self._weights["high"],

                    rationale=(
                        "Analytical capability is lower than expected for senior roles."
                    ),

                    suggested_skills=[

                        "SQL",

                        "Power BI",

                        "Python",

                        "Statistics",

                    ],

                )

            )

        # ---------------------------------------------
        # Business Breadth
        # ---------------------------------------------

        if business_breadth.overall < 60:

            recommendations.append(

                SkillRecommendation(

                    title="Increase Business Exposure",

                    priority="medium",

                    score=self._weights["medium"],

                    rationale=(
                        "Broader cross-functional experience will improve leadership readiness."
                    ),

                    suggested_skills=[

                        "Supply Chain",

                        "Operations",

                        "Project Management",

                    ],

                )

            )

        # ---------------------------------------------
        # Digital
        # ---------------------------------------------

        if future_readiness.digital_ready < 60:

            recommendations.append(

                SkillRecommendation(

                    title="Expand Digital Transformation Skills",

                    priority="medium",

                    score=self._weights["medium"],

                    rationale=(
                        "Digital capability is important for future enterprise leadership."
                    ),

                    suggested_skills=[

                        "Automation",

                        "Cloud",

                        "Data",

                        "AI",

                    ],

                )

            )

        # ---------------------------------------------
        # Cluster Gap Detection
        # ---------------------------------------------

        existing_clusters = {

            cluster.name

            for cluster in clusters

        }

        desired = {

            "Machine Learning",

            "Cloud Engineering",

            "Data Analytics",

            "Backend Development",

        }

        missing = desired - existing_clusters

        if missing:

            recommendations.append(

                SkillRecommendation(

                    title="Develop Missing Enterprise Skill Clusters",

                    priority="medium",

                    score=55,

                    rationale=(
                        "Adding these capability clusters increases enterprise versatility."
                    ),

                    suggested_skills=sorted(missing),

                )

            )

        # ---------------------------------------------
        # Sort
        # ---------------------------------------------

        recommendations.sort(

            key=lambda r: r.score,

            reverse=True,

        )

        return recommendations