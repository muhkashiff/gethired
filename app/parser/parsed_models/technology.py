"""
Enterprise Technology Parser Model

Enterprise V5

Parser-layer model for Technology extraction.

Knowledge layer:
    Technology

Parser layer:
    TechnologyParserModel
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base_parser_models import ParserModel


@dataclass
class TechnologyParserModel(ParserModel):
    """
    Parser-layer representation of an extracted technology.
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

    # Enterprise V5 repository architecture intentionally uses
    # ontology_name[:-1] for plural ontologies.
    #
    # technologies -> technologie
    entity_type: str = "technologie"

    ontology_name: str = "technologies"

    category: str = ""

    business_area: str = ""

    domain: str = ""

    description: str = ""

    ####################################################################
    # TECHNOLOGY DEFINITION
    ####################################################################

    technology_family: str = ""

    technology_group: str = ""

    vendor: str = ""

    version: str = ""

    abbreviation: str = ""

    ####################################################################
    # TECHNOLOGY CLASSIFICATION
    ####################################################################

    programming_language: bool = False

    database: bool = False

    analytics_tool: bool = False

    cloud_platform: bool = False

    operating_system: bool = False

    framework: bool = False

    erp: bool = False

    visualization_tool: bool = False

    ####################################################################
    # ENTERPRISE
    ####################################################################

    commercial: bool = False

    open_source: bool = False

    certification_available: bool = False

    maturity_level: int = 1

    ####################################################################
    # BUSINESS
    ####################################################################

    impact_weight: float = 0.95
    ####################################################################
    # GRAPH
    ####################################################################

    graph_node: bool = True

    ####################################################################
    # SOURCE
    ####################################################################

    source: str = ""

    ####################################################################
    # METADATA
    ####################################################################

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

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
    # ATS
    ####################################################################

    ats_weight: float = 1.0

    ####################################################################
    # CONVENIENCE
    ####################################################################

    @property
    def is_found(self) -> bool:
        return self.found

    @property
    def is_alias_match(self) -> bool:
        return self.matched_alias