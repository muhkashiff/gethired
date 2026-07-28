"""
Scoring Constants

Global scoring weights used by all
knowledge scoring engines.

Changing weights here automatically
updates the entire scoring system.

This file should NEVER contain business logic.

Only configuration.
"""

# ----------------------------------------------------------
# Resume Score Weights
# ----------------------------------------------------------

RESUME_WEIGHTS = {

    "leadership": 20,

    "seniority": 15,

    "business_impact": 20,

    "executive": 15,

    "domain_expertise": 10,

    "technical": 10,

    "achievement": 10,

}

# ----------------------------------------------------------
# Leadership
# ----------------------------------------------------------

LEADERSHIP_WEIGHTS = {

    "leadership_action": 4,

    "leadership_domain": 3,

    "people_object": 3,

    "executive_modifier": 2,

    "positive_measurement": 2,

}

# ----------------------------------------------------------
# Seniority
# ----------------------------------------------------------

SENIORITY_WEIGHTS = {

    "strategy": 5,

    "leadership": 4,

    "management": 4,

    "implementation": 2,

    "optimization": 2,

}

# ----------------------------------------------------------
# Executive Readiness
# ----------------------------------------------------------

EXECUTIVE_WEIGHTS = {

    "strategy": 5,

    "transformation": 5,

    "leadership": 4,

    "financial": 4,

    "business_growth": 5,

    "innovation": 4,

}

# ----------------------------------------------------------
# Achievement
# ----------------------------------------------------------

ACHIEVEMENT_WEIGHTS = {

    "quantified": 4,

    "positive_measurement": 4,

    "optimization": 2,

    "implementation": 2,

}

# ----------------------------------------------------------
# Domain Expertise
# ----------------------------------------------------------

DOMAIN_WEIGHTS = {

    "food_safety": 4,

    "quality": 4,

    "operations": 3,

    "manufacturing": 3,

    "finance": 3,

    "leadership": 3,

    "people": 2,

}

# ----------------------------------------------------------
# Score Levels
# ----------------------------------------------------------

SCORE_LEVELS = {

    "Exceptional": 95,

    "Excellent": 90,

    "Very Strong": 80,

    "Strong": 70,

    "Moderate": 60,

    "Developing": 50,

    "Weak": 0,

}

# ----------------------------------------------------------
# Executive Threshold
# ----------------------------------------------------------

EXECUTIVE_THRESHOLD = 80

# ----------------------------------------------------------
# Manager Threshold
# ----------------------------------------------------------

MANAGER_THRESHOLD = 65

# ----------------------------------------------------------
# Leadership Threshold
# ----------------------------------------------------------

LEADERSHIP_THRESHOLD = 70