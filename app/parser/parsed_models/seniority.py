"""
GetHired
Seniority Model
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Seniority:

    name: str

    level: int = 0

    confidence: float = 1.0

    matched: bool = False

    score: float = 0.0

    evidence: List[str] = field(default_factory=list)

    normalized_name: str = ""