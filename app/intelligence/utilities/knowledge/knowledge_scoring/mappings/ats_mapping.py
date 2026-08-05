"""
Enterprise ATS Capability Mapping

Enterprise V12

Maps enterprise capabilities into ATS relevance buckets.

These buckets are later used to calculate
Resume ↔ Job Description similarity.
"""

ATS_MAPPING = {

    # ==========================================================
    # Technical
    # ==========================================================

    "Programming": "technical",

    "Software Development": "technical",

    "Machine Learning": "technical",

    "Artificial Intelligence": "technical",

    "Data Analytics": "technical",

    "Business Intelligence": "technical",

    "Dashboarding": "technical",

    "Database": "technical",

    "SQL": "technical",

    "Python": "technical",

    "Automation": "technical",

    "Statistical Analysis": "technical",

    "Visualization": "technical",

    # ==========================================================
    # Quality
    # ==========================================================

    "Quality Assurance": "quality",

    "Quality Systems": "quality",

    "Quality Management": "quality",

    "Quality Improvement": "quality",

    "Food Safety": "quality",

    "Food Safety Management": "quality",

    "HACCP": "quality",

    "Preventive Controls": "quality",

    "Compliance": "quality",

    "Regulatory Compliance": "quality",

    # ==========================================================
    # Manufacturing
    # ==========================================================

    "Manufacturing Operations": "manufacturing",

    "Manufacturing Excellence": "manufacturing",

    "Operational Excellence": "manufacturing",

    "Manufacturing Efficiency": "manufacturing",

    "Lean Manufacturing": "manufacturing",

    "Six Sigma": "manufacturing",

    "Continuous Improvement": "manufacturing",

    "Process Optimization": "manufacturing",

    # ==========================================================
    # Supply Chain
    # ==========================================================

    "Supply Chain": "supply_chain",

    "Supply Chain Management": "supply_chain",

    "Inventory Management": "supply_chain",

    "Supplier Management": "supply_chain",

    "Distribution Management": "supply_chain",

    "Warehouse Operations": "supply_chain",

    "Logistics": "supply_chain",

    # ==========================================================
    # Leadership
    # ==========================================================

    "Leadership": "leadership",

    "People Management": "leadership",

    "Team Building": "leadership",

    "Coaching": "leadership",

    "Mentoring": "leadership",

    "People Development": "leadership",

    "Decision Making": "leadership",

    "Stakeholder Management": "leadership",

    # ==========================================================
    # Executive
    # ==========================================================

    "Executive Readiness": "executive",

    "Strategy": "executive",

    "Strategic Planning": "executive",

    "Business Strategy": "executive",

    "Transformation": "executive",

    "Financial Impact": "executive",

    "Business Value": "executive",

    "Innovation": "executive",

    # ==========================================================
    # Business
    # ==========================================================

    "Business Operations": "business",

    "Project Delivery": "business",

    "Execution": "business",

    "Customer Satisfaction": "business",

    "Customer Service": "business",

    "Business Growth": "business",

    "Productivity": "business",

    # ==========================================================
    # Laboratory
    # ==========================================================

    "Laboratory Operations": "laboratory",

    "Analytical Testing": "laboratory",

    "Microbiology": "laboratory",

}