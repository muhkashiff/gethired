
"""
Business KPI Knowledge Model
Enterprise V5

Represents a Business KPI resolved from the business_kpi ontology.

Responsibilities
----------------
• Store resolved Business KPI information
• Preserve repository entity information
• Expose KPI-specific metadata
• Support downstream extraction and scoring
• Remain compatible with RepositoryEntity
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class BusinessKPIKnowledge:
    """
    Knowledge object returned by BusinessKPIExtractor.
    """

    # ----------------------------------------------------------------
    # BASIC MATCH INFORMATION
    # ----------------------------------------------------------------

    found: bool = False

    confidence: float = 0.0

    original: str = ""

    canonical: str = ""

    normalized: str = ""

    # ----------------------------------------------------------------
    # ENTITY IDENTITY
    # ----------------------------------------------------------------

    category: str = ""

    entity_id: str = ""

    entity_type: str = ""

    ontology_name: str = ""

    business_area: str = ""

    # ----------------------------------------------------------------
    # KPI INFORMATION
    # ----------------------------------------------------------------

    description: str = ""

    related_metrics: list[str] = field(
        default_factory=list
    )

    higher_is_better: bool = True

    impact_weight: float = 1.0

    # ----------------------------------------------------------------
    # MATCH INFORMATION
    # ----------------------------------------------------------------

    matched_phrase: str = ""

    matched_alias: bool = False

    # ----------------------------------------------------------------
    # POSITION INFORMATION
    # ----------------------------------------------------------------

    start_char: int = -1

    end_char: int = -1

    token_index: int = -1

    token_count: int = 0

    sentence_index: int = 0

    # ----------------------------------------------------------------
    # GRAPH INFORMATION
    # ----------------------------------------------------------------

    graph_node: bool = True

    # ----------------------------------------------------------------
    # REPOSITORY OBJECT
    # ----------------------------------------------------------------

    kpi_object: Optional[Any] = None

    # ----------------------------------------------------------------
    # OPTIONAL REASONING INFORMATION
    #
    # Kept compatible with the Enterprise V5 knowledge architecture.
    # These remain empty unless a future business_kpi_reasoning
    # ontology is introduced.
    # ----------------------------------------------------------------

    reasoning_id: str = ""

    reasoning_object: Optional[Any] = None

    reasoning_confidence: float = 0.0

    primary_domain: str = ""

    secondary_domains: list[str] = field(
        default_factory=list
    )

    trigger_actions: list[str] = field(
        default_factory=list
    )

    trigger_objects: list[str] = field(
        default_factory=list
    )

    trigger_skills: list[str] = field(
        default_factory=list
    )

    trigger_metrics: list[str] = field(
        default_factory=list
    )

    trigger_certifications: list[str] = field(
        default_factory=list
    )

    # ----------------------------------------------------------------
    # CONVENIENCE PROPERTIES
    # ----------------------------------------------------------------

    @property
    def is_found(self) -> bool:
        """
        Returns True when a KPI was successfully resolved.
        """

        return self.found

    @property
    def is_alias_match(self) -> bool:
        """
        Returns True when the KPI was matched through an alias.
        """

        return self.matched_alias

    @property
    def metric_count(self) -> int:
        """
        Number of related metrics.
        """

        return len(self.related_metrics)

    # ----------------------------------------------------------------
    # REPRESENTATION
    # ----------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "BusinessKPIKnowledge("
            f"found={self.found!r}, "
            f"confidence={self.confidence!r}, "
            f"original={self.original!r}, "
            f"canonical={self.canonical!r}, "
            f"normalized={self.normalized!r}, "
            f"category={self.category!r}, "
            f"entity_id={self.entity_id!r}, "
            f"entity_type={self.entity_type!r}, "
            f"ontology_name={self.ontology_name!r}, "
            f"business_area={self.business_area!r}, "
            f"related_metrics={self.related_metrics!r}, "
            f"higher_is_better={self.higher_is_better!r}, "
            f"impact_weight={self.impact_weight!r}"
            ")"
        )

