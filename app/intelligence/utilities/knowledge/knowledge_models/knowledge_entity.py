"""
Enterprise Knowledge Entity

Base class for every ontology entity used inside
the Knowledge Intelligence Engine.

Author : GetHired AI
Version : Enterprise V3
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class KnowledgeEntity:

    ####################################################################
    # DETECTION
    ####################################################################

    found: bool = False

    confidence: float = 0.0

    extraction_method: str = "ontology"

    ####################################################################
    # LINGUISTICS
    ####################################################################

    original: str = ""

    canonical: str = ""

    normalized: str = ""

    ####################################################################
    # ONTOLOGY
    ####################################################################

    entity_id: str = ""

    entity_type: str = ""

    category: str = ""

    business_area: str = ""

    domain: str = ""

    impact_weight: float = 1.0

    source: str = ""

    matched_phrase: str = ""

    matched_alias: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)

    ####################################################################
    # POSITION
    ####################################################################

    start_char: int = -1

    end_char: int = -1

    token_index: int = -1

    token_count: int = 1

    sentence_index: int = 0

    clause_index: int = 0

    ####################################################################
    # GRAPH
    ####################################################################

    graph_node_created: bool = False

    graph_node_id: str = ""

    graph_cluster_id: str = ""

    ####################################################################
    # REASONING
    ####################################################################

    executive: bool = False

    strategic: bool = False

    tactical: bool = False

    operational: bool = False

    ####################################################################
    # RELATIONSHIPS
    ####################################################################

    related_entities: List[str] = field(default_factory=list)

    ####################################################################
    # SERIALIZATION
    ####################################################################

    def to_dict(self):

        return self.__dict__.copy()

    ####################################################################
    # DISPLAY
    ####################################################################

    def __repr__(self):

        return (

            f"{self.entity_type.upper()}"

            f"(canonical='{self.canonical}', "

            f"id='{self.entity_id}', "

            f"confidence={self.confidence:.2f})"

        )