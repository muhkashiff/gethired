"""
Enterprise Relation Knowledge Model
Enterprise V5

Represents a semantic relationship between two extracted
knowledge entities.

This is an EXTRACTION object.

Repository relation:
    RelationRepositoryRecord

Extraction result:
    RelationKnowledge
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RelationKnowledge:

    ####################################################################
    # DETECTION
    ####################################################################

    found: bool = False

    confidence: float = 0.0

    ####################################################################
    # RELATION IDENTITY
    ####################################################################

    relation_id: str = ""

    relation_type: str = ""

    relation_family: str = ""

    ####################################################################
    # SOURCE ENTITY
    ####################################################################

    source_entity_id: str = ""

    source_entity_type: str = ""

    source_canonical: str = ""

    source_phrase: str = ""

    ####################################################################
    # TARGET ENTITY
    ####################################################################

    target_entity_id: str = ""

    target_entity_type: str = ""

    target_canonical: str = ""

    target_phrase: str = ""

    ####################################################################
    # TEXT POSITION
    ####################################################################

    start_char: int = -1

    end_char: int = -1

    sentence_index: int = 0

    ####################################################################
    # SEMANTIC INFORMATION
    ####################################################################

    business_area: str = ""

    domain: str = ""

    description: str = ""

    impact_weight: float = 1.0

    ####################################################################
    # GRAPH
    ####################################################################

    graph_edge: bool = True

    ####################################################################
    # SOURCE
    ####################################################################

    source: str = "relation_extractor"

    ####################################################################
    # METADATA
    ####################################################################

    metadata: dict = field(
        default_factory=dict
    )