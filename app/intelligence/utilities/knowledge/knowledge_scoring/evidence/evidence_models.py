"""
Enterprise Evidence Models

Enterprise V12

Every score category owns one Evidence object.

These are populated ONLY by the GenericEvidenceBuilder.
"""

from dataclasses import dataclass, field


# ==========================================================
# BASE
# ==========================================================

@dataclass
class EvidenceBase:

    total_score: float = 0.0

    metadata: dict = field(default_factory=dict)


# ==========================================================
# DOMAIN
# ==========================================================

@dataclass
class DomainEvidence(EvidenceBase):

    food_safety: float = 0.0

    manufacturing: float = 0.0

    quality: float = 0.0

    laboratory: float = 0.0

    supply_chain: float = 0.0

    retail: float = 0.0

    operations: float = 0.0

    compliance: float = 0.0

    business_operations: float = 0.0

    customer_service: float = 0.0


# ==========================================================
# TECHNICAL
# ==========================================================

@dataclass
class TechnicalEvidence(EvidenceBase):

    programming: float = 0.0

    analytics: float = 0.0

    business_intelligence: float = 0.0

    machine_learning: float = 0.0

    statistics: float = 0.0

    database: float = 0.0

    automation: float = 0.0

    visualization: float = 0.0


# ==========================================================
# LEADERSHIP
# ==========================================================

@dataclass
class LeadershipEvidence(EvidenceBase):

    leadership: float = 0.0

    people_management: float = 0.0

    people_development: float = 0.0

    coaching: float = 0.0

    mentoring: float = 0.0

    executive_readiness: float = 0.0

    team_building: float = 0.0


# ==========================================================
# EXECUTIVE
# ==========================================================

@dataclass
class ExecutiveEvidence(EvidenceBase):

    strategy: float = 0.0

    governance: float = 0.0

    transformation: float = 0.0

    financial_impact: float = 0.0

    business_value: float = 0.0

    executive_readiness: float = 0.0


# ==========================================================
# BUSINESS VALUE
# ==========================================================

@dataclass
class BusinessValueEvidence(EvidenceBase):

    operational_excellence: float = 0.0

    process_optimization: float = 0.0

    continuous_improvement: float = 0.0

    financial_impact: float = 0.0

    customer_satisfaction: float = 0.0

    productivity: float = 0.0

    manufacturing_efficiency: float = 0.0


# ==========================================================
# ATS
# ==========================================================

@dataclass
class ATSEvidence(EvidenceBase):

    standards: float = 0.0

    methodologies: float = 0.0

    technical: float = 0.0

    leadership: float = 0.0

    business: float = 0.0

    achievements: float = 0.0