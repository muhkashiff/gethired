from dataclasses import dataclass, field
from typing import Dict


@dataclass
class EntityResult:

    entity_id: str = ""

    entity_type: str = ""

    canonical: str = ""

    matched_text: str = ""

    confidence: float = 0.0

    category: str = ""

    business_area: str = ""

    source: str = ""

    priority: int = 0

    metadata: Dict = field(default_factory=dict)