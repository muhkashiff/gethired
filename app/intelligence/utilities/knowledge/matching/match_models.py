"""
Knowledge Match Models
======================

Phase 3.1 - Knowledge Matcher contracts.

These models represent the direct output of requirement-to-candidate
matching.

Architecture:

    Resume DocumentKnowledgeProfile
                    +
    JDRequirementProfile
                    |
                    v
            KnowledgeMatcher
                    |
                    v
           KnowledgeMatchResult

Important
---------
This module does NOT:

    - perform extraction
    - modify KnowledgeProfile
    - modify JDRequirementProfile
    - calculate ATS scores
    - perform gap analysis
    - generate recommendations
    - generate cover letters

Those responsibilities belong to later phases.

Object In
---------
KnowledgeMatchRequest

Object Out
----------
KnowledgeMatchResult
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ============================================================================
# MATCH STATUS
# ============================================================================


class MatchStatus(str, Enum):
    """
    Result of comparing one JD requirement against candidate knowledge.
    """

    MATCHED = "matched"

    PARTIAL = "partial"

    UNMATCHED = "unmatched"


# ============================================================================
# MATCH BASIS
# ============================================================================


class MatchBasis(str, Enum):
    """
    Evidence used to establish a match.

    ENTITY_ID
        Exact ontology/entity identity.

    CANONICAL
        Exact normalized canonical concept.

    STATEMENT_ENTITY
        Requirement concept appears inside a candidate business statement.

    DOMAIN
        Candidate has compatible domain evidence.

    NONE
        No positive evidence was found.
    """

    ENTITY_ID = "entity_id"

    CANONICAL = "canonical"

    STATEMENT_ENTITY = "statement_entity"

    DOMAIN = "domain"

    NONE = "none"


# ============================================================================
# REQUIREMENT MATCH
# ============================================================================


@dataclass(frozen=True)
class RequirementMatch:
    """
    Match result for one JDRequirement.

    This is intentionally an atomic object.

    It explains:

        what requirement was evaluated
        what candidate evidence was found
        how it was matched
        how strong the match is
    """

    requirement_id: str

    requirement_subject: str

    requirement_type: str

    priority: str

    status: MatchStatus

    score: float

    basis: MatchBasis

    candidate_entity_ids: tuple[str, ...] = ()

    candidate_evidence: tuple[str, ...] = ()

    evidence_count: int = 0

    reason: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        if not isinstance(
            self.requirement_id,
            str,
        ) or not self.requirement_id.strip():

            raise ValueError(
                "RequirementMatch.requirement_id "
                "must be a non-empty string."
            )

        if not isinstance(
            self.requirement_subject,
            str,
        ) or not self.requirement_subject.strip():

            raise ValueError(
                "RequirementMatch.requirement_subject "
                "must be a non-empty string."
            )

        if not isinstance(
            self.status,
            MatchStatus,
        ):

            raise TypeError(
                "RequirementMatch.status "
                "must be MatchStatus."
            )

        if not isinstance(
            self.basis,
            MatchBasis,
        ):

            raise TypeError(
                "RequirementMatch.basis "
                "must be MatchBasis."
            )

        try:
            score = float(self.score)
        except (
            TypeError,
            ValueError,
        ) as exc:

            raise ValueError(
                "RequirementMatch.score "
                "must be numeric."
            ) from exc

        if not 0.0 <= score <= 1.0:

            raise ValueError(
                "RequirementMatch.score "
                "must be between 0 and 1."
            )

        if self.evidence_count != len(
            self.candidate_evidence
        ):

            raise ValueError(
                "RequirementMatch.evidence_count "
                "must equal candidate_evidence length."
            )


# ============================================================================
# MATCH REQUEST
# ============================================================================


@dataclass(frozen=True)
class KnowledgeMatchRequest:
    """
    Input object for KnowledgeMatcher.

    Object In
        Resume DocumentKnowledgeProfile
        +
        JDRequirementProfile
    """

    resume_profile: Any

    jd_requirement_profile: Any

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        if self.resume_profile is None:

            raise ValueError(
                "KnowledgeMatchRequest.resume_profile "
                "cannot be None."
            )

        if self.jd_requirement_profile is None:

            raise ValueError(
                "KnowledgeMatchRequest.jd_requirement_profile "
                "cannot be None."
            )


# ============================================================================
# MATCH RESULT
# ============================================================================


@dataclass(frozen=True)
class KnowledgeMatchResult:
    """
    Complete output of KnowledgeMatcher.

    This is NOT the final KnowledgeMatchProfile.

    Phase 4 will transform this atomic matching output into the richer
    KnowledgeMatchProfile used by later analysis stages.
    """

    matches: tuple[
        RequirementMatch,
        ...
    ] = ()

    total_requirements: int = 0

    matched_count: int = 0

    partial_count: int = 0

    unmatched_count: int = 0

    overall_score: float = 0.0

    confidence: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

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
                match,
                RequirementMatch,
            )
            for match in matches
        ):

            raise TypeError(
                "KnowledgeMatchResult.matches "
                "must contain only RequirementMatch objects."
            )

        expected_total = len(matches)

        if (
            self.total_requirements
            != expected_total
        ):

            raise ValueError(
                "total_requirements does not "
                "match matches."
            )

        expected_matched = sum(
            match.status
            == MatchStatus.MATCHED
            for match in matches
        )

        expected_partial = sum(
            match.status
            == MatchStatus.PARTIAL
            for match in matches
        )

        expected_unmatched = sum(
            match.status
            == MatchStatus.UNMATCHED
            for match in matches
        )

        if (
            self.matched_count
            != expected_matched
        ):

            raise ValueError(
                "matched_count does not "
                "match matches."
            )

        if (
            self.partial_count
            != expected_partial
        ):

            raise ValueError(
                "partial_count does not "
                "match matches."
            )

        if (
            self.unmatched_count
            != expected_unmatched
        ):

            raise ValueError(
                "unmatched_count does not "
                "match matches."
            )

        for field_name in (
            "overall_score",
            "confidence",
        ):

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
                    f"{field_name} must be "
                    "between 0 and 1."
                )

    # =========================================================================
    # FACTORY
    # =========================================================================

    @classmethod
    def from_matches(
        cls,
        matches: list[RequirementMatch],
    ) -> "KnowledgeMatchResult":
        """
        Construct a complete result from atomic matches.

        All counters are derived from the actual match objects.
        """

        items = tuple(
            matches
        )

        if not items:

            return cls(
                matches=(),
                total_requirements=0,
                matched_count=0,
                partial_count=0,
                unmatched_count=0,
                overall_score=0.0,
                confidence=0.0,
            )

        matched = sum(
            match.status
            == MatchStatus.MATCHED
            for match in items
        )

        partial = sum(
            match.status
            == MatchStatus.PARTIAL
            for match in items
        )

        unmatched = sum(
            match.status
            == MatchStatus.UNMATCHED
            for match in items
        )

        overall_score = (
            sum(
                match.score
                for match in items
            )
            / len(items)
        )

        evidence_backed = sum(
            match.evidence_count > 0
            for match in items
        )

        confidence = (
            evidence_backed
            / len(items)
        )

        return cls(
            matches=items,

            total_requirements=len(
                items
            ),

            matched_count=matched,

            partial_count=partial,

            unmatched_count=unmatched,

            overall_score=round(
                overall_score,
                4,
            ),

            confidence=round(
                confidence,
                4,
            ),
        )


__all__ = [
    "MatchStatus",
    "MatchBasis",
    "RequirementMatch",
    "KnowledgeMatchRequest",
    "KnowledgeMatchResult",
]