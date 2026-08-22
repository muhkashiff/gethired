"""
Phase 6 Recommendation Models
==============================

Object-in / object-out contracts for resume recommendations.

Pipeline
--------

    ATSResumeAnalysisResult
            |
            v
    RecommendationAnalyzer
            |
            v
    RecommendationResult

Design rules
------------

1. Phase 6 consumes the exact Phase 5 ATSResumeAnalysisResult object.
2. Phase 6 preserves the exact Phase 5 object identity.
3. Phase 6 preserves the exact Phase 4 KnowledgeMatchProfile identity.
4. Recommendations are typed objects, never dictionaries.
5. RecommendationResult is the sole aggregate output of Phase 6.
6. No SemanticEntity is defined here.
7. Compatibility conversion is allowed only when constructing a model
   from legacy data. The public pipeline remains object-based.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
        ATSResumeAnalysisResult,
    )

    from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
        KnowledgeMatchProfile,
    )


# ============================================================================
# HELPERS
# ============================================================================


def _text(
    value: Any,
    field_name: str,
) -> str:
    if value is None:
        return ""

    result = str(value).strip()

    if not result:
        raise ValueError(
            f"{field_name} must not be empty."
        )

    return result


def _score(
    value: Any,
    field_name: str,
) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(
            f"{field_name} must be numeric."
        ) from exc

    if not 0.0 <= result <= 1.0:
        raise ValueError(
            f"{field_name} must be between 0.0 and 1.0."
        )

    return result


def _non_negative_int(
    value: Any,
    field_name: str,
) -> int:
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(
            f"{field_name} must be an integer."
        ) from exc

    if result < 0:
        raise ValueError(
            f"{field_name} must be >= 0."
        )

    return result


def _tuple_strings(
    value: Optional[Iterable[Any]],
) -> tuple[str, ...]:
    if value is None:
        return ()

    if isinstance(value, str):
        value = (value,)

    return tuple(
        str(item).strip()
        for item in value
        if item is not None
        and str(item).strip()
    )


# ============================================================================
# ENUMS
# ============================================================================


class RecommendationType(str, Enum):
    """Classification of a Phase-6 recommendation."""

    KEYWORD = "keyword"
    SECTION = "section"
    FORMATTING = "formatting"
    READABILITY = "readability"
    TERMINOLOGY = "terminology"
    QUANTIFICATION = "quantification"
    PARSEABILITY = "parseability"
    KNOWLEDGE_GAP = "knowledge_gap"
    GENERAL = "general"


class RecommendationPriority(str, Enum):
    """Execution priority of a recommendation."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationStatus(str, Enum):
    """Lifecycle state of a recommendation."""

    OPEN = "open"
    ACTIONABLE = "actionable"
    INFORMATIONAL = "informational"


# ============================================================================
# RECOMMENDATION
# ============================================================================


