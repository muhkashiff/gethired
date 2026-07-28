"""
Measurement Knowledge Model

Represents one measurable business KPI.

Examples

Production Yield = 99%

Customer Complaints = -60%

Cost Savings = $2M
"""

from dataclasses import dataclass, field


@dataclass
class MeasurementKnowledge:

    # ---------------------------------------------------------
    # Detection
    # ---------------------------------------------------------

    found: bool = False

    confidence: float = 0.0

    # ---------------------------------------------------------
    # Metric Information
    # ---------------------------------------------------------

    metric: str = ""

    canonical: str = ""

    category: str = ""

    # ---------------------------------------------------------
    # Measurement
    # ---------------------------------------------------------

    value: str = ""

    numeric_value: float = 0.0

    normalized_value: float = 0.0

    unit: str = ""

    operator: str = ""

    # ---------------------------------------------------------
    # Business Interpretation
    # (Added by MeasurementReasoner)
    # ---------------------------------------------------------

    direction: str = ""

    effect: str = ""

    business_meaning: str = ""

    # ---------------------------------------------------------
    # Ontology
    # ---------------------------------------------------------

    entity_id: str = ""

    business_area: str = ""

    impact_weight: float = 1.0

    source: str = ""

    metadata: dict = field(default_factory=dict)