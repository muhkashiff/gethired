"""
Enterprise Intent Models

Enterprise Intent Context
Enterprise Intent Result

IntentResult now inherits from KnowledgeEntity
so it can participate in the Knowledge Graph.

Enterprise V5
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.knowledge_extractor_models.base_models import (
    KnowledgeEntity,
)


# ==========================================================
# INTENT CONTEXT
# ==========================================================

@dataclass
class IntentContext:

    ####################################################################
    # Action
    ####################################################################

    action: str = ""

    action_category: str = ""

    ####################################################################
    # Entity Lists
    ####################################################################

    objects: list = field(default_factory=list)

    standards: list = field(default_factory=list)

    methodologies: list = field(default_factory=list)

    metrics: list = field(default_factory=list)

    measurements: list = field(default_factory=list)

    domains: list = field(default_factory=list)

    skills: list = field(default_factory=list)

    technologies: list = field(default_factory=list)

    certifications: list = field(default_factory=list)

    ####################################################################
    # Entity Counts
    ####################################################################

    object_count: int = 0

    standard_count: int = 0

    methodology_count: int = 0

    metric_count: int = 0

    measurement_count: int = 0

    domain_count: int = 0

    skill_count: int = 0

    technology_count: int = 0

    certification_count: int = 0

    ####################################################################
    # Business
    ####################################################################

    primary_domain: str = ""

    business_area: str = ""


# ==========================================================
# INTENT RESULT
# ==========================================================

@dataclass
class IntentResult(KnowledgeEntity):

    ####################################################################
    # Entity
    ####################################################################

    entity_type: str = "intent"

    ontology_name: str = "intents"

    ####################################################################
    # Intent
    ####################################################################

    intent: str = ""

    semantic_type: str = ""

    achievement: bool = False

    ####################################################################
    # Business Context
    ####################################################################

    primary_domain: str = ""

    business_area: str = ""

    ####################################################################
    # Explainability
    ####################################################################

    matched_rule: str = ""

    reasoning: str = ""

    trigger_entities: list = field(default_factory=list)

    ####################################################################
    # Metadata
    ####################################################################

    metadata: dict = field(default_factory=dict)