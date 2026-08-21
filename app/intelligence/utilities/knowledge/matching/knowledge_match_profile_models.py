"""
Knowledge Match Profile Models
==============================

Phase 4 - Knowledge Match Profile contracts.

Phase 4 consumes the complete Phase 3 matching pipeline:

    Phase 3.1
        KnowledgeMatchResult
            +
    Phase 3.2
        EnrichedKnowledgeMatchResult
            +
    Phase 3.3
        KnowledgeGapAnalysisResult
            |
            v
    Phase 4
        KnowledgeMatchProfile

Purpose
-------

The KnowledgeMatchProfile is the stable, downstream-facing profile of
resume-to-JD knowledge alignment.

Phase 4 does NOT:

    - perform document extraction
    - perform entity extraction
    - perform semantic resolution
    - modify KnowledgeProfile
    - modify JDRequirementProfile
    - perform matching
    - collect evidence
    - perform gap analysis
    - calculate ATS scores
    - generate recommendations
    - rewrite resumes
    - generate cover letters

Those responsibilities belong to earlier or later phases.

Traceability
------------

The complete Phase 3 chain remains available:

    KnowledgeMatchProfile
            |
            +-- match_result
            |
            +-- enriched_match_result
            |
            +-- gap_analysis_result
            |
            +-- requirements[]
                    |
                    +-- RequirementMatch
                    +-- MatchEvidence[]
                    +-- RequirementGap


Object In
---------

    ProjectMatchResult


Object Out
----------

    KnowledgeMatchProfile
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchResult,
)

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
    EnrichedRequirementMatch,
)

from app.intelligence.utilities.knowledge.matching.gap_models import (
    GapSeverity,
    GapStatus,
    KnowledgeGapAnalysisResult,
    RequirementGap,
)


# ============================================================================
# REQUIREMENT PROFILE
# ============================================================================


@dataclass(frozen=True)
class KnowledgeRequirementProfile:
    """
    Phase 4 consolidated profile for one JD requirement.

    This object intentionally retains both enriched evidence and gap
    information rather than recalculating either one.
    """

    enriched_match: EnrichedRequirementMatch

    gap: RequirementGap

    def __post_init__(self) -> None:

        if not isinstance(
            self.enriched_match,
            EnrichedRequirementMatch,
        ):
            raise TypeError(
                "KnowledgeRequirementProfile.enriched_match "
                "must be EnrichedRequirementMatch."
            )

        if not isinstance(
            self.gap,
            RequirementGap,
        ):
            raise TypeError(
                "KnowledgeRequirementProfile.gap "
                "must be RequirementGap."
            )

        # ------------------------------------------------------------------
        # IMPORTANT
        # ------------------------------------------------------------------
        #
        # RequirementGap must retain the exact same enriched match object.
        #
        # The relationship is:
        #
        #     KnowledgeRequirementProfile.enriched_match
        #             is
        #     KnowledgeRequirementProfile.gap.enriched_match
        #
        # This preserves Phase 3.2 object identity and prevents the Phase 4
        # profile from accidentally combining unrelated requirement objects.
        # ------------------------------------------------------------------

        if (
            self.enriched_match
            is not self.gap.enriched_match
        ):
            raise ValueError(
                "KnowledgeRequirementProfile.enriched_match "
                "and gap must refer to the same enriched match."
            )

    # =========================================================================
    # REQUIREMENT ACCESS
    # =========================================================================

    @property
    def requirement_id(self) -> str:
        """
        Return the original JD requirement identifier.
        """

        return self.enriched_match.match.requirement_id

    @property
    def requirement_subject(self) -> str:
        """
        Return the original JD requirement subject.
        """

        return self.enriched_match.match.requirement_subject

    @property
    def requirement_type(self) -> str:
        """
        Return the original JD requirement type.
        """

        return self.enriched_match.match.requirement_type

    @property
    def priority(self) -> str:
        """
        Return the original JD requirement priority.
        """

        return self.enriched_match.match.priority

    # =========================================================================
    # MATCH ACCESS
    # =========================================================================

    @property
    def match_status(self) -> Any:
        """
        Return the authoritative Phase 3.1 match status.
        """

        return self.enriched_match.match.status

    @property
    def match_score(self) -> float:
        """
        Return the authoritative Phase 3.1 match score.
        """

        return self.enriched_match.match.score

    # =========================================================================
    # EVIDENCE ACCESS
    # =========================================================================

    @property
    def evidence(self) -> tuple:
        """
        Return Phase 3.2 evidence without modifying it.
        """

        return self.enriched_match.evidence

    @property
    def evidence_count(self) -> int:
        """
        Return the number of Phase 3.2 evidence items.
        """

        return self.enriched_match.evidence_count

    @property
    def enrichment_confidence(self) -> float:
        """
        Return the Phase 3.2 enrichment confidence.
        """

        return self.enriched_match.enrichment_confidence

    @property
    def evidence_backed(self) -> bool:
        """
        Return True when the requirement has supporting evidence.
        """

        return self.evidence_count > 0

    # =========================================================================
    # GAP ACCESS
    # =========================================================================

    @property
    def gap_status(self) -> GapStatus:
        """
        Return the Phase 3.3 gap status.
        """

        return self.gap.gap_status

    @property
    def gap_severity(self) -> GapSeverity:
        """
        Return the Phase 3.3 gap severity.
        """

        return self.gap.severity

    @property
    def gap_reason(self) -> str:
        """
        Return the Phase 3.3 gap reason.
        """

        return self.gap.reason

    @property
    def has_gap(self) -> bool:
        """
        Return True when the requirement has any gap.
        """

        return self.gap.has_gap


# ============================================================================
# KNOWLEDGE MATCH PROFILE
# ============================================================================


@dataclass(frozen=True)
class KnowledgeMatchProfile:
    """
    Complete Phase 4 knowledge match profile.

    This is the consolidated downstream representation of the complete
    Phase 3 pipeline.

    No Phase 3 intelligence is recalculated here.

    The canonical stored profile-level confidence field is:

        profile_confidence

    The public ``confidence`` property is an intentional compatibility
    alias for downstream consumers and tests.
    """

    # ------------------------------------------------------------------
    # Phase 3 source boundaries
    # ------------------------------------------------------------------

    match_result: KnowledgeMatchResult

    enriched_match_result: EnrichedKnowledgeMatchResult

    gap_analysis_result: KnowledgeGapAnalysisResult

    # ------------------------------------------------------------------
    # Requirement-level consolidated profiles
    # ------------------------------------------------------------------

    requirements: tuple[
        KnowledgeRequirementProfile,
        ...
    ] = ()

    # ------------------------------------------------------------------
    # Aggregate counts
    # ------------------------------------------------------------------

    total_requirements: int = 0

    matched_count: int = 0

    partial_count: int = 0

    unmatched_count: int = 0

    evidence_backed_count: int = 0

    no_gap_count: int = 0

    partial_gap_count: int = 0

    full_gap_count: int = 0

    # ------------------------------------------------------------------
    # Aggregate scores
    # ------------------------------------------------------------------

    coverage_score: float = 0.0

    matching_score: float = 0.0

    matching_confidence: float = 0.0

    enrichment_confidence: float = 0.0

    gap_analysis_confidence: float = 0.0

    # ------------------------------------------------------------------
    # Phase 4 consolidated confidence
    # ------------------------------------------------------------------

    profile_confidence: float = 0.0

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        # ------------------------------------------------------------------
        # SOURCE VALIDATION
        # ------------------------------------------------------------------

        if not isinstance(
            self.match_result,
            KnowledgeMatchResult,
        ):
            raise TypeError(
                "KnowledgeMatchProfile.match_result must "
                "be KnowledgeMatchResult."
            )

        if not isinstance(
            self.enriched_match_result,
            EnrichedKnowledgeMatchResult,
        ):
            raise TypeError(
                "KnowledgeMatchProfile.enriched_match_result must "
                "be EnrichedKnowledgeMatchResult."
            )

        if not isinstance(
            self.gap_analysis_result,
            KnowledgeGapAnalysisResult,
        ):
            raise TypeError(
                "KnowledgeMatchProfile.gap_analysis_result must "
                "be KnowledgeGapAnalysisResult."
            )

        # ------------------------------------------------------------------
        # SOURCE CHAIN VALIDATION
        # ------------------------------------------------------------------

        if (
            self.enriched_match_result.match_result
            is not self.match_result
        ):
            raise ValueError(
                "enriched_match_result must reference "
                "the supplied match_result."
            )

        if (
            self.gap_analysis_result.enriched_match_result
            is not self.enriched_match_result
        ):
            raise ValueError(
                "gap_analysis_result must reference "
                "the supplied enriched_match_result."
            )

        # ------------------------------------------------------------------
        # NORMALIZE REQUIREMENTS
        # ------------------------------------------------------------------

        requirements = tuple(
            self.requirements
        )

        object.__setattr__(
            self,
            "requirements",
            requirements,
        )

        if any(
            not isinstance(
                item,
                KnowledgeRequirementProfile,
            )
            for item in requirements
        ):
            raise TypeError(
                "requirements must contain only "
                "KnowledgeRequirementProfile objects."
            )

        # ------------------------------------------------------------------
        # REQUIREMENT COUNT
        # ------------------------------------------------------------------

        if (
            self.total_requirements
            != len(requirements)
        ):
            raise ValueError(
                "total_requirements does not match requirements."
            )

        # ------------------------------------------------------------------
        # DERIVED MATCH COUNTS
        # ------------------------------------------------------------------

        expected_matched = (
            self.match_result.matched_count
        )

        expected_partial = (
            self.match_result.partial_count
        )

        expected_unmatched = (
            self.match_result.unmatched_count
        )

        if self.matched_count != expected_matched:
            raise ValueError(
                "matched_count does not match match_result."
            )

        if self.partial_count != expected_partial:
            raise ValueError(
                "partial_count does not match match_result."
            )

        if self.unmatched_count != expected_unmatched:
            raise ValueError(
                "unmatched_count does not match match_result."
            )

        # ------------------------------------------------------------------
        # EVIDENCE COUNT
        # ------------------------------------------------------------------

        expected_evidence_backed = (
            self.enriched_match_result.evidence_backed_count
        )

        if (
            self.evidence_backed_count
            != expected_evidence_backed
        ):
            raise ValueError(
                "evidence_backed_count does not match "
                "enriched_match_result."
            )

        # ------------------------------------------------------------------
        # GAP COUNTS
        # ------------------------------------------------------------------

        if (
            self.no_gap_count
            != self.gap_analysis_result.no_gap_count
        ):
            raise ValueError(
                "no_gap_count does not match "
                "gap_analysis_result."
            )

        if (
            self.partial_gap_count
            != self.gap_analysis_result.partial_gap_count
        ):
            raise ValueError(
                "partial_gap_count does not match "
                "gap_analysis_result."
            )

        if (
            self.full_gap_count
            != self.gap_analysis_result.full_gap_count
        ):
            raise ValueError(
                "full_gap_count does not match "
                "gap_analysis_result."
            )

        # ------------------------------------------------------------------
        # NUMERIC VALIDATION
        # ------------------------------------------------------------------

        numeric_fields = (
            "coverage_score",
            "matching_score",
            "matching_confidence",
            "enrichment_confidence",
            "gap_analysis_confidence",
            "profile_confidence",
        )

        for field_name in numeric_fields:

            try:
                value = float(
                    getattr(
                        self,
                        field_name,
                    )
                )
            except (
                TypeError,
                ValueError,
            ) as exc:

                raise ValueError(
                    f"{field_name} must be numeric."
                ) from exc

            if not 0.0 <= value <= 1.0:

                raise ValueError(
                    f"{field_name} must be between 0 and 1."
                )

    # =========================================================================
    # PUBLIC CONFIDENCE CONTRACT
    # =========================================================================

    @property
    def confidence(self) -> float:
        """
        Return the Phase 4 profile confidence.

        ``profile_confidence`` is the canonical stored field.

        ``confidence`` is the stable public shorthand used by downstream
        consumers.
        """

        return self.profile_confidence


# ============================================================================
# FACTORY
# ============================================================================


def build_knowledge_match_profile(
    *,
    match_result: KnowledgeMatchResult,
    enriched_match_result: EnrichedKnowledgeMatchResult,
    gap_analysis_result: KnowledgeGapAnalysisResult,
) -> KnowledgeMatchProfile:
    """
    Build the Phase 4 profile from the complete Phase 3 result chain.

    This function performs consolidation only.

    It does not perform new matching, evidence collection, or gap analysis.
    """

    # ------------------------------------------------------------------
    # SOURCE CHAIN VALIDATION
    # ------------------------------------------------------------------

    if (
        enriched_match_result.match_result
        is not match_result
    ):
        raise ValueError(
            "enriched_match_result does not belong to match_result."
        )

    if (
        gap_analysis_result.enriched_match_result
        is not enriched_match_result
    ):
        raise ValueError(
            "gap_analysis_result does not belong to "
            "enriched_match_result."
        )

    # ------------------------------------------------------------------
    # INDEX PHASE 3.2 ENRICHED MATCHES
    # ------------------------------------------------------------------

    enriched_by_id = {
        item.match.requirement_id: item
        for item in enriched_match_result.matches
    }

    # ------------------------------------------------------------------
    # INDEX PHASE 3.3 GAPS
    # ------------------------------------------------------------------

    gap_by_id = {
        item.requirement_id: item
        for item in gap_analysis_result.gaps
    }

    requirement_ids = list(
        enriched_by_id.keys()
    )

    if set(requirement_ids) != set(
        gap_by_id.keys()
    ):
        raise ValueError(
            "Phase 3.2 and Phase 3.3 requirement sets "
            "do not match."
        )

    # ------------------------------------------------------------------
    # BUILD REQUIREMENT PROFILES
    # ------------------------------------------------------------------

    requirements = []

    for requirement_id in requirement_ids:

        enriched_match = (
            enriched_by_id[
                requirement_id
            ]
        )

        gap = (
            gap_by_id[
                requirement_id
            ]
        )

        requirements.append(
            KnowledgeRequirementProfile(
                enriched_match=enriched_match,
                gap=gap,
            )
        )

    total = len(
        requirements
    )

    # ------------------------------------------------------------------
    # MATCHING SCORE
    # ------------------------------------------------------------------

    matching_score = (
        float(
            match_result.overall_score
        )
        if total
        else 0.0
    )

    # ------------------------------------------------------------------
    # MATCHING CONFIDENCE
    # ------------------------------------------------------------------

    matching_confidence = (
        float(
            match_result.confidence
        )
        if total
        else 0.0
    )

    # ------------------------------------------------------------------
    # ENRICHMENT CONFIDENCE
    # ------------------------------------------------------------------

    enrichment_confidence = (
        float(
            enriched_match_result.enrichment_confidence
        )
        if total
        else 0.0
    )

    # ------------------------------------------------------------------
    # GAP ANALYSIS CONFIDENCE
    # ------------------------------------------------------------------

    gap_analysis_confidence = (
        float(
            gap_analysis_result.confidence
        )
        if total
        else 0.0
    )

    # ------------------------------------------------------------------
    # COVERAGE SCORE
    # ------------------------------------------------------------------

    coverage_score = (
        float(
            gap_analysis_result.gap_coverage_score
        )
        if total
        else 0.0
    )

    # ------------------------------------------------------------------
    # PROFILE CONFIDENCE
    # ------------------------------------------------------------------
    #
    # Phase 4 does not invent a new intelligence score.
    #
    # It combines the confidence values already produced by:
    #
    #     Phase 3.1
    #     Phase 3.2
    #     Phase 3.3
    #
    # Equal weighting is intentional at this stage.
    # ------------------------------------------------------------------

    if total:

        profile_confidence = (
            (
                matching_confidence
                + enrichment_confidence
                + gap_analysis_confidence
            )
            / 3.0
        )

    else:

        profile_confidence = 0.0

    # ------------------------------------------------------------------
    # RETURN COMPLETE PHASE 4 PROFILE
    # ------------------------------------------------------------------

    return KnowledgeMatchProfile(
        match_result=match_result,

        enriched_match_result=(
            enriched_match_result
        ),

        gap_analysis_result=(
            gap_analysis_result
        ),

        requirements=tuple(
            requirements
        ),

        total_requirements=total,

        matched_count=(
            match_result.matched_count
        ),

        partial_count=(
            match_result.partial_count
        ),

        unmatched_count=(
            match_result.unmatched_count
        ),

        evidence_backed_count=(
            enriched_match_result.evidence_backed_count
        ),

        no_gap_count=(
            gap_analysis_result.no_gap_count
        ),

        partial_gap_count=(
            gap_analysis_result.partial_gap_count
        ),

        full_gap_count=(
            gap_analysis_result.full_gap_count
        ),

        coverage_score=round(
            coverage_score,
            4,
        ),

        matching_score=round(
            matching_score,
            4,
        ),

        matching_confidence=round(
            matching_confidence,
            4,
        ),

        enrichment_confidence=round(
            enrichment_confidence,
            4,
        ),

        gap_analysis_confidence=round(
            gap_analysis_confidence,
            4,
        ),

        profile_confidence=round(
            profile_confidence,
            4,
        ),
    )


# ============================================================================
# PUBLIC EXPORTS
# ============================================================================


__all__ = [
    "KnowledgeRequirementProfile",
    "KnowledgeMatchProfile",
    "build_knowledge_match_profile",
]