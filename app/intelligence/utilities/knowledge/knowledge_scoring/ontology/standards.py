"""
Enterprise Standards Ontology

Enterprise V12

Single source of truth for all
Quality & Food Safety Standards.
"""

from .ontology_models import (
    OntologyItem,
    CapabilityWeight,
)

from .ontology_registry import registry


# ==========================================================
# ISO 9001
# ==========================================================

registry.register(

    OntologyItem(

        canonical="ISO 9001",

        category="Standard",

        aliases=[

            "ISO9001",

            "QMS",

            "Quality Management System",

        ],

        description="Quality Management System",

        capabilities=[

            CapabilityWeight(
                "Quality Management Systems",
                3.0,
            ),

            CapabilityWeight(
                "Auditing",
                2.0,
            ),

            CapabilityWeight(
                "Process Improvement",
                2.0,
            ),

            CapabilityWeight(
                "Continuous Improvement",
                2.0,
            ),

            CapabilityWeight(
                "Risk Based Thinking",
                1.5,
            ),

        ],

    )

)

# ==========================================================
# FSSC22000
# ==========================================================

registry.register(

    OntologyItem(

        canonical="FSSC22000",

        category="Standard",

        aliases=[

            "FSSC 22000",

            "FSSC",

        ],

        description="Food Safety System Certification",

        capabilities=[

            CapabilityWeight(
                "Food Safety Management Systems",
                3.0,
            ),

            CapabilityWeight(
                "HACCP",
                3.0,
            ),

            CapabilityWeight(
                "Risk Assessment",
                2.5,
            ),

            CapabilityWeight(
                "Prerequisite Programs",
                2.0,
            ),

            CapabilityWeight(
                "Regulatory Compliance",
                2.0,
            ),

        ],

    )

)

# ==========================================================
# ISO 22000
# ==========================================================

registry.register(

    OntologyItem(

        canonical="ISO 22000",

        category="Standard",

        aliases=[

            "ISO22000",

        ],

        description="Food Safety Management System",

        capabilities=[

            CapabilityWeight(
                "Food Safety Management Systems",
                3.0,
            ),

            CapabilityWeight(
                "HACCP",
                2.5,
            ),

            CapabilityWeight(
                "Risk Assessment",
                2.0,
            ),

        ],

    )

)

# ==========================================================
# BRCGS
# ==========================================================

registry.register(

    OntologyItem(

        canonical="BRCGS",

        category="Standard",

        aliases=[

            "BRC",

            "British Retail Consortium",

            "Global Standard Food Safety",

        ],

        description="BRCGS Global Standard",

        capabilities=[

            CapabilityWeight(
                "Food Safety Management Systems",
                3.0,
            ),

            CapabilityWeight(
                "Supplier Management",
                2.5,
            ),

            CapabilityWeight(
                "Auditing",
                2.5,
            ),

            CapabilityWeight(
                "Product Safety",
                2.0,
            ),

        ],

    )

)

# ==========================================================
# HACCP
# ==========================================================

registry.register(

    OntologyItem(

        canonical="HACCP",

        category="Standard",

        aliases=[],

        description="Hazard Analysis Critical Control Points",

        capabilities=[

            CapabilityWeight(
                "Hazard Analysis",
                3.0,
            ),

            CapabilityWeight(
                "Risk Assessment",
                3.0,
            ),

            CapabilityWeight(
                "Critical Control Points",
                2.5,
            ),

            CapabilityWeight(
                "Food Safety",
                2.5,
            ),

        ],

    )

)

# ==========================================================
# GMP
# ==========================================================

registry.register(

    OntologyItem(

        canonical="GMP",

        category="Standard",

        aliases=[

            "Good Manufacturing Practices",

        ],

        description="Good Manufacturing Practices",

        capabilities=[

            CapabilityWeight(
                "Manufacturing Compliance",
                2.5,
            ),

            CapabilityWeight(
                "Operational Excellence",
                2.0,
            ),

            CapabilityWeight(
                "Food Safety",
                2.0,
            ),

        ],

    )

)

# ==========================================================
# PCQI
# ==========================================================

registry.register(

    OntologyItem(

        canonical="PCQI",

        category="Certification",

        aliases=[

            "Preventive Controls Qualified Individual",

        ],

        description="FSPCA PCQI",

        capabilities=[

            CapabilityWeight(
                "Preventive Controls",
                3.0,
            ),

            CapabilityWeight(
                "Food Safety",
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
# FSPCA
# ==========================================================

registry.register(

    OntologyItem(

        canonical="FSPCA",

        category="Organization",

        aliases=[],

        description="Food Safety Preventive Controls Alliance",

        capabilities=[

            CapabilityWeight(
                "Preventive Controls",
                2.5,
            ),

            CapabilityWeight(
                "Food Safety",
                2.0,
            ),

        ],

    )

)