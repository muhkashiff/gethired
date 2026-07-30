from dataclasses import dataclass, field

@dataclass
class PracticeKnowledge:

    found: bool = False

    entity_id: str = ""

    canonical: str = ""

    category: str = ""

    business_area: str = ""

    confidence: float = 0.0

    impact_weight: float = 1.0

    source: str = ""

    metadata: dict = field(default_factory=dict)