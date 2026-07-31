"""
Knowledge Graph Builder V2

Enterprise Knowledge Graph Builder

Pipeline

KnowledgeDocument
        +
SemanticResolution
        ↓
Business Statements
        ↓
Knowledge Graph
"""

import uuid

from app.intelligence.utilities.knowledge.knowledge_graph.graph_document import (
    KnowledgeGraphDocument,
)

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphNode,
    GraphEdge,
)


class KnowledgeGraphBuilder:

    def __init__(self):
        pass

    # ==========================================================
    # BUILD GRAPH
    # ==========================================================

    def build(
        self,
        knowledge_document,
        semantic_result,
    ):

        graph_document = KnowledgeGraphDocument()

        graph_document.knowledge_document = knowledge_document

        graph = graph_document.graph

        node_lookup = {}

        # ======================================================
        # BUSINESS STATEMENT NODES
        # ======================================================

        for statement in semantic_result.business_statements:

            statement_node = GraphNode(

                node_id=statement.statement_id,

                entity_id=statement.statement_id,

                node_type="BusinessStatement",

                label=statement.label,

                canonical=statement.label,

                category="Business Statement",

                business_area=(
                    statement.intent.business_area
                    if statement.intent
                    else ""
                ),

                confidence=statement.confidence,

                metadata={

                    "intent": (
                        statement.intent.intent
                        if statement.intent
                        else ""
                    ),

                    "primary_domain": (
                        statement.intent.primary_domain
                        if statement.intent
                        else ""
                    ),

                    "semantic_type": (
                        statement.intent.semantic_type
                        if statement.intent
                        else ""
                    ),

                    "achievement": (
                        statement.intent.achievement
                        if statement.intent
                        else False
                    ),

                },

            )

            graph.add_node(statement_node)

            node_lookup[statement.statement_id] = statement_node

            # --------------------------------------------------
            # Action
            # --------------------------------------------------

            self._connect_entity(
                graph,
                node_lookup,
                statement_node,
                statement.action,
                "HAS_ACTION",
            )

            # --------------------------------------------------
            # Targets
            # --------------------------------------------------

            for entity in statement.targets:

                self._connect_entity(
                    graph,
                    node_lookup,
                    statement_node,
                    entity,
                    "HAS_TARGET",
                )

            # --------------------------------------------------
            # Standards
            # --------------------------------------------------

            for entity in statement.standards:

                self._connect_entity(
                    graph,
                    node_lookup,
                    statement_node,
                    entity,
                    "COMPLIES_WITH",
                )

            # --------------------------------------------------
            # Methods
            # --------------------------------------------------

            for entity in statement.methods:

                self._connect_entity(
                    graph,
                    node_lookup,
                    statement_node,
                    entity,
                    "USES_METHOD",
                )

            # --------------------------------------------------
            # Skills
            # --------------------------------------------------

            for entity in statement.skills:

                self._connect_entity(
                    graph,
                    node_lookup,
                    statement_node,
                    entity,
                    "REQUIRES_SKILL",
                )

            # --------------------------------------------------
            # Metrics
            # --------------------------------------------------

            for entity in statement.metrics:

                self._connect_entity(
                    graph,
                    node_lookup,
                    statement_node,
                    entity,
                    "AFFECTS_METRIC",
                )

            # --------------------------------------------------
            # Domains
            # --------------------------------------------------

            for entity in statement.domains:

                self._connect_entity(
                    graph,
                    node_lookup,
                    statement_node,
                    entity,
                    "BELONGS_TO",
                )

        # ======================================================
        # DOCUMENT METADATA
        # ======================================================

        graph.confidence = semantic_result.confidence

        graph.metadata = {

            "primary_domain":
                semantic_result.metadata.primary_domain,

            "business_area":
                semantic_result.metadata.primary_business_area,

            "semantic_type":
                semantic_result.metadata.semantic_type,

            "achievement":
                semantic_result.metadata.achievement,

        }

        graph_document.confidence = semantic_result.confidence

        graph_document.statistics = {

            "nodes": graph.node_count,

            "edges": graph.edge_count,

            "business_statements":
                len(semantic_result.business_statements),

        }

        graph_document.metadata = graph.metadata

        return graph_document

        # =========================================================
    # Connect Business Statement → Entity
    # =========================================================

    def _connect_entity(
        self,
        graph,
        node_lookup,
        statement_node,
        entity,
        relationship,
    ):

        if entity is None:
            return

        # --------------------------------------------------
        # Create Entity Node only once
        # --------------------------------------------------

        if entity.entity_id not in node_lookup:

            entity_node = GraphNode(

                node_id=entity.entity_id,

                entity_id=entity.entity_id,

                node_type=entity.entity_type,

                label=entity.original or entity.canonical,

                canonical=entity.canonical,

                category=entity.category,

                business_area=entity.business_area,

                confidence=entity.confidence,

                impact_weight=getattr(
                    entity,
                    "impact_weight",
                    1.0,
                ),

                metadata=entity.metadata,

            )

            graph.add_node(entity_node)

            node_lookup[entity.entity_id] = entity_node

        else:

            entity_node = node_lookup[entity.entity_id]

        # --------------------------------------------------
        # Create Graph Edge
        # --------------------------------------------------

        edge = GraphEdge(

            edge_id=(
                f"{statement_node.node_id}"
                f"_{relationship}"
                f"_{entity.entity_id}"
            ),

            source_node=statement_node.node_id,

            target_node=entity.entity_id,

            relationship=relationship,

            relationship_label=relationship.replace(
                "_",
                " "
            ).title(),

            confidence=entity.confidence,

        )

        graph.add_edge(edge)

        # --------------------------------------------------
        # Maintain node connectivity
        # --------------------------------------------------

        statement_node.add_edge(edge)

        entity_node.add_edge(edge)