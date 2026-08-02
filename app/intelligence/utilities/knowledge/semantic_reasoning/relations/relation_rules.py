"""
Enterprise Relation Rules

Defines semantic relationships between extracted entities.

Enterprise V5
"""

RELATION_RULES = [

    # ==========================================================
    # ACTION → OBJECT
    # ==========================================================

    {
        "source": "action",
        "target": "object",
        "relation": "acts_on",
    },

    # ==========================================================
    # ACTION → STANDARD
    # ==========================================================

    {
        "source": "action",
        "target": "standard",
        "relation": "acts_on",
    },

    # ==========================================================
    # ACTION → METHODOLOGY
    # ==========================================================

    {
        "source": "action",
        "target": "methodology",
        "relation": "uses",
    },

    # ==========================================================
    # ACTION → TECHNOLOGY
    # ==========================================================

    {
        "source": "action",
        "target": "technology",
        "relation": "uses",
    },

    # ==========================================================
    # ACTION → SKILL
    # ==========================================================

    {
        "source": "action",
        "target": "skill",
        "relation": "requires",
    },

    # ==========================================================
    # ACTION → METRIC
    # ==========================================================

    {
        "source": "action",
        "target": "metric",
        "relation": "changes",
    },

    # ==========================================================
    # METRIC → MEASUREMENT
    # ==========================================================

    {
        "source": "metric",
        "target": "measurement",
        "relation": "measured_by",
    },

    # ==========================================================
    # STANDARD → DOMAIN
    # ==========================================================

    {
        "source": "standard",
        "target": "domain",
        "relation": "belongs_to",
    },

    # ==========================================================
    # OBJECT → DOMAIN
    # ==========================================================

    {
        "source": "object",
        "target": "domain",
        "relation": "belongs_to",
    },

    # ==========================================================
    # METHODOLOGY → DOMAIN
    # ==========================================================

    {
        "source": "methodology",
        "target": "domain",
        "relation": "belongs_to",
    },

    # ==========================================================
    # TECHNOLOGY → DOMAIN
    # ==========================================================

    {
        "source": "technology",
        "target": "domain",
        "relation": "belongs_to",
    },

    # ==========================================================
    # CERTIFICATION → DOMAIN
    # ==========================================================

    {
        "source": "certification",
        "target": "domain",
        "relation": "belongs_to",
    },

    # ==========================================================
    # INTENT → DOMAIN
    # ==========================================================

    {
        "source": "intent",
        "target": "domain",
        "relation": "supports",
    },

    # ==========================================================
    # INTENT → STANDARD
    # ==========================================================

    {
        "source": "intent",
        "target": "standard",
        "relation": "driven_by",
    },

    # ==========================================================
    # INTENT → OBJECT
    # ==========================================================

    {
        "source": "intent",
        "target": "object",
        "relation": "targets",
    },

]