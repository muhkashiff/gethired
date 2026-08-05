"""
Enterprise Domain Rules

Enterprise V12

These rules map graph relationships into
Domain Capabilities.

The CapabilityReasoner consumes these rules.

NO reasoning logic belongs here.

Only business knowledge.
"""

from app.intelligence.utilities.knowledge.knowledge_scoring.base.relation_rule_engine import (
    RelationRule,
)

# ==========================================================
# DOMAIN RULES
# ==========================================================

DOMAIN_RULES = [

    # -----------------------------------------------------
    # Domain Ownership
    # -----------------------------------------------------

    RelationRule(
        relation="BELONGS_TO",
        source_type="Action",
        target_type="Domain",
        capability="Domain Expertise",
        weight=3.0,
    ),

    # -----------------------------------------------------
    # Standards
    # -----------------------------------------------------

    RelationRule(
        relation="COMPLIES_WITH",
        source_type="Action",
        target_type="Standard",
        capability="Quality Systems",
        weight=2.5,
    ),

    RelationRule(
        relation="COMPLIES_WITH",
        source_type="Action",
        target_type="Standard",
        capability="Food Safety Systems",
        weight=2.5,
    ),

    RelationRule(
        relation="COMPLIES_WITH",
        source_type="Action",
        target_type="Standard",
        capability="Regulatory Compliance",
        weight=2.0,
    ),

    # -----------------------------------------------------
    # Methodologies
    # -----------------------------------------------------

    RelationRule(
        relation="USES",
        source_type="Action",
        target_type="Methodology",
        capability="Continuous Improvement",
        weight=2.0,
    ),

    RelationRule(
        relation="USES",
        source_type="Action",
        target_type="Methodology",
        capability="Problem Solving",
        weight=2.0,
    ),

    RelationRule(
        relation="USES",
        source_type="Action",
        target_type="Methodology",
        capability="Operational Excellence",
        weight=2.0,
    ),

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    RelationRule(
        relation="AFFECTS",
        source_type="Action",
        target_type="Metric",
        capability="Performance Improvement",
        weight=2.5,
    ),

    RelationRule(
        relation="ACHIEVED",
        source_type="Action",
        target_type="Metric",
        capability="Business Results",
        weight=3.0,
    ),

]