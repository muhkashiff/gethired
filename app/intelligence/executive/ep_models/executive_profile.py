"""
Executive Potential Profile
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ExecutiveProfile:

    # Overall

    executive_score: float = 0.0

    executive_rating: str = ""

    executive_readiness: str = ""

    confidence: float = 0.0

    # Leadership

    leadership_maturity: float = 0.0

    people_leadership: float = 0.0

    strategic_leadership: float = 0.0

    operational_leadership: float = 0.0

    # Career

    promotion_maturity: float = 0.0

    career_maturity: float = 0.0

    stability_maturity: float = 0.0

    trajectory_maturity: float = 0.0

    # Business

    business_acumen: float = 0.0

    commercial_exposure: float = 0.0

    change_leadership: float = 0.0

    executive_presence: float = 0.0

    # Recommendations

    next_role: str = ""

    future_roles: List[str] = field(default_factory=list)

    strengths: List[str] = field(default_factory=list)

    development_areas: List[str] = field(default_factory=list)

    score_breakdown: Dict = field(default_factory=dict)

    evidence: List[str] = field(default_factory=list)