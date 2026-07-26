"""
Domain Knowledge Model
"""

from dataclasses import dataclass


@dataclass
class DomainKnowledge:

    found: bool = False

    domain: str = ""

    reasoning: str = ""

    confidence: float = 0.0