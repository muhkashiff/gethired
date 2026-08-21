
"""
Knowledge Gap Analyzer
======================

Phase 3.3

Object In
----------
EnrichedKnowledgeMatchResult

Object Out
-----------
KnowledgeGapAnalysisResult

Architecture
------------

Phase 3.1
    KnowledgeMatchResult
            |
            v
Phase 3.2
    EnrichedKnowledgeMatchResult
            |
            v
Phase 3.3
    KnowledgeGapAnalyzer
            |
            v
    KnowledgeGapAnalysisResult


Responsibilities
----------------

This module:

    - interprets existing match statuses
    - classifies requirement gaps
    - assigns gap severity
    - preserves Phase 3.1 match identity
    - preserves Phase 3.2 evidence
    - calculates requirement coverage
    - calculates gap-analysis confidence

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


Important
---------

Phase 3.3 is an interpretation layer.

The authoritative matching decision remains the Phase 3.1
KnowledgeMatchResult.

Phase 3.2 evidence is supporting evidence only.

Phase 3.3 does not recalculate the match score.
"""

from __future__ import annotations

from typing import Any

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
    EnrichedRequirementMatch,
)

from app.intelligence.utilities.knowledge.matching.match_models import (
    MatchStatus,
)

from app.intelligence.utilities.knowledge.matching.gap_models import (
    GapSeverity,
    GapStatus,
    KnowledgeGapAnalysisResult,
    RequirementGap,
)


