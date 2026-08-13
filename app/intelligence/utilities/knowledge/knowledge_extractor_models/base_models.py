"""
Enterprise Knowledge Entity
Enterprise V5

Common knowledge model shared by all ontology parser extractors.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class KnowledgeEntity:
    """
    Common base model for every ontology-derived knowledge object.

    Examples:

        SkillKnowledge
        ActionKnowledge
        CertificationKnowledge
        StandardKnowledge
        TechnologyKnowledge
        BusinessKPIKnowledge
    """

    # ==============================================================
    # DETECTION
    # ==============================================================

    found: bool = False

    confidence: float = 0.0

    # ==============================================================
    # LINGUISTIC
    # ==============================================================

    original: str = ""

    canonical: str = ""

    normalized: str = ""

    base: str = ""

    past: str = ""

    gerund: str = ""

    plural: str = ""

    singular: str = ""

    abbreviation: str = ""

    short_name: str = ""

    # ==============================================================
    # CLASSIFICATION
    # ==============================================================

    category: str = ""

    entity_id: str = ""

    entity_type: str = ""

    ontology_name: str = ""

    business_area: str = ""

    domain: str = ""

    description: str = ""

    # ==============================================================
    # BUSINESS / SEMANTIC
    # ==============================================================

    related_metrics: list[str] = field(
        default_factory=list
    )

    impact_weight: float = 1.0

    business_meaning: str = ""

    preferred_direction: str = ""

    preferred_unit: str = ""

    higher_is_better: bool = True

    # ==============================================================
    # MATCH INFORMATION
    # ==============================================================

    matched_phrase: str = ""

    matched_alias: bool = False

    # ==============================================================
    # POSITION
    # ==============================================================

    start_char: int = -1

    end_char: int = -1

    token_index: int = -1

    token_count: int = 0

    sentence_index: int = 0

    # ==============================================================
    # REPOSITORY
    # ==============================================================

    source: str = ""

    metadata: dict = field(
        default_factory=dict
    )