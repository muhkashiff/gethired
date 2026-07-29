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

    @property
    def value(self):
        return self.metadata.get("value")


    @property
    def numeric_value(self):
        return self.metadata.get("numeric_value")


    @property
    def normalized_value(self):
        return self.metadata.get("normalized_value")


    @property
    def unit(self):
        return self.metadata.get("unit")


    @property
    def start_value(self):
        return self.metadata.get("start_value")


    @property
    def from_value(self):
        return self.metadata.get("start_value")


    @property
    def end_value(self):
        return self.metadata.get("end_value")


    @property
    def to_value(self):
        return self.metadata.get("end_value")


    @property
    def change_value(self):
        return self.metadata.get("change_value")


    @property
    def percent_change(self):
        return self.metadata.get("percent_change")


    @property
    def measurement_type(self):
        return self.metadata.get("measurement_type")


    @property
    def comparison_operator(self):
        return self.metadata.get("comparison_operator")


    @property
    def direction(self):
        return self.metadata.get("direction")


    @property
    def effect(self):
        return self.metadata.get("effect")


    @property
    def business_meaning(self):
        return self.metadata.get("business_meaning")