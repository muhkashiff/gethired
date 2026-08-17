"""
Enterprise Knowledge Graph Builder

Enterprise V13

Architecture

KnowledgeDocument
        ↓
KnowledgeFact
        ↓
KnowledgeInterpretation
        ↓
KnowledgeEntity
        ↓
BusinessStatementBuilder
        ↓
KnowledgeGraphBuilder
        ↓
KnowledgeGraph

Responsibilities
----------------
• Consume BusinessStatementBuilder output
• Convert business statements into graph nodes
• Convert statement relations into graph edges
• Preserve entity identity and metadata
• Preserve technologies as technology entities
• Preserve methodologies as methodology entities
• Preserve certifications and standards
• Preserve metrics and measurements
• Preserve achievement relationships
• Prevent duplicate graph nodes
• Prevent duplicate graph edges

This builder does NOT:

• extract entities
• perform ontology matching
• perform semantic resolution
• calculate scores
• predict seniority
• predict career level
• build KnowledgeProfile
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional


# ================================================================
# GRAPH NODE
# ================================================================

@dataclass
class KnowledgeGraphNode:
    """
    One node in the enterprise KnowledgeGraph.
    """

    node_id: str = ""

    entity_id: str = ""

    label: str = ""

    canonical: str = ""

    normalized: str = ""

    entity_type: str = ""

    category: str = ""

    ontology_name: str = ""

    primary_domain: str = ""

    business_area: str = ""

    description: str = ""

    confidence: float = 0.0

    source: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


# ================================================================
# GRAPH EDGE
# ================================================================

@dataclass
class KnowledgeGraphEdge:
    """
    One relationship in the enterprise KnowledgeGraph.
    """

    edge_id: str = ""

    source_id: str = ""

    target_id: str = ""

    relation: str = ""

    confidence: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


# ================================================================
# KNOWLEDGE GRAPH
# ================================================================

class KnowledgeGraph:
    """
    Enterprise knowledge graph.

    Stores:

        nodes
        edges

    and provides deterministic lookup/traversal.
    """

    def __init__(self):

        self.nodes: dict[
            str,
            KnowledgeGraphNode,
        ] = {}

        self.edges: dict[
            str,
            KnowledgeGraphEdge,
        ] = {}

    # ============================================================
    # NODE OPERATIONS
    # ============================================================

    def add_node(
        self,
        node: KnowledgeGraphNode,
    ) -> KnowledgeGraphNode:

        if not node.node_id:

            raise ValueError(
                "KnowledgeGraphNode.node_id cannot be empty."
            )

        existing = self.nodes.get(
            node.node_id
        )

        if existing is not None:

            existing.metadata.update(
                node.metadata
            )

            if node.confidence > existing.confidence:

                existing.confidence = (
                    node.confidence
                )

            return existing

        self.nodes[
            node.node_id
        ] = node

        return node

    # ============================================================

    def get_node(
        self,
        node_id: str,
    ) -> Optional[KnowledgeGraphNode]:

        return self.nodes.get(
            node_id
        )

    # ============================================================

    def get_nodes(
        self,
    ) -> list[KnowledgeGraphNode]:

        return list(
            self.nodes.values()
        )

    # ============================================================
    # EDGE OPERATIONS
    # ============================================================

    def add_edge(
        self,
        edge: KnowledgeGraphEdge,
    ) -> KnowledgeGraphEdge:

        if not edge.edge_id:

            raise ValueError(
                "KnowledgeGraphEdge.edge_id cannot be empty."
            )

        if edge.source_id not in self.nodes:

            raise ValueError(
                f"Source node does not exist: "
                f"{edge.source_id}"
            )

        if edge.target_id not in self.nodes:

            raise ValueError(
                f"Target node does not exist: "
                f"{edge.target_id}"
            )

        existing = self.edges.get(
            edge.edge_id
        )

        if existing is not None:

            existing.metadata.update(
                edge.metadata
            )

            if edge.confidence > existing.confidence:

                existing.confidence = (
                    edge.confidence
                )

            return existing

        self.edges[
            edge.edge_id
        ] = edge

        return edge

    # ============================================================

    def get_edge(
        self,
        edge_id: str,
    ) -> Optional[KnowledgeGraphEdge]:

        return self.edges.get(
            edge_id
        )

    # ============================================================

    def get_edges(
        self,
    ) -> list[KnowledgeGraphEdge]:

        return list(
            self.edges.values()
        )

    # ============================================================
    # TYPE FILTER
    # ============================================================

    def find_by_type(
        self,
        entity_type: str,
    ) -> list[KnowledgeGraphNode]:

        target = str(
            entity_type
        ).strip().casefold()

        return [
            node
            for node in self.nodes.values()
            if node.entity_type.casefold()
            == target
        ]

    # ============================================================
    # RELATION FILTER
    # ============================================================

    def relations(
        self,
        relation: str,
    ) -> list[KnowledgeGraphEdge]:

        target = str(
            relation
        ).strip().upper()

        return [
            edge
            for edge in self.edges.values()
            if edge.relation.upper()
            == target
        ]

    # ============================================================
    # TRAVERSAL
    # ============================================================

    def successors(
        self,
        node_id: str,
    ) -> list[KnowledgeGraphNode]:

        output = []

        for edge in self.edges.values():

            if edge.source_id == node_id:

                node = self.nodes.get(
                    edge.target_id
                )

                if node is not None:

                    output.append(
                        node
                    )

        return output

    # ============================================================

    def predecessors(
        self,
        node_id: str,
    ) -> list[KnowledgeGraphNode]:

        output = []

        for edge in self.edges.values():

            if edge.target_id == node_id:

                node = self.nodes.get(
                    edge.source_id
                )

                if node is not None:

                    output.append(
                        node
                    )

        return output

    # ============================================================

    def neighbors(
        self,
        node_id: str,
    ) -> list[KnowledgeGraphNode]:

        output = []

        for edge in self.edges.values():

            if edge.source_id == node_id:

                node = self.nodes.get(
                    edge.target_id
                )

                if node is not None:

                    output.append(node)

            elif edge.target_id == node_id:

                node = self.nodes.get(
                    edge.source_id
                )

                if node is not None:

                    output.append(node)

        return output

    # ============================================================
    # STATISTICS
    # ============================================================

    @property
    def node_count(self) -> int:

        return len(
            self.nodes
        )

    @property
    def edge_count(self) -> int:

        return len(
            self.edges
        )

    # ============================================================

    def __repr__(self):

        return (
            "<KnowledgeGraph "
            f"nodes={self.node_count} "
            f"edges={self.edge_count}>"
        )


# ================================================================
# BUILDER
# ================================================================

class KnowledgeGraphBuilder:
    """
    Converts BusinessStatementBuilder output
    into the enterprise KnowledgeGraph.

    The builder is intentionally independent of
    the old ontology capability architecture.
    """

    def __init__(self):

        self.graph = KnowledgeGraph()

        self._node_index: dict[
            str,
            str,
        ] = {}

        self._edge_index: set[
            tuple[str, str, str]
        ] = set()

    # ============================================================
    # PUBLIC BUILD
    # ============================================================

    def build(
        self,
        statements,
    ) -> KnowledgeGraph:
        """
        Build KnowledgeGraph from BusinessStatementBuilder output.

        `statements` may be:

            • a single BusinessStatementBuilder result
            • a list
            • a tuple
            • any iterable
        """

        self.graph = KnowledgeGraph()

        self._node_index.clear()

        self._edge_index.clear()

        for statement in self._as_iterable(
            statements
        ):

            if statement is None:

                continue

            self._build_statement(
                statement
            )

        return self.graph

    # ============================================================
    # STATEMENT
    # ============================================================

    def _build_statement(
        self,
        statement,
    ) -> None:

        entities = getattr(
            statement,
            "entities",
            None,
        )

        relations = getattr(
            statement,
            "relations",
            None,
        )

        if entities is None:

            return

        entity_nodes = {}

        for entity in entities:

            node = self._get_or_create_node(
                entity
            )

            if node is not None:

                entity_nodes[
                    self._entity_key(entity)
                ] = node

        if relations:

            for relation in relations:

                self._build_relation(
                    relation,
                    entity_nodes,
                )

    # ============================================================
    # ENTITY → NODE
    # ============================================================

    def _get_or_create_node(
        self,
        entity,
    ) -> Optional[KnowledgeGraphNode]:

        if entity is None:

            return None

        key = self._entity_key(
            entity
        )

        if not key:

            return None

        existing_id = self._node_index.get(
            key
        )

        if existing_id:

            return self.graph.get_node(
                existing_id
            )

        node_id = self._make_node_id(
            entity
        )

        node = KnowledgeGraphNode(

            node_id=node_id,

            entity_id=str(
                getattr(
                    entity,
                    "entity_id",
                    "",
                )
            ),

            label=self._first_value(
                entity,
                "label",
                "original",
                "canonical",
                "name",
            ),

            canonical=str(
                getattr(
                    entity,
                    "canonical",
                    "",
                )
            ),

            normalized=str(
                getattr(
                    entity,
                    "normalized",
                    "",
                )
            ),

            entity_type=self._normalize_type(
                entity
            ),

            category=str(
                getattr(
                    entity,
                    "category",
                    "",
                )
            ),

            ontology_name=str(
                getattr(
                    entity,
                    "ontology_name",
                    "",
                )
            ),

            primary_domain=str(
                getattr(
                    entity,
                    "primary_domain",
                    getattr(
                        entity,
                        "domain",
                        "",
                    ),
                )
            ),

            business_area=str(
                getattr(
                    entity,
                    "business_area",
                    "",
                )
            ),

            description=str(
                getattr(
                    entity,
                    "description",
                    "",
                )
            ),

            confidence=self._confidence(
                entity
            ),

            source=str(
                getattr(
                    entity,
                    "source",
                    "",
                )
            ),

            metadata=self._metadata(
                entity
            ),
        )

        self.graph.add_node(
            node
        )

        self._node_index[
            key
        ] = node_id

        return node

    # ============================================================
    # RELATION → EDGE
    # ============================================================

    def _build_relation(
        self,
        relation,
        entity_nodes,
    ) -> None:

        if relation is None:

            return

        source_id = str(
            getattr(
                relation,
                "source_id",
                "",
            )
        )

        target_id = str(
            getattr(
                relation,
                "target_id",
                "",
            )
        )

        relation_type = str(
            getattr(
                relation,
                "relation_type",
                getattr(
                    relation,
                    "relation",
                    "",
                ),
            )
        ).strip().upper()

        if not source_id or not target_id:

            return

        source_node = self._find_node_by_entity_id(
            source_id
        )

        target_node = self._find_node_by_entity_id(
            target_id
        )

        if source_node is None or target_node is None:

            return

        signature = (
            source_node.node_id,
            relation_type,
            target_node.node_id,
        )

        if signature in self._edge_index:

            return

        edge_id = self._make_edge_id(
            source_node.node_id,
            relation_type,
            target_node.node_id,
        )

        edge = KnowledgeGraphEdge(

            edge_id=edge_id,

            source_id=source_node.node_id,

            target_id=target_node.node_id,

            relation=relation_type,

            confidence=self._confidence(
                relation
            ),

            metadata=self._metadata(
                relation
            ),
        )

        self.graph.add_edge(
            edge
        )

        self._edge_index.add(
            signature
        )

    # ============================================================
    # LOOKUP
    # ============================================================

    def _find_node_by_entity_id(
        self,
        entity_id: str,
    ) -> Optional[KnowledgeGraphNode]:

        for node in self.graph.get_nodes():

            if node.entity_id == entity_id:

                return node

        return None

    # ============================================================
    # ENTITY KEY
    # ============================================================

    @staticmethod
    def _entity_key(
        entity,
    ) -> str:

        entity_id = str(
            getattr(
                entity,
                "entity_id",
                "",
            )
        ).strip()

        if entity_id:

            return (
                "id:"
                + entity_id.casefold()
            )

        canonical = str(
            getattr(
                entity,
                "canonical",
                "",
            )
        ).strip()

        entity_type = str(
            getattr(
                entity,
                "entity_type",
                "",
            )
        ).strip()

        if canonical:

            return (
                "canonical:"
                + entity_type.casefold()
                + ":"
                + canonical.casefold()
            )

        original = str(
            getattr(
                entity,
                "original",
                "",
            )
        ).strip()

        if original:

            return (
                "original:"
                + entity_type.casefold()
                + ":"
                + original.casefold()
            )

        return ""

    # ============================================================
    # NODE ID
    # ============================================================

    @classmethod
    def _make_node_id(
        cls,
        entity,
    ) -> str:

        entity_id = str(
            getattr(
                entity,
                "entity_id",
                "",
            )
        ).strip()

        if entity_id:

            return (
                "entity:"
                + entity_id
            )

        entity_type = cls._normalize_type(
            entity
        )

        canonical = str(
            getattr(
                entity,
                "canonical",
                "",
            )
        ).strip()

        if not canonical:

            canonical = str(
                getattr(
                    entity,
                    "original",
                    "",
                )
            ).strip()

        safe = (
            canonical
            .casefold()
            .replace(
                " ",
                "_",
            )
            .replace(
                "/",
                "_",
            )
        )

        return (
            "entity:"
            + entity_type.casefold()
            + ":"
            + safe
        )

    # ============================================================
    # EDGE ID
    # ============================================================

    @staticmethod
    def _make_edge_id(
        source_id: str,
        relation: str,
        target_id: str,
    ) -> str:

        return (
            "edge:"
            + source_id
            + ":"
            + relation.casefold()
            + ":"
            + target_id
        )

    # ============================================================
    # ENTITY TYPE
    # ============================================================

    @staticmethod
    def _normalize_type(
        entity,
    ) -> str:

        value = str(
            getattr(
                entity,
                "entity_type",
                "",
            )
        ).strip()

        if value:

            return value

        category = str(
            getattr(
                entity,
                "category",
                "",
            )
        ).strip()

        return category

    # ============================================================
    # CONFIDENCE
    # ============================================================

    @staticmethod
    def _confidence(
        obj,
    ) -> float:

        value = getattr(
            obj,
            "confidence",
            0.0,
        )

        try:

            return max(
                0.0,
                min(
                    1.0,
                    float(value),
                ),
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    # ============================================================
    # METADATA
    # ============================================================

    @staticmethod
    def _metadata(
        obj,
    ) -> dict[str, Any]:

        metadata = getattr(
            obj,
            "metadata",
            {},
        )

        if isinstance(
            metadata,
            dict,
        ):

            return dict(
                metadata
            )

        return {}

    # ============================================================
    # FIRST VALUE
    # ============================================================

    @staticmethod
    def _first_value(
        obj,
        *attributes,
    ) -> str:

        for attribute in attributes:

            value = getattr(
                obj,
                attribute,
                None,
            )

            if value:

                return str(
                    value
                )

        return ""

    # ============================================================
    # ITERABLE
    # ============================================================

    @staticmethod
    def _as_iterable(
        value,
    ) -> Iterable:

        if value is None:

            return []

        if isinstance(
            value,
            (list, tuple, set),
        ):

            return value

        return [value]


# ================================================================
# CONVENIENCE API
# ================================================================

def build_knowledge_graph(
    statements,
) -> KnowledgeGraph:

    builder = KnowledgeGraphBuilder()

    return builder.build(
        statements
    )


__all__ = [
    "KnowledgeGraphNode",
    "KnowledgeGraphEdge",
    "KnowledgeGraph",
    "KnowledgeGraphBuilder",
    "build_knowledge_graph",
]