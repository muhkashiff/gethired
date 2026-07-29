"""
Metric Reasoner

Repairs missing KPI information before
Measurement Extraction begins.
"""

from .metric_defaults import MetricDefaults
from .temporary_metric_builder import TemporaryMetricBuilder


class MetricReasoner:

    def __init__(self):

        self.builder = TemporaryMetricBuilder()

    def reason(

        self,

        text,

        metric,

        action=None,

        obj=None,

    ):

        # -----------------------------
        # Already identified
        # -----------------------------

        if metric.found:

            return metric

        sentence = text.lower()

        # -----------------------------
        # Infer temporary KPI
        # -----------------------------

        patterns = [

            "availability",

            "uptime",

            "downtime",

            "yield",

            "efficiency",

            "waste",

            "inventory",

            "stock",

            "complaints",

            "complaint",

            "defect",

            "audit",

            "cost",

            "saving",

            "revenue",

            "profit",

            "team",

            "training",

            "safety",

        ]

        for pattern in patterns:

            if pattern in sentence:

                return self.builder.build(pattern)

        # -----------------------------
        # No KPI
        # -----------------------------

        return MetricDefaults.unknown()