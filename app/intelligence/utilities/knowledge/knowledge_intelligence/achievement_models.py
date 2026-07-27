"""
Achievement Analysis Models

Represents the analysed strength of a resume achievement.
"""

from dataclasses import dataclass


@dataclass
class AchievementAnalysis:

    found: bool = False

    title: str = ""

    category: str = ""

    quantified: bool = False

    leadership: bool = False

    executive: bool = False

    business_impact: bool = False

    score: float = 0.0

    confidence: float = 0.0

    recommendation: str = ""