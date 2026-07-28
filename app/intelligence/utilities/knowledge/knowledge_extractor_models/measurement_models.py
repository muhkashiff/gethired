"""
Measurement Knowledge Model

Represents one measurable business KPI.

Examples

Production Yield = 99%

Customer Complaints = -60%

Cost Savings = $2M

NEW

Supports

    • from → to measurements
    • delta measurements
    • absolute measurements
    • percent change
"""

from dataclasses import dataclass, field


@dataclass
class MeasurementKnowledge:

    # =========================================================
    # Detection
    # =========================================================

    found: bool = False

    confidence: float = 0.0

    # =========================================================
    # Metric Information
    # =========================================================

    metric: str = ""

    canonical: str = ""

    category: str = ""

    # =========================================================
    # Original Measurement
    # =========================================================

    value: str = ""

    numeric_value: float = 0.0

    normalized_value: float = 0.0

    unit: str = ""

    operator: str = ""

    # =========================================================
    # NEW
    # Advanced Measurement Information
    # =========================================================

    measurement_type: str = ""
    # range
    # delta
    # absolute

    from_value: float | None = None

    to_value: float | None = None

    change_value: float | None = None

    percent_change: float | None = None

    comparison_operator: str = ""

    # =========================================================
    # Business Interpretation
    # =========================================================

    direction: str = ""

    effect: str = ""

    business_meaning: str = ""

    # =========================================================
    # Ontology
    # =========================================================

    entity_id: str = ""

    business_area: str = ""

    impact_weight: float = 1.0

    source: str = ""

    # =========================================================
    # Metadata
    # =========================================================

    metadata: dict = field(default_factory=dict)

    # =========================================================
    # Convenience Properties
    # =========================================================

    @property
    def has_range(self):

        return (

            self.from_value is not None

            and

            self.to_value is not None

        )

    # ---------------------------------------------------------

    @property
    def has_delta(self):

        return self.change_value is not None

    # ---------------------------------------------------------

    @property
    def is_percentage(self):

        return self.unit == "%"

    # ---------------------------------------------------------

    @property
    def improvement(self):

        if self.direction.lower() == "increase":

            return True

        if self.direction.lower() == "positive":

            return True

        return False

    # ---------------------------------------------------------

    def summary(self):

        return {

            "metric": self.metric,

            "value": self.value,

            "numeric_value": self.numeric_value,

            "unit": self.unit,

            "measurement_type": self.measurement_type,

            "from_value": self.from_value,

            "to_value": self.to_value,

            "change_value": self.change_value,

            "percent_change": self.percent_change,

            "direction": self.direction,

            "effect": self.effect,

            "confidence": self.confidence,

        }