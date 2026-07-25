"""
GetHired
Technology Model
"""

from dataclasses import dataclass


@dataclass
class Technology:

    name: str

    category: str = ""

    vendor: str = ""

    confidence: float = 1.0

    matched: bool = False

    score: float = 0.0

    raw_text: str = ""

    normalized_name: str = ""