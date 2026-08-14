"""
Enterprise Domain Parser Model

Enterprise V5

Parser-layer representation of a domain extracted from text.

Architecture
------------

Sentence
    ↓
ExtractionRequest
    ↓
GenericOntologyParserExtractor
    ↓
KnowledgeV5Pipeline
    ↓
MatchResult[]
    ↓
DomainParserModel[]
    ↓
ExtractionResult[DomainParserModel]

Important
---------
This is a PARSER layer model.

It is intentionally independent from DomainKnowledge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base_parser_models import ParserModel
@dataclass
class DomainParserModel(ParserModel):
    """
    Represents one domain extracted from a sentence.
    """

    # ================================================================
    # DETECTION
    # ================================================================

    found: bool = False

    confidence: float = 0.0

    original: str = ""

    canonical: str = ""

    normalized: str = ""

    # ================================================================
    # ENTITY IDENTITY
    # ================================================================

    entity_id: str = ""

    entity_type: str = "domain"

    ontology_name: str = "domains"

    category: str = ""

    business_area: str = ""

    domain: str = ""

    description: str = ""

    impact_weight: float = 1.0

    # ================================================================
    # DOMAIN DEFINITION
    # ================================================================

    domain_family: str = ""

    parent_domain: str = ""

    business_function: str = ""

    # ================================================================
    # CLASSIFICATION
    # ================================================================

    strategic: bool = False

    operational: bool = False

    technical: bool = False

    compliance: bool = False

    management: bool = False

    # ================================================================
    # ENTERPRISE
    # ================================================================

    enterprise_level: int = 1

    criticality: float = 1.0

    # ================================================================
    # MATCH INFORMATION
    # ================================================================

    matched_phrase: str = ""

    matched_alias: bool = False

    # ================================================================
    # POSITION INFORMATION
    # ================================================================

    start_char: int = -1

    end_char: int = -1

    token_index: int = -1

    token_count: int = 0

    sentence_index: int = 0

    # ================================================================
    # KNOWLEDGE GRAPH
    # ================================================================

    graph_node: bool = True

    # ================================================================
    # PARSER SOURCE
    # ================================================================

    source: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # ================================================================
    # CONVENIENCE
    # ================================================================

    @property
    def is_found(self) -> bool:
        return self.found

    @property
    def is_alias_match(self) -> bool:
        return self.matched_alias

    # ================================================================
    # REPRESENTATION
    # ================================================================

    def __repr__(self) -> str:

        return (
            "DomainParserModel("
            f"found={self.found!r}, "
            f"confidence={self.confidence!r}, "
            f"original={self.original!r}, "
            f"canonical={self.canonical!r}, "
            f"normalized={self.normalized!r}, "
            f"entity_id={self.entity_id!r}, "
            f"entity_type={self.entity_type!r}, "
            f"ontology_name={self.ontology_name!r}, "
            f"category={self.category!r}, "
            f"business_area={self.business_area!r}, "
            f"domain={self.domain!r}, "
            f"impact_weight={self.impact_weight!r}"
            ")"
        )