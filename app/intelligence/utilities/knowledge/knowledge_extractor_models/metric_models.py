"""
Metric Knowledge Model

Represents a Business KPI detected from a sentence.

Examples

Production Yield
Customer Complaints
Downtime
Efficiency
Productivity
"""

from dataclasses import dataclass, field


@dataclass
class MetricKnowledge:

    # ---------------------------------------------------------
    # Detection
    # ---------------------------------------------------------

    found: bool = False

    confidence: float = 0.0

    # ---------------------------------------------------------
    # Linguistic
    # ---------------------------------------------------------

    metric: str = ""

    canonical: str = ""

    category: str = ""

    unit: str = ""

    # ---------------------------------------------------------
    # Ontology
    # ---------------------------------------------------------

    entity_id: str = ""

    business_area: str = ""

    impact_weight: float = 1.0

    preferred_unit: str = ""

    higher_is_better: bool = True

    source: str = ""

    metadata: dict = field(default_factory=dict)