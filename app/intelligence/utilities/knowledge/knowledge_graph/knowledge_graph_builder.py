"""
Enterprise Knowledge Graph Builder

Builds the Enterprise Knowledge Graph directly from
Business Statements.

Pipeline

Semantic Resolution
        ↓
Business Statements
        ↓
Entities
        ↓
Relations
        ↓
Knowledge Graph

Enterprise V7
"""

import uuid

from app.intelligence.utilities.knowledge.knowledge_graph.knowledge_graph import (
    KnowledgeGraph,
)

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphNode,
    GraphEdge,
)

from app.intelligence.utilities.knowledge.knowledge_graph.knowledge_graph_build_result import (
    KnowledgeGraphBuildResult,
)


class KnowledgeGraphBuilder:

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(self):

        self.graph = None

    ####################################################################
    # Public Build API
    ####################################################################

    def build(self, semantic_resolution):

        """
        Build complete enterprise graph.

        Input
        -----
        SemanticResolution

        Output
        ------
        KnowledgeGraphBuildResult
        """

        self.graph = KnowledgeGraph()

        # ----------------------------------------------------------
        # Build every Business Statement
        # ----------------------------------------------------------

        for statement in semantic_resolution.business_statements:

            self._add_statement(statement)

        # ----------------------------------------------------------
        # Return wrapper
        # ----------------------------------------------------------

        result = KnowledgeGraphBuildResult(

            graph=self.graph,

        )

        return result

    ####################################################################
    # Add One Business Statement
    ####################################################################

    def _add_statement(self, statement):

        """
        Adds every entity and every semantic relation
        belonging to a Business Statement.
        """

        self._add_entities(statement)

        self._add_relations(statement)

        ####################################################################
    # Add Entities
    ####################################################################

    def _add_entities(self, statement):

        """
        Every SemanticEntity becomes exactly ONE GraphNode.

        The KnowledgeGraph itself prevents duplicates.
        """

        for entity in statement.entities:

            node = self._entity_to_node(entity)

            self.graph.add_node(node)

    ####################################################################
    # SemanticEntity -> GraphNode
    ####################################################################

    def _entity_to_node(self, entity):

        """
        Converts SemanticEntity into GraphNode.

        GraphNode contains only graph information.

        Semantic information remains inside SemanticEntity.
        """

        metadata = {}

        if entity.metadata:

            metadata = entity.metadata.copy()

        return GraphNode(

            # -------------------------------------------------
            # Identity
            # -------------------------------------------------

            node_id=entity.entity_id,

            entity_id=entity.entity_id,

            entity_type=entity.entity_type,

            ontology_name=entity.entity_type,

            # -------------------------------------------------
            # Display
            # -------------------------------------------------

            label=entity.canonical,

            canonical=entity.canonical,

            category=entity.category,

            # -------------------------------------------------
            # Business
            # -------------------------------------------------

            domain=metadata.get(
                "primary_domain",
                "",
            ),

            business_area=entity.business_area,

            impact_weight=1.0,

            # -------------------------------------------------
            # Metadata
            # -------------------------------------------------

            metadata=metadata,

        )

    ####################################################################
    # Add Relations
    ####################################################################

    def _add_relations(self, statement):

        """
        Every StatementRelation becomes exactly ONE GraphEdge.

        Relations are now the SINGLE SOURCE OF TRUTH.

        We no longer build edges from DependencyResolver.
        """

        for relation in statement.relations:

            source = statement.entity(
                relation.source_id
            )

            target = statement.entity(
                relation.target_id
            )

            if source is None:
                continue

            if target is None:
                continue

            edge = self._relation_to_edge(

                relation,

                source,

                target,

            )

            self.graph.add_edge(edge)

        ####################################################################
    # StatementRelation -> GraphEdge
    ####################################################################

    def _relation_to_edge(

        self,

        relation,

        source,

        target,

    ):

        """
        Converts a StatementRelation into a GraphEdge.
        """

        metadata = {}

        if relation.metadata:

            metadata = relation.metadata.copy()

        return GraphEdge(

            # -------------------------------------------------
            # Identity
            # -------------------------------------------------

            edge_id=uuid.uuid4().hex,

            relation=relation.relation_type,

            confidence=relation.confidence,

            # -------------------------------------------------
            # Source
            # -------------------------------------------------

            source_id=relation.source_id,

            source_type=source.entity_type,

            # -------------------------------------------------
            # Target
            # -------------------------------------------------

            target_id=relation.target_id,

            target_type=target.entity_type,

            # -------------------------------------------------
            # Explainability
            # -------------------------------------------------

            reasoning=relation.reasoning,

            # -------------------------------------------------
            # Metadata
            # -------------------------------------------------

            metadata=metadata,

        )

    ####################################################################
    # Convenience API
    ####################################################################

    @property
    def node_count(self):

        if self.graph is None:

            return 0

        return len(self.graph.nodes)

    ####################################################################

    @property
    def edge_count(self):

        if self.graph is None:

            return 0

        return len(self.graph.edges)

    ####################################################################

    def summary(self):

        if self.graph is None:

            return {}

        return self.graph.summary()

    ####################################################################

    def reset(self):

        """
        Clears internal graph.
        """

        self.graph = None


    def get_node(self, node_id):

        return self.nodes.get(node_id)


    def get_nodes(self):

        return list(self.nodes.values())


    def get_edges(self):

        return list(self.edges.values())