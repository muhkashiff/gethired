"""
Object Knowledge Model
"""

from dataclasses import dataclass


@dataclass
class ObjectKnowledge:

    found: bool = False

    original: str = ""

    canonical: str = ""

    category: str = ""

    confidence: float = 0.0