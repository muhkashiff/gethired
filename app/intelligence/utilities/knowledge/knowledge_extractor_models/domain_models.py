from dataclasses import dataclass, field

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

    ####################################################################
    # Domain Object
    ####################################################################

    domain_object: object | None = None

    ####################################################################
    # Domain Reasoning
    ####################################################################

    reasoning_id: str = ""

    reasoning_object: object | None = None

    reasoning_confidence: float = 0.0

    ####################################################################
    # Reasoning Relationships
    ####################################################################

    primary_domain: str = ""

    secondary_domains: list[str] = field(
        default_factory=list
    )

    trigger_actions: list[str] = field(
        default_factory=list
    )

    trigger_objects: list[str] = field(
        default_factory=list
    )

    trigger_skills: list[str] = field(
        default_factory=list
    )

    trigger_metrics: list[str] = field(
        default_factory=list
    )

    trigger_certifications: list[str] = field(
        default_factory=list
    )