@dataclass(frozen=True)
class Recommendation:
    """
    One typed Phase-6 recommendation.

    No Phase-5 dictionaries or reconstructed Phase-4 objects are stored.
    """

    recommendation_id: str
    recommendation_type: RecommendationType
    priority: RecommendationPriority

    title: str
    description: str

    rationale: str = ""

    status: RecommendationStatus = (
        RecommendationStatus.ACTIONABLE
    )

    source_component: str = ""

    evidence: tuple[str, ...] = ()

    target_items: tuple[str, ...] = ()

    confidence: float = 1.0

    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "recommendation_id",
            _text(
                self.recommendation_id,
                "Recommendation.recommendation_id",
            ),
        )

        object.__setattr__(
            self,
            "title",
            _text(
                self.title,
                "Recommendation.title",
            ),
        )

        object.__setattr__(
            self,
            "description",
            _text(
                self.description,
                "Recommendation.description",
            ),
        )

        object.__setattr__(
            self,
            "rationale",
            str(
                self.rationale or ""
            ).strip(),
        )

        object.__setattr__(
            self,
            "source_component",
            str(
                self.source_component or ""
            ).strip(),
        )

        object.__setattr__(
            self,
            "evidence",
            _tuple_strings(
                self.evidence
            ),
        )

        object.__setattr__(
            self,
            "target_items",
            _tuple_strings(
                self.target_items
            ),
        )

        object.__setattr__(
            self,
            "confidence",
            _score(
                self.confidence,
                "Recommendation.confidence",
            ),
        )

        object.__setattr__(
            self,
            "metadata",
            dict(
                self.metadata or {}
            ),
        )

    @property
    def is_high_priority(self) -> bool:
        return self.priority in (
            RecommendationPriority.CRITICAL,
            RecommendationPriority.HIGH,
        )

    @property
    def is_actionable(self) -> bool:
        return (
            self.status
            == RecommendationStatus.ACTIONABLE
        )

    @classmethod
    def from_value(
        cls,
        value: Any,
    ) -> "Recommendation":
        """
        Compatibility constructor.

        Normal Phase-6 execution already produces Recommendation objects.
        """

        if isinstance(
            value,
            cls,
        ):
            return value

        if not isinstance(
            value,
            Mapping,
        ):
            raise TypeError(
                "Recommendation must be a Recommendation "
                "or mapping."
            )

        return cls(
            recommendation_id=str(
                value.get(
                    "recommendation_id",
                    value.get(
                        "id",
                        "",
                    ),
                )
            ),
            recommendation_type=RecommendationType(
                value.get(
                    "recommendation_type",
                    value.get(
                        "type",
                        RecommendationType.GENERAL.value,
                    ),
                )
            ),
            priority=RecommendationPriority(
                value.get(
                    "priority",
                    RecommendationPriority.MEDIUM.value,
                )
            ),
            title=str(
                value.get(
                    "title",
                    "",
                )
            ),
            description=str(
                value.get(
                    "description",
                    "",
                )
            ),
            rationale=str(
                value.get(
                    "rationale",
                    "",
                )
            ),
            status=RecommendationStatus(
                value.get(
                    "status",
                    RecommendationStatus.ACTIONABLE.value,
                )
            ),
            source_component=str(
                value.get(
                    "source_component",
                    "",
                )
            ),
            evidence=value.get(
                "evidence",
                (),
            ),
            target_items=value.get(
                "target_items",
                (),
            ),
            confidence=value.get(
                "confidence",
                1.0,
            ),
            metadata=value.get(
                "metadata",
                {},
            ),
        )


# ============================================================================
# SUMMARY
# ============================================================================


@dataclass(frozen=True)
class RecommendationSummary:
    """Aggregate summary of Phase-6 recommendations."""

    total: int = 0

    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0

    keyword_count: int = 0
    section_count: int = 0
    formatting_count: int = 0
    readability_count: int = 0
    terminology_count: int = 0
    quantification_count: int = 0
    parseability_count: int = 0
    knowledge_gap_count: int = 0

    def __post_init__(self) -> None:
        fields = (
            "total",
            "critical",
            "high",
            "medium",
            "low",
            "keyword_count",
            "section_count",
            "formatting_count",
            "readability_count",
            "terminology_count",
            "quantification_count",
            "parseability_count",
            "knowledge_gap_count",
        )

        for name in fields:
            object.__setattr__(
                self,
                name,
                _non_negative_int(
                    getattr(
                        self,
                        name,
                    ),
                    f"RecommendationSummary.{name}",
                ),
            )

    @classmethod
    def from_recommendations(
        cls,
        recommendations: Iterable[Recommendation],
    ) -> "RecommendationSummary":
        items = tuple(
            Recommendation.from_value(
                item
            )
            for item in recommendations
        )

        return cls(
            total=len(items),

            critical=sum(
                1
                for item in items
                if item.priority
                == RecommendationPriority.CRITICAL
            ),

            high=sum(
                1
                for item in items
                if item.priority
                == RecommendationPriority.HIGH
            ),

            medium=sum(
                1
                for item in items
                if item.priority
                == RecommendationPriority.MEDIUM
            ),

            low=sum(
                1
                for item in items
                if item.priority
                == RecommendationPriority.LOW
            ),

            keyword_count=sum(
                1
                for item in items
                if item.recommendation_type
                == RecommendationType.KEYWORD
            ),

            section_count=sum(
                1
                for item in items
                if item.recommendation_type
                == RecommendationType.SECTION
            ),

            formatting_count=sum(
                1
                for item in items
                if item.recommendation_type
                == RecommendationType.FORMATTING
            ),

            readability_count=sum(
                1
                for item in items
                if item.recommendation_type
                == RecommendationType.READABILITY
            ),

            terminology_count=sum(
                1
                for item in items
                if item.recommendation_type
                == RecommendationType.TERMINOLOGY
            ),

            quantification_count=sum(
                1
                for item in items
                if item.recommendation_type
                == RecommendationType.QUANTIFICATION
            ),

            parseability_count=sum(
                1
                for item in items
                if item.recommendation_type
                == RecommendationType.PARSEABILITY
            ),

            knowledge_gap_count=sum(
                1
                for item in items
                if item.recommendation_type
                == RecommendationType.KNOWLEDGE_GAP
            ),
        )


