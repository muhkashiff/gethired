"""
Enterprise Metrics Ontology

Enterprise V12

Defines enterprise KPIs and measurable business outcomes.

Metrics are used by:
- Achievement Scoring
- Business Value
- Executive Readiness
- Leadership Impact
"""

from .ontology_models import (
    OntologyItem,
    CapabilityWeight,
)

from .ontology_registry import registry


# ==========================================================
# Production Yield
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Production Yield",

        category="Metric",

        aliases=[
            "Yield",
            "Yield Improvement",
        ],

        description="Production Yield",

        capabilities=[

            CapabilityWeight(
                "Process Optimization",
                4.0,
            ),

            CapabilityWeight(
                "Operational Excellence",
                3.5,
            ),

            CapabilityWeight(
                "Manufacturing Efficiency",
                3.0,
            ),

        ],

    )

)


# ==========================================================
# Productivity
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Productivity",

        category="Metric",

        aliases=[],

        capabilities=[

            CapabilityWeight(
                "Operational Excellence",
                4.0,
            ),

            CapabilityWeight(
                "Business Value",
                3.5,
            ),

        ],

    )

)


# ==========================================================
# Cost Saving
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Cost Saving",

        category="Metric",

        aliases=[
            "Cost Reduction",
            "Savings",
        ],

        capabilities=[

            CapabilityWeight(
                "Business Value",
                5.0,
            ),

            CapabilityWeight(
                "Financial Impact",
                4.5,
            ),

            CapabilityWeight(
                "Operational Excellence",
                3.0,
            ),

        ],

    )

)


# ==========================================================
# Waste Reduction
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Waste",

        category="Metric",

        aliases=[
            "Waste Reduction",
            "Loss",
        ],

        capabilities=[

            CapabilityWeight(
                "Lean Manufacturing",
                4.0,
            ),

            CapabilityWeight(
                "Continuous Improvement",
                3.5,
            ),

        ],

    )

)


# ==========================================================
# Customer Complaints
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Customer Complaints",

        category="Metric",

        aliases=[
            "Customer Complaint",
        ],

        capabilities=[

            CapabilityWeight(
                "Customer Satisfaction",
                4.0,
            ),

            CapabilityWeight(
                "Quality Improvement",
                3.5,
            ),

        ],

    )

)


# ==========================================================
# Defect Rate
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Defect Rate",

        category="Metric",

        aliases=[
            "Defects",
        ],

        capabilities=[

            CapabilityWeight(
                "Quality Assurance",
                4.0,
            ),

            CapabilityWeight(
                "Process Optimization",
                3.0,
            ),

        ],

    )

)


# ==========================================================
# Downtime
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Downtime",

        category="Metric",

        aliases=[],

        capabilities=[

            CapabilityWeight(
                "Operational Excellence",
                4.0,
            ),

            CapabilityWeight(
                "Maintenance Excellence",
                3.0,
            ),

        ],

    )

)


# ==========================================================
# OEE
# ==========================================================

registry.register(

    OntologyItem(

        canonical="OEE",

        category="Metric",

        aliases=[
            "Overall Equipment Effectiveness",
        ],

        capabilities=[

            CapabilityWeight(
                "Manufacturing Excellence",
                5.0,
            ),

            CapabilityWeight(
                "Operational Excellence",
                4.0,
            ),

        ],

    )

)


# ==========================================================
# Throughput
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Throughput",

        category="Metric",

        aliases=[],

        capabilities=[

            CapabilityWeight(
                "Operational Excellence",
                4.0,
            ),

            CapabilityWeight(
                "Manufacturing Efficiency",
                3.0,
            ),

        ],

    )

)


# ==========================================================
# Inventory Accuracy
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Inventory Accuracy",

        category="Metric",

        aliases=[],

        capabilities=[

            CapabilityWeight(
                "Inventory Management",
                4.0,
            ),

            CapabilityWeight(
                "Supply Chain",
                3.0,
            ),

        ],

    )

)


# ==========================================================
# Audit Score
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Audit Score",

        category="Metric",

        aliases=[
            "Audit Result",
        ],

        capabilities=[

            CapabilityWeight(
                "Compliance",
                4.0,
            ),

            CapabilityWeight(
                "Auditing",
                4.0,
            ),

        ],

    )

)


# ==========================================================
# On Time Delivery
# ==========================================================

registry.register(

    OntologyItem(

        canonical="On Time Delivery",

        category="Metric",

        aliases=[
            "OTD",
            "OTIF",
        ],

        capabilities=[

            CapabilityWeight(
                "Supply Chain",
                4.0,
            ),

            CapabilityWeight(
                "Customer Satisfaction",
                3.5,
            ),

        ],

    )

)


# ==========================================================
# Quality Score
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Quality Score",

        category="Metric",

        aliases=[],

        capabilities=[

            CapabilityWeight(
                "Quality Assurance",
                4.5,
            ),

            CapabilityWeight(
                "Quality Systems",
                3.5,
            ),

        ],

    )

)