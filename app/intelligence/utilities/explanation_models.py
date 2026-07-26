"""
Explanation Models
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Explanation:

    title: str = ""

    summary: str = ""

    strengths: List[str] = field(default_factory=list)

    weaknesses: List[str] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)

    evidence: List[str] = field(default_factory=list)

    confidence: float = 0.0