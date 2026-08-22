"""
Phase 6 Recommendation Analyzer
================================

Consumes the exact Phase-5 ATSResumeAnalysisResult and produces the
Phase-6 RecommendationResult.

Object-in:

    ATSResumeAnalysisResult

Object-out:

    RecommendationResult

No dictionary-oriented public API exists.
"""

from __future__ import annotations

from typing import Iterable

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSResumeAnalysisResult,
)

from app.intelligence.utilities.knowledge.recommendations.recommendation_models import (
    Recommendation,
    RecommendationPriority,
    RecommendationResult,
    RecommendationStatus,
    RecommendationType,
)


class RecommendationAnalyzer:
    """Phase-6 application service."""

    def __init__(
        self,
        *,
        minimum_confidence: float = 0.0,
    ) -> None:

        if not 0.0 <= minimum_confidence <= 1.0:
            raise ValueError(
                "minimum_confidence must be between 0.0 and 1.0."
            )

        self.minimum_confidence = (
            minimum_confidence
        )

    # ========================================================================
    # PUBLIC API
    # ========================================================================

    def process(
        self,
        ats_result: ATSResumeAnalysisResult,
    ) -> RecommendationResult:
        """
        Analyze the exact Phase-5 result object.

        No Phase-5 object is copied or reconstructed.
        """

        self._validate_input(
            ats_result
        )

        recommendations: list[
            Recommendation
        ] = []

        self._add_keyword_recommendation(
            ats_result,
            recommendations,
        )

        self._add_section_recommendation(
            ats_result,
            recommendations,
        )

        self._add_formatting_recommendation(
            ats_result,
            recommendations,
        )

        self._add_readability_recommendation(
            ats_result,
            recommendations,
        )

        self._add_terminology_recommendation(
            ats_result,
            recommendations,
        )

        self._add_quantification_recommendation(
            ats_result,
            recommendations,
        )

        self._add_parseability_recommendation(
            ats_result,
            recommendations,
        )

        self._add_knowledge_gap_recommendations(
            ats_result,
            recommendations,
        )

        recommendations = list(
            self._unique_recommendations(
                recommendations
            )
        )

        recommendations = [
            recommendation
            for recommendation in recommendations
            if recommendation.confidence
            >= self.minimum_confidence
        ]

        result = RecommendationResult(
            ats_result=ats_result,
            recommendations=tuple(
                recommendations
            ),
        )

        result.validate()

        return result

    # ========================================================================
    # VALIDATION
    # ========================================================================

    @staticmethod
    def _validate_input(
        ats_result: ATSResumeAnalysisResult,
    ) -> None:

        if not isinstance(
            ats_result,
            ATSResumeAnalysisResult,
        ):
            raise TypeError(
                "RecommendationAnalyzer.process expects an "
                "ATSResumeAnalysisResult object."
            )

        ats_result.validate()

    # ========================================================================
    # CONFIDENCE
    # ========================================================================

    def _confidence(
        self,
        ats_result: ATSResumeAnalysisResult,
    ) -> float:
        return max(
            0.0,
            min(
                1.0,
                float(
                    ats_result.confidence
                ),
            ),
        )

    # ========================================================================
    # KEYWORDS
    # ========================================================================

    def _add_keyword_recommendation(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendations: list[Recommendation],
    ) -> None:

        analysis = (
            ats_result.keyword_analysis
        )

        missing = tuple(
            analysis.missing_keywords
        )

        if not missing:
            return

        score = (
            analysis.keyword_coverage_score
        )

        priority = (
            RecommendationPriority.HIGH
            if score < 0.50
            else RecommendationPriority.MEDIUM
        )

        recommendations.append(
            Recommendation(
                recommendation_id=(
                    "REC-KEYWORDS-001"
                ),
                recommendation_type=(
                    RecommendationType.KEYWORD
                ),
                priority=priority,
                title="Improve keyword coverage",
                description=(
                    "Add relevant missing job-description keywords "
                    "to appropriate resume content where they are "
                    "truthfully supported by your experience."
                ),
                rationale=(
                    "Phase 5 identified required keywords that are "
                    "not currently represented in the resume text."
                ),
                status=(
                    RecommendationStatus.ACTIONABLE
                ),
                source_component=(
                    "keyword_analysis"
                ),
                evidence=missing,
                target_items=missing,
                confidence=self._confidence(
                    ats_result
                ),
            )
        )

    # ========================================================================
    # SECTIONS
    # ========================================================================

    def _add_section_recommendation(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendations: list[Recommendation],
    ) -> None:

        analysis = (
            ats_result.section_analysis
        )

        missing = tuple(
            analysis.missing_sections
        )

        if not missing:
            return

        priority = (
            RecommendationPriority.HIGH
            if len(missing) >= 2
            else RecommendationPriority.MEDIUM
        )

        recommendations.append(
            Recommendation(
                recommendation_id=(
                    "REC-SECTIONS-001"
                ),
                recommendation_type=(
                    RecommendationType.SECTION
                ),
                priority=priority,
                title=(
                    "Complete missing resume sections"
                ),
                description=(
                    "Add the missing standard resume sections "
                    "that are relevant to the candidate's actual "
                    "background."
                ),
                rationale=(
                    "Phase 5 detected incomplete standard resume "
                    "section coverage."
                ),
                source_component=(
                    "section_analysis"
                ),
                evidence=missing,
                target_items=missing,
                confidence=self._confidence(
                    ats_result
                ),
            )
        )

    # ========================================================================
    # FORMATTING
    # ========================================================================

    def _add_formatting_recommendation(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendations: list[Recommendation],
    ) -> None:

        analysis = (
            ats_result.formatting_analysis
        )

        problems: list[str] = []

        if analysis.has_complex_layout:
            problems.append(
                "complex layout"
            )

        if analysis.has_tables:
            problems.append(
                "tables"
            )

        if analysis.has_columns:
            problems.append(
                "columns"
            )

        if analysis.has_graphics:
            problems.append(
                "graphics"
            )

        if not problems:
            return

        recommendations.append(
            Recommendation(
                recommendation_id=(
                    "REC-FORMATTING-001"
                ),
                recommendation_type=(
                    RecommendationType.FORMATTING
                ),
                priority=(
                    RecommendationPriority.HIGH
                ),
                title=(
                    "Simplify ATS-sensitive formatting"
                ),
                description=(
                    "Prefer a simple single-column resume layout "
                    "and remove formatting elements that can interfere "
                    "with automated resume parsing."
                ),
                rationale=(
                    "Phase 5 detected formatting characteristics "
                    "that may reduce ATS reliability."
                ),
                source_component=(
                    "formatting_analysis"
                ),
                evidence=tuple(
                    problems
                ),
                target_items=tuple(
                    problems
                ),
                confidence=self._confidence(
                    ats_result
                ),
            )
        )

    # ========================================================================
    # READABILITY
    # ========================================================================

    def _add_readability_recommendation(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendations: list[Recommendation],
    ) -> None:

        analysis = (
            ats_result.readability_analysis
        )

        if (
            analysis.long_sentence_count
            <= 0
        ):
            return

        recommendations.append(
            Recommendation(
                recommendation_id=(
                    "REC-READABILITY-001"
                ),
                recommendation_type=(
                    RecommendationType.READABILITY
                ),
                priority=(
                    RecommendationPriority.MEDIUM
                ),
                title=(
                    "Improve sentence readability"
                ),
                description=(
                    "Break overly long sentences into concise "
                    "achievement-oriented statements."
                ),
                rationale=(
                    "Phase 5 detected long sentences that may reduce "
                    "resume readability."
                ),
                source_component=(
                    "readability_analysis"
                ),
                evidence=(
                    f"long_sentence_count="
                    f"{analysis.long_sentence_count}",
                ),
                target_items=(
                    "long sentences",
                ),
                confidence=self._confidence(
                    ats_result
                ),
            )
        )

    # ========================================================================
    # TERMINOLOGY
    # ========================================================================

    def _add_terminology_recommendation(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendations: list[Recommendation],
    ) -> None:

        analysis = (
            ats_result.terminology_analysis
        )

        missing = tuple(
            analysis.missing_terms
        )

        if not missing:
            return

        recommendations.append(
            Recommendation(
                recommendation_id=(
                    "REC-TERMINOLOGY-001"
                ),
                recommendation_type=(
                    RecommendationType.TERMINOLOGY
                ),
                priority=(
                    RecommendationPriority.MEDIUM
                ),
                title=(
                    "Improve terminology alignment"
                ),
                description=(
                    "Use relevant job-description terminology where "
                    "it accurately describes existing experience."
                ),
                rationale=(
                    "Phase 5 identified terminology that is present "
                    "in the target requirements but absent from the "
                    "resume."
                ),
                source_component=(
                    "terminology_analysis"
                ),
                evidence=missing,
                target_items=missing,
                confidence=self._confidence(
                    ats_result
                ),
            )
        )

    # ========================================================================
    # QUANTIFICATION
    # ========================================================================

    def _add_quantification_recommendation(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendations: list[Recommendation],
    ) -> None:

        analysis = (
            ats_result.quantification_analysis
        )

        if (
            analysis.quantification_score
            >= 0.70
        ):
            return

        recommendations.append(
            Recommendation(
                recommendation_id=(
                    "REC-QUANTIFICATION-001"
                ),
                recommendation_type=(
                    RecommendationType.QUANTIFICATION
                ),
                priority=(
                    RecommendationPriority.MEDIUM
                ),
                title=(
                    "Strengthen measurable impact"
                ),
                description=(
                    "Where your experience supports it, add real "
                    "metrics, scale, scope, time, volume, cost, "
                    "performance, or outcome evidence to achievement "
                    "statements."
                ),
                rationale=(
                    "Phase 5 detected limited quantitative evidence."
                ),
                source_component=(
                    "quantification_analysis"
                ),
                evidence=(
                    f"quantified_achievement_count="
                    f"{analysis.quantified_achievement_count}",
                    f"quantified_bullet_count="
                    f"{analysis.quantified_bullet_count}",
                ),
                target_items=(
                    "achievement statements",
                ),
                confidence=self._confidence(
                    ats_result
                ),
                metadata={
                    "truth_safe": True,
                    "never_invent_metrics": True,
                },
            )
        )

    # ========================================================================
    # PARSEABILITY
    # ========================================================================

    def _add_parseability_recommendation(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendations: list[Recommendation],
    ) -> None:

        analysis = (
            ats_result.parseability_analysis
        )

        if analysis.parseable:
            return

        recommendations.append(
            Recommendation(
                recommendation_id=(
                    "REC-PARSEABILITY-001"
                ),
                recommendation_type=(
                    RecommendationType.PARSEABILITY
                ),
                priority=(
                    RecommendationPriority.CRITICAL
                ),
                title=(
                    "Fix resume parseability issues"
                ),
                description=(
                    "Resolve the detected extraction or source "
                    "problems before making other resume changes."
                ),
                rationale=(
                    "Phase 5 determined that the resume source "
                    "is not reliably parseable."
                ),
                source_component=(
                    "parseability_analysis"
                ),
                evidence=tuple(
                    analysis.warnings
                ),
                target_items=(
                    "resume source",
                ),
                confidence=self._confidence(
                    ats_result
                ),
            )
        )

    # ========================================================================
    # KNOWLEDGE GAPS
    # ========================================================================

    def _add_knowledge_gap_recommendations(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendations: list[Recommendation],
    ) -> None:

        profile = (
            ats_result.knowledge_match_profile
        )

        if profile is None:
            return

        gap_result = getattr(
            profile,
            "gap_analysis_result",
            None,
        )

        if gap_result is None:
            return

        gaps = getattr(
            gap_result,
            "gaps",
            (),
        )

        if not gaps:
            return

        for index, gap in enumerate(
            gaps,
            start=1,
        ):
            subject = (
                getattr(
                    gap,
                    "requirement_subject",
                    None,
                )
                or getattr(
                    gap,
                    "subject",
                    None,
                )
                or getattr(
                    gap,
                    "requirement",
                    None,
                )
                or f"knowledge gap {index}"
            )

            priority_value = str(
                getattr(
                    gap,
                    "priority",
                    "medium",
                )
            ).lower()

            priority = (
                RecommendationPriority.HIGH
                if priority_value
                == "high"
                else RecommendationPriority.MEDIUM
            )

            recommendations.append(
                Recommendation(
                    recommendation_id=(
                        f"REC-KNOWLEDGE-GAP-{index:03d}"
                    ),
                    recommendation_type=(
                        RecommendationType.KNOWLEDGE_GAP
                    ),
                    priority=priority,
                    title=(
                        f"Address knowledge gap: {subject}"
                    ),
                    description=(
                        "Strengthen the resume only with "
                        "knowledge or experience that is "
                        "actually possessed by the candidate."
                    ),
                    rationale=(
                        "Phase 4 identified a knowledge or "
                        "requirement gap."
                    ),
                    source_component=(
                        "knowledge_match_profile."
                        "gap_analysis_result"
                    ),
                    evidence=(
                        str(subject),
                    ),
                    target_items=(
                        str(subject),
                    ),
                    confidence=self._confidence(
                        ats_result
                    ),
                    metadata={
                        "truth_safe": True,
                    },
                )
            )

    # ========================================================================
    # UNIQUE RESULTS
    # ========================================================================

    @staticmethod
    def _unique_recommendations(
        recommendations: Iterable[Recommendation],
    ) -> tuple[Recommendation, ...]:

        seen: set[str] = set()
        result: list[Recommendation] = []

        for recommendation in recommendations:

            if (
                recommendation.recommendation_id
                in seen
            ):
                continue

            seen.add(
                recommendation.recommendation_id
            )

            result.append(
                recommendation
            )

        return tuple(
            result
        )


__all__ = [
    "RecommendationAnalyzer",
]