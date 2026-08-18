"""
Enterprise Knowledge Graph Builder
Enterprise V14

Architecture
------------

KnowledgeDocument
        ↓
KnowledgeFact
        ↓
KnowledgeInterpretation
        ↓
SemanticEntity
        ↓
BusinessStatementBuilder
        ↓
BusinessStatement[]
        ↓
KnowledgeGraphBuilder
        ↓
KnowledgeGraph
        ↓
KnowledgeProfileBuilder
        ↓
KnowledgeProfile

Responsibilities
----------------

• Consume BusinessStatement objects
• Convert BusinessStatement.entities into graph nodes
• Convert BusinessStatement.relations into graph edges
• Preserve entity identity
• Preserve entity metadata
• Preserve impact_weight
• Preserve ATS information
• Preserve technologies
• Preserve methodologies
• Preserve certifications
• Preserve standards
• Preserve metrics
• Preserve achievement information
• Preserve statement information
• Prevent duplicate nodes
• Prevent duplicate edges
• Provide deterministic graph traversal
• Remain tolerant of small model differences

This builder does NOT:

• perform entity extraction
• perform ontology matching
• perform semantic resolution
• calculate final profile scores
• predict seniority
• predict career level
• build KnowledgeProfile

The KnowledgeProfileBuilder consumes the resulting KnowledgeGraph.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional


# =====================================================================
# KNOWLEDGE GRAPH NODE
# =====================================================================


@dataclass
class KnowledgeGraphNode:
    """
    One entity represented as a node in the KnowledgeGraph.

    The node deliberately preserves important semantic information
    required by downstream KnowledgeProfileBuilder.
    """

    # -----------------------------------------------------------------
    # IDENTITY
    # -----------------------------------------------------------------

    node_id: str = ""

    entity_id: str = ""

    label: str = ""

    canonical: str = ""

    normalized: str = ""

    # -----------------------------------------------------------------
    # SEMANTIC TYPE
    # -----------------------------------------------------------------

    entity_type: str = ""

    category: str = ""

    ontology_name: str = ""

    # -----------------------------------------------------------------
    # BUSINESS CONTEXT
    # -----------------------------------------------------------------

    primary_domain: str = ""

    secondary_domains: list[str] = field(
        default_factory=list
    )

    domain: str = ""

    business_area: str = ""

    description: str = ""

    # -----------------------------------------------------------------
    # BUSINESS MEANING
    # -----------------------------------------------------------------

    achievement: bool = False

    quantified: bool = False

    impact: str = ""

    business_value: str = ""

    higher_is_better: Optional[bool] = None

    # -----------------------------------------------------------------
    # SCORING INFORMATION
    # -----------------------------------------------------------------

    confidence: float = 0.0

    impact_weight: float = 1.0

    ats_score: Optional[float] = None

    ats_weight: Optional[float] = None

    # -----------------------------------------------------------------
    # SOURCE
    # -----------------------------------------------------------------

    source: str = ""

    statement_id: str = ""

    fact_id: str = ""

    sentence_index: int = -1

    # -----------------------------------------------------------------
    # METADATA
    # -----------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


# =====================================================================
# KNOWLEDGE GRAPH EDGE
# =====================================================================


@dataclass
class KnowledgeGraphEdge:
    """
    Relationship between two KnowledgeGraph nodes.
    """

    edge_id: str = ""

    source_id: str = ""

    target_id: str = ""

    relation: str = ""

    confidence: float = 0.0

    statement_id: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


# =====================================================================
# KNOWLEDGE GRAPH
# =====================================================================


class KnowledgeGraph:
    """
    Enterprise knowledge graph.

    Stores:

        nodes
        edges

    and provides:

        lookup
        filtering
        traversal
        statistics
    """

    def __init__(self) -> None:

        self.nodes: dict[
            str,
            KnowledgeGraphNode,
        ] = {}

        self.edges: dict[
            str,
            KnowledgeGraphEdge,
        ] = {}

    # =================================================================
    # NODE OPERATIONS
    # =================================================================

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

            self._merge_node(
                existing,
                node,
            )

            return existing

        self.nodes[
            node.node_id
        ] = node

        return node

    # -----------------------------------------------------------------

    @staticmethod
    def _merge_node(
        existing: KnowledgeGraphNode,
        incoming: KnowledgeGraphNode,
    ) -> None:

        # Preserve better populated scalar values.

        scalar_fields = (
            "entity_id",
            "label",
            "canonical",
            "normalized",
            "entity_type",
            "category",
            "ontology_name",
            "primary_domain",
            "domain",
            "business_area",
            "description",
            "impact",
            "business_value",
            "source",
            "statement_id",
            "fact_id",
        )

        for field_name in scalar_fields:

            current = getattr(
                existing,
                field_name,
                None,
            )

            incoming_value = getattr(
                incoming,
                field_name,
                None,
            )

            if (
                not current
                and incoming_value
            ):

                setattr(
                    existing,
                    field_name,
                    incoming_value,
                )

        # Lists

        for field_name in (
            "secondary_domains",
        ):

            current = getattr(
                existing,
                field_name,
                [],
            )

            incoming_value = getattr(
                incoming,
                field_name,
                [],
            )

            if incoming_value:

                for value in incoming_value:

                    if value not in current:

                        current.append(
                            value
                        )

        # Boolean business information.

        if incoming.achievement:

            existing.achievement = True

        if incoming.quantified:

            existing.quantified = True

        # Confidence should retain strongest value.

        if (
            incoming.confidence
            > existing.confidence
        ):

            existing.confidence = (
                incoming.confidence
            )

        # Impact weight.

        if (
            incoming.impact_weight
            > existing.impact_weight
        ):

            existing.impact_weight = (
                incoming.impact_weight
            )

        # ATS.

        if incoming.ats_score is not None:

            if (
                existing.ats_score is None
                or incoming.ats_score
                > existing.ats_score
            ):

                existing.ats_score = (
                    incoming.ats_score
                )

        if incoming.ats_weight is not None:

            if (
                existing.ats_weight is None
                or incoming.ats_weight
                > existing.ats_weight
            ):

                existing.ats_weight = (
                    incoming.ats_weight
                )

        # Metadata.

        existing.metadata.update(
            incoming.metadata
        )

    # -----------------------------------------------------------------

    def get_node(
        self,
        node_id: str,
    ) -> Optional[KnowledgeGraphNode]:

        return self.nodes.get(
            node_id
        )

    # -----------------------------------------------------------------

    def get_nodes(
        self,
    ) -> list[KnowledgeGraphNode]:

        return list(
            self.nodes.values()
        )

    # =================================================================
    # EDGE OPERATIONS
    # =================================================================

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
                "Source node does not exist: "
                f"{edge.source_id}"
            )

        if edge.target_id not in self.nodes:

            raise ValueError(
                "Target node does not exist: "
                f"{edge.target_id}"
            )

        existing = self.edges.get(
            edge.edge_id
        )

        if existing is not None:

            existing.metadata.update(
                edge.metadata
            )

            if (
                edge.confidence
                > existing.confidence
            ):

                existing.confidence = (
                    edge.confidence
                )

            if not existing.statement_id:

                existing.statement_id = (
                    edge.statement_id
                )

            return existing

        self.edges[
            edge.edge_id
        ] = edge

        return edge

    # -----------------------------------------------------------------

    def get_edge(
        self,
        edge_id: str,
    ) -> Optional[KnowledgeGraphEdge]:

        return self.edges.get(
            edge_id
        )

    # -----------------------------------------------------------------

    def get_edges(
        self,
    ) -> list[KnowledgeGraphEdge]:

        return list(
            self.edges.values()
        )

    # =================================================================
    # TYPE FILTER
    # =================================================================

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

    # =================================================================
    # RELATION FILTER
    # =================================================================

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

    # =================================================================
    # TRAVERSAL
    # =================================================================

    def successors(
        self,
        node_id: str,
    ) -> list[KnowledgeGraphNode]:

        output = []

        for edge in self.edges.values():

            if edge.source_id != node_id:

                continue

            node = self.nodes.get(
                edge.target_id
            )

            if node is not None:

                output.append(
                    node
                )

        return output

    # -----------------------------------------------------------------

    def predecessors(
        self,
        node_id: str,
    ) -> list[KnowledgeGraphNode]:

        output = []

        for edge in self.edges.values():

            if edge.target_id != node_id:

                continue

            node = self.nodes.get(
                edge.source_id
            )

            if node is not None:

                output.append(
                    node
                )

        return output

    # -----------------------------------------------------------------

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

                    output.append(
                        node
                    )

            elif edge.target_id == node_id:

                node = self.nodes.get(
                    edge.source_id
                )

                if node is not None:

                    output.append(
                        node
                    )

        return output

    # =================================================================
    # STATISTICS
    # =================================================================

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

    # =================================================================
    # REPRESENTATION
    # =================================================================

    def __repr__(self) -> str:

        return (
            "<KnowledgeGraph "
            f"nodes={self.node_count} "
            f"edges={self.edge_count}>"
        )


# =====================================================================
# KNOWLEDGE GRAPH BUILDER
# =====================================================================


class KnowledgeGraphBuilder:
    """
    Convert BusinessStatement output into KnowledgeGraph.

    The critical contract is:

        BusinessStatement.entities
                    ↓
              graph nodes

        BusinessStatement.relations
                    ↓
              graph edges

    This builder deliberately accepts the current BusinessStatement
    architecture without requiring BusinessStatement to be rebuilt.
    """

    def __init__(self) -> None:

        self.graph = KnowledgeGraph()

        self._node_index: dict[
            str,
            str,
        ] = {}

        self._entity_id_index: dict[
            str,
            str,
        ] = {}

        self._edge_index: set[
            tuple[str, str, str]
        ] = set()

    # =================================================================
    # PUBLIC BUILD API
    # =================================================================

    def build(
        self,
        statements: Any = None,
        *,
        business_statements: Any = None,
    ) -> KnowledgeGraph:
        """
        Build the KnowledgeGraph.

        Supported calls:

            builder.build(statements)

        or:

            builder.build(
                business_statements=statements
            )

        The method is intentionally tolerant of:

            • single BusinessStatement
            • list
            • tuple
            • set
            • generator
            • iterable
        """

        self.graph = KnowledgeGraph()

        self._node_index.clear()

        self._entity_id_index.clear()

        self._edge_index.clear()

        if statements is None:

            statements = (
                business_statements
            )

        for statement in self._as_iterable(
            statements
        ):

            if statement is None:

                continue

            self._build_statement(
                statement
            )

        return self.graph

    # =================================================================
    # STATEMENT
    # =================================================================

    def _build_statement(
        self,
        statement: Any,
    ) -> None:
        """
        Convert one BusinessStatement.

        IMPORTANT:

        We do not rely only on one particular model field.

        The current architecture stores semantic entities in:

            statement.entities

        and relations in:

            statement.relations
        """

        statement_id = self._statement_id(
            statement
        )

        entities = self._as_iterable(
            getattr(
                statement,
                "entities",
                None,
            )
        )

        relations = self._as_iterable(
            getattr(
                statement,
                "relations",
                None,
            )
        )

        entity_nodes: dict[
            str,
            KnowledgeGraphNode,
        ] = {}

        # -------------------------------------------------------------
        # BUILD ALL NODES FIRST
        # -------------------------------------------------------------

        for entity in entities:

            node = self._get_or_create_node(
                entity,
                statement=statement,
            )

            if node is None:

                continue

            entity_key = self._entity_key(
                entity
            )

            if entity_key:

                entity_nodes[
                    entity_key
                ] = node

            entity_id = self._entity_id(
                entity
            )

            if entity_id:

                entity_nodes[
                    entity_id.casefold()
                ] = node

        # -------------------------------------------------------------
        # BUILD RELATIONS SECOND
        # -------------------------------------------------------------

        for relation in relations:

            self._build_relation(
                relation=relation,
                statement=statement,
                entity_nodes=entity_nodes,
            )

        # -------------------------------------------------------------
        # FALLBACK RELATION CONSTRUCTION
        #
        # Some semantic implementations expose dependencies rather
        # than relations on BusinessStatement.
        # -------------------------------------------------------------

        dependencies = self._as_iterable(
            getattr(
                statement,
                "dependencies",
                None,
            )
        )

        for dependency in dependencies:

            self._build_relation(
                relation=dependency,
                statement=statement,
                entity_nodes=entity_nodes,
            )

    # =================================================================
    # ENTITY → NODE
    # =================================================================

    def _get_or_create_node(
        self,
        entity: Any,
        *,
        statement: Any = None,
    ) -> Optional[KnowledgeGraphNode]:

        if entity is None:

            return None

        key = self._entity_key(
            entity
        )

        if not key:

            return None

        existing_id = (
            self._node_index.get(
                key
            )
        )

        if existing_id:

            return self.graph.get_node(
                existing_id
            )

        entity_id = self._entity_id(
            entity
        )

        # -------------------------------------------------------------
        # SECONDARY LOOKUP BY ENTITY ID
        # -------------------------------------------------------------

        if entity_id:

            existing_id = (
                self._entity_id_index.get(
                    entity_id.casefold()
                )
            )

            if existing_id:

                self._node_index[
                    key
                ] = existing_id

                return self.graph.get_node(
                    existing_id
                )

        node_id = self._make_node_id(
            entity
        )

        node = KnowledgeGraphNode(

            node_id=node_id,

            entity_id=entity_id,

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
                or ""
            ),

            normalized=str(
                getattr(
                    entity,
                    "normalized",
                    "",
                )
                or ""
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
                or ""
            ),

            ontology_name=str(
                getattr(
                    entity,
                    "ontology_name",
                    "",
                )
                or ""
            ),

            primary_domain=self._first_value(
                entity,
                "primary_domain",
                "domain",
            ),

            secondary_domains=self._list_value(
                entity,
                "secondary_domains",
            ),

            domain=self._first_value(
                entity,
                "domain",
            ),

            business_area=str(
                getattr(
                    entity,
                    "business_area",
                    "",
                )
                or ""
            ),

            description=str(
                getattr(
                    entity,
                    "description",
                    "",
                )
                or ""
            ),

            achievement=self._bool_value(
                entity,
                "achievement",
            ),

            quantified=self._bool_value(
                entity,
                "quantified",
            ),

            impact=str(
                getattr(
                    entity,
                    "impact",
                    "",
                )
                or ""
            ),

            business_value=str(
                getattr(
                    entity,
                    "business_value",
                    "",
                )
                or ""
            ),

            higher_is_better=(
                getattr(
                    entity,
                    "higher_is_better",
                    None,
                )
            ),

            confidence=self._confidence(
                entity
            ),

            impact_weight=self._float_value(
                entity,
                "impact_weight",
                default=1.0,
            ),

            ats_score=self._extract_ats_score(
                entity
            ),

            ats_weight=self._extract_ats_weight(
                entity
            ),

            source=self._first_value(
                entity,
                "source",
            ),

            statement_id=(
                statement_id
                if (
                    statement_id := self._statement_id(
                        statement
                    )
                )
                else self._first_value(
                    entity,
                    "statement_id",
                    "business_statement_id",
                )
            ),

            fact_id=self._first_value(
                entity,
                "fact_id",
                "source_fact_id",
            ),

            sentence_index=self._int_value(
                entity,
                "sentence_index",
                default=-1,
            ),

            metadata=self._build_node_metadata(
                entity=entity,
                statement=statement,
            ),
        )

        self.graph.add_node(
            node
        )

        self._node_index[
            key
        ] = node_id

        if entity_id:

            self._entity_id_index[
                entity_id.casefold()
            ] = node_id

        return node

    # =================================================================
    # RELATION → EDGE
    # =================================================================

    def _build_relation(
        self,
        relation: Any,
        statement: Any,
        entity_nodes: dict[str, KnowledgeGraphNode],
    ) -> None:

        if relation is None:

            return

        source_reference = (
            self._relation_source_id(
                relation
            )
        )

        target_reference = (
            self._relation_target_id(
                relation
            )
        )

        relation_type = (
            self._relation_type(
                relation
            )
        )

        if not relation_type:

            relation_type = (
                "RELATED_TO"
            )

        if (
            not source_reference
            or not target_reference
        ):

            return

        source_node = (
            self._resolve_relation_node(
                source_reference,
                entity_nodes,
            )
        )

        target_node = (
            self._resolve_relation_node(
                target_reference,
                entity_nodes,
            )
        )

        # -------------------------------------------------------------
        # RELATION MAY USE GRAPH NODE IDS
        # -------------------------------------------------------------

        if source_node is None:

            source_node = self.graph.get_node(
                source_reference
            )

        if target_node is None:

            target_node = self.graph.get_node(
                target_reference
            )

        if (
            source_node is None
            or target_node is None
        ):

            return

        if (
            source_node.node_id
            == target_node.node_id
        ):

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

        edge_metadata = (
            self._metadata(
                relation
            )
        )

        statement_id = self._statement_id(
            statement
        )

        if statement_id:

            edge_metadata.setdefault(
                "statement_id",
                statement_id,
            )

        edge = KnowledgeGraphEdge(

            edge_id=edge_id,

            source_id=source_node.node_id,

            target_id=target_node.node_id,

            relation=relation_type,

            confidence=self._confidence(
                relation
            ),

            statement_id=statement_id,

            metadata=edge_metadata,
        )

        self.graph.add_edge(
            edge
        )

        self._edge_index.add(
            signature
        )

    # =================================================================
    # RELATION NODE RESOLUTION
    # =================================================================

    def _resolve_relation_node(
        self,
        reference: str,
        entity_nodes: dict[str, KnowledgeGraphNode],
    ) -> Optional[KnowledgeGraphNode]:

        if not reference:

            return None

        normalized = (
            reference
            .strip()
            .casefold()
        )

        # Direct entity map.

        node = entity_nodes.get(
            normalized
        )

        if node is not None:

            return node

        # Global entity ID index.

        node_id = (
            self._entity_id_index.get(
                normalized
            )
        )

        if node_id:

            return self.graph.get_node(
                node_id
            )

        # Direct node ID.

        node = self.graph.get_node(
            reference
        )

        if node is not None:

            return node

        # Entity ID search.

        for graph_node in (
            self.graph.get_nodes()
        ):

            if (
                graph_node.entity_id
                and graph_node.entity_id.casefold()
                == normalized
            ):

                return graph_node

        return None

    # =================================================================
    # ENTITY KEY
    # =================================================================

    @classmethod
    def _entity_key(
        cls,
        entity: Any,
    ) -> str:

        entity_id = cls._entity_id(
            entity
        )

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
            or ""
        ).strip()

        entity_type = (
            cls._normalize_type(
                entity
            )
        )

        if canonical:

            return (
                "canonical:"
                + entity_type.casefold()
                + ":"
                + canonical.casefold()
            )

        normalized = str(
            getattr(
                entity,
                "normalized",
                "",
            )
            or ""
        ).strip()

        if normalized:

            return (
                "normalized:"
                + entity_type.casefold()
                + ":"
                + normalized.casefold()
            )

        original = str(
            getattr(
                entity,
                "original",
                "",
            )
            or ""
        ).strip()

        if original:

            return (
                "original:"
                + entity_type.casefold()
                + ":"
                + original.casefold()
            )

        return ""

    # =================================================================
    # ENTITY ID
    # =================================================================

    @staticmethod
    def _entity_id(
        entity: Any,
    ) -> str:

        return str(
            getattr(
                entity,
                "entity_id",
                "",
            )
            or ""
        ).strip()

    # =================================================================
    # NODE ID
    # =================================================================

    @classmethod
    def _make_node_id(
        cls,
        entity: Any,
    ) -> str:

        entity_id = cls._entity_id(
            entity
        )

        if entity_id:

            return (
                "entity:"
                + entity_id
            )

        entity_type = (
            cls._normalize_type(
                entity
            )
        )

        canonical = str(
            getattr(
                entity,
                "canonical",
                "",
            )
            or ""
        ).strip()

        if not canonical:

            canonical = str(
                getattr(
                    entity,
                    "normalized",
                    "",
                )
                or ""
            ).strip()

        if not canonical:

            canonical = str(
                getattr(
                    entity,
                    "original",
                    "",
                )
                or ""
            ).strip()

        safe = cls._safe_identifier(
            canonical
        )

        return (
            "entity:"
            + cls._safe_identifier(
                entity_type
            )
            + ":"
            + safe
        )

    # =================================================================
    # EDGE ID
    # =================================================================

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

    # =================================================================
    # ENTITY TYPE
    # =================================================================

    @staticmethod
    def _normalize_type(
        entity: Any,
    ) -> str:

        value = str(
            getattr(
                entity,
                "entity_type",
                "",
            )
            or ""
        ).strip()

        if value:

            return value

        category = str(
            getattr(
                entity,
                "category",
                "",
            )
            or ""
        ).strip()

        return category

    # =================================================================
    # STATEMENT ID
    # =================================================================

    @staticmethod
    def _statement_id(
        statement: Any,
    ) -> str:

        if statement is None:

            return ""

        for attribute in (
            "statement_id",
            "business_statement_id",
            "fact_id",
            "source_statement_id",
        ):

            value = getattr(
                statement,
                attribute,
                None,
            )

            if value:

                return str(
                    value
                ).strip()

        return ""

    # =================================================================
    # RELATION TYPE
    # =================================================================

    @staticmethod
    def _relation_type(
        relation: Any,
    ) -> str:

        for attribute in (
            "relation_type",
            "relation",
            "type",
            "relationship",
        ):

            value = getattr(
                relation,
                attribute,
                None,
            )

            if value:

                return str(
                    value
                ).strip().upper()

        return ""

    # =================================================================
    # RELATION SOURCE
    # =================================================================

    @staticmethod
    def _relation_source_id(
        relation: Any,
    ) -> str:

        for attribute in (
            "source_id",
            "source_entity_id",
            "from_id",
            "source",
            "from_entity_id",
        ):

            value = getattr(
                relation,
                attribute,
                None,
            )

            if value:

                if isinstance(
                    value,
                    str,
                ):

                    return value.strip()

                nested_id = getattr(
                    value,
                    "entity_id",
                    None,
                )

                if nested_id:

                    return str(
                        nested_id
                    ).strip()

                nested_node_id = getattr(
                    value,
                    "node_id",
                    None,
                )

                if nested_node_id:

                    return str(
                        nested_node_id
                    ).strip()

        return ""

    # =================================================================
    # RELATION TARGET
    # =================================================================

    @staticmethod
    def _relation_target_id(
        relation: Any,
    ) -> str:

        for attribute in (
            "target_id",
            "target_entity_id",
            "to_id",
            "target",
            "to_entity_id",
        ):

            value = getattr(
                relation,
                attribute,
                None,
            )

            if value:

                if isinstance(
                    value,
                    str,
                ):

                    return value.strip()

                nested_id = getattr(
                    value,
                    "entity_id",
                    None,
                )

                if nested_id:

                    return str(
                        nested_id
                    ).strip()

                nested_node_id = getattr(
                    value,
                    "node_id",
                    None,
                )

                if nested_node_id:

                    return str(
                        nested_node_id
                    ).strip()

        return ""

    # =================================================================
    # NODE METADATA
    # =================================================================

    @classmethod
    def _build_node_metadata(
        cls,
        entity: Any,
        statement: Any,
    ) -> dict[str, Any]:

        metadata = cls._metadata(
            entity
        )

        # -------------------------------------------------------------
        # Preserve important semantic information.
        # -------------------------------------------------------------

        for attribute in (
            "aliases",
            "related_metrics",
            "trigger_actions",
            "trigger_objects",
            "trigger_skills",
            "trigger_metrics",
            "trigger_certifications",
            "higher_is_better",
            "unit",
            "direction",
            "magnitude",
            "value",
            "original",
            "matched_phrase",
            "matched_alias",
        ):

            value = getattr(
                entity,
                attribute,
                None,
            )

            if value is not None:

                metadata.setdefault(
                    attribute,
                    value,
                )

        # -------------------------------------------------------------
        # ATS information
        # -------------------------------------------------------------

        ats_score = cls._extract_ats_score(
            entity
        )

        if ats_score is not None:

            metadata[
                "ats_score"
            ] = ats_score

        ats_weight = cls._extract_ats_weight(
            entity
        )

        if ats_weight is not None:

            metadata[
                "ats_weight"
            ] = ats_weight

        # -------------------------------------------------------------
        # Impact
        # -------------------------------------------------------------

        impact_weight = cls._float_value(
            entity,
            "impact_weight",
            default=None,
        )

        if impact_weight is not None:

            metadata[
                "impact_weight"
            ] = impact_weight

        # -------------------------------------------------------------
        # Statement context
        # -------------------------------------------------------------

        statement_id = cls._statement_id(
            statement
        )

        if statement_id:

            metadata.setdefault(
                "statement_id",
                statement_id,
            )

        statement_text = (
            getattr(
                statement,
                "text",
                "",
            )
            or
            getattr(
                statement,
                "source_text",
                "",
            )
            or ""
        )

        if statement_text:

            metadata.setdefault(
                "statement_text",
                str(
                    statement_text
                ),
            )

        # -------------------------------------------------------------
        # Entity type
        # -------------------------------------------------------------

        metadata.setdefault(
            "entity_type",
            cls._normalize_type(
                entity
            ),
        )

        # -------------------------------------------------------------
        # Graph source
        # -------------------------------------------------------------

        metadata.setdefault(
            "graph_source",
            "BusinessStatementBuilder",
        )

        return metadata

    # =================================================================
    # ATS SCORE
    # =================================================================

    @classmethod
    def _extract_ats_score(
        cls,
        entity: Any,
    ) -> Optional[float]:

        for attribute in (
            "ats_score",
            "ats_match_score",
            "ats_relevance_score",
        ):

            value = getattr(
                entity,
                attribute,
                None,
            )

            converted = cls._safe_float(
                value
            )

            if converted is not None:

                return converted

        metadata = getattr(
            entity,
            "metadata",
            None,
        )

        if isinstance(
            metadata,
            dict,
        ):

            for key in (
                "ats_score",
                "ats_match_score",
                "ats_relevance_score",
            ):

                converted = cls._safe_float(
                    metadata.get(
                        key
                    )
                )

                if converted is not None:

                    return converted

            ats = metadata.get(
                "ats"
            )

            if isinstance(
                ats,
                dict,
            ):

                for key in (
                    "score",
                    "ats_score",
                    "match_score",
                    "relevance_score",
                ):

                    converted = cls._safe_float(
                        ats.get(
                            key
                        )
                    )

                    if converted is not None:

                        return converted

        return None

    # =================================================================
    # ATS WEIGHT
    # =================================================================

    @classmethod
    def _extract_ats_weight(
        cls,
        entity: Any,
    ) -> Optional[float]:

        for attribute in (
            "ats_weight",
            "ats_importance",
        ):

            value = getattr(
                entity,
                attribute,
                None,
            )

            converted = cls._safe_float(
                value
            )

            if converted is not None:

                return converted

        metadata = getattr(
            entity,
            "metadata",
            None,
        )

        if isinstance(
            metadata,
            dict,
        ):

            for key in (
                "ats_weight",
                "ats_importance",
            ):

                converted = cls._safe_float(
                    metadata.get(
                        key
                    )
                )

                if converted is not None:

                    return converted

            ats = metadata.get(
                "ats"
            )

            if isinstance(
                ats,
                dict,
            ):

                for key in (
                    "weight",
                    "ats_weight",
                    "importance",
                ):

                    converted = cls._safe_float(
                        ats.get(
                            key
                        )
                    )

                    if converted is not None:

                        return converted

        return None

    # =================================================================
    # CONFIDENCE
    # =================================================================

    @staticmethod
    def _confidence(
        obj: Any,
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

    # =================================================================
    # METADATA
    # =================================================================

    @staticmethod
    def _metadata(
        obj: Any,
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

    # =================================================================
    # FIRST VALUE
    # =================================================================

    @staticmethod
    def _first_value(
        obj: Any,
        *attributes: str,
    ) -> str:

        if obj is None:

            return ""

        for attribute in attributes:

            value = getattr(
                obj,
                attribute,
                None,
            )

            if value is not None:

                text = str(
                    value
                ).strip()

                if text:

                    return text

        return ""

    # =================================================================
    # LIST VALUE
    # =================================================================

    @staticmethod
    def _list_value(
        obj: Any,
        attribute: str,
    ) -> list[str]:

        value = getattr(
            obj,
            attribute,
            None,
        )

        if value is None:

            return []

        if isinstance(
            value,
            str,
        ):

            return [
                value
            ] if value.strip() else []

        try:

            return [
                str(item)
                for item in value
                if item is not None
            ]

        except TypeError:

            return []

    # =================================================================
    # BOOLEAN VALUE
    # =================================================================

    @staticmethod
    def _bool_value(
        obj: Any,
        attribute: str,
    ) -> bool:

        value = getattr(
            obj,
            attribute,
            False,
        )

        if isinstance(
            value,
            bool,
        ):

            return value

        if isinstance(
            value,
            str,
        ):

            return (
                value.strip().casefold()
                in {
                    "true",
                    "yes",
                    "1",
                    "y",
                }
            )

        return bool(
            value
        )

    # =================================================================
    # INTEGER VALUE
    # =================================================================

    @staticmethod
    def _int_value(
        obj: Any,
        attribute: str,
        default: int = -1,
    ) -> int:

        value = getattr(
            obj,
            attribute,
            default,
        )

        try:

            return int(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return default

    # =================================================================
    # FLOAT VALUE
    # =================================================================

    @staticmethod
    def _float_value(
        obj: Any,
        attribute: str,
        default: Optional[float] = 0.0,
    ) -> Optional[float]:

        value = getattr(
            obj,
            attribute,
            default,
        )

        if value is None:

            return default

        return KnowledgeGraphBuilder._safe_float(
            value,
            default=default,
        )

    # =================================================================
    # SAFE FLOAT
    # =================================================================

    @staticmethod
    def _safe_float(
        value: Any,
        default: Optional[float] = None,
    ) -> Optional[float]:

        try:

            return float(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return default

    # =================================================================
    # SAFE IDENTIFIER
    # =================================================================

    @staticmethod
    def _safe_identifier(
        value: str,
    ) -> str:

        text = str(
            value
            or ""
        ).strip().casefold()

        if not text:

            return "unknown"

        output = []

        previous_separator = False

        for character in text:

            if (
                character.isalnum()
                or character == "_"
            ):

                output.append(
                    character
                )

                previous_separator = False

            else:

                if not previous_separator:

                    output.append(
                        "_"
                    )

                    previous_separator = True

        result = "".join(
            output
        ).strip(
            "_"
        )

        return (
            result
            or "unknown"
        )

    # =================================================================
    # ITERABLE
    # =================================================================

    @staticmethod
    def _as_iterable(
        value: Any,
    ) -> Iterable[Any]:

        if value is None:

            return []

        if isinstance(
            value,
            (list, tuple, set),
        ):

            return value

        if isinstance(
            value,
            str,
        ):

            return [value]

        try:

            return list(
                value
            )

        except TypeError:

            return [value]


# =====================================================================
# CONVENIENCE API
# =====================================================================


def build_knowledge_graph(
    statements: Any = None,
    *,
    business_statements: Any = None,
) -> KnowledgeGraph:

    builder = (
        KnowledgeGraphBuilder()
    )

    return builder.build(
        statements=statements,
        business_statements=business_statements,
    )


# =====================================================================
# PUBLIC EXPORTS
# =====================================================================

__all__ = [
    "KnowledgeGraphNode",
    "KnowledgeGraphEdge",
    "KnowledgeGraph",
    "KnowledgeGraphBuilder",
    "build_knowledge_graph",
]