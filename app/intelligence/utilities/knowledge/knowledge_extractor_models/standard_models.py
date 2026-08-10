"""
Enterprise Standard Knowledge Model
Enterprise V5
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class StandardKnowledge(KnowledgeEntity):

    entity_type: str = "standard"

    ontology_name: str = "standards"

    graph_node: bool = True