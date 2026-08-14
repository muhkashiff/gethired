"""
Enterprise Methodology Parser Model

Enterprise V5

Parser-layer model for Methodology extraction.

Knowledge layer:
    MethodologyKnowledge

Parser layer:
    MethodologyParserModel
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .base_parser_models import ParserModel


@dataclass
class MethodologyParserModel(ParserModel):
    """
    Parser-layer representation of an extracted methodology.
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

    entity_type: str = "methodology"

    ontology_name: str = "methodologies"

    category: str = ""

    business_area: str = ""

    domain: str = ""

    ####################################################################
    # DESCRIPTION
    ####################################################################

    description: str = ""

    ####################################################################
    # METHODOLOGY DEFINITION
    ####################################################################

    methodology_family: str = ""

    methodology_group: str = ""

    version: str = ""

    abbreviation: str = ""

    ####################################################################
    # CLASSIFICATION
    ####################################################################

    continuous_improvement: bool = False

    quality_management: bool = False

    food_safety: bool = False

    risk_management: bool = False

    analytical: bool = False

    problem_solving: bool = False

    statistical: bool = False

    ####################################################################
    # ENTERPRISE
    ####################################################################

    certification_related: bool = False

    implementation_required: bool = False

    maturity_level: int = 1

    ####################################################################
    # BUSINESS IMPACT
    ####################################################################

    impact_weight: float = 0.0

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
    # KNOWLEDGE GRAPH
    ####################################################################

    graph_node: bool = True

    ####################################################################
    # ATS
    ####################################################################

    ats_weight: float = 1.0

    ####################################################################
    # SOURCE
    ####################################################################

    source: str = ""

    ####################################################################
    # RAW METADATA
    ####################################################################

    metadata: dict[str, Any] = None

    ####################################################################
    # CONVENIENCE
    ####################################################################

    @property
    def is_found(self) -> bool:

        return self.found

    @property
    def is_alias_match(self) -> bool:

        return self.matched_alias

    ####################################################################
    # POST INITIALIZATION
    ####################################################################

    def __post_init__(self) -> None:

        if self.metadata is None:

            self.metadata = {}