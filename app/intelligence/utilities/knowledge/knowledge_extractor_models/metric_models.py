"""
Metric Knowledge Model
"""

from dataclasses import dataclass
from dataclasses import dataclass, field

@dataclass
class MetricKnowledge:

    found: bool = False

    metric: str = ""

    canonical: str = ""

    category: str = ""

    unit: str = ""

    confidence: float = 0.0

    # ---------- Ontology ----------
    entity_id: str = ""

    business_area: str = ""

    source: str = ""

    metadata: dict = field(default_factory=dict)