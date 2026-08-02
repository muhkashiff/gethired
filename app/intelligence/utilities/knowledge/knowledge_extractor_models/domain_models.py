"""
Enterprise Domain Knowledge Model

Represents business domains extracted from text.

Examples

Food Safety
Quality Management
Operations
Supply Chain
Manufacturing
Retail
Continuous Improvement
Business Analytics
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class DomainKnowledge(KnowledgeEntity):

    ####################################################################
    # Entity
    ####################################################################

    entity_type: str = "domain"

    ontology_name: str = "domains"

    ####################################################################
    # Domain Definition
    ####################################################################

    domain_family: str = ""

    parent_domain: str = ""

    business_function: str = ""

    ####################################################################
    # Classification
    ####################################################################

    strategic: bool = False

    operational: bool = False

    technical: bool = False

    compliance: bool = False

    management: bool = False

    ####################################################################
    # Enterprise
    ####################################################################

    enterprise_level: int = 1

    criticality: float = 1.0

    ####################################################################
    # Knowledge Graph
    ####################################################################

    graph_node: bool = True