"""
ATS / Resume Analysis Models
=============================

Phase 5 result contracts.

These are observation/result models only.

They do not contain recommendation logic or resume rewriting logic.

All models are immutable.

Score convention
----------------

All normalized scores use:

    0.0 <= score <= 1.0

Confidence convention
---------------------

All confidence values use:

    0.0 <= confidence <= 1.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


from app.intelligence.utilities.knowledge.ats.ats_analysis_request import (
    ATSResumeAnalysisRequest,
)


# ============================================================================
# VALIDATION
# ============================================================================


def _validate_unit_interval(
    value: float,
    field_name: str,
) -> float:

    try:
        normalized = float(value)
    except (
        TypeError,
        ValueError,
    ) as exc:
        raise ValueError(
            f"{field_name} must be numeric."
        ) from exc

    if not 0.0 <= normalized <= 1.0:
        raise ValueError(
            f"{field_name} must be between 0 and 1."
        )

    return round(
        normalized,
        4,
    )


# ============================================================================
# ATS SCORE
# ============================================================================


@dataclass(frozen=True)
class ATSScore:
    """
    Final ATS score.
    """

    score: float

    confidence: float

    def __post_init__(self) -> None:

        object.__setattr__(
            self,
            "score",
            _validate_unit_interval(
                self.score,
                "score",
            ),
        )

        object.__setattr__(
            self,
            "confidence",
            _validate_unit_interval(
                self.confidence,
                "confidence",
            ),
        )


# ============================================================================
# SCORE BREAKDOWN
# ============================================================================


@dataclass(frozen=True)
class ATSScoreBreakdown:
    """
    Component-level ATS score breakdown.

    Weights are retained so the resulting score remains traceable.
    """

    keyword_score: float = 0.0

    section_score: float = 0.0

    formatting_score: float = 0.0

    readability_score: float = 0.0

    terminology_score: float = 0.0

    quantification_score: float = 0.0

    parseability_score: float = 0.0

    structure_score: float = 0.0

    weights: dict[str, float] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        score_fields = (
            "keyword_score",
            "section_score",
            "formatting_score",
            "readability_score",
            "terminology_score",
            "quantification_score",
            "parseability_score",
            "structure_score",
        )

        for field_name in score_fields:

            object.__setattr__(
                self,
                field_name,
                _validate_unit_interval(
                    getattr(
                        self,
                        field_name,
                    ),
                    field_name,
                ),
            )

        weights = dict(
            self.weights
        )

        if not weights:
            weights = {
                "keyword": 1.0,
            }

        normalized_weights = {}

        for name, value in weights.items():

            try:
                numeric = float(value)
            except (
                TypeError,
                ValueError,
            ) as exc:
                raise ValueError(
                    f"weight {name!r} must be numeric."
                ) from exc

            if numeric < 0.0:
                raise ValueError(
                    f"weight {name!r} cannot be negative."
                )

            normalized_weights[name] = numeric

        total = sum(
            normalized_weights.values()
        )

        if total <= 0.0:
            raise ValueError(
                "weights must contain a positive total."
            )

        object.__setattr__(
            self,
            "weights",
            normalized_weights,
        )

    @property
    def weighted_score(self) -> float:
        """
        Return the normalized weighted component score.
        """

        scores = {
            "keyword": self.keyword_score,
            "section": self.section_score,
            "formatting": self.formatting_score,
            "readability": self.readability_score,
            "terminology": self.terminology_score,
            "quantification": self.quantification_score,
            "parseability": self.parseability_score,
        }

        numerator = 0.0
        denominator = 0.0

        for name, weight in self.weights.items():

            if name not in scores:
                continue

            numerator += (
                scores[name]
                * weight
            )

            denominator += weight

        if denominator <= 0.0:
            return 0.0

        return round(
            numerator / denominator,
            4,
        )


# ============================================================================
# KEYWORD ANALYSIS
# ============================================================================


@dataclass(frozen=True)
class ATSKeywordAnalysis:

    required_keywords: tuple[str, ...] = ()

    matched_keywords: tuple[str, ...] = ()

    missing_keywords: tuple[str, ...] = ()

    additional_keywords: tuple[str, ...] = ()

    keyword_coverage_score: float = 0.0

    confidence: float = 0.0

    def __post_init__(self) -> None:

        required = tuple(
            self.required_keywords
        )

        matched = tuple(
            self.matched_keywords
        )

        missing = tuple(
            self.missing_keywords
        )

        additional = tuple(
            self.additional_keywords
        )

        object.__setattr__(
            self,
            "required_keywords",
            required,
        )

        object.__setattr__(
            self,
            "matched_keywords",
            matched,
        )

        object.__setattr__(
            self,
            "missing_keywords",
            missing,
        )

        object.__setattr__(
            self,
            "additional_keywords",
            additional,
        )

        if not set(matched).issubset(
            set(required)
        ):
            raise ValueError(
                "matched_keywords must be contained "
                "within required_keywords."
            )

        if not set(missing).issubset(
            set(required)
        ):
            raise ValueError(
                "missing_keywords must be contained "
                "within required_keywords."
            )

        if set(matched) & set(missing):
            raise ValueError(
                "A keyword cannot be both matched and missing."
            )

        object.__setattr__(
            self,
            "keyword_coverage_score",
            _validate_unit_interval(
                self.keyword_coverage_score,
                "keyword_coverage_score",
            ),
        )

        object.__setattr__(
            self,
            "confidence",
            _validate_unit_interval(
                self.confidence,
                "confidence",
            ),
        )


# ============================================================================
# SECTION ANALYSIS
# ============================================================================


@dataclass(frozen=True)
class ATSSectionAnalysis:

    detected_sections: tuple[str, ...] = ()

    missing_sections: tuple[str, ...] = ()

    section_order_valid: bool = True

    section_completeness_score: float = 0.0

    confidence: float = 0.0

    def __post_init__(self) -> None:

        object.__setattr__(
            self,
            "detected_sections",
            tuple(
                self.detected_sections
            ),
        )

        object.__setattr__(
            self,
            "missing_sections",
            tuple(
                self.missing_sections
            ),
        )

        object.__setattr__(
            self,
            "section_completeness_score",
            _validate_unit_interval(
                self.section_completeness_score,
                "section_completeness_score",
            ),
        )

        object.__setattr__(
            self,
            "confidence",
            _validate_unit_interval(
                self.confidence,
                "confidence",
            ),
        )


# ============================================================================
# FORMATTING ANALYSIS
# ============================================================================


@dataclass(frozen=True)
class ATSFormattingAnalysis:

    formatting_score: float = 0.0

    has_complex_layout: bool = False

    has_tables: bool = False

    has_columns: bool = False

    has_graphics: bool = False

    has_unusual_symbols: bool = False

    confidence: float = 0.0

    def __post_init__(self) -> None:

        object.__setattr__(
            self,
            "formatting_score",
            _validate_unit_interval(
                self.formatting_score,
                "formatting_score",
            ),
        )

        object.__setattr__(
            self,
            "confidence",
            _validate_unit_interval(
                self.confidence,
                "confidence",
            ),
        )


# ============================================================================
# READABILITY
# ============================================================================


@dataclass(frozen=True)
class ATSReadabilityAnalysis:

    readability_score: float = 0.0

    estimated_word_count: int = 0

    average_sentence_length: float = 0.0

    long_sentence_count: int = 0

    confidence: float = 0.0

    def __post_init__(self) -> None:

        if self.estimated_word_count < 0:
            raise ValueError(
                "estimated_word_count cannot be negative."
            )

        if self.long_sentence_count < 0:
            raise ValueError(
                "long_sentence_count cannot be negative."
            )

        object.__setattr__(
            self,
            "readability_score",
            _validate_unit_interval(
                self.readability_score,
                "readability_score",
            ),
        )

        object.__setattr__(
            self,
            "average_sentence_length",
            round(
                float(
                    self.average_sentence_length
                ),
                4,
            ),
        )

        object.__setattr__(
            self,
            "confidence",
            _validate_unit_interval(
                self.confidence,
                "confidence",
            ),
        )


# ============================================================================
# TERMINOLOGY
# ============================================================================


@dataclass(frozen=True)
class ATSTerminologyAnalysis:

    aligned_terms: tuple[str, ...] = ()

    missing_terms: tuple[str, ...] = ()

    terminology_score: float = 0.0

    confidence: float = 0.0

    def __post_init__(self) -> None:

        object.__setattr__(
            self,
            "aligned_terms",
            tuple(
                self.aligned_terms
            ),
        )

        object.__setattr__(
            self,
            "missing_terms",
            tuple(
                self.missing_terms
            ),
        )

        object.__setattr__(
            self,
            "terminology_score",
            _validate_unit_interval(
                self.terminology_score,
                "terminology_score",
            ),
        )

        object.__setattr__(
            self,
            "confidence",
            _validate_unit_interval(
                self.confidence,
                "confidence",
            ),
        )


# ============================================================================
# QUANTIFICATION
# ============================================================================


@dataclass(frozen=True)
class ATSQuantificationAnalysis:

    quantified_achievement_count: int = 0

    quantified_bullet_count: int = 0

    quantification_score: float = 0.0

    confidence: float = 0.0

    def __post_init__(self) -> None:

        if self.quantified_achievement_count < 0:
            raise ValueError(
                "quantified_achievement_count cannot be negative."
            )

        if self.quantified_bullet_count < 0:
            raise ValueError(
                "quantified_bullet_count cannot be negative."
            )

        object.__setattr__(
            self,
            "quantification_score",
            _validate_unit_interval(
                self.quantification_score,
                "quantification_score",
            ),
        )

        object.__setattr__(
            self,
            "confidence",
            _validate_unit_interval(
                self.confidence,
                "confidence",
            ),
        )


# ============================================================================
# PARSEABILITY
# ============================================================================


@dataclass(frozen=True)
class ATSParseabilityAnalysis:

    parseable: bool = True

    parseability_score: float = 0.0

    extraction_warning_count: int = 0

    warnings: tuple[str, ...] = ()

    confidence: float = 0.0

    def __post_init__(self) -> None:

        warnings = tuple(
            self.warnings
        )

        object.__setattr__(
            self,
            "warnings",
            warnings,
        )

        if (
            self.extraction_warning_count
            != len(warnings)
        ):
            raise ValueError(
                "extraction_warning_count must match "
                "the number of warnings."
            )

        object.__setattr__(
            self,
            "parseability_score",
            _validate_unit_interval(
                self.parseability_score,
                "parseability_score",
            ),
        )

        object.__setattr__(
            self,
            "confidence",
            _validate_unit_interval(
                self.confidence,
                "confidence",
            ),
        )


# ============================================================================
# FINAL RESULT
# ============================================================================


@dataclass(frozen=True)
class ATSResumeAnalysisResult:
    """
    Complete Phase 5 ATS result.

    The exact original request is retained.
    """

    request: ATSResumeAnalysisRequest

    ats_score: ATSScore

    score_breakdown: ATSScoreBreakdown

    keyword_analysis: ATSKeywordAnalysis

    section_analysis: ATSSectionAnalysis

    formatting_analysis: ATSFormattingAnalysis

    readability_analysis: ATSReadabilityAnalysis

    terminology_analysis: ATSTerminologyAnalysis

    quantification_analysis: ATSQuantificationAnalysis

    parseability_analysis: ATSParseabilityAnalysis

    confidence: float

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        if not isinstance(
            self.request,
            ATSResumeAnalysisRequest,
        ):
            raise TypeError(
                "request must be ATSResumeAnalysisRequest."
            )

        components = (
            (
                "ats_score",
                self.ats_score,
                ATSScore,
            ),
            (
                "score_breakdown",
                self.score_breakdown,
                ATSScoreBreakdown,
            ),
            (
                "keyword_analysis",
                self.keyword_analysis,
                ATSKeywordAnalysis,
            ),
            (
                "section_analysis",
                self.section_analysis,
                ATSSectionAnalysis,
            ),
            (
                "formatting_analysis",
                self.formatting_analysis,
                ATSFormattingAnalysis,
            ),
            (
                "readability_analysis",
                self.readability_analysis,
                ATSReadabilityAnalysis,
            ),
            (
                "terminology_analysis",
                self.terminology_analysis,
                ATSTerminologyAnalysis,
            ),
            (
                "quantification_analysis",
                self.quantification_analysis,
                ATSQuantificationAnalysis,
            ),
            (
                "parseability_analysis",
                self.parseability_analysis,
                ATSParseabilityAnalysis,
            ),
        )

        for (
            field_name,
            value,
            expected_type,
        ) in components:

            if not isinstance(
                value,
                expected_type,
            ):
                raise TypeError(
                    f"{field_name} must be "
                    f"{expected_type.__name__}."
                )

        object.__setattr__(
            self,
            "confidence",
            _validate_unit_interval(
                self.confidence,
                "confidence",
            ),
        )

        object.__setattr__(
            self,
            "metadata",
            dict(
                self.metadata
            ),
        )

    @property
    def knowledge_match_profile(self):
        """
        Compatibility/access property.

        The authoritative Phase 4 object remains inside the request.
        """

        return (
            self.request
            .knowledge_match_profile
        )


__all__ = [
    "ATSScore",
    "ATSScoreBreakdown",
    "ATSKeywordAnalysis",
    "ATSSectionAnalysis",
    "ATSFormattingAnalysis",
    "ATSReadabilityAnalysis",
    "ATSTerminologyAnalysis",
    "ATSQuantificationAnalysis",
    "ATSParseabilityAnalysis",
    "ATSResumeAnalysisResult",
]