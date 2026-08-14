"""
Enterprise V5
Resume Intelligence Enrichment Pipeline

Pipeline
--------

Resume
  ↓
Experience Enrichment
  ↓
Education Enrichment
  ↓
Seniority Detection
  ↓
Industry Detection
  ↓
Resume Enrichment Result
  ↓
JD Matching

The pipeline does NOT modify ResumeBuilder.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.intelligence.enrichment.experience_enricher import (
    ExperienceEnrichment,
    ExperienceEnrichmentResult,
    ExperienceEnricher,
)


# ======================================================================
# GENERIC INTELLIGENCE RESULT
# ======================================================================


@dataclass
class EnrichmentFinding:
    text: str = ""

    category: str = ""

    score: float = 0.0

    confidence: float = 0.0


@dataclass
class IntelligenceResult:
    title: str = ""

    score: float = 0.0

    confidence: float = 0.0

    findings: list[EnrichmentFinding] = field(
        default_factory=list
    )

    strengths: list[str] = field(
        default_factory=list
    )

    weaknesses: list[str] = field(
        default_factory=list
    )

    recommendations: list[str] = field(
        default_factory=list
    )


# ======================================================================
# RESUME ENRICHMENT
# ======================================================================


@dataclass
class ResumeEnrichment:
    """
    Complete intelligence layer output.

    This object is deliberately separate from Resume.
    """

    success: bool = False

    experience: list[ExperienceEnrichment] = field(
        default_factory=list
    )

    experience_result: ExperienceEnrichmentResult | None = None

    seniority: IntelligenceResult = field(
        default_factory=lambda:
        IntelligenceResult(
            title="Seniority"
        )
    )

    education: IntelligenceResult = field(
        default_factory=lambda:
        IntelligenceResult(
            title="Education"
        )
    )

    industry: IntelligenceResult = field(
        default_factory=lambda:
        IntelligenceResult(
            title="Industry"
        )
    )

    leadership: IntelligenceResult = field(
        default_factory=lambda:
        IntelligenceResult(
            title="Leadership"
        )
    )

    quality: IntelligenceResult = field(
        default_factory=lambda:
        IntelligenceResult(
            title="Quality"
        )
    )

    operations: IntelligenceResult = field(
        default_factory=lambda:
        IntelligenceResult(
            title="Operations"
        )
    )

    achievements: IntelligenceResult = field(
        default_factory=lambda:
        IntelligenceResult(
            title="Achievements"
        )
    )

    overall_score: float = 0.0

    confidence: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    errors: list[str] = field(
        default_factory=list
    )


# ======================================================================
# PIPELINE
# ======================================================================


class ResumeEnrichmentPipeline:

    def __init__(
        self,
        *,
        experience_enricher: ExperienceEnricher | None = None,
        seniority_detector: Any = None,
        education_enricher: Any = None,
        industry_detector: Any = None,
    ) -> None:

        self.experience_enricher = (
            experience_enricher
            or ExperienceEnricher()
        )

        self.seniority_detector = (
            seniority_detector
        )

        self.education_enricher = (
            education_enricher
        )

        self.industry_detector = (
            industry_detector
        )

    # ==================================================================
    # MAIN API
    # ==================================================================

    def enrich(
        self,
        resume: Any,
    ) -> ResumeEnrichment:

        result = ResumeEnrichment()

        if resume is None:

            result.errors.append(
                "Resume is None."
            )

            return result

        try:

            # ----------------------------------------------------------
            # 1. EXPERIENCE
            # ----------------------------------------------------------

            experiences = list(
                getattr(
                    resume,
                    "experience",
                    [],
                )
                or []
            )

            experience_result = (
                self.experience_enricher.enrich(
                    experiences
                )
            )

            result.experience_result = (
                experience_result
            )

            result.experience = (
                experience_result.records
            )

            # ----------------------------------------------------------
            # 2. SENIORITY
            # ----------------------------------------------------------

            result.seniority = (
                self._run_seniority(
                    resume,
                    result.experience,
                )
            )

            # ----------------------------------------------------------
            # 3. EDUCATION
            # ----------------------------------------------------------

            result.education = (
                self._run_education(
                    resume
                )
            )

            # ----------------------------------------------------------
            # 4. INDUSTRY
            # ----------------------------------------------------------

            result.industry = (
                self._run_industry(
                    resume,
                    result.experience,
                )
            )

            # ----------------------------------------------------------
            # 5. LEADERSHIP
            # ----------------------------------------------------------

            result.leadership = (
                self._build_leadership(
                    result.experience
                )
            )

            # ----------------------------------------------------------
            # 6. QUALITY
            # ----------------------------------------------------------

            result.quality = (
                self._build_quality(
                    result.experience
                )
            )

            # ----------------------------------------------------------
            # 7. OPERATIONS
            # ----------------------------------------------------------

            result.operations = (
                self._build_operations(
                    result.experience
                )
            )

            # ----------------------------------------------------------
            # 8. ACHIEVEMENTS
            # ----------------------------------------------------------

            result.achievements = (
                self._build_achievements(
                    result.experience
                )
            )

            # ----------------------------------------------------------
            # 9. OVERALL SCORE
            # ----------------------------------------------------------

            result.overall_score = (
                self._overall_score(
                    result
                )
            )

            result.confidence = (
                self._overall_confidence(
                    result
                )
            )

            result.metadata = {
                "experience_count": len(
                    result.experience
                ),
                "education_count": len(
                    getattr(
                        resume,
                        "education",
                        [],
                    )
                    or []
                ),
                "pipeline_version": "Enterprise V5",
                "builder_boundary_preserved": True,
            }

            result.success = (
                len(result.errors) == 0
            )

            return result

        except Exception as exc:

            result.success = False

            result.errors.append(
                str(exc)
            )

            return result

    # ==================================================================
    # SENIORITY
    # ==================================================================

    def _run_seniority(
        self,
        resume: Any,
        experiences: list[ExperienceEnrichment],
    ) -> IntelligenceResult:

        # Existing detector takes priority.
        if self.seniority_detector is not None:

            detected = self._call_external(
                self.seniority_detector,
                resume,
            )

            if detected is not None:

                return IntelligenceResult(
                    title="Seniority",
                    score=float(
                        getattr(
                            detected,
                            "score",
                            getattr(
                                detected,
                                "overall_score",
                                0.0,
                            ),
                        )
                        or 0.0
                    ),
                    confidence=float(
                        getattr(
                            detected,
                            "confidence",
                            0.95,
                        )
                        or 0.95
                    ),
                    strengths=[
                        str(
                            getattr(
                                detected,
                                "level",
                                "",
                            )
                        )
                    ]
                    if getattr(
                        detected,
                        "level",
                        "",
                    )
                    else [],
                )

        # Fallback based on experience enrichment.

        if not experiences:

            return IntelligenceResult(
                title="Seniority",
                score=0.0,
                confidence=0.0,
            )

        strongest = max(
            experiences,
            key=lambda x:
            x.seniority_score,
        )

        return IntelligenceResult(
            title="Seniority",
            score=strongest.seniority_score,
            confidence=strongest.confidence,
            strengths=[
                strongest.seniority
            ],
        )

    # ==================================================================
    # EDUCATION
    # ==================================================================

    def _run_education(
        self,
        resume: Any,
    ) -> IntelligenceResult:

        education = list(
            getattr(
                resume,
                "education",
                [],
            )
            or []
        )

        if not education:

            return IntelligenceResult(
                title="Education",
                score=0.0,
                confidence=0.0,
            )

        if self.education_enricher is not None:

            detected = self._call_external(
                self.education_enricher,
                resume,
            )

            if detected is not None:

                return self._external_to_intelligence(
                    "Education",
                    detected,
                )

        score = 0.0
        findings = []
        strengths = []

        for item in education:

            degree = str(
                getattr(
                    item,
                    "degree",
                    "",
                )
                or ""
            )

            level = str(
                getattr(
                    item,
                    "level",
                    "",
                )
                or ""
            )

            major = str(
                getattr(
                    item,
                    "major",
                    "",
                )
                or ""
            )

            institution = str(
                getattr(
                    item,
                    "institution",
                    "",
                )
                or ""
            )

            text = (
                f"{degree} "
                f"{major} "
                f"{institution}"
            ).strip()

            findings.append(
                EnrichmentFinding(
                    text=text,
                    category=level,
                    score=10.0,
                    confidence=0.95,
                )
            )

            score += 10

            if level in {
                "master",
                "doctorate",
                "phd",
            }:
                strengths.append(
                    f"{degree} qualification"
                )

        return IntelligenceResult(
            title="Education",
            score=min(
                score,
                100,
            ),
            confidence=0.95,
            findings=findings,
            strengths=strengths,
        )

    # ==================================================================
    # INDUSTRY
    # ==================================================================

    def _run_industry(
        self,
        resume: Any,
        experiences: list[ExperienceEnrichment],
    ) -> IntelligenceResult:

        if self.industry_detector is not None:

            detected = self._call_external(
                self.industry_detector,
                resume,
            )

            if detected is not None:

                return self._external_to_intelligence(
                    "Industry",
                    detected,
                )

        counts: dict[str, int] = {}

        for experience in experiences:

            for domain in experience.domains:

                counts[domain] = (
                    counts.get(
                        domain,
                        0,
                    )
                    + 1
                )

        if not counts:

            return IntelligenceResult(
                title="Industry",
                confidence=0.0,
            )

        ordered = sorted(
            counts.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        findings = [
            EnrichmentFinding(
                text=domain,
                category="experience_domain",
                score=count * 10,
                confidence=0.90,
            )
            for domain, count in ordered
        ]

        return IntelligenceResult(
            title="Industry",
            score=min(
                ordered[0][1] * 20,
                100,
            ),
            confidence=0.90,
            findings=findings,
            strengths=[
                ordered[0][0]
            ],
        )

    # ==================================================================
    # LEADERSHIP
    # ==================================================================

    @staticmethod
    def _build_leadership(
        experiences: list[ExperienceEnrichment],
    ) -> IntelligenceResult:

        if not experiences:

            return IntelligenceResult(
                title="Leadership"
            )

        score = max(
            item.leadership_score
            for item in experiences
        )

        findings = []

        for item in experiences:

            if item.leadership_score <= 0:
                continue

            findings.append(
                EnrichmentFinding(
                    text=item.title,
                    category="leadership",
                    score=item.leadership_score,
                    confidence=item.confidence,
                )
            )

        return IntelligenceResult(
            title="Leadership",
            score=score,
            confidence=0.90,
            findings=findings,
        )

    # ==================================================================
    # QUALITY
    # ==================================================================

    @staticmethod
    def _build_quality(
        experiences: list[ExperienceEnrichment],
    ) -> IntelligenceResult:

        score = max(
            (
                item.quality_score
                for item in experiences
            ),
            default=0.0,
        )

        return IntelligenceResult(
            title="Quality",
            score=score,
            confidence=0.90,
        )

    # ==================================================================
    # OPERATIONS
    # ==================================================================

    @staticmethod
    def _build_operations(
        experiences: list[ExperienceEnrichment],
    ) -> IntelligenceResult:

        score = max(
            (
                item.operational_score
                for item in experiences
            ),
            default=0.0,
        )

        return IntelligenceResult(
            title="Operations",
            score=score,
            confidence=0.90,
        )

    # ==================================================================
    # ACHIEVEMENTS
    # ==================================================================

    @staticmethod
    def _build_achievements(
        experiences: list[ExperienceEnrichment],
    ) -> IntelligenceResult:

        all_achievements = []

        for experience in experiences:

            all_achievements.extend(
                experience.achievements
            )

        if not all_achievements:

            return IntelligenceResult(
                title="Achievements",
                confidence=0.0,
            )

        findings = []

        for achievement in all_achievements:

            findings.append(
                EnrichmentFinding(
                    text=achievement.text,
                    category=achievement.category,
                    score=achievement.score,
                    confidence=achievement.confidence,
                )
            )

        score = sum(
            item.score
            for item in all_achievements
        ) / len(
            all_achievements
        )

        strengths = []

        if any(
            item.quantified
            for item in all_achievements
        ):
            strengths.append(
                "Quantified achievements present"
            )

        if any(
            item.business_impact
            for item in all_achievements
        ):
            strengths.append(
                "Business impact demonstrated"
            )

        recommendations = []

        if not all(
            item.quantified
            for item in all_achievements
        ):
            recommendations.append(
                "Quantify additional achievements."
            )

        return IntelligenceResult(
            title="Achievements",
            score=round(
                min(score, 100),
                2,
            ),
            confidence=0.95,
            findings=findings,
            strengths=strengths,
            recommendations=recommendations,
        )

    # ==================================================================
    # OVERALL
    # ==================================================================

    @staticmethod
    def _overall_score(
        result: ResumeEnrichment,
    ) -> float:

        scores = [
            result.seniority.score,
            result.education.score,
            result.industry.score,
            result.leadership.score,
            result.quality.score,
            result.operations.score,
            result.achievements.score,
        ]

        active = [
            score
            for score in scores
            if score > 0
        ]

        if not active:
            return 0.0

        return round(
            sum(active)
            / len(active),
            2,
        )

    @staticmethod
    def _overall_confidence(
        result: ResumeEnrichment,
    ) -> float:

        values = [
            result.seniority.confidence,
            result.education.confidence,
            result.industry.confidence,
            result.leadership.confidence,
            result.quality.confidence,
            result.operations.confidence,
            result.achievements.confidence,
        ]

        active = [
            value
            for value in values
            if value > 0
        ]

        if not active:
            return 0.0

        return round(
            sum(active)
            / len(active),
            3,
        )

    # ==================================================================
    # EXTERNAL ADAPTER
    # ==================================================================

    @staticmethod
    def _call_external(
        engine: Any,
        resume: Any,
    ) -> Any:

        if hasattr(
            engine,
            "enrich",
        ):
            return engine.enrich(
                resume
            )

        if hasattr(
            engine,
            "detect",
        ):
            return engine.detect(
                resume
            )

        if hasattr(
            engine,
            "resolve",
        ):
            return engine.resolve(
                resume
            )

        return None

    @staticmethod
    def _external_to_intelligence(
        title: str,
        value: Any,
    ) -> IntelligenceResult:

        return IntelligenceResult(
            title=title,
            score=float(
                getattr(
                    value,
                    "score",
                    getattr(
                        value,
                        "overall_score",
                        0.0,
                    ),
                )
                or 0.0
            ),
            confidence=float(
                getattr(
                    value,
                    "confidence",
                    0.90,
                )
                or 0.90
            ),
            strengths=list(
                getattr(
                    value,
                    "strengths",
                    [],
                )
                or []
            ),
            weaknesses=list(
                getattr(
                    value,
                    "weaknesses",
                    [],
                )
                or []
            ),
            recommendations=list(
                getattr(
                    value,
                    "recommendations",
                    [],
                )
                or []
            ),
        )