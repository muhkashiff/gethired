"""
Linked Entity

Returned by EntityLinker.
"""

from dataclasses import dataclass, field


@dataclass
class LinkedEntity:

    found: bool = False

    entity_id: str = ""

    canonical: str = ""

    category: str = ""

    business_area: str = ""

    preferred_direction: str = ""

    impact_weight: int = 0

    business_meaning: str = ""

    source: str = ""

    confidence: float = 0.0

    aliases: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)