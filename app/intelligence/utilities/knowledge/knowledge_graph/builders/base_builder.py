"""
Enterprise Base Graph Builder

Every Graph Builder inherits from this class.

Enterprise V8

Responsibilities
----------------

• Create Nodes

• Create Edges

• Register Nodes

• Register Edges

• Duplicate Prevention

• ID Generation

Concrete builders only implement business logic.
"""

from abc import ABC, abstractmethod

from app.intelligence.utilities.knowledge.knowledge_graph.utilities.graph_id_generator import (
    GraphIDGenerator,
)

from app.intelligence.utilities.knowledge.knowledge_graph.build_context import (
    BuildContext,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.business_statement_builder import (
    BusinessStatement,
)

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphNode,
    GraphEdge,
)


class BaseBuilder(ABC):

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.id_generator = GraphIDGenerator()

    ####################################################################
    # ABSTRACT BUILD
    ####################################################################

    @abstractmethod
    def build(

        self,

        context: BuildContext,

        statement: BusinessStatement,

    ):
        """
        Build graph objects from one BusinessStatement.
        """
        raise NotImplementedError

    ####################################################################
    # NODE FACTORY
    ####################################################################

    def create_node(

        self,

        entity,

        entity_type,

    ) -> GraphNode:

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

    ####################################################################
    # EDGE FACTORY
    ####################################################################

    def create_edge(

        self,

        source,

        relation,

        target,

        confidence=1.0,

    ) -> GraphEdge:

        edge = GraphEdge()

        edge.edge_id = self.id_generator.edge_id(

            source.node_id,

            relation,

            target.node_id,

        )

        edge.source_id = source.node_id

        edge.target_id = target.node_id

        edge.source_type = source.entity_type

        edge.target_type = target.entity_type

        edge.relation = relation

        edge.confidence = confidence

        return edge

    ####################################################################
    # REGISTER NODE
    ####################################################################

    def register_node(

        self,

        context: BuildContext,

        node: GraphNode,

    ) -> GraphNode:

        existing = context.graph.get_node(

            node.node_id,

        )

        if existing is not None:

            return existing

        context.graph.add_node(

            node,

        )

        return node

    ####################################################################
    # REGISTER EDGE
    ####################################################################

    def register_edge(

        self,

        context: BuildContext,

        edge: GraphEdge,

    ) -> GraphEdge:

        for existing in context.graph.edges:

            if existing.edge_id == edge.edge_id:

                return existing

        context.graph.add_edge(

            edge,

        )

        return edge

    ####################################################################
    # HELPER
    ####################################################################

    def exists(

        self,

        context: BuildContext,

        node_id,

    ):

        return context.graph.get_node(

            node_id,

        ) is not None