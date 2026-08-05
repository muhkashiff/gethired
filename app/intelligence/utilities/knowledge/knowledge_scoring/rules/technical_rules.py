"""
Enterprise Technical Rules

Enterprise V12

Maps graph relationships into Technical Capabilities.

NO reasoning logic.

Only enterprise knowledge.
"""

from app.intelligence.utilities.knowledge.knowledge_scoring.base.relation_rule_engine import (
    RelationRule,
)

# ==========================================================
# TECHNICAL RULES
# ==========================================================

TECHNICAL_RULES = [

    # -----------------------------------------------------
    # Quality Management Systems
    # -----------------------------------------------------

    RelationRule(
        relation="COMPLIES_WITH",
        source_type="Action",
        target_type="Standard",
        capability="Quality Management Systems",
        weight=3.0,
    ),

    RelationRule(
        relation="COMPLIES_WITH",
        source_type="Action",
        target_type="Standard",
        capability="Food Safety Management Systems",
        weight=3.0,
    ),

    RelationRule(
        relation="COMPLIES_WITH",
        source_type="Action",
        target_type="Standard",
        capability="Regulatory Compliance",
        weight=2.5,
    ),

    # -----------------------------------------------------
    # Continuous Improvement
    # -----------------------------------------------------

    RelationRule(
        relation="USES",
        source_type="Action",
        target_type="Methodology",
        capability="Continuous Improvement",
        weight=2.5,
    ),

    RelationRule(
        relation="USES",
        source_type="Action",
        target_type="Methodology",
        capability="Root Cause Analysis",
        weight=3.0,
    ),

    RelationRule(
        relation="USES",
        source_type="Action",
        target_type="Methodology",
        capability="Corrective Action",
        weight=2.5,
    ),

    RelationRule(
        relation="USES",
        source_type="Action",
        target_type="Methodology",
        capability="Preventive Action",
        weight=2.5,
    ),

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    RelationRule(
        relation="AFFECTS",
        source_type="Action",
        target_type="Metric",
        capability="Process Optimization",
        weight=2.5,
    ),

    RelationRule(
        relation="ACHIEVED",
        source_type="Action",
        target_type="Metric",
        capability="Operational Excellence",
        weight=3.0,
    ),

    RelationRule(
        relation="MEASURED_BY",
        source_type="Metric",
        target_type="Measurement",
        capability="Performance Measurement",
        weight=2.0,
    ),

    # -----------------------------------------------------
    # Domains
    # -----------------------------------------------------

    RelationRule(
        relation="BELONGS_TO",
        source_type="Action",
        target_type="Domain",
        capability="Manufacturing",
        weight=2.0,
    ),

    RelationRule(
        relation="BELONGS_TO",
        source_type="Action",
        target_type="Domain",
        capability="Quality Assurance",
        weight=2.0,
    ),

    RelationRule(
        relation="BELONGS_TO",
        source_type="Action",
        target_type="Domain",
        capability="Food Safety",
        weight=2.0,
    ),

]