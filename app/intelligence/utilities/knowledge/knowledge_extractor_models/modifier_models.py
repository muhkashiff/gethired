"""
Modifier Models

Represents linguistic modifiers that qualify
actions, scope, impact, or achievement.
"""

from dataclasses import dataclass, field


@dataclass
class ModifierKnowledge:

    # Detection
    found: bool = False

    confidence: float = 0.0

    # Linguistics
    original: str = ""

    canonical: str = ""

    category: str = ""

    strength: float = 1.0

    executive_weight: float = 1.0

    # Ontology
    entity_id: str = ""

    business_area: str = ""

    impact_weight: float = 1.0

    source: str = ""

    metadata: dict = field(default_factory=dict)