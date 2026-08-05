"""
Skill Reasoning Models

Enterprise Skill Intelligence

Produces structured skill intelligence used by

- Leadership Reasoner
- Seniority Reasoner
- Executive Reasoner
- Knowledge Profile
"""
from typing import Any

from .skill_models import SkillRecommendation
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphNode,
)


# ==========================================================
# Individual Skill
# ==========================================================

@dataclass
class SkillEvidence:

    skill: Optional[GraphNode] = None

    confidence: float = 0.0

    business_area: str = ""

    domain: str = ""

    category: str = ""

    impact_weight: float = 1.0

    metadata: Dict = field(default_factory=dict)


# ==========================================================
# Skill Cluster
# ==========================================================

@dataclass
class SkillCluster:

    name: str = ""

    category: str = ""

    confidence: float = 0.0

    skills: List[SkillEvidence] = field(default_factory=list)

    score: float = 0.0

    metadata: Dict = field(default_factory=dict)


# ==========================================================
# Technical Depth
# ==========================================================

@dataclass
class TechnicalDepth:

    programming: float = 0.0

    analytics: float = 0.0

    quality: float = 0.0

    food_safety: float = 0.0

    operations: float = 0.0

    leadership: float = 0.0

    automation: float = 0.0

    cloud: float = 0.0

    ai: float = 0.0

    overall: float = 0.0


# ==========================================================
# Business Breadth
# ==========================================================

@dataclass
class BusinessBreadth:

    manufacturing: float = 0.0

    retail: float = 0.0

    logistics: float = 0.0

    quality: float = 0.0

    food_safety: float = 0.0

    engineering: float = 0.0

    management: float = 0.0

    digital: float = 0.0

    overall: float = 0.0


# ==========================================================
# Future Readiness
# ==========================================================

@dataclass
class FutureReadiness:

    ai_ready: float = 0.0

    automation_ready: float = 0.0

    digital_ready: float = 0.0

    analytics_ready: float = 0.0

    cloud_ready: float = 0.0

    data_ready: float = 0.0

    overall: float = 0.0
# ==========================================================
# Recommendation
# ==========================================================
    @dataclass
    class SkillRecommendation:

        title: str = ""

        priority: str = ""

        score: int = 0

        rationale: str = ""

        suggested_skills: List[str] = field(default_factory=list)

# ==========================================================
# Final Skill Reasoning Result
# ==========================================================

@dataclass
class SkillReasoningResult:

    ##########################################################
    # Scores
    ##########################################################

    overall_score: float = 0.0


    ##########################################################
    # Intelligence Components
    ##########################################################

    technical_depth: TechnicalDepth = field(
        default_factory=TechnicalDepth
    )


    business_breadth: BusinessBreadth = field(
        default_factory=BusinessBreadth
    )


    future_readiness: FutureReadiness = field(
        default_factory=FutureReadiness
    )


    ##########################################################
    # Skill Intelligence
    ##########################################################

    skill_nodes: List[Any] = field(
        default_factory=list
    )


    skill_clusters: List[SkillCluster] = field(
        default_factory=list
    )


    derived_skills: List[str] = field(
        default_factory=list
    )


    ##########################################################
    # Distribution Intelligence
    ##########################################################

    category_distribution: Dict[str, int] = field(
        default_factory=dict
    )


    domain_distribution: Dict[str, int] = field(
        default_factory=dict
    )


    ##########################################################
    # Recommendations
    ##########################################################

    recommendations: List[SkillRecommendation] = field(
        default_factory=list
    )


    ##########################################################
    # Quality
    ##########################################################

    confidence: float = 0.0


    warnings: List[str] = field(
        default_factory=list
    )


    ##########################################################
    # Metadata
    ##########################################################

    metadata: Dict = field(
        default_factory=dict
    )