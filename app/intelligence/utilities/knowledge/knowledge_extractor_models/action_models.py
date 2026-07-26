"""
Action Knowledge Model
"""

from dataclasses import dataclass


@dataclass
class ActionKnowledge:

    found: bool = False

    original: str = ""

    base: str = ""

    gerund: str = ""

    category: str = ""

    confidence: float = 0.0