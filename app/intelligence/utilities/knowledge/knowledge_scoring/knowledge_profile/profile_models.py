"""
Knowledge Profile Models

The Knowledge Profile is the structured representation
of everything extracted from a resume.

Every downstream AI engine works from this profile.
"""

from dataclasses import dataclass, field
from typing import Any


# ------------------------------------------------------
# Summary Profile
# ------------------------------------------------------

@dataclass
class SummaryProfile:

    overall_score: float = 0.0

    achievement_score: float = 0.0

    leadership_score: float = 0.0

    seniority_score: float = 0.0

    career_level: str = ""


# ------------------------------------------------------
# Achievement Profile
# ------------------------------------------------------

@dataclass
class AchievementProfile:

    overall_score: float = 0.0

    achievement_count: int = 0

    impact_score: float = 0.0

    magnitude_score: float = 0.0

    top_achievements: list = field(default_factory=list)

    top_metrics: list = field(default_factory=list)

    impact_distribution: dict = field(default_factory=dict)

    magnitude_distribution: dict = field(default_factory=dict)

    details: Any = None


# ------------------------------------------------------
# Leadership Profile
# ------------------------------------------------------

@dataclass
class LeadershipProfile:

    score: float = 0.0

    level: str = ""

    actions: dict = field(default_factory=dict)

    executive_actions: int = 0


# ------------------------------------------------------
# Seniority Profile
# ------------------------------------------------------

@dataclass
class SeniorityProfile:

    score: float = 0.0

    level: str = ""

    actions: dict = field(default_factory=dict)

    domains: dict = field(default_factory=dict)


# ------------------------------------------------------
# Metric Profile
# ------------------------------------------------------

@dataclass
class MetricProfile:

    total_metrics: int = 0

    positive_metrics: int = 0

    negative_metrics: int = 0

    increase_metrics: int = 0

    decrease_metrics: int = 0


# ------------------------------------------------------
# Domain Profile
# ------------------------------------------------------

@dataclass
class DomainProfile:

    domains: dict = field(default_factory=dict)

    business_areas: dict = field(default_factory=dict)


# ------------------------------------------------------
# Modifier Profile
# ------------------------------------------------------

@dataclass
class ModifierProfile:

    total_modifiers: int = 0

    executive_modifiers: int = 0

    categories: dict = field(default_factory=dict)


# ------------------------------------------------------
# Master Knowledge Profile
# ------------------------------------------------------

@dataclass
class KnowledgeProfile:

    summary: SummaryProfile = field(
        default_factory=SummaryProfile
    )

    achievement: AchievementProfile = field(
        default_factory=AchievementProfile
    )

    leadership: LeadershipProfile = field(
        default_factory=LeadershipProfile
    )

    seniority: SeniorityProfile = field(
        default_factory=SeniorityProfile
    )

    metrics: MetricProfile = field(
        default_factory=MetricProfile
    )

    domains: DomainProfile = field(
        default_factory=DomainProfile
    )

    modifiers: ModifierProfile = field(
        default_factory=ModifierProfile
    )

    confidence: float = 1.0