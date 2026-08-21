"""
Knowledge Gap Analysis Models
=============================

Phase 3.3 - Gap Analysis contracts.

These models represent the structured interpretation of the enriched
KnowledgeMatchResult produced by Phase 3.2.

Architecture:

    KnowledgeMatchResult
            +
    EnrichedKnowledgeMatchResult
            |
            v
        GapAnalyzer
            |
            v
    KnowledgeGapAnalysisResult

Important
---------

This module does NOT:

    - perform document extraction
    - perform entity extraction
    - perform semantic resolution
    - modify KnowledgeProfile
    - modify JDRequirementProfile
    - perform matching
    - collect evidence
    - calculate ATS scores
    - generate recommendations
    - rewrite resumes
    - generate cover letters

Those responsibilities belong to their respective phases.

Traceability
------------

Phase 3.3 intentionally preserves the complete Phase 3.1 and Phase 3.2
traceability chain.

    JDRequirement
          |
          v
    RequirementMatch
          |
          v
    EnrichedRequirementMatch
          |
          v
    RequirementGap

The RequirementGap retains the complete EnrichedRequirementMatch rather
than copying or flattening its evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
    EnrichedRequirementMatch,
)


# ============================================================================
# GAP STATUS
# ============================================================================


class GapStatus(str, Enum):
    """
    Result of evaluating the coverage gap for one JD requirement.
    """

    NONE = "none"

    PARTIAL = "partial"

    FULL = "full"


# ============================================================================
# GAP SEVERITY
# ============================================================================


class GapSeverity(str, Enum):
    """
    Severity of a requirement gap.
    """

    NONE = "none"

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


# ============================================================================
# REQUIREMENT GAP
# ============================================================================


@dataclass(frozen=True)
class RequirementGap:
    """
    Gap analysis result for one enriched requirement match.

    The exact Phase 3.2 EnrichedRequirementMatch instance is retained.

    Identity invariant:

        gap.enriched_match
            is
        the original Phase 3.2 enriched match
    """

    enriched_match: EnrichedRequirementMatch

    gap_status: GapStatus

    severity: GapSeverity

    reason: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        if not isinstance(
            self.enriched_match,
            EnrichedRequirementMatch,
        ):
            raise TypeError(
                "RequirementGap.enriched_match must be "
                "EnrichedRequirementMatch."
            )

        if not isinstance(
            self.gap_status,
            GapStatus,
        ):
            raise TypeError(
                "RequirementGap.gap_status must be GapStatus."
            )

        if not isinstance(
            self.severity,
            GapSeverity,
        ):
            raise TypeError(
                "RequirementGap.severity must be GapSeverity."
            )

        if not isinstance(
            self.reason,
            str,
        ):
            raise TypeError(
                "RequirementGap.reason must be a string."
            )

    @property
    def requirement_id(self) -> str:
        return (
            self.enriched_match
            .match
            .requirement_id
        )

    @property
    def requirement_subject(self) -> str:
        return (
            self.enriched_match
            .match
            .requirement_subject
        )

    @property
    def requirement_type(self) -> str:
        return (
            self.enriched_match
            .match
            .requirement_type
        )

    @property
    def priority(self) -> str:
        return (
            self.enriched_match
            .match
            .priority
        )

    @property
    def evidence(self) -> tuple:
        return self.enriched_match.evidence

    @property
    def evidence_count(self) -> int:
        return self.enriched_match.evidence_count

    @property
    def match_status(self) -> Any:
        return (
            self.enriched_match
            .match
            .status
        )

    @property
    def match_score(self) -> float:
        return (
            self.enriched_match
            .match
            .score
        )

    @property
    def enrichment_confidence(self) -> float:
        return (
            self.enriched_match
            .enrichment_confidence
        )

    @property
    def has_gap(self) -> bool:
        return (
            self.gap_status
            != GapStatus.NONE
        )


# ============================================================================
# KNOWLEDGE GAP ANALYSIS RESULT
# ============================================================================


@dataclass(frozen=True)
class KnowledgeGapAnalysisResult:
    """
    Complete Phase 3.3 gap analysis result.

    The exact Phase 3.2 EnrichedKnowledgeMatchResult is retained.
    """

    enriched_match_result: EnrichedKnowledgeMatchResult

    gaps: tuple[
        RequirementGap,
        ...
    ] = ()

    total_requirements: int = 0

    no_gap_count: int = 0

    partial_gap_count: int = 0

    full_gap_count: int = 0

    gap_coverage_score: float = 0.0

    confidence: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        if not isinstance(
            self.enriched_match_result,
            EnrichedKnowledgeMatchResult,
        ):
            raise TypeError(
                "enriched_match_result must be "
                "EnrichedKnowledgeMatchResult."
            )

        gaps = tuple(
            self.gaps
        )

        object.__setattr__(
            self,
            "gaps",
            gaps,
        )

        if any(
            not isinstance(
                gap,
                RequirementGap,
            )
            for gap in gaps
        ):
            raise TypeError(
                "KnowledgeGapAnalysisResult.gaps must "
                "contain only RequirementGap objects."
            )

        # ------------------------------------------------------------------
        # IMPORTANT IDENTITY CONTRACT
        # ------------------------------------------------------------------
        #
        # Every gap must preserve the exact EnrichedRequirementMatch object
        # from the supplied EnrichedKnowledgeMatchResult.
        # ------------------------------------------------------------------

        enriched_by_id = {
            item.match.requirement_id: item
            for item in (
                self.enriched_match_result.matches
            )
        }

        for gap in gaps:

            requirement_id = (
                gap.requirement_id
            )

            expected = (
                enriched_by_id.get(
                    requirement_id
                )
            )

            if expected is None:

                raise ValueError(
                    "RequirementGap refers to a requirement "
                    "that does not exist in "
                    "enriched_match_result."
                )

            if (
                gap.enriched_match
                is not expected
            ):

                raise ValueError(
                    "RequirementGap.enriched_match must "
                    "preserve the exact "
                    "EnrichedRequirementMatch instance "
                    "from enriched_match_result."
                )

        if (
            self.total_requirements
            != len(gaps)
        ):
            raise ValueError(
                "total_requirements does not match gaps."
            )

        expected_no_gap = sum(
            gap.gap_status
            == GapStatus.NONE
            for gap in gaps
        )

        expected_partial = sum(
            gap.gap_status
            == GapStatus.PARTIAL
            for gap in gaps
        )

        expected_full = sum(
            gap.gap_status
            == GapStatus.FULL
            for gap in gaps
        )

        if (
            self.no_gap_count
            != expected_no_gap
        ):
            raise ValueError(
                "no_gap_count does not match gaps."
            )

        if (
            self.partial_gap_count
            != expected_partial
        ):
            raise ValueError(
                "partial_gap_count does not match gaps."
            )

        if (
            self.full_gap_count
            != expected_full
        ):
            raise ValueError(
                "full_gap_count does not match gaps."
            )

        try:
            coverage_score = float(
                self.gap_coverage_score
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValueError(
                "gap_coverage_score must be numeric."
            ) from exc

        if not 0.0 <= coverage_score <= 1.0:
            raise ValueError(
                "gap_coverage_score must be "
                "between 0 and 1."
            )

        try:
            confidence = float(
                self.confidence
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValueError(
                "confidence must be numeric."
            ) from exc

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "confidence must be "
                "between 0 and 1."
            )

    @classmethod
    def from_gaps(
        cls,
        *,
        enriched_match_result: EnrichedKnowledgeMatchResult,
        gaps: list[RequirementGap],
    ) -> "KnowledgeGapAnalysisResult":
        """
        Construct a complete gap-analysis result.

        The original Phase 3.2 objects are preserved unchanged.
        """

        if not isinstance(
            enriched_match_result,
            EnrichedKnowledgeMatchResult,
        ):
            raise TypeError(
                "enriched_match_result must be "
                "EnrichedKnowledgeMatchResult."
            )

        items = tuple(
            gaps
        )

        if not items:

            return cls(
                enriched_match_result=(
                    enriched_match_result
                ),
                gaps=(),
                total_requirements=0,
                no_gap_count=0,
                partial_gap_count=0,
                full_gap_count=0,
                gap_coverage_score=0.0,
                confidence=0.0,
            )

        enriched_by_id = {
            item.match.requirement_id: item
            for item in (
                enriched_match_result.matches
            )
        }

        for gap in items:

            if not isinstance(
                gap,
                RequirementGap,
            ):
                raise TypeError(
                    "gaps must contain only "
                    "RequirementGap objects."
                )

            requirement_id = (
                gap.requirement_id
            )

            expected = (
                enriched_by_id.get(
                    requirement_id
                )
            )

            if expected is None:

                raise ValueError(
                    "RequirementGap refers to a requirement "
                    "that is not present in the supplied "
                    "EnrichedKnowledgeMatchResult."
                )

            if (
                gap.enriched_match
                is not expected
            ):

                raise ValueError(
                    "RequirementGap.enriched_match must "
                    "refer to the exact "
                    "EnrichedRequirementMatch instance "
                    "from enriched_match_result."
                )

        no_gap = sum(
            gap.gap_status
            == GapStatus.NONE
            for gap in items
        )

        partial = sum(
            gap.gap_status
            == GapStatus.PARTIAL
            for gap in items
        )

        full = sum(
            gap.gap_status
            == GapStatus.FULL
            for gap in items
        )

        coverage_score = (
            (
                no_gap
                + (partial * 0.5)
            )
            / len(items)
        )

        confidence = (
            sum(
                gap.enrichment_confidence
                for gap in items
            )
            / len(items)
        )

        return cls(
            enriched_match_result=(
                enriched_match_result
            ),

            gaps=items,

            total_requirements=len(
                items
            ),

            no_gap_count=no_gap,

            partial_gap_count=partial,

            full_gap_count=full,

            gap_coverage_score=round(
                coverage_score,
                4,
            ),

            confidence=round(
                confidence,
                4,
            ),
        )


__all__ = [
    "GapStatus",
    "GapSeverity",
    "RequirementGap",
    "KnowledgeGapAnalysisResult",
]