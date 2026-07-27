"""
Knowledge Graph Models

Universal graph container used throughout
the Intelligence Engine.
"""

from dataclasses import dataclass, field
from typing import Dict, List


# --------------------------------------------------------
# Graph Node
# --------------------------------------------------------

@dataclass
class GraphNode:

    id: str

    label: str

    node_type: str

    attributes: Dict = field(default_factory=dict)


# --------------------------------------------------------
# Graph Edge
# --------------------------------------------------------

@dataclass
class GraphEdge:

    source: str

    target: str

    relation: str

    confidence: float = 1.0


# --------------------------------------------------------
# Knowledge Graph
# --------------------------------------------------------

@dataclass
class KnowledgeGraph:

    nodes: List[GraphNode] = field(default_factory=list)

    edges: List[GraphEdge] = field(default_factory=list)