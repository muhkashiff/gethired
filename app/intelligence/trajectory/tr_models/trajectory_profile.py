"""
Career Trajectory Profile
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class TrajectoryProfile:

    career_stage: str = ""

    career_trend: str = ""

    trajectory_score: float = 0.0

    momentum_score: float = 0.0

    executive_path: bool = False

    plateau_detected: bool = False

    regression_detected: bool = False

    management_growth: str = ""

    technical_growth: str = ""

    leadership_growth: str = ""

    industry_transition: str = ""

    future_projection: str = ""

    confidence: float = 0.0

    score_breakdown: Dict = field(default_factory=dict)

    evidence: List[str] = field(default_factory=list)