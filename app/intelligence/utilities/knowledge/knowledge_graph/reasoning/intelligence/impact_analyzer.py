"""
Enterprise Impact Analyzer

Enterprise V6

Purpose
-------
Transforms achievement evidence into
business impact intelligence.

Input
-----

AchievementEvidence

Output
------

BusinessImpact
"""

from typing import List

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.achievement_models import (
    AchievementEvidence,
    BusinessImpact,
)


class ImpactAnalyzer:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.business_area_map = {

            "quality": "Quality",

            "food_safety": "Food Safety",

            "manufacturing": "Operations",

            "operations": "Operations",

            "engineering": "Engineering",

            "retail": "Retail",

            "logistics": "Supply Chain",

            "supply_chain": "Supply Chain",

            "finance": "Financial",

            "commercial": "Commercial",

            "project_management": "Project Management",

            "digital": "Digital",

            "leadership": "Leadership",

        }

    ####################################################################
    # PUBLIC API
    ####################################################################

    def analyze(

        self,

        achievements: List[AchievementEvidence],

    ) -> List[BusinessImpact]:

        impacts = []

        for achievement in achievements:

            impact = self._analyze_single(

                achievement

            )

            if impact:

                impacts.append(

                    impact

                )

        return impacts

    ####################################################################
    # SINGLE ACHIEVEMENT
    ####################################################################

    def _analyze_single(

        self,

        achievement: AchievementEvidence,

    ) -> BusinessImpact:

        impact = BusinessImpact()

        ###############################################################
        # Category
        ###############################################################

        business_area = (

            achievement.business_area or ""

        ).lower()

        impact.category = self.business_area_map.get(

            business_area,

            "General",

        )

        ###############################################################
        # Score
        ###############################################################

        impact.score = self._calculate_score(

            achievement

        )

        ###############################################################
        # Confidence
        ###############################################################

        impact.confidence = achievement.confidence

        ###############################################################
        # Rationale
        ###############################################################

        impact.rationale = self._build_rationale(

            achievement,

            impact.category,

        )

        ###############################################################
        # Metadata
        ###############################################################

        impact.metadata = {

            "business_area": achievement.business_area,

            "domain": achievement.domain,

        }

        return impact

    ####################################################################
    # SCORE
    ####################################################################

    def _calculate_score(

        self,

        achievement: AchievementEvidence,

    ) -> float:

        score = 40

        if achievement.metric:

            score += 20

        if achievement.measurement:

            score += 20

        if achievement.standard:

            score += 10

        if achievement.methodology:

            score += 10

        return min(

            score,

            100,

        )

    ####################################################################
    # RATIONALE
    ####################################################################

    def _build_rationale(

        self,

        achievement: AchievementEvidence,

        category: str,

    ) -> str:

        parts = []

        if achievement.action:

            parts.append(

                f"Action: {achievement.action.name}"

            )

        if achievement.metric:

            parts.append(

                f"Metric: {achievement.metric.name}"

            )

        if achievement.measurement:

            parts.append(

                "Quantified Result"

            )

        if not parts:

            return f"{category} impact inferred."

        return (

            f"{category} impact identified. "

            + " | ".join(parts)

        )