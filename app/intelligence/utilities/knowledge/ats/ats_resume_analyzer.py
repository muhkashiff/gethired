"""
ATS Resume Analyzer
===================

Phase 5 - ATS / Resume Analysis.

Object In
---------

    ATSResumeAnalysisRequest

Object Out
----------

    ATSResumeAnalysisResult

The analyzer consumes the authoritative Phase 4 profile and the
document-aware resume/JD profiles.

It does not introduce a second matching system.
"""

from __future__ import annotations

import re
from typing import Any


from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSKeywordAnalysis,
    ATSScore,
    ATSScoreBreakdown,
    ATSSectionAnalysis,
    ATSFormattingAnalysis,
    ATSReadabilityAnalysis,
    ATSTerminologyAnalysis,
    ATSQuantificationAnalysis,
    ATSParseabilityAnalysis,
    ATSResumeAnalysisResult,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_policy import (
    ATSAnalysisPolicy,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_request import (
    ATSResumeAnalysisRequest,
)


class ATSResumeAnalyzer:
    """
    Stateless Phase 5 ATS analysis service.

    Policy belongs to the analyzer, not the request.
    """

    def __init__(
        self,
        *,
        policy: ATSAnalysisPolicy | None = None,
    ) -> None:

        self.policy = (
            policy
            if policy is not None
            else ATSAnalysisPolicy()
        )

        if not isinstance(
            self.policy,
            ATSAnalysisPolicy,
        ):
            raise TypeError(
                "ATSResumeAnalyzer.policy must be "
                "an ATSAnalysisPolicy."
            )

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def process(
        self,
        request: ATSResumeAnalysisRequest,
    ) -> ATSResumeAnalysisResult:

        self._validate_request(
            request
        )

        profile = (
            request.knowledge_match_profile
        )

        resume_text = self._resume_text(
            request
        )

        keyword_analysis = (
            self._analyze_keywords(
                request=request,
            )
        )

        section_analysis = (
            self._analyze_sections(
                resume_text=resume_text,
            )
        )

        formatting_analysis = (
            self._analyze_formatting(
                resume_text=resume_text,
            )
        )

        readability_analysis = (
            self._analyze_readability(
                resume_text=resume_text,
            )
        )

        terminology_analysis = (
            self._analyze_terminology(
                request=request,
                resume_text=resume_text,
            )
        )

        quantification_analysis = (
            self._analyze_quantification(
                request=request,
                resume_text=resume_text,
            )
        )

        parseability_analysis = (
            self._analyze_parseability(
                resume_text=resume_text,
                request=request,
            )
        )

        score_breakdown = (
            self._build_score_breakdown(
                keyword_analysis=keyword_analysis,
                section_analysis=section_analysis,
                formatting_analysis=formatting_analysis,
                readability_analysis=readability_analysis,
                terminology_analysis=terminology_analysis,
                quantification_analysis=quantification_analysis,
                parseability_analysis=parseability_analysis,
            )
        )

        ats_score = self._build_ats_score(
            score_breakdown=score_breakdown,
            profile=profile,
        )

        result = ATSResumeAnalysisResult(
            request=request,
            ats_score=ats_score,
            score_breakdown=score_breakdown,
            keyword_analysis=keyword_analysis,
            section_analysis=section_analysis,
            formatting_analysis=formatting_analysis,
            readability_analysis=readability_analysis,
            terminology_analysis=terminology_analysis,
            quantification_analysis=quantification_analysis,
            parseability_analysis=parseability_analysis,
            confidence=ats_score.confidence,
        )

        self._validate_result(
            result=result,
            request=request,
        )

        return result

    # =========================================================================
    # REQUEST VALIDATION
    # =========================================================================

    def _validate_request(
        self,
        request: ATSResumeAnalysisRequest,
    ) -> None:

        if not isinstance(
            request,
            ATSResumeAnalysisRequest,
        ):
            raise TypeError(
                "ATSResumeAnalyzer.process() expects "
                "an ATSResumeAnalysisRequest."
            )

        if not isinstance(
            self.policy,
            ATSAnalysisPolicy,
        ):
            raise TypeError(
                "ATSResumeAnalyzer.policy must be "
                "an ATSAnalysisPolicy."
            )

        if not request.resume_profile.is_resume:
            raise ValueError(
                "ATSResumeAnalysisRequest.resume_profile "
                "must represent a resume."
            )

        resume_text = self._resume_text(
            request
        )

        if not resume_text.strip():
            raise ValueError(
                "ATSResumeAnalysisRequest resume source "
                "must not be empty."
            )

    # =========================================================================
    # RESUME SOURCE
    # =========================================================================

    @staticmethod
    def _resume_text(
        request: ATSResumeAnalysisRequest,
    ) -> str:
        """
        Recover source resume text from the existing document pipeline.

        The Phase 5 request does not carry a duplicate resume_text field.

        Preferred source:

            resume_profile.source_result
                -> knowledge_document
                -> raw_text

        A small number of compatible source layouts are supported because
        older pipeline result wrappers may expose the document differently.
        """

        source_result = (
            request
            .resume_profile
            .source_result
        )

        if source_result is None:
            return ""

        knowledge_document = getattr(
            source_result,
            "knowledge_document",
            None,
        )

        if knowledge_document is not None:

            raw_text = getattr(
                knowledge_document,
                "raw_text",
                "",
            )

            if isinstance(
                raw_text,
                str,
            ):
                return raw_text

        raw_text = getattr(
            source_result,
            "raw_text",
            "",
        )

        if isinstance(
            raw_text,
            str,
        ):
            return raw_text

        result = getattr(
            source_result,
            "result",
            None,
        )

        if result is not None:

            knowledge_document = getattr(
                result,
                "knowledge_document",
                None,
            )

            if knowledge_document is not None:

                raw_text = getattr(
                    knowledge_document,
                    "raw_text",
                    "",
                )

                if isinstance(
                    raw_text,
                    str,
                ):
                    return raw_text

            raw_text = getattr(
                result,
                "raw_text",
                "",
            )

            if isinstance(
                raw_text,
                str,
            ):
                return raw_text

        return ""

    # =========================================================================
    # KEYWORDS
    # =========================================================================

    def _analyze_keywords(
        self,
        *,
        request: ATSResumeAnalysisRequest,
    ) -> ATSKeywordAnalysis:

        requirements = (
            request
            .knowledge_match_profile
            .requirements
        )

        required = []

        matched = []

        missing = []

        for requirement in requirements:

            subject = (
                requirement
                .requirement_subject
            )

            if not subject:
                continue

            subject = str(
                subject
            ).strip()

            if not subject:
                continue

            required.append(
                subject
            )

            if requirement.match_status.value == "matched":
                matched.append(
                    subject
                )
            else:
                missing.append(
                    subject
                )

        required = self._unique_strings(
            required
        )

        matched = self._unique_strings(
            matched
        )

        missing = [
            item
            for item in self._unique_strings(
                missing
            )
            if item not in matched
        ]

        coverage = (
            len(matched)
            / len(required)
            if required
            else 0.0
        )

        confidence = (
            request
            .knowledge_match_profile
            .matching_confidence
        )

        return ATSKeywordAnalysis(
            required_keywords=tuple(
                required
            ),
            matched_keywords=tuple(
                matched
            ),
            missing_keywords=tuple(
                missing
            ),
            additional_keywords=(),
            keyword_coverage_score=coverage,
            confidence=confidence,
        )

    # =========================================================================
    # SECTIONS
    # =========================================================================

    def _analyze_sections(
        self,
        *,
        resume_text: str,
    ) -> ATSSectionAnalysis:

        text = resume_text.casefold()

        detected = []

        missing = []

        for section in (
            self.policy.required_sections
        ):

            if section.casefold() in text:
                detected.append(
                    section
                )
            else:
                missing.append(
                    section
                )

        score = (
            len(detected)
            / len(
                self.policy.required_sections
            )
            if self.policy.required_sections
            else 1.0
        )

        return ATSSectionAnalysis(
            detected_sections=tuple(
                detected
            ),
            missing_sections=tuple(
                missing
            ),
            section_order_valid=True,
            section_completeness_score=score,
            confidence=1.0,
        )

    # =========================================================================
    # FORMATTING
    # =========================================================================

    def _analyze_formatting(
        self,
        *,
        resume_text: str,
    ) -> ATSFormattingAnalysis:

        lines = resume_text.splitlines()

        long_lines = sum(
            1
            for line in lines
            if len(line)
            > self.policy.max_line_length
        )

        has_tables = (
            "|" in resume_text
        )

        has_columns = any(
            "\t" in line
            for line in lines
        )

        has_graphics = bool(
            re.search(
                r"[^\x00-\x7F]",
                resume_text,
            )
        )

        score = 1.0

        if long_lines:
            score -= min(
                0.5,
                long_lines
                / max(
                    len(lines),
                    1,
                ),
            )

        if has_tables:
            score -= 0.10

        if has_columns:
            score -= 0.10

        if has_graphics:
            score -= 0.05

        score = max(
            0.0,
            min(
                1.0,
                score,
            ),
        )

        return ATSFormattingAnalysis(
            formatting_score=score,
            has_complex_layout=False,
            has_tables=has_tables,
            has_columns=has_columns,
            has_graphics=has_graphics,
            has_unusual_symbols=has_graphics,
            confidence=1.0,
        )

    # =========================================================================
    # READABILITY
    # =========================================================================

    def _analyze_readability(
        self,
        *,
        resume_text: str,
    ) -> ATSReadabilityAnalysis:

        words = resume_text.split()

        word_count = len(
            words
        )

        sentences = [
            item.strip()
            for item in re.split(
                r"[.!?]+",
                resume_text,
            )
            if item.strip()
        ]

        sentence_count = max(
            1,
            len(sentences),
        )

        average_length = (
            word_count
            / sentence_count
        )

        long_sentence_count = sum(
            1
            for sentence in sentences
            if len(
                sentence.split()
            ) > 40
        )

        readability_score = (
            self._readability_score(
                average_length
            )
        )

        return ATSReadabilityAnalysis(
            readability_score=readability_score,
            estimated_word_count=word_count,
            average_sentence_length=average_length,
            long_sentence_count=long_sentence_count,
            confidence=1.0,
        )

    @staticmethod
    def _readability_score(
        average_sentence_length: float,
    ) -> float:

        if average_sentence_length <= 20:
            return 1.0

        if average_sentence_length >= 40:
            return 0.0

        return max(
            0.0,
            min(
                1.0,
                1.0
                - (
                    average_sentence_length
                    - 20.0
                )
                / 20.0,
            ),
        )

    # =========================================================================
    # TERMINOLOGY
    # =========================================================================

    def _analyze_terminology(
        self,
        *,
        request: ATSResumeAnalysisRequest,
        resume_text: str,
    ) -> ATSTerminologyAnalysis:

        resume_lower = resume_text.casefold()

        aligned = []

        missing = []

        for requirement in (
            request
            .knowledge_match_profile
            .requirements
        ):

            subject = (
                requirement
                .requirement_subject
            )

            if not subject:
                continue

            subject = str(
                subject
            ).strip()

            if not subject:
                continue

            if subject.casefold() in resume_lower:
                aligned.append(
                    subject
                )
            else:
                missing.append(
                    subject
                )

        aligned = self._unique_strings(
            aligned
        )

        missing = [
            item
            for item in self._unique_strings(
                missing
            )
            if item not in aligned
        ]

        total = (
            len(aligned)
            + len(missing)
        )

        score = (
            len(aligned)
            / total
            if total
            else 1.0
        )

        return ATSTerminologyAnalysis(
            aligned_terms=tuple(
                aligned
            ),
            missing_terms=tuple(
                missing
            ),
            terminology_score=score,
            confidence=1.0,
        )

    # =========================================================================
    # QUANTIFICATION
    # =========================================================================

    def _analyze_quantification(
        self,
        *,
        request: ATSResumeAnalysisRequest,
        resume_text: str,
    ) -> ATSQuantificationAnalysis:

        document = self._knowledge_document(
            request
        )

        facts = []

        if document is not None:
            facts = list(
                getattr(
                    document,
                    "facts",
                    [],
                )
                or []
            )

        quantified_achievements = sum(
            1
            for fact in facts
            if getattr(
                fact,
                "achievement",
                False,
            )
            and getattr(
                fact,
                "quantified",
                False,
            )
        )

        quantified_bullets = sum(
            1
            for fact in facts
            if getattr(
                fact,
                "quantified",
                False,
            )
        )

        if not facts:

            quantified_tokens = [
                token
                for token in resume_text.split()
                if any(
                    character.isdigit()
                    for character in token
                )
            ]

            quantified_bullets = len(
                quantified_tokens
            )

        target = (
            self.policy.minimum_quantifications
        )

        score = (
            1.0
            if target == 0
            else min(
                1.0,
                quantified_bullets
                / target,
            )
        )

        return ATSQuantificationAnalysis(
            quantified_achievement_count=(
                quantified_achievements
            ),
            quantified_bullet_count=(
                quantified_bullets
            ),
            quantification_score=score,
            confidence=1.0,
        )

    # =========================================================================
    # PARSEABILITY
    # =========================================================================

    def _analyze_parseability(
        self,
        *,
        resume_text: str,
        request: ATSResumeAnalysisRequest,
    ) -> ATSParseabilityAnalysis:

        warnings = []

        if not resume_text.strip():
            warnings.append(
                "Resume source contains no extractable text."
            )

        if request.resume_profile.source_result is None:
            warnings.append(
                "Resume source result is unavailable."
            )

        parseable = bool(
            resume_text.strip()
        )

        score = (
            1.0
            if parseable
            else 0.0
        )

        return ATSParseabilityAnalysis(
            parseable=parseable,
            parseability_score=score,
            extraction_warning_count=len(
                warnings
            ),
            warnings=tuple(
                warnings
            ),
            confidence=1.0,
        )

    # =========================================================================
    # SCORE BREAKDOWN
    # =========================================================================

    def _build_score_breakdown(
        self,
        *,
        keyword_analysis: ATSKeywordAnalysis,
        section_analysis: ATSSectionAnalysis,
        formatting_analysis: ATSFormattingAnalysis,
        readability_analysis: ATSReadabilityAnalysis,
        terminology_analysis: ATSTerminologyAnalysis,
        quantification_analysis: ATSQuantificationAnalysis,
        parseability_analysis: ATSParseabilityAnalysis,
    ) -> ATSScoreBreakdown:

        return ATSScoreBreakdown(
            keyword_score=(
                keyword_analysis
                .keyword_coverage_score
            ),
            section_score=(
                section_analysis
                .section_completeness_score
            ),
            formatting_score=(
                formatting_analysis
                .formatting_score
            ),
            readability_score=(
                readability_analysis
                .readability_score
            ),
            terminology_score=(
                terminology_analysis
                .terminology_score
            ),
            quantification_score=(
                quantification_analysis
                .quantification_score
            ),
            parseability_score=(
                parseability_analysis
                .parseability_score
            ),
            structure_score=(
                section_analysis
                .section_completeness_score
            ),
            weights=dict(
                self.policy.score_weights
            ),
        )

    # =========================================================================
    # FINAL SCORE
    # =========================================================================

    def _build_ats_score(
        self,
        *,
        score_breakdown: ATSScoreBreakdown,
        profile: Any,
    ) -> ATSScore:

        score = (
            score_breakdown
            .weighted_score
        )

        confidence_components = (
            float(
                profile.matching_confidence
            ),
            float(
                profile.enrichment_confidence
            ),
            float(
                profile.gap_analysis_confidence
            ),
        )

        confidence = (
            sum(
                confidence_components
            )
            / len(
                confidence_components
            )
            if confidence_components
            else 0.0
        )

        return ATSScore(
            score=score,
            confidence=confidence,
        )

    # =========================================================================
    # RESULT VALIDATION
    # =========================================================================

    @staticmethod
    def _validate_result(
        *,
        result: ATSResumeAnalysisResult,
        request: ATSResumeAnalysisRequest,
    ) -> None:

        if not isinstance(
            result,
            ATSResumeAnalysisResult,
        ):
            raise TypeError(
                "ATS analyzer must return an "
                "ATSResumeAnalysisResult."
            )

        if result.request is not request:
            raise ValueError(
                "ATS analysis result must preserve "
                "the exact request instance."
            )

        if (
            result.knowledge_match_profile
            is not request.knowledge_match_profile
        ):
            raise ValueError(
                "ATS analysis result must preserve "
                "the exact Phase 4 KnowledgeMatchProfile."
            )

        score = float(
            result.ats_score.score
        )

        if not 0.0 <= score <= 1.0:
            raise ValueError(
                "ATS score must be between 0 and 1."
            )

    # =========================================================================
    # SOURCE HELPERS
    # =========================================================================

    @staticmethod
    def _knowledge_document(
        request: ATSResumeAnalysisRequest,
    ) -> Any:

        source_result = (
            request
            .resume_profile
            .source_result
        )

        if source_result is None:
            return None

        document = getattr(
            source_result,
            "knowledge_document",
            None,
        )

        if document is not None:
            return document

        result = getattr(
            source_result,
            "result",
            None,
        )

        if result is not None:

            document = getattr(
                result,
                "knowledge_document",
                None,
            )

            if document is not None:
                return document

        return None

    @staticmethod
    def _unique_strings(
        values: list[str],
    ) -> list[str]:

        result = []

        seen = set()

        for value in values:

            normalized = str(
                value
            ).strip()

            key = normalized.casefold()

            if not normalized:
                continue

            if key in seen:
                continue

            seen.add(
                key
            )

            result.append(
                normalized
            )

        return result


__all__ = [
    "ATSResumeAnalyzer",
]