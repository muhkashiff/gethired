"""
Enterprise Domain Ontology

Enterprise V12

Defines business and industry domains.

These domains become reusable across:

• Technical Scoring
• Leadership
• Business Value
• Executive Readiness
• ATS
"""

from .ontology_models import (
    OntologyItem,
    CapabilityWeight,
)

from .ontology_registry import registry


# ==========================================================
# Food Safety
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Food Safety",

        category="Domain",

        aliases=[
            "Food Quality",
        ],

        description="Food Safety",

        capabilities=[

            CapabilityWeight(
                "Food Safety Management",
                3.5,
            ),

            CapabilityWeight(
                "Regulatory Compliance",
                2.5,
            ),

            CapabilityWeight(
                "Risk Assessment",
                2.5,
            ),

        ],

    )

)

# ==========================================================
# Quality Assurance
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Quality Assurance",

        category="Domain",

        aliases=[
            "QA",
            "Quality",
        ],

        description="Quality Assurance",

        capabilities=[

            CapabilityWeight(
                "Quality Systems",
                3.5,
            ),

            CapabilityWeight(
                "Auditing",
                2.5,
            ),

            CapabilityWeight(
                "Continuous Improvement",
                2.5,
            ),

        ],

    )

)

# ==========================================================
# Manufacturing
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Manufacturing",

        category="Domain",

        aliases=[
            "Production",
        ],

        description="Manufacturing",

        capabilities=[

            CapabilityWeight(
                "Manufacturing Operations",
                3.0,
            ),

            CapabilityWeight(
                "Operational Excellence",
                3.0,
            ),

            CapabilityWeight(
                "Process Optimization",
                2.5,
            ),

        ],

    )

)

# ==========================================================
# Beverage Production
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Beverage Production",

        category="Domain",

        aliases=[
            "Juice Production",
            "Soft Drink Manufacturing",
        ],

        description="Beverage Manufacturing",

        capabilities=[

            CapabilityWeight(
                "Beverage Manufacturing",
                3.5,
            ),

            CapabilityWeight(
                "Production Planning",
                2.5,
            ),

            CapabilityWeight(
                "Yield Optimization",
                3.0,
            ),

        ],

    )

)

# ==========================================================
# Supply Chain
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Supply Chain",

        category="Domain",

        aliases=[
            "SCM",
        ],

        description="Supply Chain",

        capabilities=[

            CapabilityWeight(
                "Supply Chain Management",
                3.5,
            ),

            CapabilityWeight(
                "Inventory Management",
                2.5,
            ),

            CapabilityWeight(
                "Supplier Management",
                2.5,
            ),

        ],

    )

)

# ==========================================================
# Distribution
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Distribution",

        category="Domain",

        aliases=[],

        description="Distribution",

        capabilities=[

            CapabilityWeight(
                "Distribution Management",
                3.0,
            ),

            CapabilityWeight(
                "Warehouse Operations",
                2.0,
            ),

        ],

    )

)

# ==========================================================
# Retail
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Retail",

        category="Domain",

        aliases=[
            "Retail Operations",
        ],

        description="Retail",

        capabilities=[

            CapabilityWeight(
                "Retail Operations",
                3.5,
            ),

            CapabilityWeight(
                "Customer Service",
                2.5,
            ),

            CapabilityWeight(
                "Store Management",
                3.0,
            ),

        ],

    )

)

# ==========================================================
# Laboratory
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Laboratory",

        category="Domain",

        aliases=[
            "Lab",
        ],

        description="Laboratory",

        capabilities=[

            CapabilityWeight(
                "Laboratory Operations",
                3.5,
            ),

            CapabilityWeight(
                "Microbiology",
                2.5,
            ),

            CapabilityWeight(
                "Analytical Testing",
                2.5,
            ),

        ],

    )

)

# ==========================================================
# Compliance
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Compliance",

        category="Domain",

        aliases=[],

        description="Compliance",

        capabilities=[

            CapabilityWeight(
                "Regulatory Compliance",
                3.5,
            ),

            CapabilityWeight(
                "Risk Management",
                2.5,
            ),

        ],

    )

)

# ==========================================================
# Operations
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Operations",

        category="Domain",

        aliases=[],

        description="Operations",

        capabilities=[

            CapabilityWeight(
                "Operations Management",
                3.5,
            ),

            CapabilityWeight(
                "Operational Excellence",
                3.0,
            ),

            CapabilityWeight(
                "Business Operations",
                2.5,
            ),

        ],

    )

)