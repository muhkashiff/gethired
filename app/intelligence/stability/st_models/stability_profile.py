"""
GetHired
Career Stability Profile
"""

from dataclasses import dataclass, field
from typing import List
from typing import Dict


@dataclass
class StabilityProfile:

    average_tenure: float = 0.0

    longest_tenure: float = 0.0

    shortest_tenure: float = 0.0

    total_companies: int = 0

    total_experience: float = 0.0

    stability_score: float = 0.0

    stability_rating: str = ""

    employment_risk: str = ""

    job_hopper: bool = False

    loyalty_rating: str = ""

    career_consistency: str = ""

    score_breakdown: dict = field(default_factory=dict)

    confidence: float = 0.0

    evidence: List[str] = field(default_factory=list)