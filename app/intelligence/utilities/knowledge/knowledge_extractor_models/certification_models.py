"""
Enterprise Certification Knowledge Model

Represents Certifications extracted from text.

Examples

Lead Auditor ISO 9001
PCQI
CQI IRCA
FSPCA
Lean Six Sigma Black Belt
PMP
AWS Certified Solutions Architect
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class CertificationKnowledge(KnowledgeEntity):

    ####################################################################
    # Entity
    ####################################################################

    entity_type: str = "certification"

    ontology_name: str = "certifications"

    ####################################################################
    # Certification Definition
    ####################################################################

    certification_family: str = ""

    certification_group: str = ""

    issuing_body: str = ""

    abbreviation: str = ""

    version: str = ""

    ####################################################################
    # Classification
    ####################################################################

    professional: bool = False

    regulatory: bool = False

    food_safety: bool = False

    quality_management: bool = False

    project_management: bool = False

    cloud: bool = False

    analytics: bool = False

    ####################################################################
    # Validity
    ####################################################################

    renewable: bool = False

    validity_years: int = 0

    examination_required: bool = False

    ####################################################################
    # Enterprise
    ####################################################################

    globally_recognized: bool = False

    maturity_level: int = 1

    ####################################################################
    # Knowledge Graph
    ####################################################################

    graph_node: bool = True

    ats_weight: float = 1.0