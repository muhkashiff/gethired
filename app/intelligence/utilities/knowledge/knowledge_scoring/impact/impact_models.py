"""
Impact Models

Represents the business impact produced by a resume.

Impact is one of the core intelligence outputs
used throughout the GetHired platform.

Later modules

• Executive Readiness

• ATS Ranking

• Resume Rewrite

• Recruiter Summary

• Career Progression

• Job Matching
"""

from dataclasses import dataclass, field


# -----------------------------------------------------


@dataclass
class ImpactEvidence:
    """
    Individual evidence contributing to impact.
    """

    title: str = ""

    category: str = ""

    score: float = 0.0

    confidence: float = 1.0

    source: str = ""


# -----------------------------------------------------


@dataclass
class ImpactProfile:

    overall_score: float = 0.0

    level: str = ""

    operational_score: float = 0.0

    financial_score: float = 0.0

    quality_score: float = 0.0

    leadership_score: float = 0.0

    strategic_score: float = 0.0

    innovation_score: float = 0.0

    evidence: list[ImpactEvidence] = field(default_factory=list)

    confidence: float = 1.0