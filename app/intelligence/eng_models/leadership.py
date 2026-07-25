"""
GetHired
Leadership Intelligence Model
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Leadership:

    # Overall score (0-100)
    overall_score: float = 0.0

    # Leadership dimensions
    people_management: float = 0.0
    strategic_leadership: float = 0.0
    operational_leadership: float = 0.0
    technical_leadership: float = 0.0
    financial_leadership: float = 0.0
    commercial_leadership: float = 0.0

    coaching: float = 0.0
    mentoring: float = 0.0

    change_management: float = 0.0
    stakeholder_management: float = 0.0
    project_management: float = 0.0

    continuous_improvement: float = 0.0

    confidence: float = 1.0

    evidence: List[str] = field(default_factory=list)

    strengths: List[str] = field(default_factory=list)

    weaknesses: List[str] = field(default_factory=list)