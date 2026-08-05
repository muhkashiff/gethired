"""
Enterprise Leadership Signal Detector

Enterprise V6

Purpose
-------
Detects leadership behaviours hidden inside
achievement evidence.

Input
-----

AchievementEvidence

Output
------

LeadershipSignal
"""

from typing import List

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.achievement_models import (
    AchievementEvidence,
    LeadershipSignal,
)


class LeadershipSignalDetector:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.rules = {

            "lead": "Leadership",

            "led": "Leadership",

            "manage": "Management",

            "managed": "Management",

            "mentor": "People Development",

            "mentored": "People Development",

            "coach": "People Development",

            "coached": "People Development",

            "train": "People Development",

            "trained": "People Development",

            "develop": "Execution",

            "developed": "Execution",

            "implement": "Execution",

            "implemented": "Execution",

            "coordinate": "Collaboration",

            "coordinated": "Collaboration",

            "collaborate": "Collaboration",

            "collaborated": "Collaboration",

            "improve": "Continuous Improvement",

            "improved": "Continuous Improvement",

            "optimize": "Continuous Improvement",

            "optimized": "Continuous Improvement",

            "transform": "Transformation",

            "transformed": "Transformation",

            "drive": "Strategic Leadership",

            "drove": "Strategic Leadership",

            "deliver": "Execution",

            "delivered": "Execution",

        }

    ####################################################################
    # PUBLIC API
    ####################################################################

    def analyze(

        self,

        achievements: List[AchievementEvidence],

    ) -> List[LeadershipSignal]:

        signals = []

        for achievement in achievements:

            signal = self._detect(

                achievement

            )

            if signal:

                signals.append(

                    signal

                )

        return signals

    ####################################################################
    # DETECTION
    ####################################################################

    def _detect(

        self,

        achievement: AchievementEvidence,

    ):

        if achievement.action is None:

            return None

        action_text = achievement.action.name.lower()

        for keyword, category in self.rules.items():

            if keyword in action_text:

                signal = LeadershipSignal()

                signal.category = category

                signal.description = achievement.action.name

                signal.score = self._score(

                    category

                )

                signal.confidence = achievement.confidence

                signal.metadata = {

                    "matched_keyword": keyword,

                    "business_area": achievement.business_area,

                    "domain": achievement.domain,

                }

                return signal

        return None

    ####################################################################
    # SCORING
    ####################################################################

    def _score(

        self,

        category,

    ):

        scores = {

            "Leadership": 100,

            "Management": 95,

            "Strategic Leadership": 95,

            "Transformation": 90,

            "People Development": 90,

            "Continuous Improvement": 85,

            "Execution": 80,

            "Collaboration": 75,

        }

        return scores.get(

            category,

            60,

        )