"""
Universal Ontology Entity

Every ontology lookup returns this object.
"""

from dataclasses import dataclass, field


@dataclass
class EntityRecord:

    # -------------------------------------------------
    # Core
    # -------------------------------------------------

    entity_id: str = ""

    canonical: str = ""

    aliases: list = field(default_factory=list)

    category: str = ""

    business_area: str = ""

    description: str = ""

    # -------------------------------------------------
    # KPI Properties
    # -------------------------------------------------

    preferred_unit: str = ""

    higher_is_better: bool = True

    preferred_direction: str = ""

    impact_weight: float = 1.0

    business_meaning: str = ""

    # -------------------------------------------------
    # Source
    # -------------------------------------------------

    source: str = "ontology"

    metadata: dict = field(default_factory=dict)