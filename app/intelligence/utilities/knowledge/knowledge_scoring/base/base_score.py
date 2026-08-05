"""
Score Base

Enterprise V12

Every scoring engine returns a Score object.

Examples

AchievementScore

LeadershipScore

TechnicalScore

ExecutiveScore

BusinessValueScore

All inherit from ScoreBase.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


# ==========================================================
# Score Base
# ==========================================================

@dataclass
class ScoreBase:
    """
    Parent score object for every engine.
    """

    score_type: str = ""

    overall_score: float = 0.0

    confidence: float = 0.0

    level: str = ""

    summary: str = ""

    evidence_count: int = 0

    strengths: list[str] = field(default_factory=list)

    weaknesses: list[str] = field(default_factory=list)

    recommendations: list[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------

    def normalize(
        self,
        minimum=0,
        maximum=100,
    ):

        if self.overall_score < minimum:
            self.overall_score = minimum

        if self.overall_score > maximum:
            self.overall_score = maximum

        self.overall_score = round(
            self.overall_score,
            2,
        )

        return self.overall_score

    # -----------------------------------------------------

    def add_strength(self, text):

        if text not in self.strengths:
            self.strengths.append(text)

    # -----------------------------------------------------

    def add_weakness(self, text):

        if text not in self.weaknesses:
            self.weaknesses.append(text)

    # -----------------------------------------------------

    def add_recommendation(self, text):

        if text not in self.recommendations:
            self.recommendations.append(text)

    # -----------------------------------------------------

    def update_confidence(
        self,
        confidence,
    ):

        self.confidence = round(
            confidence,
            2,
        )

    # -----------------------------------------------------

    def update_level(
        self,
        level,
    ):

        self.level = level

    # -----------------------------------------------------

    def update_summary(
        self,
        summary,
    ):

        self.summary = summary

    # -----------------------------------------------------

    def __repr__(self):

        return (

            f"<{self.score_type} "

            f"score={self.overall_score} "

            f"confidence={self.confidence}>"

        )