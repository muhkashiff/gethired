"""
Enterprise Base Graph Builder

All Graph Builders inherit from this class.

Examples

ActionBuilder
MetricBuilder
SkillBuilder
DomainBuilder
StandardBuilder
MeasurementBuilder

Enterprise V5
"""

from abc import ABC, abstractmethod

from app.intelligence.utilities.knowledge.knowledge_graph.utilities.graph_id_generator import (
    GraphIDGenerator,
)

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphNode,
    GraphEdge,
)


class BaseBuilder(ABC):
    """
    Base class for every Graph Builder.

    Provides common functionality:

    • Create Nodes
    • Create Edges
    • Avoid duplicates
    • ID generation
    """

    def __init__(self):

        self.id_generator = GraphIDGenerator()

    # =====================================================
    # Public Interface
    # =====================================================

    @abstractmethod
    def build(self, graph, fact):
        """
        Implement inside every builder.

        Parameters

            graph : KnowledgeGraph

            fact : KnowledgeFact

        Returns

            list[GraphNode]
        """
        raise NotImplementedError

    # =====================================================
    # Node Factory
    # =====================================================

    def create_node(
        self,
        entity,
        entity_type,
    ):

        node = GraphNode()

        node.node_id = self.id_generator.node_id(
            entity_type,
            entity.entity_id,
        )

        node.entity_id = entity.entity_id

        node.entity_type = entity_type

        node.ontology_name = getattr(
            entity,
            "ontology_name",
            "",
        )

        node.label = getattr(
            entity,
            "canonical",
            "",
        )

        node.canonical = getattr(
            entity,
            "canonical",
            "",
        )

        node.category = getattr(
            entity,
            "category",
            "",
        )

        node.domain = getattr(
            entity,
            "domain",
            "",
        )

        node.business_area = getattr(
            entity,
            "business_area",
            "",
        )

        node.impact_weight = getattr(
            entity,
            "impact_weight",
            1.0,
        )

        node.metadata = getattr(
            entity,
            "metadata",
            {},
        ).copy()

        return node

    # =====================================================
    # Edge Factory
    # =====================================================

    def create_edge(
        self,
        source,
        relation,
        target,
        confidence=1.0,
    ):

        edge = GraphEdge()

        edge.edge_id = self.id_generator.edge_id(
            source.node_id,
            relation,
            target.node_id,
        )

        edge.relation = relation

        edge.confidence = confidence

        edge.source_id = source.node_id

        edge.source_type = source.entity_type

        edge.target_id = target.node_id

        edge.target_type = target.entity_type

        return edge

    # =====================================================
    # Register Node
    # =====================================================

    def register_node(
        self,
        graph,
        node,
    ):
        """
        Adds node if it does not already exist.
        """

        existing = graph.get_node(node.node_id)

        if existing is not None:

            return existing

        graph.add_node(node)

        return node

    # =====================================================
    # Register Edge
    # =====================================================

    def register_edge(
        self,
        graph,
        edge,
    ):
        """
        Avoid duplicate edges.
        """

        for existing in graph.edges:

            if existing.edge_id == edge.edge_id:

                return existing

        graph.add_edge(edge)

        return edge