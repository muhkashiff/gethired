"""
Universal Ontology Entity

Every ontology lookup returns this object.
"""

from dataclasses import dataclass, field


@dataclass
class EntityRecord:

    entity_id: str = ""

    canonical: str = ""

    aliases: list = field(default_factory=list)

    category: str = ""

    business_area: str = ""

    preferred_direction: str = ""

    impact_weight: int = 0

    business_meaning: str = ""

    source: str = ""

    metadata: dict = field(default_factory=dict)