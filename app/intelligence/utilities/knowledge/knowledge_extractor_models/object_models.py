from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class ObjectKnowledge(KnowledgeEntity):

    ####################################################################
    # Entity
    ####################################################################

    entity_type: str = "object"

    ontology_name: str = "objects"

    ####################################################################
    # Business Object
    ####################################################################

    object_family: str = ""

    object_group: str = ""

    tangible: bool = False

    intangible: bool = False

    measurable: bool = False

    critical: bool = False

    ####################################################################
    # Classification
    ####################################################################

    lifecycle: str = ""

    ownership: str = ""

    parent_object: str = ""

    ####################################################################
    # Parsing
    ####################################################################

    role: str = ""