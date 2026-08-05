"""
Enterprise Methodologies Ontology

Enterprise V12

Knowledge of business methodologies,
problem solving techniques,
continuous improvement,
quality tools and operational excellence.
"""

from .ontology_models import (
    OntologyItem,
    CapabilityWeight,
)

from .ontology_registry import registry


# ==========================================================
# Root Cause Analysis
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Root Cause Analysis",

        category="Methodology",

        aliases=[
            "RCA",
        ],

        description="Root Cause Analysis",

        capabilities=[

            CapabilityWeight(
                "Problem Solving",
                3.0,
            ),

            CapabilityWeight(
                "Continuous Improvement",
                2.5,
            ),

            CapabilityWeight(
                "Quality Engineering",
                2.0,
            ),

        ],

    )

)


# ==========================================================
# CAPA
# ==========================================================

registry.register(

    OntologyItem(

        canonical="CAPA",

        category="Methodology",

        aliases=[
            "Corrective and Preventive Action",
        ],

        description="Corrective Action Preventive Action",

        capabilities=[

            CapabilityWeight(
                "Corrective Action",
                3.0,
            ),

            CapabilityWeight(
                "Risk Reduction",
                2.5,
            ),

            CapabilityWeight(
                "Quality Systems",
                2.0,
            ),

        ],

    )

)


# ==========================================================
# SPC
# ==========================================================

registry.register(

    OntologyItem(

        canonical="SPC",

        category="Methodology",

        aliases=[
            "Statistical Process Control",
        ],

        description="Statistical Process Control",

        capabilities=[

            CapabilityWeight(
                "Statistical Analysis",
                3.0,
            ),

            CapabilityWeight(
                "Process Optimization",
                2.5,
            ),

            CapabilityWeight(
                "Quality Improvement",
                2.0,
            ),

        ],

    )

)


# ==========================================================
# Lean
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Lean",

        category="Methodology",

        aliases=[
            "Lean Manufacturing",
        ],

        description="Lean Manufacturing",

        capabilities=[

            CapabilityWeight(
                "Operational Excellence",
                3.0,
            ),

            CapabilityWeight(
                "Waste Reduction",
                3.0,
            ),

            CapabilityWeight(
                "Continuous Improvement",
                2.5,
            ),

        ],

    )

)


# ==========================================================
# Six Sigma
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Six Sigma",

        category="Methodology",

        aliases=[
            "Green Belt",
            "Black Belt",
        ],

        description="Six Sigma",

        capabilities=[

            CapabilityWeight(
                "Process Optimization",
                3.5,
            ),

            CapabilityWeight(
                "Statistical Analysis",
                3.5,
            ),

            CapabilityWeight(
                "Continuous Improvement",
                3.0,
            ),

            CapabilityWeight(
                "Business Improvement",
                2.5,
            ),

        ],

    )

)


# ==========================================================
# DMAIC
# ==========================================================

registry.register(

    OntologyItem(

        canonical="DMAIC",

        category="Methodology",

        aliases=[],

        description="Define Measure Analyze Improve Control",

        capabilities=[

            CapabilityWeight(
                "Continuous Improvement",
                3.0,
            ),

            CapabilityWeight(
                "Process Optimization",
                3.0,
            ),

            CapabilityWeight(
                "Statistical Analysis",
                2.5,
            ),

        ],

    )

)


# ==========================================================
# Kaizen
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Kaizen",

        category="Methodology",

        aliases=[],

        description="Kaizen",

        capabilities=[

            CapabilityWeight(
                "Continuous Improvement",
                3.0,
            ),

            CapabilityWeight(
                "Operational Excellence",
                2.5,
            ),

        ],

    )

)


# ==========================================================
# PDCA
# ==========================================================

registry.register(

    OntologyItem(

        canonical="PDCA",

        category="Methodology",

        aliases=[
            "Plan Do Check Act",
        ],

        description="PDCA",

        capabilities=[

            CapabilityWeight(
                "Quality Management",
                3.0,
            ),

            CapabilityWeight(
                "Continuous Improvement",
                2.5,
            ),

        ],

    )

)


# ==========================================================
# FMEA
# ==========================================================

registry.register(

    OntologyItem(

        canonical="FMEA",

        category="Methodology",

        aliases=[
            "Failure Mode and Effects Analysis",
        ],

        description="Failure Mode Effect Analysis",

        capabilities=[

            CapabilityWeight(
                "Risk Assessment",
                3.5,
            ),

            CapabilityWeight(
                "Preventive Controls",
                3.0,
            ),

            CapabilityWeight(
                "Quality Engineering",
                2.5,
            ),

        ],

    )

)


# ==========================================================
# Fishbone
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Fishbone",

        category="Methodology",

        aliases=[
            "Ishikawa",
            "Cause and Effect",
        ],

        description="Fishbone Diagram",

        capabilities=[

            CapabilityWeight(
                "Problem Solving",
                2.5,
            ),

            CapabilityWeight(
                "Root Cause Analysis",
                2.5,
            ),

        ],

    )

)


# ==========================================================
# 5 Why
# ==========================================================

registry.register(

    OntologyItem(

        canonical="5 Why",

        category="Methodology",

        aliases=[
            "Five Why",
        ],

        description="Five Why Analysis",

        capabilities=[

            CapabilityWeight(
                "Problem Solving",
                2.5,
            ),

            CapabilityWeight(
                "Root Cause Analysis",
                3.0,
            ),

        ],

    )

)