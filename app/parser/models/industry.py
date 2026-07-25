"""
GetHired
Industry Model
"""

from dataclasses import dataclass


@dataclass
class Industry:

    name: str

    confidence: float = 1.0

    matched: bool = False

    score: float = 0.0

    evidence: list[str] = None

    normalized_name: str = ""