"""
GetHired

Leadership Pattern Model
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class LeadershipPattern:

    text: str

    dimensions: List[str] = field(default_factory=list)

    weight: float = 0.0

    confidence: float = 1.0

    action: str = ""

    achievement: bool = False

    quantified: bool = False

    metric: str = ""

    matched_keywords: List[str] = field(default_factory=list)