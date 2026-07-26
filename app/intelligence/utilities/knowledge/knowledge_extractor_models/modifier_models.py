"""
Modifier Models

Represents linguistic modifiers that qualify
actions, scope, impact, or achievement.
"""

from dataclasses import dataclass


@dataclass
class ModifierKnowledge:

    found: bool = False

    original: str = ""

    canonical: str = ""

    category: str = ""

    strength: float = 0.0

    executive_weight: float = 0.0

    confidence: float = 0.0