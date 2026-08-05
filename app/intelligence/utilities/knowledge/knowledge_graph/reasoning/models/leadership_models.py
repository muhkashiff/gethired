"""
Leadership Reasoning Models
"""

from dataclasses import dataclass, field
from typing import Dict, List


# ==========================================================
# Leadership Reasoning Result
# ==========================================================

@dataclass
class LeadershipReasoningResult:

    overall_score: float = 0.0

    people_score: float = 0.0

    operational_score: float = 0.0

    technical_score: float = 0.0

    strategic_score: float = 0.0

    change_score: float = 0.0

    financial_score: float = 0.0

    commercial_score: float = 0.0

    stakeholder_score: float = 0.0

    executive_score: float = 0.0

    level: str = ""

    executive_actions: int = 0

    actions: Dict[str, int] = field(default_factory=dict)

    evidence: List[str] = field(default_factory=list)

    confidence: float = 0.0