class KnowledgeGapAnalyzer:
    """
    Phase 3.3 gap-analysis boundary.

    Object In
        EnrichedKnowledgeMatchResult

    Object Out
        KnowledgeGapAnalysisResult

    The analyzer never changes the underlying match or evidence objects.
    """

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def process(
        self,
        enriched_match_result: EnrichedKnowledgeMatchResult,
    ) -> KnowledgeGapAnalysisResult:
        """
        Analyze requirement gaps from an enriched matching result.

        The analyzer consumes the already-established Phase 3.1
        matching decisions and the optional Phase 3.2 evidence.

        No matching decision is recalculated.
        """

        # =================================================================
        # INPUT VALIDATION
        # =================================================================

        if not isinstance(
            enriched_match_result,
            EnrichedKnowledgeMatchResult,
        ):
            raise TypeError(
                "KnowledgeGapAnalyzer.process() expects "
                "an EnrichedKnowledgeMatchResult."
            )

        # =================================================================
        # BUILD REQUIREMENT GAPS
        # =================================================================

        gaps: list[RequirementGap] = []

        for enriched_match in (
            enriched_match_result.matches
        ):

            if not isinstance(
                enriched_match,
                EnrichedRequirementMatch,
            ):
                raise TypeError(
                    "EnrichedKnowledgeMatchResult.matches "
                    "must contain EnrichedRequirementMatch objects."
                )

            gap_status = self._classify_gap_status(
                enriched_match
            )

            severity = self._classify_severity(
                enriched_match=enriched_match,
                gap_status=gap_status,
            )

            reason = self._build_reason(
                enriched_match=enriched_match,
                gap_status=gap_status,
                severity=severity,
            )

            gaps.append(
                RequirementGap(
                    enriched_match=enriched_match,
                    gap_status=gap_status,
                    severity=severity,
                    reason=reason,
                )
            )

        # =================================================================
        # BUILD COMPLETE RESULT
        # =================================================================

        return KnowledgeGapAnalysisResult.from_gaps(
            enriched_match_result=(
                enriched_match_result
            ),
            gaps=gaps,
        )

    # =========================================================================
    # GAP STATUS
    # =========================================================================

    @staticmethod
    def _classify_gap_status(
        enriched_match: EnrichedRequirementMatch,
    ) -> GapStatus:
        """
        Translate the authoritative Phase 3.1 match status into
        the Phase 3.3 gap status.

        Mapping:

            MATCHED
                -> NONE

            PARTIAL
                -> PARTIAL

            UNMATCHED
                -> FULL

        Phase 3.3 does not reinterpret the matching decision.
        """

        status = (
            enriched_match
            .match
            .status
        )

        if status == MatchStatus.MATCHED:
            return GapStatus.NONE

        if status == MatchStatus.PARTIAL:
            return GapStatus.PARTIAL

        if status == MatchStatus.UNMATCHED:
            return GapStatus.FULL

        raise ValueError(
            "KnowledgeGapAnalyzer encountered an "
            f"unsupported MatchStatus: {status!r}"
        )

    # =========================================================================
    # GAP SEVERITY
    # =========================================================================

    @classmethod
    def _classify_severity(
        cls,
        *,
        enriched_match: EnrichedRequirementMatch,
        gap_status: GapStatus,
    ) -> GapSeverity:
        """
        Classify the severity of a requirement gap.

        Severity is deliberately conservative.

        No gap:
            NONE

        Partial gap:
            LOW / MEDIUM / HIGH depending on requirement priority
            and available evidence.

        Full gap:
            MEDIUM / HIGH / CRITICAL depending on requirement priority.

        This is a gap classification, not a recommendation or ATS score.
        """

        if gap_status == GapStatus.NONE:
            return GapSeverity.NONE

        priority = cls._normalize_priority(
            enriched_match
            .match
            .priority
        )

        evidence_count = (
            enriched_match.evidence_count
        )

        # -----------------------------------------------------------------
        # FULL GAP
        # -----------------------------------------------------------------

        if gap_status == GapStatus.FULL:

            if priority in {
                "critical",
                "mandatory",
                "required",
            }:
                return GapSeverity.CRITICAL

            if priority in {
                "high",
                "important",
            }:
                return GapSeverity.HIGH

            if priority in {
                "medium",
                "moderate",
            }:
                return GapSeverity.MEDIUM

            return GapSeverity.MEDIUM

        # -----------------------------------------------------------------
        # PARTIAL GAP
        # -----------------------------------------------------------------

        if gap_status == GapStatus.PARTIAL:

            if priority in {
                "critical",
                "mandatory",
                "required",
            }:

                if evidence_count == 0:
                    return GapSeverity.HIGH

                return GapSeverity.MEDIUM

            if priority in {
                "high",
                "important",
            }:

                if evidence_count == 0:
                    return GapSeverity.MEDIUM

                return GapSeverity.LOW

            if evidence_count == 0:
                return GapSeverity.MEDIUM

            return GapSeverity.LOW

        return GapSeverity.NONE

    # =========================================================================
    # REASON
    # =========================================================================

    @classmethod
    def _build_reason(
        cls,
        *,
        enriched_match: EnrichedRequirementMatch,
        gap_status: GapStatus,
        severity: GapSeverity,
    ) -> str:
        """
        Build a concise deterministic explanation of the gap.

        The reason describes the Phase 3.1/3.2 state only.

        It does not recommend how the candidate should address the gap.
        """

        requirement_subject = (
            enriched_match
            .match
            .requirement_subject
        )

        subject = (
            str(requirement_subject).strip()
            if requirement_subject is not None
            else "requirement"
        )

        evidence_count = (
            enriched_match.evidence_count
        )

        if gap_status == GapStatus.NONE:

            if evidence_count > 0:
                return (
                    f"{subject} is sufficiently covered by "
                    f"the existing candidate match and "
                    f"{evidence_count} evidence item(s)."
                )

            return (
                f"{subject} is sufficiently covered by "
                "the existing candidate match."
            )

        if gap_status == GapStatus.PARTIAL:

            if evidence_count > 0:
                return (
                    f"{subject} has partial candidate coverage "
                    f"with {evidence_count} evidence item(s); "
                    "coverage remains incomplete."
                )

            return (
                f"{subject} has partial candidate coverage "
                "but no supporting evidence was identified."
            )

        if gap_status == GapStatus.FULL:

            return (
                f"{subject} has no sufficient candidate "
                "coverage in the established match."
            )

        return (
            f"{subject} has an unclassified coverage state."
        )

    # =========================================================================
    # HELPERS
    # =========================================================================

    @staticmethod
    def _normalize_priority(
        priority: Any,
    ) -> str:
        """
        Normalize requirement priority without changing the source object.
        """

        if priority is None:
            return ""

        value = getattr(
            priority,
            "value",
            priority,
        )

        return str(
            value
        ).strip().lower()

    # =========================================================================
    # CONVENIENCE HELPERS
    # =========================================================================

    @staticmethod
    def analyze(
        enriched_match_result: EnrichedKnowledgeMatchResult,
    ) -> KnowledgeGapAnalysisResult:
        """
        Convenience class-level entry point.

        Equivalent to:

            KnowledgeGapAnalyzer().process(
                enriched_match_result
            )
        """

        return KnowledgeGapAnalyzer().process(
            enriched_match_result
        )


__all__ = [
    "KnowledgeGapAnalyzer",
]

