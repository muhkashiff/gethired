"""
Enterprise Standard Knowledge Model
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class StandardKnowledge(KnowledgeEntity):

    ####################################################################
    # Core
    ####################################################################

    entity_type: str = "standard"

    ontology_name: str = "standards"

    ####################################################################
    # Standard Information
    ####################################################################

    category: str = ""

    business_area: str = ""

    ####################################################################
    # Parsing
    ####################################################################

    graph_node: bool = True