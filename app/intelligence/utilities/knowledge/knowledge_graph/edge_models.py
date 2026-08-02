"""
Knowledge Graph Edge Models

Edges define semantic relationships between nodes.

Examples

Implemented  ----targets----> FSSC 22000

Implemented  ----improved----> Production Yield

Production Yield ----measured_by----> 99%

FSSC22000 ----belongs_to----> Food Safety

Cross Functional ----supports----> Leadership
"""

from dataclasses import dataclass, field


@dataclass
class GraphEdge:
    """
    Universal Graph Relationship
    """

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    edge_id: str = ""

    # --------------------------------------------------
    # Graph Connection
    # --------------------------------------------------

    source_id: str = ""

    target_id: str = ""
    # --------------------------------------------------
    # Relationship
    # --------------------------------------------------

    relation: str = ""

    relationship_label: str = ""

    direction: str = "forward"

    # --------------------------------------------------
    # Confidence
    # --------------------------------------------------

    confidence: float = 1.0

    weight: float = 1.0

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    source: str = "knowledge_pipeline"

    metadata: dict = field(default_factory=dict)

    # --------------------------------------------------
    # BACK COMPATIBILITY
    # --------------------------------------------------

    @property
    def source_node(self):
        return self.source_id


    @property
    def target_node(self):
        return self.target_id


    @property
    def relationship(self):
        return self.relation