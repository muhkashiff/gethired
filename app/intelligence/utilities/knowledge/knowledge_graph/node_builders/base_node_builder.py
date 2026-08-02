"""
Enterprise Base Node Builder

Every Node Builder inherits from this class.

Responsibilities

• Create graph nodes
• Register graph nodes
• Prevent duplicate code

Enterprise V6
"""

from abc import ABC, abstractmethod

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphNode,
)


class BaseNodeBuilder(ABC):

    """
    Base class for every node builder.
    """

    # -------------------------------------------------------------

    @abstractmethod
    def build(self, graph, fact):
        """
        Build graph nodes from one fact.
        """
        raise NotImplementedError

    # -------------------------------------------------------------

    def create_node(
        self,
        entity,
        entity_type: str,
    ) -> GraphNode:

        return GraphNode(

            node_id=entity.entity_id,

            entity_id=entity.entity_id,

            entity_type=entity_type,

            ontology_name=getattr(entity, "ontology_name", ""),

            label=getattr(entity, "canonical", ""),

            canonical=getattr(entity, "canonical", ""),

            category=getattr(entity, "category", ""),

            domain=getattr(entity, "domain", ""),

            business_area=getattr(entity, "business_area", ""),

            impact_weight=getattr(entity, "impact_weight", 1.0),

            metadata=getattr(entity, "metadata", {}),

        )

    # -------------------------------------------------------------

    def register_node(
        self,
        graph,
        node,
    ):

        graph.add_node(node)