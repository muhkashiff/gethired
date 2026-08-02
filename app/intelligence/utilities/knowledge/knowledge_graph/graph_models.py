"""
Enterprise Knowledge Graph Models

Defines:

- GraphNode
- GraphEdge
- GraphStatistics

Every extracted KnowledgeEntity becomes a GraphNode.

Every KnowledgeRelation becomes a GraphEdge.

Enterprise V5
"""

from dataclasses import dataclass, field


# ==========================================================
# GRAPH NODE
# ==========================================================

@dataclass
class GraphNode:

    ####################################################################
    # Identity
    ####################################################################

    node_id: str = ""

    entity_id: str = ""

    entity_type: str = ""

    ontology_name: str = ""

    ####################################################################
    # Display
    ####################################################################

    label: str = ""

    canonical: str = ""

    category: str = ""

    ####################################################################
    # Business
    ####################################################################

    domain: str = ""

    business_area: str = ""

    impact_weight: float = 1.0

    ####################################################################
    # Metadata
    ####################################################################

    metadata: dict = field(default_factory=dict)

    ####################################################################
    # Graph
    ####################################################################

    incoming_edges: list = field(default_factory=list)

    outgoing_edges: list = field(default_factory=list)


# ==========================================================
# GRAPH EDGE
# ==========================================================

@dataclass
class GraphEdge:

    ####################################################################
    # Identity
    ####################################################################

    edge_id: str = ""

    relation: str = ""

    confidence: float = 0.0

    ####################################################################
    # Source
    ####################################################################

    source_id: str = ""

    source_type: str = ""

    ####################################################################
    # Target
    ####################################################################

    target_id: str = ""

    target_type: str = ""

    ####################################################################
    # Explainability
    ####################################################################

    reasoning: str = ""

    ####################################################################
    # Metadata
    ####################################################################

    metadata: dict = field(default_factory=dict)


# ==========================================================
# GRAPH STATISTICS
# ==========================================================

@dataclass
class GraphStatistics:

    node_count: int = 0

    edge_count: int = 0

    entity_counts: dict = field(default_factory=dict)

    relation_counts: dict = field(default_factory=dict)