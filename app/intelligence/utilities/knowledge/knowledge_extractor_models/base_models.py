"""
Enterprise Knowledge Entity

Every ontology knowledge model inherits from this.
"""

from dataclasses import dataclass, field


@dataclass
class KnowledgeEntity:

    ####################################################################
    # Detection
    ####################################################################

    found: bool = False

    confidence: float = 0.0

    ####################################################################
    # Linguistic
    ####################################################################

    original: str = ""

    canonical: str = ""

    normalized: str = ""

    category: str = ""

    ####################################################################
    # Ontology
    ####################################################################

    entity_id: str = ""

    entity_type: str = ""

    matched_phrase: str = ""

    matched_alias: bool = False

    ontology_name: str = ""

    business_area: str = ""

    domain: str = ""

    impact_weight: float = 1.0

    source: str = ""

    metadata: dict = field(default_factory=dict)

    ####################################################################
    # Position
    ####################################################################

    start_char: int = -1

    end_char: int = -1

    token_index: int = -1

    token_count: int = 0

    sentence_index: int = 0