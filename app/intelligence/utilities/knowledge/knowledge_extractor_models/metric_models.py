"""
Enterprise Metric Knowledge Model

Represents business metrics extracted from text.

Examples

Yield
Efficiency
Productivity
Quality Score
Customer Satisfaction
Downtime
OEE
Waste
Complaint Rate
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class MetricKnowledge(KnowledgeEntity):

    ####################################################################
    # Entity
    ####################################################################

    entity_type: str = "metric"

    ontology_name: str = "metrics"

    ####################################################################
    # Metric Definition
    ####################################################################

    metric_family: str = ""

    metric_group: str = ""

    unit: str = ""

    ####################################################################
    # Behaviour
    ####################################################################

    higher_is_better: bool = True

    lower_is_better: bool = False

    percentage_metric: bool = False

    financial_metric: bool = False

    quality_metric: bool = False

    productivity_metric: bool = False

    operational_metric: bool = False

    ####################################################################
    # Business
    ####################################################################

    kpi: bool = False

    benchmark_available: bool = False

    target_value: float = 0.0

    ####################################################################
    # Parsing
    ####################################################################

    measurement_expected: bool = True