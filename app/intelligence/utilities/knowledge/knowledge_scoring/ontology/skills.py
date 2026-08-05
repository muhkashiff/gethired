"""
Enterprise Skills Ontology

Enterprise V12

Defines professional skills used throughout
all reasoning engines.

These are NOT resume keywords.

They represent enterprise capabilities.
"""

from .ontology_models import (
    OntologyItem,
    CapabilityWeight,
)

from .ontology_registry import registry


# ==========================================================
# HACCP
# ==========================================================

registry.register(

    OntologyItem(

        canonical="HACCP",

        category="Skill",

        aliases=[],

        description="Hazard Analysis Critical Control Points",

        capabilities=[

            CapabilityWeight("Food Safety", 4.0),

            CapabilityWeight("Risk Assessment", 3.5),

            CapabilityWeight("Preventive Controls", 3.0),

        ],

    )

)

# ==========================================================
# GMP
# ==========================================================

registry.register(

    OntologyItem(

        canonical="GMP",

        category="Skill",

        aliases=["Good Manufacturing Practices"],

        description="Good Manufacturing Practices",

        capabilities=[

            CapabilityWeight("Manufacturing Compliance", 3.5),

            CapabilityWeight("Food Safety", 2.5),

            CapabilityWeight("Operational Excellence", 2.5),

        ],

    )

)

# ==========================================================
# Internal Auditing
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Internal Auditing",

        category="Skill",

        aliases=["Internal Audit"],

        description="Internal Auditing",

        capabilities=[

            CapabilityWeight("Auditing", 4.0),

            CapabilityWeight("Compliance", 3.0),

            CapabilityWeight("Quality Systems", 2.5),

        ],

    )

)

# ==========================================================
# Supplier Auditing
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Supplier Auditing",

        category="Skill",

        aliases=[],

        description="Supplier Auditing",

        capabilities=[

            CapabilityWeight("Supplier Management", 3.5),

            CapabilityWeight("Auditing", 3.0),

            CapabilityWeight("Compliance", 2.5),

        ],

    )

)

# ==========================================================
# SPC
# ==========================================================

registry.register(

    OntologyItem(

        canonical="SPC",

        category="Skill",

        aliases=["Statistical Process Control"],

        description="SPC",

        capabilities=[

            CapabilityWeight("Statistical Analysis", 4.0),

            CapabilityWeight("Process Optimization", 3.5),

            CapabilityWeight("Quality Engineering", 3.0),

        ],

    )

)

# ==========================================================
# Root Cause Analysis
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Root Cause Analysis",

        category="Skill",

        aliases=["RCA"],

        description="Root Cause Analysis",

        capabilities=[

            CapabilityWeight("Problem Solving", 4.0),

            CapabilityWeight("Continuous Improvement", 3.0),

            CapabilityWeight("Corrective Action", 2.5),

        ],

    )

)

# ==========================================================
# CAPA
# ==========================================================

registry.register(

    OntologyItem(

        canonical="CAPA",

        category="Skill",

        aliases=["Corrective Action"],

        description="CAPA",

        capabilities=[

            CapabilityWeight("Corrective Action", 4.0),

            CapabilityWeight("Preventive Controls", 3.0),

            CapabilityWeight("Risk Reduction", 3.0),

        ],

    )

)

# ==========================================================
# Statistical Analysis
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Statistical Analysis",

        category="Skill",

        aliases=[],

        description="Statistics",

        capabilities=[

            CapabilityWeight("Data Analytics", 4.0),

            CapabilityWeight("Business Intelligence", 3.0),

            CapabilityWeight("Problem Solving", 2.5),

        ],

    )

)

# ==========================================================
# Python
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Python",

        category="Skill",

        aliases=[],

        description="Python",

        capabilities=[

            CapabilityWeight("Programming", 4.0),

            CapabilityWeight("Automation", 3.5),

            CapabilityWeight("Data Analytics", 3.0),

            CapabilityWeight("Machine Learning", 3.0),

        ],

    )

)

# ==========================================================
# SQL
# ==========================================================

registry.register(

    OntologyItem(

        canonical="SQL",

        category="Skill",

        aliases=[],

        description="SQL",

        capabilities=[

            CapabilityWeight("Database", 4.0),

            CapabilityWeight("Data Analytics", 3.5),

            CapabilityWeight("Reporting", 2.5),

        ],

    )

)

# ==========================================================
# Tableau
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Tableau",

        category="Skill",

        aliases=[],

        description="Tableau",

        capabilities=[

            CapabilityWeight("Business Intelligence", 4.0),

            CapabilityWeight("Reporting", 3.5),

            CapabilityWeight("Dashboarding", 3.0),

        ],

    )

)

# ==========================================================
# Power BI
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Power BI",

        category="Skill",

        aliases=["PowerBI"],

        description="Power BI",

        capabilities=[

            CapabilityWeight("Business Intelligence", 4.0),

            CapabilityWeight("Reporting", 3.5),

            CapabilityWeight("Dashboarding", 3.0),

        ],

    )

)

# ==========================================================
# Leadership
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Leadership",

        category="Skill",

        aliases=[],

        description="Leadership",

        capabilities=[

            CapabilityWeight("Leadership", 5.0),

            CapabilityWeight("People Management", 4.0),

            CapabilityWeight("Executive Readiness", 3.0),

        ],

    )

)

# ==========================================================
# Coaching
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Coaching",

        category="Skill",

        aliases=[],

        description="Coaching",

        capabilities=[

            CapabilityWeight("Leadership", 3.5),

            CapabilityWeight("People Development", 4.0),

            CapabilityWeight("Team Building", 3.5),

        ],

    )

)

# ==========================================================
# Project Management
# ==========================================================

registry.register(

    OntologyItem(

        canonical="Project Management",

        category="Skill",

        aliases=[],

        description="Project Management",

        capabilities=[

            CapabilityWeight("Project Delivery", 4.0),

            CapabilityWeight("Planning", 3.5),

            CapabilityWeight("Execution", 3.0),

        ],

    )

)