"""
Generic Knowledge Entity
"""

from dataclasses import dataclass, field



@dataclass
class KnowledgeEntity:

    entity_id: str = ""

    entity_type: str = ""

    canonical: str = ""

    matched_text: str = ""

    category: str = ""

    business_area: str = ""

    confidence: float = 0.0

    metadata: dict = field(default_factory=dict)

    