"""
Enterprise Achievement Pattern Analyzer

Enterprise V6

Purpose
-------
Discovers recurring enterprise achievement patterns.

Input
-----

AchievementEvidence

Output
------

AchievementPattern
"""

from collections import defaultdict
from typing import List

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.achievement_models import (
    AchievementEvidence,
    AchievementPattern,
)


class AchievementPatternAnalyzer:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.pattern_rules = {

            "yield": "Operational Excellence",

            "waste": "Cost Reduction",

            "loss": "Cost Reduction",

            "downtime": "Operational Excellence",

            "efficiency": "Operational Excellence",

            "quality": "Quality Improvement",

            "complaint": "Customer Satisfaction",

            "customer": "Customer Satisfaction",

            "food safety": "Food Safety",

            "fssc": "Food Safety",

            "haccp": "Food Safety",

            "gmp": "Food Safety",

            "lean": "Continuous Improvement",

            "six sigma": "Continuous Improvement",

            "automation": "Digital Transformation",

            "digital": "Digital Transformation",

            "training": "People Development",

            "team": "Leadership",

            "project": "Project Delivery",

        }

    ####################################################################
    # PUBLIC API
    ####################################################################

    def analyze(

        self,

        achievements: List[AchievementEvidence],

    ) -> List[AchievementPattern]:

        grouped = defaultdict(list)

        ###############################################################
        # Detect patterns
        ###############################################################

        for achievement in achievements:

            categories = self._detect_categories(

                achievement

            )

            for category in categories:

                grouped[category].append(

                    achievement

                )

        ###############################################################
        # Build objects
        ###############################################################

        patterns = []

        for category, evidence in grouped.items():

            pattern = AchievementPattern()

            pattern.name = category

            pattern.category = category

            pattern.occurrences = len(evidence)

            pattern.score = self._calculate_score(

                evidence

            )

            pattern.confidence = self._confidence(

                evidence

            )

            pattern.rationale = (

                self._rationale(

                    category,

                    evidence,

                )

            )

            pattern.metadata = {

                "business_areas":

                    sorted(

                        {

                            e.business_area

                            for e in evidence

                            if e.business_area

                        }

                    ),

                "domains":

                    sorted(

                        {

                            e.domain

                            for e in evidence

                            if e.domain

                        }

                    ),

            }

            patterns.append(pattern)

        ###############################################################
        # Highest score first
        ###############################################################

        patterns.sort(

            key=lambda x: (

                x.score,

                x.occurrences,

            ),

            reverse=True,

        )

        return patterns

    ####################################################################
    # DETECT
    ####################################################################

    def _detect_categories(

        self,

        achievement,

    ):

        detected = set()

        searchable = []

        if achievement.action:

            searchable.append(

                achievement.action.name.lower()

            )

        if achievement.metric:

            searchable.append(

                achievement.metric.name.lower()

            )

        if achievement.measurement:

            searchable.append(

                achievement.measurement.name.lower()

            )

        text = " ".join(searchable)

        for keyword, category in self.pattern_rules.items():

            if keyword in text:

                detected.add(category)

        return detected

    ####################################################################
    # SCORE
    ####################################################################

    def _calculate_score(

        self,

        evidence,

    ):

        if not evidence:

            return 0

        confidence = sum(

            e.confidence

            for e in evidence

        ) / len(evidence)

        score = (

            confidence * 100

            + len(evidence) * 5

        )

        return round(

            min(score, 100),

            2,

        )

    ####################################################################
    # CONFIDENCE
    ####################################################################

    def _confidence(

        self,

        evidence,

    ):

        if not evidence:

            return 0

        return round(

            sum(

                e.confidence

                for e in evidence

            )

            /

            len(evidence),

            2,

        )

    ####################################################################
    # RATIONALE
    ####################################################################

    def _rationale(

        self,

        category,

        evidence,

    ):

        return (

            f"{len(evidence)} achievement(s) "

            f"indicate recurring "

            f"{category.lower()} capability."
        )