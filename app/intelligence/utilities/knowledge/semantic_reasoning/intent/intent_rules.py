"""
Enterprise Intent Rules

Business reasoning rules.

Enterprise V5
"""

INTENT_RULES = [

    # ==========================================================
    # COMPLIANCE
    # ==========================================================

    {

        "id": "compliance",

        "actions": [

            "implement",

            "certify",

            "audit",

            "validate",

        ],

        "requires": [

            "standards",

        ],

        "intent": "compliance",

        "primary_domain": "Quality",

        "business_area": "Food Safety",

        "achievement": True,

        "confidence": 0.99,

    },

    # ==========================================================
    # CONTINUOUS IMPROVEMENT
    # ==========================================================

    {

        "id": "continuous_improvement",

        "actions": [

            "improve",

            "increase",

            "reduce",

            "optimize",

        ],

        "requires": [],

        "intent": "continuous_improvement",

        "primary_domain": "Operations",

        "business_area": "Continuous Improvement",

        "achievement": True,

        "confidence": 0.99,

    },

    # ==========================================================
    # LEADERSHIP
    # ==========================================================

    {

        "id": "leadership",

        "actions": [

            "lead",

            "mentor",

            "coach",

            "supervise",

            "direct",

        ],

        "requires": [],

        "intent": "leadership",

        "primary_domain": "Management",

        "business_area": "Leadership",

        "achievement": False,

        "confidence": 0.98,

    },

    # ==========================================================
    # OPERATIONS MANAGEMENT
    # ==========================================================

    {

        "id": "operations_management",

        "actions": [

            "manage",

        ],

        "requires": [

            "objects",

        ],

        "intent": "operations_management",

        "primary_domain": "Operations",

        "business_area": "Operations",

        "achievement": False,

        "confidence": 0.98,

    },

    # ==========================================================
    # PROBLEM SOLVING
    # ==========================================================

    {

        "id": "problem_solving",

        "actions": [

            "perform",

            "analyze",

            "investigate",

            "diagnose",

        ],

        "requires": [

            "methodologies",

        ],

        "intent": "problem_solving",

        "primary_domain": "Quality",

        "business_area": "Root Cause Analysis",

        "achievement": False,

        "confidence": 0.97,

    },

    # ==========================================================
    # DEVELOPMENT
    # ==========================================================

    {

        "id": "development",

        "actions": [

            "develop",

            "design",

            "build",

            "create",

        ],

        "requires": [],

        "intent": "development",

        "primary_domain": "Engineering",

        "business_area": "Development",

        "achievement": False,

        "confidence": 0.95,

    },

]