"""
Enterprise Achievement Models

Enterprise V6

Stores achievement intelligence
generated from knowledge graph.

No reasoning logic belongs here.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any


# ==========================================================
# Achievement Evidence
# ==========================================================

@dataclass
class AchievementEvidence:
    """
    Raw achievement evidence extracted
    from graph relationships.
    """

    source_node: Any = None

    action: Any = None

    metric: Any = None

    measurement: Any = None

    standard: Any = None

    methodology: Any = None

    business_area: str = ""

    domain: str = ""

    result: str = ""

    improvement: str = ""

    confidence: float = 1.0

    metadata: Dict = field(
        default_factory=dict
    )


# ==========================================================
# Quantified Achievement
# ==========================================================

@dataclass
class QuantifiedAchievement:

    """
    Achievement containing measurable impact.

    Example:

    Reduced waste by 30%

    Increased yield from 70% to 99%
    """

    description: str = ""

    metric: str = ""

    value: float = 0.0

    unit: str = ""

    direction: str = ""

    confidence: float = 1.0



# ==========================================================
# Achievement Statistics
# ==========================================================

@dataclass
class AchievementStatistics:

    total: int = 0

    quantified: int = 0

    improvement_count: int = 0

    leadership_related: int = 0

    operational_related: int = 0

    technical_related: int = 0
# ==========================================================
# Business Impact
# ==========================================================

@dataclass
class BusinessImpact:
    """
    Represents the business impact inferred
    from an achievement.
    """

    category: str = ""

    score: float = 0.0

    rationale: str = ""

    confidence: float = 0.0

    metadata: Dict = field(
        default_factory=dict
    )


# ==========================================================
# Leadership Signal
# ==========================================================

@dataclass
class LeadershipSignal:
    """
    Represents leadership evidence inferred
    from an achievement.
    """

    category: str = ""

    description: str = ""

    score: float = 0.0

    confidence: float = 0.0

    metadata: Dict = field(
        default_factory=dict
    )


# ==========================================================
# Achievement Pattern
# ==========================================================

@dataclass
class AchievementPattern:
    """
    Represents recurring enterprise achievement patterns.

    Example

    Operational Excellence

    Cost Reduction

    Food Safety

    Digital Transformation
    """

    name: str = ""

    category: str = ""

    score: float = 0.0

    confidence: float = 0.0

    occurrences: int = 0

    rationale: str = ""

    metadata: Dict = field(
        default_factory=dict
    )


# ==========================================================
# Achievement Reasoning Result
# ==========================================================

@dataclass
class AchievementReasoningResult:

    overall_score: float = 0.0

    ##########################################################
    # Achievement Objects
    ##########################################################

    achievements: List[AchievementEvidence] = field(
        default_factory=list
    )


    quantified_results: List[QuantifiedAchievement] = field(
        default_factory=list
    )


    ##########################################################
    # Classification
    ##########################################################

    improvement_actions: List[Any] = field(
        default_factory=list
    )


    business_impacts: List[BusinessImpact] = field(
    default_factory=list
    )

    leadership_signals: List[LeadershipSignal] = field(
        default_factory=list
    )

    achievement_patterns: List[AchievementPattern] = field(
        default_factory=list
    )


    ##########################################################
    # Statistics
    ##########################################################

    statistics: AchievementStatistics = field(
        default_factory=AchievementStatistics
    )


    ##########################################################
    # Quality
    ##########################################################

    confidence: float = 0.0


    warnings: List[str] = field(
        default_factory=list
    )


    metadata: Dict = field(
        default_factory=dict
    )