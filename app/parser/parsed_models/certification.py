
"""
Enterprise Certification Parser Model
Enterprise V5

Represents a certification detected by the parser.

Pipeline:

MatchResult
    ↓
CertificationParserExtractor
    ↓
CertificationParserModel

This model represents the parser-level certification result.
It is intentionally separate from CertificationKnowledge.
"""

from __future__ import annotations

from dataclasses import dataclass

from .base_parser_models import ParserModel


@dataclass
class CertificationParserModel(ParserModel):
    """
    Parser-level representation of a certification.
    """

    ####################################################################
    # ENTITY
    ####################################################################

    entity_type: str = "certification"

    ontology_name: str = "certifications"

    ####################################################################
    # CERTIFICATION DEFINITION
    ####################################################################

    certification_family: str = ""

    certification_group: str = ""

    issuing_body: str = ""

    abbreviation: str = ""

    version: str = ""

    ####################################################################
    # CLASSIFICATION
    ####################################################################

    professional: bool = False

    regulatory: bool = False

    food_safety: bool = False

    quality_management: bool = False

    project_management: bool = False

    cloud: bool = False

    analytics: bool = False

    ####################################################################
    # VALIDITY
    ####################################################################

    renewable: bool = False

    validity_years: int = 0

    examination_required: bool = False

    ####################################################################
    # ENTERPRISE
    ####################################################################

    globally_recognized: bool = False

    maturity_level: int = 1

    ####################################################################
    # KNOWLEDGE GRAPH
    ####################################################################

    graph_node: bool = True

    ####################################################################
    # ATS
    ####################################################################

    ats_weight: float = 1.0

