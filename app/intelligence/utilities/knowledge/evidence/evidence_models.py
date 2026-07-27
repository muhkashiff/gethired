"""
Evidence Models
"""

from dataclasses import dataclass


@dataclass
class ClauseEvidence:

    score: float = 0.0

    leadership: float = 0.0

    achievement: float = 0.0

    quantified: float = 0.0

    business_impact: float = 0.0

    executive: float = 0.0

    certification: float = 0.0

    improvement: float = 0.0

    confidence: float = 0.0