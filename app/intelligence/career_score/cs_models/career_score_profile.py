"""
Career Score Profile
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CareerScoreProfile:

    # ======================================================
    # MASTER SCORES
    # ======================================================

    overall_score: float = 0.0

    leadership_index: float = 0.0

    career_health_index: float = 0.0

    market_readiness_index: float = 0.0

    # ======================================================
    # RATINGS
    # ======================================================

    overall_rating: str = ""

    recruiter_readiness: str = ""

    ats_strength: str = ""

    career_grade: str = ""

    market_position: str = ""

    career_risk: str = ""

    confidence: float = 0.0

    # ======================================================
    # RAW ENGINE INDICES
    # ======================================================

    promotion_index: float = 0.0

    stability_index: float = 0.0

    trajectory_index: float = 0.0

    executive_index: float = 0.0

    growth_index: float = 0.0

    # ======================================================
    # EXPLAINABILITY
    # ======================================================

    score_breakdown: Dict = field(default_factory=dict)

    strengths: List[str] = field(default_factory=list)

    development_areas: List[str] = field(default_factory=list)

    evidence: List[str] = field(default_factory=list)