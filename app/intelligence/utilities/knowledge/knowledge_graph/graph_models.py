"""
Knowledge Graph Model

Represents the complete semantic graph extracted
from one resume or one document.
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.knowledge_graph.edge_models import (
    GraphEdge,
)

from app.intelligence.utilities.knowledge.knowledge_graph.node_models import (
    GraphNode,
)


@dataclass
class KnowledgeGraph:

    # --------------------------------------------------
    # Graph Contents
    # --------------------------------------------------

    nodes: list[GraphNode] = field(default_factory=list)

    edges: list[GraphEdge] = field(default_factory=list)

    # --------------------------------------------------
    # Fast Lookup Indexes
    # --------------------------------------------------

    node_index: dict[str, GraphNode] = field(default_factory=dict)

    edge_index: dict[str, GraphEdge] = field(default_factory=dict)

    entity_index: dict[str, str] = field(default_factory=dict)

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    node_count: int = 0

    edge_count: int = 0

    confidence: float = 0.0

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    source: str = "resume"

    metadata: dict = field(default_factory=dict)

    # ==================================================
    # Node Management
    # ==================================================

    def add_node(self, node: GraphNode):

        if node.node_id in self.node_index:
            return

        self.nodes.append(node)

        self.node_index[node.node_id] = node

        if node.entity_id:
            self.entity_index[node.entity_id] = node.node_id

        self.node_count = len(self.nodes)

    # --------------------------------------------------

    def add_edge(self, edge: GraphEdge):

        if edge.edge_id in self.edge_index:
            return

        self.edges.append(edge)

        self.edge_index[edge.edge_id] = edge

        self.edge_count = len(self.edges)

    # ==================================================
    # Lookup
    # ==================================================

    def get_node(self, node_id):

        return self.node_index.get(node_id)

    # --------------------------------------------------

    def get_node_by_entity(self, entity_id):

        node_id = self.entity_index.get(entity_id)

        if node_id is None:
            return None

        return self.node_index.get(node_id)

    # ==================================================
    # Edge Lookup
    # ==================================================

    def get_edges_from(self, entity_id):

        return [

            edge

            for edge in self.edges

            if edge.source_node == entity_id

        ]

    # --------------------------------------------------

    def get_edges_to(self, entity_id):

        return [

            edge

            for edge in self.edges

            if edge.target_node == entity_id

        ]

    # ==================================================
    # Typed Collections
    # ==================================================

    def actions(self):

        return [

            node

            for node in self.nodes

            if node.node_type == "Action"

        ]

    # --------------------------------------------------

    def objects(self):

        return [

            node

            for node in self.nodes

            if node.node_type == "Object"

        ]

    # --------------------------------------------------

    def metrics(self):

        return [

            node

            for node in self.nodes

            if node.node_type == "Metric"

        ]

    # --------------------------------------------------

    def measurements(self):

        return [

            node

            for node in self.nodes

            if node.node_type == "Measurement"

        ]

    # --------------------------------------------------

    def domains(self):

        return [

            node

            for node in self.nodes

            if node.node_type == "Domain"

        ]

    # --------------------------------------------------

    def certifications(self):

        return [

            node

            for node in self.nodes

            if node.node_type == "Certification"

        ]

    # --------------------------------------------------

    def technologies(self):

        return [

            node

            for node in self.nodes

            if node.node_type == "Technology"

        ]

    # --------------------------------------------------

    def modifiers(self):

        return [

            node

            for node in self.nodes

            if node.node_type == "Modifier"

        ]

    # ==================================================
    # Summary
    # ==================================================

    def summary(self):

        return {

            "nodes": self.node_count,

            "edges": self.edge_count,

            "confidence": self.confidence,

        }