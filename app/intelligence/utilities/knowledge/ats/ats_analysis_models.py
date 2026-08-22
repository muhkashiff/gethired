"""
ATS Analysis Models
===================

Phase 5 typed object contracts.

Architecture
------------

    ATSResumeAnalysisRequest
                |
                v
        ATSResumeAnalyzer
                |
                v
      ATSResumeAnalysisResult

Design rules
------------

* Object-in / object-out.
* No raw analysis dictionaries at the public model boundary.
* Every analysis component has its own typed value object.
* KnowledgeMatchProfile is preserved by object identity.
* The existing ``score`` / ``breakdown`` vocabulary is supported through
  compatibility properties while the canonical object names are
  ``ats_score`` and ``score_breakdown``.
* Dictionary input is accepted only as a compatibility conversion at the
  model boundary and is immediately converted into typed objects.
* Semantic entities belong to the semantic model layer; this module does
  not define or import SemanticEntity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
        KnowledgeMatchProfile,
    )


# ============================================================================
# HELPERS
# ============================================================================


def _bounded_score(value: Any, field_name: str) -> float:
    """Normalize a score and enforce the ATS [0, 1] contract."""
    try:
        score = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(
            f"{field_name} must be a numeric value."
        ) from exc

    if not 0.0 <= score <= 1.0:
        raise ValueError(
            f"{field_name} must be between 0.0 and 1.0."
        )

    return score


def _non_negative_int(value: Any, field_name: str) -> int:
    """Normalize a non-negative integer."""
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


def _non_negative_float(value: Any, field_name: str) -> float:
    """Normalize a non-negative float."""
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise TypeError(
            f"{field_name} must be numeric."
        ) from exc

    if result < 0.0:
        raise ValueError(
            f"{field_name} must be >= 0."
        )

    return result


def _tuple_strings(
    value: Optional[Iterable[Any]],
    field_name: str,
) -> tuple[str, ...]:
    """Convert an iterable of values into an immutable string tuple."""
    if value is None:
        return ()

    if isinstance(value, str):
        return (value,)

    try:
        return tuple(
            str(item)
            for item in value
            if item is not None
        )
    except TypeError as exc:
        raise TypeError(
            f"{field_name} must be an iterable."
        ) from exc


def _dict_value(
    source: Mapping[str, Any],
    *names: str,
    default: Any = None,
) -> Any:
    """Read the first available key from a mapping."""
    for name in names:
        if name in source:
            return source[name]
    return default


# ============================================================================
# ATS SCORE
# ============================================================================


@dataclass(frozen=True)
class ATSScore:
    """
    Final normalized ATS score.

    ``score`` and ``confidence`` are always in [0, 1].
    """

    score: float = 0.0
    confidence: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "score",
            _bounded_score(
                self.score,
                "ATSScore.score",
            ),
        )
        object.__setattr__(
            self,
            "confidence",
            _bounded_score(
                self.confidence,
                "ATSScore.confidence",
            ),
        )

    @classmethod
    def from_value(
        cls,
        value: Any,
        confidence: Optional[float] = None,
    ) -> "ATSScore":
        """Create an ATSScore from an object or compatibility mapping."""
        if isinstance(value, cls):
            if confidence is None:
                return value
            return cls(
                score=value.score,
                confidence=confidence,
            )

        if isinstance(value, Mapping):
            score = _dict_value(
                value,
                "score",
                "ats_score",
                "value",
                default=0.0,
            )
            conf = _dict_value(
                value,
                "confidence",
                default=0.0 if confidence is None else confidence,
            )
            return cls(
                score=score,
                confidence=conf,
            )

        return cls(
            score=value,
            confidence=0.0 if confidence is None else confidence,
        )


# ============================================================================
# ATS SCORE BREAKDOWN
# ============================================================================


@dataclass(frozen=True)
class ATSScoreBreakdown:
    """
    Typed weighted ATS component breakdown.

    All component scores are normalized to [0, 1].

    ``weighted_score`` is the final weighted result produced by the policy.
    """

    keyword_score: float = 0.0
    section_score: float = 0.0
    formatting_score: float = 0.0
    readability_score: float = 0.0
    terminology_score: float = 0.0
    quantification_score: float = 0.0
    parseability_score: float = 0.0
    structure_score: float = 0.0
    weighted_score: float = 0.0

    def __post_init__(self) -> None:
        for field_name in (
            "keyword_score",
            "section_score",
            "formatting_score",
            "readability_score",
            "terminology_score",
            "quantification_score",
            "parseability_score",
            "structure_score",
            "weighted_score",
        ):
            object.__setattr__(
                self,
                field_name,
                _bounded_score(
                    getattr(self, field_name),
                    f"ATSScoreBreakdown.{field_name}",
                ),
            )

    @classmethod
    def from_value(
        cls,
        value: Any,
    ) -> "ATSScoreBreakdown":
        """Convert an existing object or dictionary to this value object."""
        if isinstance(value, cls):
            return value

        if not isinstance(value, Mapping):
            raise TypeError(
                "ATSScoreBreakdown must be an ATSScoreBreakdown "
                "or mapping."
            )

        return cls(
            keyword_score=_dict_value(
                value,
                "keyword_score",
                "keywords",
                default=0.0,
            ),
            section_score=_dict_value(
                value,
                "section_score",
                "sections",
                default=0.0,
            ),
            formatting_score=_dict_value(
                value,
                "formatting_score",
                "formatting",
                default=0.0,
            ),
            readability_score=_dict_value(
                value,
                "readability_score",
                "readability",
                default=0.0,
            ),
            terminology_score=_dict_value(
                value,
                "terminology_score",
                "terminology",
                default=0.0,
            ),
            quantification_score=_dict_value(
                value,
                "quantification_score",
                "quantification",
                default=0.0,
            ),
            parseability_score=_dict_value(
                value,
                "parseability_score",
                "parseability",
                default=0.0,
            ),
            structure_score=_dict_value(
                value,
                "structure_score",
                "structure",
                default=0.0,
            ),
            weighted_score=_dict_value(
                value,
                "weighted_score",
                "score",
                "total",
                default=0.0,
            ),
        )


# ============================================================================
# KEYWORD ANALYSIS
# ============================================================================


@dataclass(frozen=True)
class ATSKeywordAnalysis:
    """Typed keyword coverage analysis."""

    required_keywords: tuple[str, ...] = ()
    matched_keywords: tuple[str, ...] = ()
    missing_keywords: tuple[str, ...] = ()
    additional_keywords: tuple[str, ...] = ()
    keyword_coverage_score: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "required_keywords",
            _tuple_strings(
                self.required_keywords,
                "ATSKeywordAnalysis.required_keywords",
            ),
        )
        object.__setattr__(
            self,
            "matched_keywords",
            _tuple_strings(
                self.matched_keywords,
                "ATSKeywordAnalysis.matched_keywords",
            ),
        )
        object.__setattr__(
            self,
            "missing_keywords",
            _tuple_strings(
                self.missing_keywords,
                "ATSKeywordAnalysis.missing_keywords",
            ),
        )
        object.__setattr__(
            self,
            "additional_keywords",
            _tuple_strings(
                self.additional_keywords,
                "ATSKeywordAnalysis.additional_keywords",
            ),
        )
        object.__setattr__(
            self,
            "keyword_coverage_score",
            _bounded_score(
                self.keyword_coverage_score,
                "ATSKeywordAnalysis.keyword_coverage_score",
            ),
        )

    @classmethod
    def from_value(
        cls,
        value: Any,
    ) -> "ATSKeywordAnalysis":
        if isinstance(value, cls):
            return value

        if not isinstance(value, Mapping):
            raise TypeError(
                "ATSKeywordAnalysis must be an ATSKeywordAnalysis "
                "or mapping."
            )

        return cls(
            required_keywords=_dict_value(
                value,
                "required_keywords",
                "required",
                default=(),
            ),
            matched_keywords=_dict_value(
                value,
                "matched_keywords",
                "matched",
                default=(),
            ),
            missing_keywords=_dict_value(
                value,
                "missing_keywords",
                "missing",
                default=(),
            ),
            additional_keywords=_dict_value(
                value,
                "additional_keywords",
                "additional",
                default=(),
            ),
            keyword_coverage_score=_dict_value(
                value,
                "keyword_coverage_score",
                "coverage_score",
                "score",
                default=0.0,
            ),
        )


# ============================================================================
# SECTION ANALYSIS
# ============================================================================


@dataclass(frozen=True)
class ATSSectionAnalysis:
    """Typed resume-section analysis."""

    detected_sections: tuple[str, ...] = ()
    missing_sections: tuple[str, ...] = ()
    section_order_valid: bool = True
    section_completeness_score: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "detected_sections",
            _tuple_strings(
                self.detected_sections,
                "ATSSectionAnalysis.detected_sections",
            ),
        )
        object.__setattr__(
            self,
            "missing_sections",
            _tuple_strings(
                self.missing_sections,
                "ATSSectionAnalysis.missing_sections",
            ),
        )
        object.__setattr__(
            self,
            "section_completeness_score",
            _bounded_score(
                self.section_completeness_score,
                "ATSSectionAnalysis.section_completeness_score",
            ),
        )

    @classmethod
    def from_value(
        cls,
        value: Any,
    ) -> "ATSSectionAnalysis":
        if isinstance(value, cls):
            return value

        if not isinstance(value, Mapping):
            raise TypeError(
                "ATSSectionAnalysis must be an ATSSectionAnalysis "
                "or mapping."
            )

        return cls(
            detected_sections=_dict_value(
                value,
                "detected_sections",
                "sections",
                default=(),
            ),
            missing_sections=_dict_value(
                value,
                "missing_sections",
                "missing",
                default=(),
            ),
            section_order_valid=_dict_value(
                value,
                "section_order_valid",
                "order_valid",
                default=True,
            ),
            section_completeness_score=_dict_value(
                value,
                "section_completeness_score",
                "completeness_score",
                "score",
                default=0.0,
            ),
        )


# ============================================================================
# FORMATTING ANALYSIS
# ============================================================================


@dataclass(frozen=True)
class ATSFormattingAnalysis:
    """Typed ATS formatting observations."""

    has_complex_layout: bool = False
    has_tables: bool = False
    has_columns: bool = False
    has_graphics: bool = False
    formatting_score: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "formatting_score",
            _bounded_score(
                self.formatting_score,
                "ATSFormattingAnalysis.formatting_score",
            ),
        )

    @classmethod
    def from_value(
        cls,
        value: Any,
    ) -> "ATSFormattingAnalysis":
        if isinstance(value, cls):
            return value

        if not isinstance(value, Mapping):
            raise TypeError(
                "ATSFormattingAnalysis must be an ATSFormattingAnalysis "
                "or mapping."
            )

        return cls(
            has_complex_layout=bool(
                _dict_value(
                    value,
                    "has_complex_layout",
                    "complex_layout",
                    default=False,
                )
            ),
            has_tables=bool(
                _dict_value(
                    value,
                    "has_tables",
                    "tables",
                    default=False,
                )
            ),
            has_columns=bool(
                _dict_value(
                    value,
                    "has_columns",
                    "columns",
                    default=False,
                )
            ),
            has_graphics=bool(
                _dict_value(
                    value,
                    "has_graphics",
                    "graphics",
                    default=False,
                )
            ),
            formatting_score=_dict_value(
                value,
                "formatting_score",
                "score",
                default=0.0,
            ),
        )


# ============================================================================
# READABILITY ANALYSIS
# ============================================================================


@dataclass(frozen=True)
class ATSReadabilityAnalysis:
    """Typed readability observations."""

    estimated_word_count: int = 0
    long_sentence_count: int = 0
    average_sentence_length: float = 0.0
    readability_score: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "estimated_word_count",
            _non_negative_int(
                self.estimated_word_count,
                "ATSReadabilityAnalysis.estimated_word_count",
            ),
        )
        object.__setattr__(
            self,
            "long_sentence_count",
            _non_negative_int(
                self.long_sentence_count,
                "ATSReadabilityAnalysis.long_sentence_count",
            ),
        )
        object.__setattr__(
            self,
            "average_sentence_length",
            _non_negative_float(
                self.average_sentence_length,
                "ATSReadabilityAnalysis.average_sentence_length",
            ),
        )
        object.__setattr__(
            self,
            "readability_score",
            _bounded_score(
                self.readability_score,
                "ATSReadabilityAnalysis.readability_score",
            ),
        )

    @classmethod
    def from_value(
        cls,
        value: Any,
    ) -> "ATSReadabilityAnalysis":
        if isinstance(value, cls):
            return value

        if not isinstance(value, Mapping):
            raise TypeError(
                "ATSReadabilityAnalysis must be an ATSReadabilityAnalysis "
                "or mapping."
            )

        return cls(
            estimated_word_count=_dict_value(
                value,
                "estimated_word_count",
                "word_count",
                default=0,
            ),
            long_sentence_count=_dict_value(
                value,
                "long_sentence_count",
                default=0,
            ),
            average_sentence_length=_dict_value(
                value,
                "average_sentence_length",
                "avg_sentence_length",
                default=0.0,
            ),
            readability_score=_dict_value(
                value,
                "readability_score",
                "score",
                default=0.0,
            ),
        )


# ============================================================================
# TERMINOLOGY ANALYSIS
# ============================================================================


@dataclass(frozen=True)
class ATSTerminologyAnalysis:
    """Typed terminology alignment analysis."""

    aligned_terms: tuple[str, ...] = ()
    missing_terms: tuple[str, ...] = ()
    terminology_score: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "aligned_terms",
            _tuple_strings(
                self.aligned_terms,
                "ATSTerminologyAnalysis.aligned_terms",
            ),
        )
        object.__setattr__(
            self,
            "missing_terms",
            _tuple_strings(
                self.missing_terms,
                "ATSTerminologyAnalysis.missing_terms",
            ),
        )
        object.__setattr__(
            self,
            "terminology_score",
            _bounded_score(
                self.terminology_score,
                "ATSTerminologyAnalysis.terminology_score",
            ),
        )

    @classmethod
    def from_value(
        cls,
        value: Any,
    ) -> "ATSTerminologyAnalysis":
        if isinstance(value, cls):
            return value

        if not isinstance(value, Mapping):
            raise TypeError(
                "ATSTerminologyAnalysis must be an ATSTerminologyAnalysis "
                "or mapping."
            )

        return cls(
            aligned_terms=_dict_value(
                value,
                "aligned_terms",
                "aligned",
                default=(),
            ),
            missing_terms=_dict_value(
                value,
                "missing_terms",
                "missing",
                default=(),
            ),
            terminology_score=_dict_value(
                value,
                "terminology_score",
                "score",
                default=0.0,
            ),
        )


# ============================================================================
# QUANTIFICATION ANALYSIS
# ============================================================================


@dataclass(frozen=True)
class ATSQuantificationAnalysis:
    """Typed quantitative-evidence analysis."""

    quantified_achievement_count: int = 0
    quantified_bullet_count: int = 0
    quantification_score: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "quantified_achievement_count",
            _non_negative_int(
                self.quantified_achievement_count,
                "ATSQuantificationAnalysis.quantified_achievement_count",
            ),
        )
        object.__setattr__(
            self,
            "quantified_bullet_count",
            _non_negative_int(
                self.quantified_bullet_count,
                "ATSQuantificationAnalysis.quantified_bullet_count",
            ),
        )
        object.__setattr__(
            self,
            "quantification_score",
            _bounded_score(
                self.quantification_score,
                "ATSQuantificationAnalysis.quantification_score",
            ),
        )

    @classmethod
    def from_value(
        cls,
        value: Any,
    ) -> "ATSQuantificationAnalysis":
        if isinstance(value, cls):
            return value

        if not isinstance(value, Mapping):
            raise TypeError(
                "ATSQuantificationAnalysis must be an "
                "ATSQuantificationAnalysis or mapping."
            )

        return cls(
            quantified_achievement_count=_dict_value(
                value,
                "quantified_achievement_count",
                "achievement_count",
                default=0,
            ),
            quantified_bullet_count=_dict_value(
                value,
                "quantified_bullet_count",
                "bullet_count",
                default=0,
            ),
            quantification_score=_dict_value(
                value,
                "quantification_score",
                "score",
                default=0.0,
            ),
        )


# ============================================================================
# PARSEABILITY ANALYSIS
# ============================================================================


@dataclass(frozen=True)
class ATSParseabilityAnalysis:
    """Typed ATS extraction / parseability analysis."""

    parseable: bool = True
    extraction_warning_count: int = 0
    warnings: tuple[str, ...] = ()
    parseability_score: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "warnings",
            _tuple_strings(
                self.warnings,
                "ATSParseabilityAnalysis.warnings",
            ),
        )

        warning_count = _non_negative_int(
            self.extraction_warning_count,
            "ATSParseabilityAnalysis.extraction_warning_count",
        )

        # The warning collection is authoritative. If callers supplied
        # only warnings, derive the count. If both are supplied, require
        # consistency rather than silently producing two truths.
        if warning_count != len(self.warnings):
            if warning_count == 0 and self.warnings:
                warning_count = len(self.warnings)
            else:
                raise ValueError(
                    "ATSParseabilityAnalysis.extraction_warning_count "
                    "must equal len(warnings)."
                )

        object.__setattr__(
            self,
            "extraction_warning_count",
            warning_count,
        )
        object.__setattr__(
            self,
            "parseability_score",
            _bounded_score(
                self.parseability_score,
                "ATSParseabilityAnalysis.parseability_score",
            ),
        )

    @classmethod
    def from_value(
        cls,
        value: Any,
    ) -> "ATSParseabilityAnalysis":
        if isinstance(value, cls):
            return value

        if not isinstance(value, Mapping):
            raise TypeError(
                "ATSParseabilityAnalysis must be an "
                "ATSParseabilityAnalysis or mapping."
            )

        warnings = _dict_value(
            value,
            "warnings",
            "extraction_warnings",
            default=(),
        )

        return cls(
            parseable=bool(
                _dict_value(
                    value,
                    "parseable",
                    default=True,
                )
            ),
            extraction_warning_count=_dict_value(
                value,
                "extraction_warning_count",
                "warning_count",
                default=0,
            ),
            warnings=warnings,
            parseability_score=_dict_value(
                value,
                "parseability_score",
                "score",
                default=0.0,
            ),
        )


# ============================================================================
# FINAL RESULT
# ============================================================================


@dataclass
class ATSResumeAnalysisResult:
    """
    Complete Phase 5 result.

    This is deliberately an aggregate object: the result owns the exact
    request, the exact Phase 4 profile, and typed ATS observations.

    Canonical fields
    ----------------
    request
    knowledge_match_profile
    ats_score
    score_breakdown
    keyword_analysis
    section_analysis
    formatting_analysis
    readability_analysis
    terminology_analysis
    quantification_analysis
    parseability_analysis
    confidence

    Compatibility aliases
    ---------------------
    score
    breakdown

    The compatibility aliases exist so older orchestration code can migrate
    without changing the object model.
    """

    request: Any
    knowledge_match_profile: Optional["KnowledgeMatchProfile"]

    ats_score: ATSScore
    score_breakdown: ATSScoreBreakdown

    keyword_analysis: ATSKeywordAnalysis
    section_analysis: ATSSectionAnalysis
    formatting_analysis: ATSFormattingAnalysis
    readability_analysis: ATSReadabilityAnalysis
    terminology_analysis: ATSTerminologyAnalysis
    quantification_analysis: ATSQuantificationAnalysis
    parseability_analysis: ATSParseabilityAnalysis

    confidence: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    def __post_init__(self) -> None:
        # These imports remain local to avoid a circular dependency between
        # Phase 4 and Phase 5 model modules.
        from app.intelligence.utilities.knowledge.ats.ats_analysis_request import (
            ATSResumeAnalysisRequest,
        )
        from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
            KnowledgeMatchProfile,
        )

        if not isinstance(
            self.request,
            ATSResumeAnalysisRequest,
        ):
            raise TypeError(
                "ATSResumeAnalysisResult.request must be an "
                "ATSResumeAnalysisRequest."
            )

        if self.knowledge_match_profile is None:
            self.knowledge_match_profile = (
                self.request.knowledge_match_profile
            )

        if not isinstance(
            self.knowledge_match_profile,
            KnowledgeMatchProfile,
        ):
            raise TypeError(
                "ATSResumeAnalysisResult.knowledge_match_profile must be "
                "a KnowledgeMatchProfile."
            )

        # Preserve Phase 4 identity exactly.
        if (
            self.knowledge_match_profile
            is not self.request.knowledge_match_profile
        ):
            raise ValueError(
                "ATSResumeAnalysisResult.knowledge_match_profile must be "
                "the exact KnowledgeMatchProfile carried by the request."
            )

        self.ats_score = ATSScore.from_value(
            self.ats_score,
            confidence=self.confidence,
        )

        self.score_breakdown = ATSScoreBreakdown.from_value(
            self.score_breakdown,
        )

        self.keyword_analysis = ATSKeywordAnalysis.from_value(
            self.keyword_analysis,
        )

        self.section_analysis = ATSSectionAnalysis.from_value(
            self.section_analysis,
        )

        self.formatting_analysis = ATSFormattingAnalysis.from_value(
            self.formatting_analysis,
        )

        self.readability_analysis = ATSReadabilityAnalysis.from_value(
            self.readability_analysis,
        )

        self.terminology_analysis = ATSTerminologyAnalysis.from_value(
            self.terminology_analysis,
        )

        self.quantification_analysis = ATSQuantificationAnalysis.from_value(
            self.quantification_analysis,
        )

        self.parseability_analysis = ATSParseabilityAnalysis.from_value(
            self.parseability_analysis,
        )

        self.confidence = _bounded_score(
            self.confidence,
            "ATSResumeAnalysisResult.confidence",
        )

        # The score object owns confidence as well. Keep both representations
        # synchronized.
        if self.ats_score.confidence != self.confidence:
            self.ats_score = ATSScore(
                score=self.ats_score.score,
                confidence=self.confidence,
            )

    # ------------------------------------------------------------------
    # LEGACY COMPATIBILITY
    # ------------------------------------------------------------------

    @property
    def score(self) -> ATSScore:
        """
        Compatibility alias.

        Older code may use result.score; the canonical object is
        result.ats_score.
        """
        return self.ats_score

    @property
    def breakdown(self) -> ATSScoreBreakdown:
        """
        Compatibility alias.

        Older code may use result.breakdown; the canonical object is
        result.score_breakdown.
        """
        return self.score_breakdown

    # ------------------------------------------------------------------
    # OBJECT CONTRACT
    # ------------------------------------------------------------------

    @property
    def resume_profile(self) -> Any:
        """Expose the exact resume profile carried by the request."""
        return self.request.resume_profile

    @property
    def jd_requirement_profile(self) -> Any:
        """Expose the exact JD requirement profile carried by the request."""
        return self.request.jd_requirement_profile

    @property
    def is_parseable(self) -> bool:
        """Return the parseability observation."""
        return self.parseability_analysis.parseable

    @property
    def is_high_confidence(self) -> bool:
        """Return whether the final result confidence is at least 0.75."""
        return self.confidence >= 0.75

    def validate(self) -> None:
        """
        Re-run the complete aggregate-object contract validation.
        """
        self.__post_init__()

        if (
            self.ats_score.score
            != self.score_breakdown.weighted_score
        ):
            raise ValueError(
                "ATSResumeAnalysisResult.ats_score.score must equal "
                "ATSResumeAnalysisResult.score_breakdown.weighted_score."
            )

    def __repr__(self) -> str:
        return (
            "ATSResumeAnalysisResult("
            f"score={self.ats_score.score:.4f}, "
            f"confidence={self.confidence:.4f}, "
            f"keywords={len(self.keyword_analysis.required_keywords)}, "
            f"missing_keywords={len(self.keyword_analysis.missing_keywords)}, "
            f"parseable={self.parseability_analysis.parseable}"
            ")"
        )


# ============================================================================
# EXPORTS
# ============================================================================


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
