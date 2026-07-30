from dataclasses import dataclass
from typing import Optional


@dataclass
class DependencyEdge:

    source_entity: str

    target_entity: str

    relation: str

    confidence: float = 1.0

    sentence_index: int = 0

    clause_index: int = 0

    metadata: Optional[dict] = None