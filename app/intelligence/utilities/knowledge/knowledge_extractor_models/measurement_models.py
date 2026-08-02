"""
Enterprise Measurement Knowledge Model

Represents quantitative measurements extracted from text.

Examples

99%
70 → 99%
4 Hours
15 Days
$2 Million
5000 Units
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class MeasurementKnowledge(KnowledgeEntity):

    ####################################################################
    # Entity
    ####################################################################

    entity_type: str = "measurement"

    ontology_name: str = "measurements"

    ####################################################################
    # Raw Measurement
    ####################################################################

    value: str = ""

    numeric_value: float = 0.0

    normalized_value: float = 0.0

    unit: str = ""

    operator: str = ""

    ####################################################################
    # Measurement Type
    ####################################################################

    measurement_type: str = ""

    # absolute
    # percentage
    # currency
    # duration
    # quantity
    # ratio
    # range

    ####################################################################
    # Change Detection
    ####################################################################

    from_value: float | None = None

    to_value: float | None = None

    change_value: float | None = None

    percent_change: float | None = None

    comparison_operator: str = ""

    ####################################################################
    # Direction
    ####################################################################

    direction: str = ""

    # increase
    # decrease
    # unchanged

    improvement: bool = False
    

    ####################################################################
    # Business Meaning
    ####################################################################

    effect: str = ""

    business_meaning: str = ""

    ####################################################################
    # Semantic Links
    ####################################################################

    # Metric this measurement belongs to
    metric: str = ""

    # Original metric object
    metric_object: object | None = None

    # Object being measured
    target: str = ""

    target_object: object | None = None

    # Modifier
    modifier: str = ""

    modifier_object: object | None = None

    # Standard
    standard: str = ""

    standard_object: object | None = None

    # Domain
    domain: str = ""

    domain_object: object | None = None

    ####################################################################
    # Validation
    ####################################################################

    valid_measurement: bool = True