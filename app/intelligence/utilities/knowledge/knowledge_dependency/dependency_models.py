from dataclasses import dataclass
from typing import List, Dict


@dataclass
class DependencyEdge:

    source_entity: str

    target_entity: str

    relation: str

    confidence: float = 1.0

    metadata: Dict = None


@dataclass
class DependencyGraph:

    edges: List[DependencyEdge]

    confidence: float = 1.0