"""
Knowledge Match Enrichment Models
=================================

Phase 3.2

These models represent enriched evidence attached to the atomic
KnowledgeMatchResult produced by Phase 3.1.

Architecture:

    KnowledgeMatchResult
            +
    Candidate DocumentKnowledgeProfile
            +
    JDRequirementProfile
            |
            v
    KnowledgeMatchEnricher
            |
            v
    EnrichedKnowledgeMatchResult

Object In
----------
KnowledgeMatchResult
+
DocumentKnowledgeProfile
+
JDRequirementProfile

Object Out
-----------
EnrichedKnowledgeMatchResult

This module does NOT:

    - perform document extraction
    - modify KnowledgeProfile
    - modify JDRequirementProfile
    - calculate ATS scores
    - perform gap analysis
    - generate recommendations
    - rewrite resumes
    - generate cover letters
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.intelligence.utilities.knowledge.matching.match_models import (
    MatchBasis,
    MatchStatus,
    RequirementMatch,
)


# ============================================================================
# ENRICHED EVIDENCE
# ============================================================================


@dataclass(frozen=True)
class MatchEvidence:
    """
    One traceable piece of candidate evidence supporting a requirement match.
    """

    source: str

    evidence: str

    basis: MatchBasis

    candidate_entity_id: str | None = None

    domain: str | None = None

    confidence: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        if not isinstance(
            self.source,
            str,
        ) or not self.source.strip():

            raise ValueError(
                "MatchEvidence.source must be a "
                "non-empty string."
            )

        if not isinstance(
            self.evidence,
            str,
        ) or not self.evidence.strip():

            raise ValueError(
                "MatchEvidence.evidence must be a "
                "non-empty string."
            )

        if not isinstance(
            self.basis,
            MatchBasis,
        ):

            raise TypeError(
                "MatchEvidence.basis must be MatchBasis."
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
                "MatchEvidence.confidence must be numeric."
            ) from exc

        if not 0.0 <= confidence <= 1.0:

            raise ValueError(
                "MatchEvidence.confidence must be "
                "between 0 and 1."
            )


# ============================================================================
# ENRICHED REQUIREMENT MATCH
# ============================================================================


@dataclass(frozen=True)
class EnrichedRequirementMatch:
    """
    RequirementMatch plus structured evidence.

    The original atomic match is retained unchanged.
    """

    match: RequirementMatch

    evidence: tuple[
        MatchEvidence,
        ...
    ] = ()

    evidence_count: int = 0

    enrichment_confidence: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        if not isinstance(
            self.match,
            RequirementMatch,
        ):

            raise TypeError(
                "EnrichedRequirementMatch.match must "
                "be RequirementMatch."
            )

        evidence = tuple(
            self.evidence
        )

        object.__setattr__(
            self,
            "evidence",
            evidence,
        )

        if any(
            not isinstance(
                item,
                MatchEvidence,
            )
            for item in evidence
        ):

            raise TypeError(
                "EnrichedRequirementMatch.evidence must "
                "contain only MatchEvidence objects."
            )

        if self.evidence_count != len(
            evidence
        ):

            raise ValueError(
                "evidence_count must equal evidence length."
            )

        try:
            confidence = float(
                self.enrichment_confidence
            )
        except (
            TypeError,
            ValueError,
        ) as exc:

            raise ValueError(
                "enrichment_confidence must be numeric."
            ) from exc

        if not 0.0 <= confidence <= 1.0:

            raise ValueError(
                "enrichment_confidence must be "
                "between 0 and 1."
            )


# ============================================================================
# ENRICHED RESULT
# ============================================================================


@dataclass(frozen=True)
class EnrichedKnowledgeMatchResult:
    """
    Complete Phase 3.2 enrichment result.

    The original KnowledgeMatchResult remains available through
    match_result.
    """

    match_result: Any

    matches: tuple[
        EnrichedRequirementMatch,
        ...
    ] = ()

    total_requirements: int = 0

    evidence_backed_count: int = 0

    enrichment_confidence: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        from app.intelligence.utilities.knowledge.matching.match_models import (
            KnowledgeMatchResult,
        )

        if not isinstance(
            self.match_result,
            KnowledgeMatchResult,
        ):

            raise TypeError(
                "match_result must be KnowledgeMatchResult."
            )

        matches = tuple(
            self.matches
        )

        object.__setattr__(
            self,
            "matches",
            matches,
        )

        if any(
            not isinstance(
                item,
                EnrichedRequirementMatch,
            )
            for item in matches
        ):

            raise TypeError(
                "matches must contain only "
                "EnrichedRequirementMatch objects."
            )

        if self.total_requirements != len(
            matches
        ):

            raise ValueError(
                "total_requirements does not match matches."
            )

        expected_evidence_backed = sum(
            item.evidence_count > 0
            for item in matches
        )

        if (
            self.evidence_backed_count
            != expected_evidence_backed
        ):

            raise ValueError(
                "evidence_backed_count does not "
                "match matches."
            )

        try:
            confidence = float(
                self.enrichment_confidence
            )
        except (
            TypeError,
            ValueError,
        ) as exc:

            raise ValueError(
                "enrichment_confidence must be numeric."
            ) from exc

        if not 0.0 <= confidence <= 1.0:

            raise ValueError(
                "enrichment_confidence must be "
                "between 0 and 1."
            )

    @classmethod
    def from_matches(
        cls,
        *,
        match_result: Any,
        matches: list[EnrichedRequirementMatch],
    ) -> "EnrichedKnowledgeMatchResult":
        """
        Construct an enriched result from atomic enriched matches.
        """

        items = tuple(
            matches
        )

        evidence_backed = sum(
            item.evidence_count > 0
            for item in items
        )

        if not items:

            confidence = 0.0

        else:

            confidence = (
                sum(
                    item.enrichment_confidence
                    for item in items
                )
                / len(items)
            )

        return cls(
            match_result=match_result,

            matches=items,

            total_requirements=len(
                items
            ),

            evidence_backed_count=(
                evidence_backed
            ),

            enrichment_confidence=round(
                confidence,
                4,
            ),
        )


__all__ = [
    "MatchEvidence",
    "EnrichedRequirementMatch",
    "EnrichedKnowledgeMatchResult",
]