"""
Universal Ontology Entity

Every ontology lookup returns this object.
"""

from dataclasses import dataclass, field


@dataclass
class EntityRecord:

    ####################################################################
    # Core Identity
    ####################################################################

    entity_id: str = ""

    canonical: str = ""

    normalized: str = ""

    aliases: list = field(default_factory=list)

    ####################################################################
    # Linguistic Forms
    ####################################################################

    base: str = ""

    past: str = ""

    gerund: str = ""

    plural: str = ""

    singular: str = ""

    abbreviation: str = ""

    short_name: str = ""

    ####################################################################
    # Classification
    ####################################################################

    category: str = ""

    entity_type: str = ""

    ontology_name: str = ""

    ####################################################################
    # Business Classification
    ####################################################################

    domain: str = ""

    business_area: str = ""

    description: str = ""

    ####################################################################
    # Business Behaviour
    ####################################################################

    impact_weight: float = 1.0

    business_meaning: str = ""

    preferred_direction: str = ""

    preferred_unit: str = ""

    higher_is_better: bool = True

    ####################################################################
    # Matching
    ####################################################################

    searchable: bool = True

    active: bool = True

    ####################################################################
    # Source
    ####################################################################

    source: str = "ontology"

    metadata: dict = field(default_factory=dict)