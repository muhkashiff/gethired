"""
Enterprise Graph Reasoning Result

Master reasoning object produced by GraphReasoner.

Every reasoning module writes into this object.

Every downstream engine consumes this object.

Enterprise V5
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# ---------------------------------------------------------
# Individual reasoning models
# ---------------------------------------------------------

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.skill_models import (
    SkillReasoningResult,
)

# Future imports
#
# from achievement_models import AchievementReasoningResult
# from leadership_models import LeadershipReasoningResult
# from seniority_models import SeniorityReasoningResult
# from executive_models import ExecutiveReasoningResult
# from ontology_models import OntologyReasoningResult
# from dependency_models import DependencyReasoningResult


# ==========================================================
# Graph Reasoning Result
# ==========================================================

@dataclass
class GraphReasoningResult:

    ############################################################
    # Graph
    ############################################################

    graph = None

    ############################################################
    # Dependency Layer
    ############################################################

    dependencies = None

    ############################################################
    # Ontology Layer
    ############################################################

    ontology = None

    ############################################################
    # Skill Intelligence
    ############################################################

    skills: Optional[SkillReasoningResult] = None

    ############################################################
    # Achievement Intelligence
    ############################################################

    achievement = None

    ############################################################
    # Leadership Intelligence
    ############################################################

    leadership = None

    ############################################################
    # Seniority Intelligence
    ############################################################

    seniority = None

    ############################################################
    # Executive Intelligence
    ############################################################

    executive = None

    ############################################################
    # Derived Knowledge
    ############################################################

    inferred_capabilities: List[str] = field(
        default_factory=list
    )

    inferred_domains: List[str] = field(
        default_factory=list
    )

    inferred_strengths: List[str] = field(
        default_factory=list
    )

    inferred_gaps: List[str] = field(
        default_factory=list
    )

    ############################################################
    # Recommendations
    ############################################################

    recommendations: List[str] = field(
        default_factory=list
    )

    ############################################################
    # Statistics
    ############################################################

    confidence: float = 0.0

    completeness: float = 0.0

    reasoning_steps: List[str] = field(
        default_factory=list
    )

    ############################################################
    # Metadata
    ############################################################

    metadata: Dict = field(
        default_factory=dict
    )