"""
Enterprise Methodology Knowledge Model

Represents methodologies extracted from text.

Examples

HACCP
DMAIC
PDCA
Lean Manufacturing
Six Sigma
5S
Root Cause Analysis
Kaizen
FMEA
SPC
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class MethodologyKnowledge(KnowledgeEntity):

    ####################################################################
    # Entity
    ####################################################################

    entity_type: str = "methodology"

    ontology_name: str = "methodologies"

    ####################################################################
    # Methodology Definition
    ####################################################################

    methodology_family: str = ""

    methodology_group: str = ""

    version: str = ""

    abbreviation: str = ""

    ####################################################################
    # Classification
    ####################################################################

    continuous_improvement: bool = False

    quality_management: bool = False

    food_safety: bool = False

    risk_management: bool = False

    analytical: bool = False

    problem_solving: bool = False

    statistical: bool = False

    ####################################################################
    # Enterprise
    ####################################################################

    certification_related: bool = False

    implementation_required: bool = False

    maturity_level: int = 1

    ####################################################################
    # Knowledge Graph
    ####################################################################

    graph_node: bool = True

    ats_weight: float = 1.0