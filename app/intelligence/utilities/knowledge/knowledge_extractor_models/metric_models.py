"""
Metric Knowledge Model
"""

from dataclasses import dataclass


@dataclass
class MetricKnowledge:
    """
    Represents a business KPI or measurable metric
    extracted from a sentence.
    """

    found: bool = False

    metric: str = ""

    canonical: str = ""

    category: str = ""

    unit: str = ""

    confidence: float = 0.0