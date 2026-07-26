"""
Measurement Knowledge Model
"""

from dataclasses import dataclass


@dataclass
class MeasurementKnowledge:
    """
    Represents one measurable business KPI.

    Example

    Production Yield = 99%

    Customer Complaints = -60%

    Cost Savings = $2M
    """

    found: bool = False

    metric: str = ""

    canonical: str = ""

    category: str = ""

    value: str = ""

    numeric_value: float = 0.0

    normalized_value: float = 0.0

    unit: str = ""

    operator: str = ""

    # Added by MeasurementReasoner

    direction: str = ""

    effect: str = ""

    business_meaning: str = ""

    confidence: float = 0.0