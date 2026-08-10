"""
Enterprise Relation Knowledge Model
Enterprise V5

Represents a semantic relationship between two extracted
knowledge entities.

Example:

Action:
    implemented

Standard:
    FSSC 22000

Relation:
    implemented -> FSSC 22000
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RelationKnowledge:
    """
    Typed representation of a relationship between two
    extracted knowledge entities.
    """

    ####################################################################
    # Detection
    ####################################################################

    found: bool = False

    confidence: float = 0.0

    ####################################################################
    # Relation Identity
    ####################################################################

    relation_id: str = ""

    relation_type: str = ""

    relation_family: str = ""

    ####################################################################
    # Source Entity
    ####################################################################

    source_entity_id: str = ""

    source_entity_type: str = ""

    source_canonical: str = ""

    source_phrase: str = ""

    ####################################################################
    # Target Entity
    ####################################################################

    target_entity_id: str = ""

    target_entity_type: str = ""

    target_canonical: str = ""

    target_phrase: str = ""

    ####################################################################
    # Text Position
    ####################################################################

    start_char: int = -1

    end_char: int = -1

    sentence_index: int = 0

    ####################################################################
    # Semantic Information
    ####################################################################

    business_area: str = ""

    domain: str = ""

    description: str = ""

    impact_weight: float = 1.0

    ####################################################################
    # Graph
    ####################################################################

    graph_edge: bool = True

    ####################################################################
    # Source
    ####################################################################

    source: str = "relation_extractor"

    metadata: dict = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}