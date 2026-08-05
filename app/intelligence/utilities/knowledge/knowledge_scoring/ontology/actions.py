"""
Enterprise Actions Ontology

Enterprise V12

Defines enterprise business actions.

Actions describe WHAT the professional actually DOES.
"""

from .ontology_models import (
    OntologyItem,
    CapabilityWeight,
)

from .ontology_registry import registry


# ==========================================================
# Implement
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Implement",

        category="Action",

        aliases=[
            "Implemented",
            "Implementation",
        ],

        description="Implementation",

        capabilities=[

            CapabilityWeight(
                "Execution",
                4.0,
            ),

            CapabilityWeight(
                "Project Delivery",
                3.5,
            ),

            CapabilityWeight(
                "Operational Excellence",
                2.5,
            ),

        ],

    )

)

# ==========================================================
# Develop
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Develop",

        category="Action",

        aliases=[
            "Developed",
            "Designed",
            "Created",
            "Built",
        ],

        description="Development",

        capabilities=[

            CapabilityWeight(
                "Innovation",
                3.5,
            ),

            CapabilityWeight(
                "Solution Design",
                3.5,
            ),

            CapabilityWeight(
                "Process Improvement",
                3.0,
            ),

        ],

    )

)

# ==========================================================
# Improve
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Improve",

        category="Action",

        aliases=[
            "Improved",
            "Increase",
            "Increased",
            "Enhanced",
            "Optimized",
        ],

        description="Improvement",

        capabilities=[

            CapabilityWeight(
                "Continuous Improvement",
                4.0,
            ),

            CapabilityWeight(
                "Operational Excellence",
                3.5,
            ),

            CapabilityWeight(
                "Business Value",
                3.0,
            ),

        ],

    )

)

# ==========================================================
# Manage
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Manage",

        category="Action",

        aliases=[
            "Managed",
            "Managing",
            "Supervised",
            "Led",
        ],

        description="Management",

        capabilities=[

            CapabilityWeight(
                "Leadership",
                4.5,
            ),

            CapabilityWeight(
                "People Management",
                4.0,
            ),

            CapabilityWeight(
                "Executive Readiness",
                3.0,
            ),

        ],

    )

)

# ==========================================================
# Audit
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Audit",

        category="Action",

        aliases=[
            "Audited",
            "Audit",
            "Inspected",
            "Verified",
        ],

        description="Auditing",

        capabilities=[

            CapabilityWeight(
                "Auditing",
                4.0,
            ),

            CapabilityWeight(
                "Compliance",
                3.5,
            ),

            CapabilityWeight(
                "Quality Assurance",
                3.0,
            ),

        ],

    )

)

# ==========================================================
# Train
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Train",

        category="Action",

        aliases=[
            "Trained",
            "Training",
            "Mentored",
            "Coached",
        ],

        description="Training",

        capabilities=[

            CapabilityWeight(
                "People Development",
                4.0,
            ),

            CapabilityWeight(
                "Leadership",
                3.5,
            ),

            CapabilityWeight(
                "Knowledge Transfer",
                3.0,
            ),

        ],

    )

)