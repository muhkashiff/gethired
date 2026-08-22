
"""
Recommendation Request
======================

Phase 6 input boundary.

Canonical contract:

    ATSResumeAnalysisResult
            +
    RecommendationPolicy
            |
            v
    RecommendationRequest
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSResumeAnalysisResult,
)


@dataclass(frozen=True)
class RecommendationPolicy:
    """
    Controls Phase 6 recommendation generation.

    The policy does not contain resume content. It only controls thresholds
    and recommendation limits.
    """

    critical_ats_threshold: float = 0.50
    high_ats_threshold: float = 0.70
    medium_ats_threshold: float = 0.85

    keyword_high_threshold: float = 0.70
    keyword_medium_threshold: float = 0.85

    readability_long_sentence_threshold: int = 1

    max_recommendations: int = 20

    def __post_init__(self) -> None:
        thresholds = (
            "critical_ats_threshold",
            "high_ats_threshold",
            "medium_ats_threshold",
            "keyword_high_threshold",
            "keyword_medium_threshold",
        )

        for field_name in thresholds:
            value = float(getattr(self, field_name))

            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"{field_name} must be between 0.0 and 1.0."
                )

        if not (
            self.critical_ats_threshold
            <= self.high_ats_threshold
            <= self.medium_ats_threshold
        ):
            raise ValueError(
                "ATS thresholds must be ordered from lowest to highest."
            )

        if not (
            self.keyword_high_threshold
            <= self.keyword_medium_threshold
        ):
            raise ValueError(
                "Keyword thresholds must be ordered from lowest to highest."
            )

        if self.readability_long_sentence_threshold < 0:
            raise ValueError(
                "readability_long_sentence_threshold must be >= 0."
            )

        if self.max_recommendations <= 0:
            raise ValueError(
                "max_recommendations must be > 0."
            )


@dataclass(frozen=True)
class RecommendationRequest:
    """
    Phase 6 object-in contract.

    The ATS result is passed directly.

    No dictionary representation is accepted as the canonical input.
    """

    ats_analysis_result: ATSResumeAnalysisResult
    policy: RecommendationPolicy = field(
        default_factory=RecommendationPolicy,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.ats_analysis_result,
            ATSResumeAnalysisResult,
        ):
            raise TypeError(
                "RecommendationRequest.ats_analysis_result must be "
                "an ATSResumeAnalysisResult."
            )

        if not isinstance(
            self.policy,
            RecommendationPolicy,
        ):
            raise TypeError(
                "RecommendationRequest.policy must be "
                "a RecommendationPolicy."
            )

    @property
    def knowledge_match_profile(self) -> Any:
        """
        Return the exact Phase 4 profile carried by Phase 5.
        """

        return self.ats_analysis_result.knowledge_match_profile

    @property
    def resume_profile(self) -> Any:
        """Return the Phase 5 resume profile."""

        return self.ats_analysis_result.resume_profile

    @property
    def jd_requirement_profile(self) -> Any:
        """Return the Phase 5 JD requirement profile."""

        return self.ats_analysis_result.jd_requirement_profile

    def validate(self) -> None:
        """Validate the request and its nested Phase 5 object."""

        self.ats_analysis_result.validate()

        if not isinstance(
            self.policy,
            RecommendationPolicy,
        ):
            raise TypeError(
                "RecommendationRequest.policy must be "
                "RecommendationPolicy."
            )


__all__ = [
    "RecommendationPolicy",
    "RecommendationRequest",
]

