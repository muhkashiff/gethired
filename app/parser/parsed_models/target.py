"""
Enterprise Target Parser Model

Enterprise V5

Parser-layer model for Target extraction.

Knowledge layer:
    TargetKnowledge

Parser layer:
    TargetParserModel
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base_parser_models import ParserModel


@dataclass
class TargetParserModel(ParserModel):
    """
    Parser-layer representation of an extracted target.
    """

    ####################################################################
    # BASIC MATCH INFORMATION
    ####################################################################

    found: bool = False

    confidence: float = 0.0

    original: str = ""

    canonical: str = ""

    normalized: str = ""

    ####################################################################
    # ENTITY IDENTITY
    ####################################################################

    entity_id: str = ""

    entity_type: str = "target"

    ontology_name: str = "targets"

    category: str = ""

    business_area: str = ""

    domain: str = ""

    ####################################################################
    # DESCRIPTION
    ####################################################################

    description: str = ""

    ####################################################################
    # BUSINESS BEHAVIOUR
    ####################################################################

    impact_weight: float = 1.0

    business_meaning: str = ""

    preferred_direction: str = ""

    preferred_unit: str = ""

    higher_is_better: bool = True

    ####################################################################
    # TARGET-SPECIFIC BUSINESS OBJECT
    ####################################################################

    object_family: str = ""

    object_group: str = ""

    tangible: bool = False

    intangible: bool = False

    measurable: bool = False

    critical: bool = False

    ####################################################################
    # CLASSIFICATION
    ####################################################################

    lifecycle: str = ""

    ownership: str = ""

    parent_object: str = ""

    ####################################################################
    # PARSING
    ####################################################################

    role: str = ""

    ####################################################################
    # MATCH INFORMATION
    ####################################################################

    matched_phrase: str = ""

    matched_alias: bool = False

    ####################################################################
    # POSITION INFORMATION
    ####################################################################

    start_char: int = -1

    end_char: int = -1

    token_index: int = -1

    token_count: int = 0

    sentence_index: int = 0

    ####################################################################
    # GRAPH
    ####################################################################

    graph_node: bool = True

    ####################################################################
    # SOURCE
    ####################################################################

    source: str = ""

    ####################################################################
    # RAW METADATA
    ####################################################################

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    ####################################################################
    # CONVENIENCE
    ####################################################################

    @property
    def is_found(self) -> bool:

        return self.found

    @property
    def is_alias_match(self) -> bool:

        return self.matched_alias