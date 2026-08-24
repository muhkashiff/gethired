from __future__ import annotations
from typing import Any, Mapping, Optional

from app.intelligence.utilities.knowledge.ats.ats_analysis_request import (
    ATSResumeAnalysisRequest,
)
from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSFormattingAnalysis,
    ATSKeywordAnalysis,
    ATSParseabilityAnalysis,
    ATSQuantificationAnalysis,
    ATSReadabilityAnalysis,
    ATSResumeAnalysisResult,
    ATSScore,
    ATSScoreBreakdown,
    ATSSectionAnalysis,
    ATSTerminologyAnalysis,
)
from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeMatchProfile,
)
from app.intelligence.utilities.knowledge.education.education_equivalence import (
    EducationEquivalence,
)

class ATSResumeAnalyzer:
    def __init__(self, policy: Any) -> None:
        self.policy = policy

    def process(self, request: ATSResumeAnalysisRequest) -> ATSResumeAnalysisResult:
        if not isinstance(request, ATSResumeAnalysisRequest):
            raise TypeError(
                "ATSResumeAnalyzer.process expects an "
                "ATSResumeAnalysisRequest object."
            )
        request.validate()

        profile = request.knowledge_match_profile
        if not isinstance(profile, KnowledgeMatchProfile):
            raise TypeError(
                "ATSResumeAnalysisRequest.knowledge_match_profile must "
                "be a KnowledgeMatchProfile object."
            )

        keyword_analysis = self._keyword_analysis(request=request, profile=profile)
        section_analysis = self._section_analysis(request=request, profile=profile)
        formatting_analysis = self._formatting_analysis(request=request, profile=profile)
        readability_analysis = self._readability_analysis(request=request, profile=profile)
        terminology_analysis = self._terminology_analysis(request=request, profile=profile)
        quantification_analysis = self._quantification_analysis(request=request, profile=profile)
        parseability_analysis = self._parseability_analysis(request=request, profile=profile)

        breakdown = self._build_breakdown(
            keyword_analysis=keyword_analysis,
            section_analysis=section_analysis,
            formatting_analysis=formatting_analysis,
            readability_analysis=readability_analysis,
            terminology_analysis=terminology_analysis,
            quantification_analysis=quantification_analysis,
            parseability_analysis=parseability_analysis,
        )

        score = self._calculate_score(breakdown=breakdown)
        confidence = self._calculate_confidence(profile=profile, breakdown=breakdown)

        return self._build_result(
            request=request,
            knowledge_match_profile=profile,
            score=score,
            confidence=confidence,
            breakdown=breakdown,
            keyword_analysis=keyword_analysis,
            section_analysis=section_analysis,
            formatting_analysis=formatting_analysis,
            readability_analysis=readability_analysis,
            terminology_analysis=terminology_analysis,
            quantification_analysis=quantification_analysis,
            parseability_analysis=parseability_analysis,
        )

    def build_request(
        self,
        *,
        resume_text: str = "",
        resume_document: Any = None,
        knowledge_match_profile: KnowledgeMatchProfile,
        resume_profile: Any = None,
        jd_requirement_profile: Any = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> ATSResumeAnalysisRequest:
        return ATSResumeAnalysisRequest(
            resume_text=resume_text,
            resume_document=resume_document,
            knowledge_match_profile=knowledge_match_profile,
            resume_profile=resume_profile,
            jd_requirement_profile=jd_requirement_profile,
            metadata={} if metadata is None else dict(metadata),
        )

    # --------------------------------------------------------------
    # Analysis components (unchanged except as noted)
    # --------------------------------------------------------------

    def _keyword_analysis(self, *, request: ATSResumeAnalysisRequest, profile: KnowledgeMatchProfile) -> ATSKeywordAnalysis:
        required = self._profile_keywords(profile)
        text = request.source_text.casefold()

        structured_resume = {}
        metadata = getattr(request, "metadata", {})
        if isinstance(metadata, dict):
            structured_resume = metadata.get("structured_resume") or {}
        education_records = structured_resume.get("education", []) if isinstance(structured_resume, dict) else []

        jd_profile = getattr(request, "jd_requirement_profile", None)
        education_requirements = {}
        if jd_profile is not None:
            for requirement in getattr(jd_profile, "requirements", ()) or ():
                rtype = self._enum_value(getattr(requirement, "requirement_type", ""))
                if rtype == "education":
                    education_requirements[
                        self._normalize_keyword(getattr(requirement, "subject", ""))
                    ] = requirement

        matched_list = []
        missing_list = []

        for keyword in required:
            keyword_text = str(keyword or "").strip()
            if not keyword_text:
                continue

            if keyword_text.casefold() in text:
                matched_list.append(keyword_text)
                continue

            # A higher academic qualification satisfies a lower education
            # keyword. This prevents an M.Sc. holder from being penalized
            # merely because the literal word "Bachelor" is absent from the
            # resume.
            if EducationEquivalence.looks_like_education(keyword_text):
                requirement = education_requirements.get(
                    self._normalize_keyword(keyword_text)
                )
                education_match = EducationEquivalence.match_keyword(
                    keyword_text,
                    education_records,
                    requirement=requirement,
                )
                if education_match.matched:
                    matched_list.append(keyword_text)
                    continue

            missing_list.append(keyword_text)

        matched = tuple(matched_list)
        missing = tuple(missing_list)
        coverage = len(matched) / len(required) if required else 1.0
        return ATSKeywordAnalysis(
            required_keywords=required,
            matched_keywords=matched,
            missing_keywords=missing,
            additional_keywords=(),
            keyword_coverage_score=coverage,
        )

    def _section_analysis(self, *, request: ATSResumeAnalysisRequest, profile: KnowledgeMatchProfile) -> ATSSectionAnalysis:
        text_lower = request.source_text.lower()
        common_sections = ("professional summary", "summary", "experience", "work experience",
                           "education", "skills", "certifications", "projects")
        detected = tuple(s for s in common_sections if s in text_lower)
        required = ("professional summary", "experience", "skills", "education")
        missing = tuple(s for s in required if s not in detected and not (
            s == "professional summary" and "summary" in detected) and not (
            s == "experience" and "work experience" in detected))
        completeness = (len(required) - len(missing)) / len(required) if required else 1.0
        return ATSSectionAnalysis(
            detected_sections=detected,
            missing_sections=missing,
            section_order_valid=True,
            section_completeness_score=completeness,
        )

    def _formatting_analysis(self, *, request: ATSResumeAnalysisRequest, profile: KnowledgeMatchProfile) -> ATSFormattingAnalysis:
        text = request.source_text
        has_tables = "|" in text
        has_columns = "\t" in text
        has_graphics = False
        has_complex_layout = has_tables or has_columns
        score = 1.0
        if has_tables:
            score -= 0.15
        if has_columns:
            score -= 0.10
        if has_graphics:
            score -= 0.15
        return ATSFormattingAnalysis(
            has_complex_layout=has_complex_layout,
            has_tables=has_tables,
            has_columns=has_columns,
            has_graphics=has_graphics,
            formatting_score=max(0.0, score),
        )

    def _readability_analysis(self, *, request: ATSResumeAnalysisRequest, profile: KnowledgeMatchProfile) -> ATSReadabilityAnalysis:
        text = request.source_text.strip()
        words = text.split()
        sentences = [part.strip() for part in text.replace("!", ".").replace("?", ".").split(".") if part.strip()]
        long_sentences = sum(1 for s in sentences if len(s.split()) > 35)
        avg_len = len(words) / len(sentences) if sentences else 0.0
        score = 1.0
        if long_sentences:
            score -= min(0.50, long_sentences / max(len(sentences), 1) * 0.50)
        return ATSReadabilityAnalysis(
            estimated_word_count=len(words),
            long_sentence_count=long_sentences,
            average_sentence_length=avg_len,
            readability_score=max(0.0, score),
        )

    def _terminology_analysis(self, *, request: ATSResumeAnalysisRequest, profile: KnowledgeMatchProfile) -> ATSTerminologyAnalysis:
        required = self._profile_keywords(profile)
        text = request.source_text.lower()
        aligned = tuple(t for t in required if t.lower() in text)
        missing = tuple(t for t in required if t not in aligned)
        score = len(aligned) / len(required) if required else 1.0
        return ATSTerminologyAnalysis(
            aligned_terms=aligned,
            missing_terms=missing,
            terminology_score=score,
        )

    def _quantification_analysis(self, *, request: ATSResumeAnalysisRequest, profile: KnowledgeMatchProfile) -> ATSQuantificationAnalysis:
        text = request.source_text
        tokens = text.split()
        quantified = sum(1 for token in tokens if any(c.isdigit() for c in token))
        bullets = sum(1 for line in text.splitlines() if line.strip().startswith(("-", "•", "*")))
        score = min(1.0, quantified / 5.0) if quantified else 0.0
        return ATSQuantificationAnalysis(
            quantified_achievement_count=quantified,
            quantified_bullet_count=min(quantified, bullets),
            quantification_score=score,
        )

    def _parseability_analysis(self, *, request: ATSResumeAnalysisRequest, profile: KnowledgeMatchProfile) -> ATSParseabilityAnalysis:
        warnings = []
        text = request.source_text
        if "\x00" in text:
            warnings.append("Resume source contains null characters.")
        if not text.strip():
            warnings.append("Resume source is empty.")
        return ATSParseabilityAnalysis(
            parseable=not warnings,
            extraction_warning_count=len(warnings),
            warnings=tuple(warnings),
            parseability_score=1.0 if not warnings else 0.0,
        )

    # --------------------------------------------------------------
    # Scoring (updated to use policy weights)
    # --------------------------------------------------------------

    def _build_breakdown(
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
        weights = self.policy.score_weights

        weighted_score = (
            keyword_analysis.keyword_coverage_score * weights["keyword"] +
            section_analysis.section_completeness_score * weights["section"] +
            formatting_analysis.formatting_score * weights["formatting"] +
            readability_analysis.readability_score * weights["readability"] +
            terminology_analysis.terminology_score * weights["terminology"] +
            quantification_analysis.quantification_score * weights["quantification"] +
            parseability_analysis.parseability_score * weights["parseability"]
        )

        return ATSScoreBreakdown(
            keyword_score=keyword_analysis.keyword_coverage_score,
            section_score=section_analysis.section_completeness_score,
            formatting_score=formatting_analysis.formatting_score,
            readability_score=readability_analysis.readability_score,
            terminology_score=terminology_analysis.terminology_score,
            quantification_score=quantification_analysis.quantification_score,
            parseability_score=parseability_analysis.parseability_score,
            structure_score=section_analysis.section_completeness_score,
            weighted_score=weighted_score,
        )

    def _calculate_score(self, *, breakdown: ATSScoreBreakdown) -> float:
        return breakdown.weighted_score

    def _calculate_confidence(self, *, profile: KnowledgeMatchProfile, breakdown: ATSScoreBreakdown) -> float:
        profile_confidence = getattr(profile, "confidence", 1.0)
        try:
            profile_confidence = float(profile_confidence)
        except (TypeError, ValueError):
            profile_confidence = 1.0
        profile_confidence = max(0.0, min(1.0, profile_confidence))
        return (profile_confidence + breakdown.weighted_score) / 2.0

    # --------------------------------------------------------------
    # Result construction (unchanged)
    # --------------------------------------------------------------

    @staticmethod
    def _build_result(
        *,
        request: ATSResumeAnalysisRequest,
        knowledge_match_profile: KnowledgeMatchProfile,
        score: float,
        confidence: float,
        breakdown: ATSScoreBreakdown,
        keyword_analysis: ATSKeywordAnalysis,
        section_analysis: ATSSectionAnalysis,
        formatting_analysis: ATSFormattingAnalysis,
        readability_analysis: ATSReadabilityAnalysis,
        terminology_analysis: ATSTerminologyAnalysis,
        quantification_analysis: ATSQuantificationAnalysis,
        parseability_analysis: ATSParseabilityAnalysis,
    ) -> ATSResumeAnalysisResult:
        # Ensure consistency
        if abs(score - breakdown.weighted_score) > 1e-12:
            breakdown = ATSScoreBreakdown(
                keyword_score=breakdown.keyword_score,
                section_score=breakdown.section_score,
                formatting_score=breakdown.formatting_score,
                readability_score=breakdown.readability_score,
                terminology_score=breakdown.terminology_score,
                quantification_score=breakdown.quantification_score,
                parseability_score=breakdown.parseability_score,
                structure_score=breakdown.structure_score,
                weighted_score=score,
            )
        return ATSResumeAnalysisResult(
            request=request,
            knowledge_match_profile=knowledge_match_profile,
            ats_score=ATSScore(score=score, confidence=confidence),
            score_breakdown=breakdown,
            keyword_analysis=keyword_analysis,
            section_analysis=section_analysis,
            formatting_analysis=formatting_analysis,
            readability_analysis=readability_analysis,
            terminology_analysis=terminology_analysis,
            quantification_analysis=quantification_analysis,
            parseability_analysis=parseability_analysis,
            confidence=confidence,
        )

    # --------------------------------------------------------------
    # Profile adapter (unchanged)
    # --------------------------------------------------------------

    @staticmethod
    def _normalize_keyword(value: Any) -> str:
        return " ".join(str(value or "").casefold().split())

    @staticmethod
    def _enum_value(value: Any) -> str:
        return getattr(value, "value", value).__str__().casefold()

    @staticmethod
    def _profile_keywords(profile: KnowledgeMatchProfile) -> tuple[str, ...]:
        candidates = getattr(profile, "required_keywords", None)
        if candidates is None:
            candidates = getattr(profile, "keywords", None)
        if candidates is None:
            candidates = getattr(profile, "keyword_profile", None)
        if candidates is None:
            return ()
        if isinstance(candidates, Mapping):
            candidates = candidates.get("required") or candidates.get("required_keywords") or candidates.get("keywords") or ()
        if isinstance(candidates, str):
            candidates = (candidates,)
        try:
            return tuple(str(item) for item in candidates if item is not None)
        except TypeError:
            return ()

__all__ = ["ATSResumeAnalyzer"]