"""
Enterprise Skill Knowledge Model
Enterprise V5
"""

from dataclasses import dataclass

from .base_parser_models import ParserModel


@dataclass
class SkillParserModel(
    ParserModel
):
    """
    Knowledge representation of one
    resolved skill ontology entity.
    """

    # ==============================================================
    # IDENTITY
    # ==============================================================

    entity_type: str = "skill"

    ontology_name: str = "skills"

    # ==============================================================
    # SKILL DEFINITION
    # ==============================================================

    skill_family: str = ""

    skill_group: str = ""

    level: str = ""

    # ==============================================================
    # SKILL CLASSIFICATION
    # ==============================================================

    technical: bool = False

    managerial: bool = False

    analytical: bool = False

    operational: bool = False

    compliance: bool = False

    leadership: bool = False

    communication: bool = False

    # ==============================================================
    # ENTERPRISE
    # ==============================================================

    transferable: bool = True

    certification_required: bool = False

    years_required: float = 0.0

    # ==============================================================
    # ATS
    # ==============================================================

    ats_weight: float = 1.0

    graph_node: bool = True