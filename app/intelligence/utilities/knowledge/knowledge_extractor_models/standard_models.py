"""
Enterprise Standard Knowledge Model

Represents Standards extracted from text.

Examples

ISO 9001
ISO 22000
FSSC 22000
BRCGS
HACCP
GMP
SQF
IFS
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class StandardKnowledge(KnowledgeEntity):

    ####################################################################
    # Entity
    ####################################################################

    entity_type: str = "standard"

    ontology_name: str = "standards"

    ####################################################################
    # Standard Definition
    ####################################################################

    standard_family: str = ""

    standard_group: str = ""

    version: str = ""

    abbreviation: str = ""

    issuing_body: str = ""

    ####################################################################
    # Classification
    ####################################################################

    food_safety: bool = False

    quality_management: bool = False

    environmental: bool = False

    occupational_health: bool = False

    information_security: bool = False

    compliance_standard: bool = False

    management_system: bool = False

    ####################################################################
    # Certification
    ####################################################################

    certifiable: bool = True

    audit_required: bool = True

    surveillance_required: bool = False

    ####################################################################
    # Enterprise
    ####################################################################

    maturity_level: int = 1

    global_standard: bool = False

    regulatory: bool = False

    ####################################################################
    # Knowledge Graph
    ####################################################################

    graph_node: bool = True

    ats_weight: float = 1.0