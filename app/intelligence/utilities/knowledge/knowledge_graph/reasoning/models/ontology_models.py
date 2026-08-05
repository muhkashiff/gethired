"""
Enterprise Ontology Models

Enterprise V6

Stores semantic understanding of the enterprise
knowledge graph.

No reasoning logic belongs here.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any


# ==========================================================
# Semantic Group
# ==========================================================

@dataclass
class SemanticGroup:
    """
    Logical semantic grouping.

    Example

    Food Safety

        HACCP
        GMP
        FSSC22000
    """

    name: str = ""

    category: str = ""

    business_area: str = ""

    entities: List[Any] = field(
        default_factory=list
    )

    confidence: float = 1.0

    metadata: Dict = field(
        default_factory=dict
    )


# ==========================================================
# Ontology Statistics
# ==========================================================

@dataclass
class OntologyStatistics:

    standards: int = 0

    methodologies: int = 0

    skills: int = 0

    actions: int = 0

    metrics: int = 0

    modifiers: int = 0

    measurements: int = 0

    domains: int = 0

    business_areas: int = 0

    semantic_groups: int = 0


# ==========================================================
# Ontology Reasoning Result
# ==========================================================

@dataclass
class OntologyReasoningResult:

    ##########################################################
    # Ontology Objects
    ##########################################################

    standards: List[Any] = field(
        default_factory=list
    )

    methodologies: List[Any] = field(
        default_factory=list
    )

    skills: List[Any] = field(
        default_factory=list
    )

    actions: List[Any] = field(
        default_factory=list
    )

    metrics: List[Any] = field(
        default_factory=list
    )

    modifiers: List[Any] = field(
        default_factory=list
    )

    measurements: List[Any] = field(
        default_factory=list
    )

    ##########################################################
    # Domain Intelligence
    ##########################################################

    domains: Dict[str, List[Any]] = field(
        default_factory=dict
    )

    business_areas: Dict[str, List[Any]] = field(
        default_factory=dict
    )

    ##########################################################
    # Semantic Clusters
    ##########################################################

    semantic_groups: List[SemanticGroup] = field(
        default_factory=list
    )

    ##########################################################
    # Statistics
    ##########################################################

    statistics: OntologyStatistics = field(
        default_factory=OntologyStatistics
    )

    ##########################################################
    # Confidence
    ##########################################################

    confidence: float = 1.0

    metadata: Dict = field(
        default_factory=dict
    )