# ============================================================================
# FINAL PHASE-6 RESULT
# ============================================================================


@dataclass
class RecommendationResult:
    """
    Complete Phase-6 aggregate result.

    Identity guarantees:

        result.ats_result is ats_result

    and:

        result.knowledge_match_profile
            is ats_result.knowledge_match_profile
    """

    ats_result: "ATSResumeAnalysisResult"

    recommendations: tuple[
        Recommendation,
        ...
    ] = ()

    summary: Optional[
        RecommendationSummary
    ] = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
            ATSResumeAnalysisResult,
        )

        if not isinstance(
            self.ats_result,
            ATSResumeAnalysisResult,
        ):
            raise TypeError(
                "RecommendationResult.ats_result must be "
                "an ATSResumeAnalysisResult."
            )

        self.ats_result.validate()

        self.recommendations = tuple(
            Recommendation.from_value(
                item
            )
            for item in self.recommendations
        )

        ids = [
            item.recommendation_id
            for item in self.recommendations
        ]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "RecommendationResult recommendation IDs "
                "must be unique."
            )

        calculated_summary = (
            RecommendationSummary.from_recommendations(
                self.recommendations
            )
        )

        if self.summary is None:
            self.summary = calculated_summary

        elif self.summary != calculated_summary:
            raise ValueError(
                "RecommendationResult.summary does not match "
                "the supplied recommendations."
            )

        self.metadata = dict(
            self.metadata or {}
        )

    # ========================================================================
    # IDENTITY
    # ========================================================================

    @property
    def knowledge_match_profile(
        self,
    ) -> "KnowledgeMatchProfile":
        """Return the exact Phase-4 object."""
        return self.ats_result.knowledge_match_profile

    @property
    def resume_profile(
        self,
    ) -> Any:
        """Return the exact Phase-1 resume profile."""
        return self.ats_result.resume_profile

    @property
    def jd_requirement_profile(
        self,
    ) -> Any:
        """Return the exact Phase-2 JD requirement profile."""
        return self.ats_result.jd_requirement_profile

    @property
    def score(
        self,
    ) -> Any:
        """Return the Phase-5 ATS score object."""
        return self.ats_result.ats_score

    @property
    def confidence(
        self,
    ) -> float:
        return self.ats_result.confidence

    @property
    def has_recommendations(
        self,
    ) -> bool:
        return bool(
            self.recommendations
        )

    # ========================================================================
    # FILTERING
    # ========================================================================

    def recommendations_of_type(
        self,
        recommendation_type: RecommendationType,
    ) -> tuple[Recommendation, ...]:
        return tuple(
            item
            for item in self.recommendations
            if item.recommendation_type
            == recommendation_type
        )

    def high_priority_recommendations(
        self,
    ) -> tuple[Recommendation, ...]:
        return tuple(
            item
            for item in self.recommendations
            if item.is_high_priority
        )

    # ========================================================================
    # VALIDATION
    # ========================================================================

    def validate(self) -> None:
        """Validate the complete Phase-6 object graph."""

        if not self.ats_result:
            raise ValueError(
                "RecommendationResult requires ats_result."
            )

        self.ats_result.validate()

        if (
            self.knowledge_match_profile
            is not self.ats_result.knowledge_match_profile
        ):
            raise ValueError(
                "RecommendationResult must preserve the exact "
                "Phase-4 KnowledgeMatchProfile."
            )

        ids = [
            item.recommendation_id
            for item in self.recommendations
        ]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "Recommendation IDs must be unique."
            )

        expected_summary = (
            RecommendationSummary.from_recommendations(
                self.recommendations
            )
        )

        if self.summary != expected_summary:
            raise ValueError(
                "RecommendationResult.summary is inconsistent "
                "with recommendations."
            )


__all__ = [
    "RecommendationType",
    "RecommendationPriority",
    "RecommendationStatus",
    "Recommendation",
    "RecommendationSummary",
    "RecommendationResult",
]