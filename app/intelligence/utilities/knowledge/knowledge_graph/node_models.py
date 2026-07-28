"""
Knowledge Graph Node Models

Every extracted ontology entity becomes a node.
"""

from dataclasses import dataclass, field


@dataclass
class GraphNode:
    """
    Universal Knowledge Graph Node
    """

    # -------------------------------------------------
    # Identity
    # -------------------------------------------------

    node_id: str = ""

    entity_id: str = ""

    node_type: str = ""

    label: str = ""

    canonical: str = ""

    # -------------------------------------------------
    # Ontology
    # -------------------------------------------------

    category: str = ""

    business_area: str = ""

    impact_weight: float = 1.0

    source: str = "ontology"

    # -------------------------------------------------
    # Graph Metadata
    # -------------------------------------------------

    confidence: float = 1.0

    frequency: int = 1

    metadata: dict = field(default_factory=dict)

    properties: dict = field(default_factory=dict)

    # -------------------------------------------------
    # Graph Connections
    # -------------------------------------------------

    incoming_edges: list = field(default_factory=list)

    outgoing_edges: list = field(default_factory=list)

    # -------------------------------------------------
    # Helper Methods
    # -------------------------------------------------

    def add_edge(self, edge):
        """
        Attach an edge to this node.
        """

        if edge.source_node == self.entity_id:
            self.outgoing_edges.append(edge)

        if edge.target_node == self.entity_id:
            self.incoming_edges.append(edge)

    # -------------------------------------------------

    @property
    def degree(self):

        return len(self.incoming_edges) + len(self.outgoing_edges)