"""
Knowledge Profile Models

The Knowledge Profile is the structured representation
of everything extracted from a resume.

Every downstream AI engine works from this profile.
"""

from dataclasses import dataclass, field


@dataclass
class LeadershipProfile:

    score: float = 0.0

    level: str = ""

    actions: dict = field(default_factory=dict)

    executive_actions: int = 0


# ------------------------------------------------------


@dataclass
class SeniorityProfile:

    score: float = 0.0

    level: str = ""

    actions: dict = field(default_factory=dict)

    domains: dict = field(default_factory=dict)


# ------------------------------------------------------


@dataclass
class MetricProfile:

    total_metrics: int = 0

    positive_metrics: int = 0

    negative_metrics: int = 0

    increase_metrics: int = 0

    decrease_metrics: int = 0


# ------------------------------------------------------


@dataclass
class DomainProfile:

    domains: dict = field(default_factory=dict)

    business_areas: dict = field(default_factory=dict)


# ------------------------------------------------------


@dataclass
class ModifierProfile:

    total_modifiers: int = 0

    executive_modifiers: int = 0

    categories: dict = field(default_factory=dict)


# ------------------------------------------------------


@dataclass
class KnowledgeProfile:

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