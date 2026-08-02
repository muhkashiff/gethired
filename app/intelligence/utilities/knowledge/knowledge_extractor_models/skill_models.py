"""
Enterprise Skill Knowledge Model

Represents professional skills extracted from text.

Examples

Leadership
Root Cause Analysis
Food Safety Management
Lean Manufacturing
Problem Solving
Project Management
Business Analytics
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class SkillKnowledge(KnowledgeEntity):

    ####################################################################
    # Entity
    ####################################################################

    entity_type: str = "skill"

    ontology_name: str = "skills"

    ####################################################################
    # Skill Definition
    ####################################################################

    skill_family: str = ""

    skill_group: str = ""

    level: str = ""

    ####################################################################
    # Skill Classification
    ####################################################################

    technical: bool = False

    managerial: bool = False

    analytical: bool = False

    operational: bool = False

    compliance: bool = False

    leadership: bool = False

    communication: bool = False

    ####################################################################
    # Enterprise
    ####################################################################

    transferable: bool = True

    certification_required: bool = False

    years_required: float = 0.0

    ####################################################################
    # ATS
    ####################################################################

    ats_weight: float = 1.0

    graph_node: bool = True