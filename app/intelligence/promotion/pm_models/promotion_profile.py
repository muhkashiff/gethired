"""
GetHired
Promotion Intelligence Model
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class PromotionProfile:

    promotion_count: int = 0

    promotion_velocity: float = 0.0

    promotion_quality: float = 0.0

    highest_level: str = ""

    highest_level_score: int = 0

    title_history: List[str] = field(default_factory=list)

    level_history: List[int] = field(default_factory=list)

    promotion_jumps: List[int] = field(default_factory=list)

    early_leadership: bool = False

    fast_track: bool = False

    confidence: float = 0.0