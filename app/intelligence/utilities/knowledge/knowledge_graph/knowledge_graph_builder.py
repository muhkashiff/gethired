"""
Enterprise Knowledge Graph Builder

Enterprise V12

Builds the Enterprise Knowledge Graph directly from
Business Statements.

Pipeline

Semantic Resolution
        ↓
Business Statements
        ↓
Entities
        ↓
Statement Relations
        ↓
Knowledge Graph

Responsibilities
----------------
• Convert SemanticEntity → GraphNode
• Convert StatementRelation → GraphEdge
• Preserve KPI / BKPI distinction
• Preserve entity metadata
• Preserve relation confidence
• Preserve relation reasoning
• Prevent invalid graph references
• Keep graph construction independent from semantic resolution

Architecture

DependencyResolver
        ↓
SemanticRelationExtractor
        ↓
BusinessStatementBuilder
        ↓
KnowledgeGraphBuilder
        ↓
KnowledgeGraph
"""

from __future__ import annotations

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
    """
    Builds a KnowledgeGraph from BusinessStatement objects.

    The builder does NOT resolve semantic dependencies.

    Its only responsibility is:

        BusinessStatement
                ↓
        GraphNode + GraphEdge
                ↓
        KnowledgeGraph
    """

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self) -> None:

        self.graph: KnowledgeGraph | None = None

    # ==========================================================
    # PUBLIC BUILD API
    # ==========================================================

    def build(self, semantic_resolution) -> KnowledgeGraphBuildResult:
        """
        Build the complete enterprise knowledge graph.

        Parameters
        ----------
        semantic_resolution:
            Object containing BusinessStatement objects.

        Returns
        -------
        KnowledgeGraphBuildResult
        """

        self.graph = KnowledgeGraph()

        if semantic_resolution is None:

            return KnowledgeGraphBuildResult(
                graph=self.graph,
            )

        business_statements = getattr(
            semantic_resolution,
            "business_statements",
            [],
        )

        if business_statements is None:

            business_statements = []

        # ------------------------------------------------------
        # Build every BusinessStatement
        # ------------------------------------------------------

        for statement in business_statements:

            if statement is None:
                continue

            self._add_statement(
                statement
            )

        # ------------------------------------------------------
        # Return wrapper
        # ------------------------------------------------------

        return KnowledgeGraphBuildResult(
            graph=self.graph,
        )

    # ==========================================================
    # ADD STATEMENT
    # ==========================================================

    def _add_statement(
        self,
        statement,
    ) -> None:
        """
        Add one BusinessStatement to the graph.
        """

        if self.graph is None:
            return

        self._add_entities(
            statement
        )

        self._add_relations(
            statement
        )

    # ==========================================================
    # ADD ENTITIES
    # ==========================================================

    def _add_entities(
        self,
        statement,
    ) -> None:
        """
        Convert every SemanticEntity into one GraphNode.
        """

        if self.graph is None:
            return

        entities = getattr(
            statement,
            "entities",
            [],
        )

        if entities is None:
            return

        for entity in entities:

            if entity is None:
                continue

            if not getattr(
                entity,
                "entity_id",
                "",
            ):
                continue

            node = self._entity_to_node(
                entity
            )

            self.graph.add_node(
                node
            )

    # ==========================================================
    # SEMANTIC ENTITY → GRAPH NODE
    # ==========================================================

    @staticmethod
    def _entity_to_node(
        entity,
    ) -> GraphNode:
        """
        Convert SemanticEntity into GraphNode.

        Important:
        KPI and BKPI remain separate because
        entity_type is preserved exactly.
        """

        metadata = {}

        entity_metadata = getattr(
            entity,
            "metadata",
            None,
        )

        if entity_metadata:

            metadata = entity_metadata.copy()

        entity_type = (
            getattr(
                entity,
                "entity_type",
                "",
            )
            or ""
        )

        return GraphNode(

            # --------------------------------------------------
            # Identity
            # --------------------------------------------------

            node_id=entity.entity_id,

            entity_id=entity.entity_id,

            entity_type=entity_type,

            ontology_name=(
                getattr(
                    entity,
                    "ontology_name",
                    "",
                )
                or entity_type
            ),

            # --------------------------------------------------
            # Display
            # --------------------------------------------------

            label=(
                getattr(
                    entity,
                    "canonical",
                    "",
                )
                or ""
            ),

            canonical=(
                getattr(
                    entity,
                    "canonical",
                    "",
                )
                or ""
            ),

            category=(
                getattr(
                    entity,
                    "category",
                    "",
                )
                or ""
            ),

            # --------------------------------------------------
            # Business
            # --------------------------------------------------

            domain=metadata.get(
                "primary_domain",
                "",
            ),

            business_area=(
                getattr(
                    entity,
                    "business_area",
                    "",
                )
                or ""
            ),

            impact_weight=(
                getattr(
                    entity,
                    "impact_weight",
                    1.0,
                )
                or 1.0
            ),

            # --------------------------------------------------
            # Metadata
            # --------------------------------------------------

            metadata=metadata,

        )

    # ==========================================================
    # ADD RELATIONS
    # ==========================================================

    def _add_relations(
        self,
        statement,
    ) -> None:
        """
        Convert every StatementRelation into one GraphEdge.
        """

        if self.graph is None:
            return

        relations = getattr(
            statement,
            "relations",
            [],
        )

        if relations is None:
            return

        for relation in relations:

            if relation is None:
                continue

            source_id = getattr(
                relation,
                "source_id",
                "",
            )

            target_id = getattr(
                relation,
                "target_id",
                "",
            )

            if not source_id or not target_id:
                continue

            source = statement.entity(
                source_id
            )

            target = statement.entity(
                target_id
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

            self.graph.add_edge(
                edge
            )

    # ==========================================================
    # STATEMENT RELATION → GRAPH EDGE
    # ==========================================================

    @staticmethod
    def _relation_to_edge(
        relation,
        source,
        target,
    ) -> GraphEdge:
        """
        Convert StatementRelation into GraphEdge.
        """

        metadata = {}

        relation_metadata = getattr(
            relation,
            "metadata",
            None,
        )

        if relation_metadata:

            metadata = relation_metadata.copy()

        return GraphEdge(

            # --------------------------------------------------
            # Identity
            # --------------------------------------------------

            edge_id=uuid.uuid4().hex,

            relation=(
                getattr(
                    relation,
                    "relation_type",
                    "",
                )
                or ""
            ),

            confidence=(
                getattr(
                    relation,
                    "confidence",
                    0.0,
                )
                or 0.0
            ),

            # --------------------------------------------------
            # Source
            # --------------------------------------------------

            source_id=(
                getattr(
                    relation,
                    "source_id",
                    "",
                )
                or ""
            ),

            source_type=(
                getattr(
                    source,
                    "entity_type",
                    "",
                )
                or ""
            ),

            # --------------------------------------------------
            # Target
            # --------------------------------------------------

            target_id=(
                getattr(
                    relation,
                    "target_id",
                    "",
                )
                or ""
            ),

            target_type=(
                getattr(
                    target,
                    "entity_type",
                    "",
                )
                or ""
            ),

            # --------------------------------------------------
            # Explainability
            # --------------------------------------------------

            reasoning=(
                getattr(
                    relation,
                    "reasoning",
                    "",
                )
                or ""
            ),

            # --------------------------------------------------
            # Metadata
            # --------------------------------------------------

            metadata=metadata,

        )

    # ==========================================================
    # GRAPH ACCESS
    # ==========================================================

    @property
    def node_count(self) -> int:
        """
        Number of graph nodes.
        """

        if self.graph is None:
            return 0

        return len(
            self.graph.nodes
        )

    # ==========================================================

    @property
    def edge_count(self) -> int:
        """
        Number of graph edges.
        """

        if self.graph is None:
            return 0

        return len(
            self.graph.edges
        )

    # ==========================================================

    def summary(self) -> dict:
        """
        Return graph summary.
        """

        if self.graph is None:
            return {}

        return self.graph.summary()

    # ==========================================================

    def reset(self) -> None:
        """
        Clear the current graph.
        """

        self.graph = None

    # ==========================================================
    # NODE API
    # ==========================================================

    def get_node(
        self,
        node_id: str,
    ):

        if self.graph is None:
            return None

        return self.graph.get_node(
            node_id
        )

    # ==========================================================

    def get_nodes(self):

        if self.graph is None:
            return []

        return self.graph.get_nodes()

    # ==========================================================
    # EDGE API
    # ==========================================================

    def get_edges(self):

        if self.graph is None:
            return []

        return self.graph.get_edges()