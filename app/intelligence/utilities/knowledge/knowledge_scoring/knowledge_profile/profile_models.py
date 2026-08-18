"""
Knowledge Profile Models
Enterprise V14
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SummaryProfile:

    overall_score: float = 0.0

    impact_score: float = 0.0
    ats_score: float = 0.0
    achievement_score: float = 0.0
    leadership_score: float = 0.0
    seniority_score: float = 0.0

    career_level: str = ""


@dataclass
class EntityProfile:

    total_entities: int = 0

    entity_counts: dict[str, int] = field(
        default_factory=dict
    )

    entities: list[dict[str, Any]] = field(
        default_factory=list
    )


@dataclass
class AchievementProfile:

    overall_score: float = 0.0

    achievement_count: int = 0

    quantified_count: int = 0

    impact_score: float = 0.0

    magnitude_score: float = 0.0

    top_achievements: list[Any] = field(
        default_factory=list
    )

    top_metrics: list[Any] = field(
        default_factory=list
    )

    impact_distribution: dict[str, float] = field(
        default_factory=dict
    )

    magnitude_distribution: dict[str, float] = field(
        default_factory=dict
    )

    details: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class LeadershipProfile:

    score: float = 0.0

    level: str = ""

    entity_count: int = 0

    actions: dict[str, Any] = field(
        default_factory=dict
    )

    executive_actions: int = 0


@dataclass
class SeniorityProfile:

    score: float = 0.0

    level: str = ""

    actions: dict[str, Any] = field(
        default_factory=dict
    )

    domains: dict[str, float] = field(
        default_factory=dict
    )

    indicators: list[str] = field(
        default_factory=list
    )


@dataclass
class MetricProfile:

    total_metrics: int = 0

    positive_metrics: int = 0

    negative_metrics: int = 0

    increase_metrics: int = 0

    decrease_metrics: int = 0

    metrics: list[dict[str, Any]] = field(
        default_factory=list
    )


@dataclass
class DomainProfile:

    domains: dict[str, float] = field(
        default_factory=dict
    )

    business_areas: dict[str, float] = field(
        default_factory=dict
    )


@dataclass
class ModifierProfile:

    total_modifiers: int = 0

    executive_modifiers: int = 0

    categories: dict[str, float] = field(
        default_factory=dict
    )


@dataclass
class ImpactProfile:

    total_impact: float = 0.0

    average_impact: float = 0.0

    maximum_impact: float = 0.0

    entity_count: int = 0

    weighted_entities: list[dict[str, Any]] = field(
        default_factory=list
    )


@dataclass
class ATSProfile:

    score: float = 0.0

    entity_count: int = 0

    matched_entities: list[dict[str, Any]] = field(
        default_factory=list
    )


@dataclass
class BusinessStatementProfile:

    total_statements: int = 0

    statements: list[dict[str, Any]] = field(
        default_factory=list
    )


@dataclass
class KnowledgeProfile:

    summary: SummaryProfile = field(
        default_factory=SummaryProfile
    )

    entities: EntityProfile = field(
        default_factory=EntityProfile
    )

    achievements: AchievementProfile = field(
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

    impact: ImpactProfile = field(
        default_factory=ImpactProfile
    )

    ats: ATSProfile = field(
        default_factory=ATSProfile
    )

    business_statements: BusinessStatementProfile = field(
        default_factory=BusinessStatementProfile
    )

    confidence: float = 0.0


__all__ = [
    "KnowledgeProfile",
    "SummaryProfile",
    "EntityProfile",
    "AchievementProfile",
    "LeadershipProfile",
    "SeniorityProfile",
    "MetricProfile",
    "DomainProfile",
    "ModifierProfile",
    "ImpactProfile",
    "ATSProfile",
    "BusinessStatementProfile",
]