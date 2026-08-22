"""
Phase 6 Full Integration Test
==============================

Verifies:

    DocumentInput
        ->
    ProjectPipeline.process()
        ->
    ProjectPipeline.match()
        ->
    ATSResumeAnalysisResult
        ->
    RecommendationAnalyzer
        ->
    RecommendationResult

The test verifies object identity across the complete pipeline.
"""

from __future__ import annotations

import pytest

from app.intelligence.utilities.knowledge.documents.document_input import (
    DocumentInput,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline import (
    ProjectPipeline,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSResumeAnalysisResult,
)

from app.intelligence.utilities.knowledge.recommendations.recommendation_analyzer import (
    RecommendationAnalyzer,
)

from app.intelligence.utilities.knowledge.recommendations.recommendation_models import (
    RecommendationResult,
)


RESUME_TEXT = """
John Doe
Senior Software Engineer

SUMMARY
Senior software engineer with experience building backend applications,
REST APIs, distributed services, and production software systems.

EXPERIENCE

Senior Software Engineer
Example Technologies
2022 - Present

- Built backend services using Python.
- Developed REST APIs for internal and external consumers.
- Improved application reliability and maintainability.
- Worked with databases and cloud-based infrastructure.
- Collaborated with product and engineering teams.

Software Engineer
Previous Technologies
2019 - 2022

- Developed application features and backend integrations.
- Maintained production systems.
- Participated in code reviews and technical planning.

SKILLS
Python
REST APIs
Backend Development
Databases
Cloud
Git
Software Engineering

EDUCATION
Bachelor of Science in Computer Science
""".strip()


JD_TEXT = """
Senior Backend Software Engineer

We are looking for a Senior Backend Software Engineer.

Requirements:

- Strong Python experience.
- REST API development.
- Distributed systems experience.
- Cloud infrastructure experience.
- Database experience.
- Docker and Kubernetes experience.
- CI/CD experience.
- Strong software engineering fundamentals.
- Experience working with cross-functional teams.
""".strip()


def _build_pipeline() -> ProjectPipeline:
    return ProjectPipeline()


def _process_resume(
    pipeline: ProjectPipeline,
):
    document = DocumentInput(
        text=RESUME_TEXT,
        document_type=DocumentType.RESUME,
    )

    return pipeline.process(
        document
    )


def _process_jd(
    pipeline: ProjectPipeline,
):
    document = DocumentInput(
        text=JD_TEXT,
        document_type=DocumentType.JD,
    )

    return pipeline.process(
        document
    )


# ============================================================================
# BASIC PHASE 6 CONTRACT
# ============================================================================


def test_phase6_consumes_exact_phase5_result() -> None:
    pipeline = _build_pipeline()

    resume_result = _process_resume(
        pipeline
    )

    jd_result = _process_jd(
        pipeline
    )

    project_match_result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    ats_result = (
        project_match_result.ats_analysis_result
    )

    assert isinstance(
        ats_result,
        ATSResumeAnalysisResult,
    )

    analyzer = RecommendationAnalyzer()

    recommendation_result = analyzer.process(
        ats_result
    )

    assert isinstance(
        recommendation_result,
        RecommendationResult,
    )

    assert (
        recommendation_result.ats_result
        is ats_result
    )


# ============================================================================
# PHASE 4 IDENTITY
# ============================================================================


def test_phase6_preserves_exact_phase4_profile() -> None:
    pipeline = _build_pipeline()

    resume_result = _process_resume(
        pipeline
    )

    jd_result = _process_jd(
        pipeline
    )

    project_match_result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    ats_result = (
        project_match_result.ats_analysis_result
    )

    phase4_profile = (
        project_match_result.knowledge_match_profile
    )

    assert (
        ats_result.knowledge_match_profile
        is phase4_profile
    )

    analyzer = RecommendationAnalyzer()

    recommendation_result = analyzer.process(
        ats_result
    )

    assert (
        recommendation_result.knowledge_match_profile
        is phase4_profile
    )

    assert (
        recommendation_result.ats_result
        is ats_result
    )


# ============================================================================
# PHASE 1 IDENTITY
# ============================================================================


def test_phase6_preserves_exact_resume_profile() -> None:
    pipeline = _build_pipeline()

    resume_result = _process_resume(
        pipeline
    )

    jd_result = _process_jd(
        pipeline
    )

    project_match_result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    ats_result = (
        project_match_result.ats_analysis_result
    )

    assert (
        ats_result.resume_profile
        is resume_result.document_profile
    )

    analyzer = RecommendationAnalyzer()

    recommendation_result = analyzer.process(
        ats_result
    )

    assert (
        recommendation_result.resume_profile
        is resume_result.document_profile
    )


# ============================================================================
# PHASE 2 IDENTITY
# ============================================================================


def test_phase6_preserves_exact_jd_requirement_profile() -> None:
    pipeline = _build_pipeline()

    resume_result = _process_resume(
        pipeline
    )

    jd_result = _process_jd(
        pipeline
    )

    project_match_result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    ats_result = (
        project_match_result.ats_analysis_result
    )

    assert (
        ats_result.jd_requirement_profile
        is jd_result.jd_requirement_profile
    )

    analyzer = RecommendationAnalyzer()

    recommendation_result = analyzer.process(
        ats_result
    )

    assert (
        recommendation_result.jd_requirement_profile
        is jd_result.jd_requirement_profile
    )


# ============================================================================
# NO DICTIONARY PUBLIC OUTPUT
# ============================================================================


def test_phase6_returns_typed_recommendations() -> None:
    pipeline = _build_pipeline()

    resume_result = _process_resume(
        pipeline
    )

    jd_result = _process_jd(
        pipeline
    )

    project_match_result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    analyzer = RecommendationAnalyzer()

    result = analyzer.process(
        project_match_result.ats_analysis_result
    )

    assert isinstance(
        result,
        RecommendationResult,
    )

    for recommendation in result.recommendations:
        assert not isinstance(
            recommendation,
            dict,
        )

        assert hasattr(
            recommendation,
            "recommendation_id",
        )

        assert hasattr(
            recommendation,
            "recommendation_type",
        )

        assert hasattr(
            recommendation,
            "priority",
        )


# ============================================================================
# SUMMARY CONSISTENCY
# ============================================================================


def test_phase6_summary_is_consistent() -> None:
    pipeline = _build_pipeline()

    resume_result = _process_resume(
        pipeline
    )

    jd_result = _process_jd(
        pipeline
    )

    project_match_result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    analyzer = RecommendationAnalyzer()

    result = analyzer.process(
        project_match_result.ats_analysis_result
    )

    result.validate()

    assert result.summary is not None

    assert (
        result.summary.total
        == len(result.recommendations)
    )


# ============================================================================
# UNIQUE RECOMMENDATION IDS
# ============================================================================


def test_phase6_recommendation_ids_are_unique() -> None:
    pipeline = _build_pipeline()

    resume_result = _process_resume(
        pipeline
    )

    jd_result = _process_jd(
        pipeline
    )

    project_match_result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    analyzer = RecommendationAnalyzer()

    result = analyzer.process(
        project_match_result.ats_analysis_result
    )

    ids = [
        recommendation.recommendation_id
        for recommendation in result.recommendations
    ]

    assert len(ids) == len(set(ids))


# ============================================================================
# CONFIDENCE FILTER
# ============================================================================


def test_phase6_minimum_confidence_filters_recommendations() -> None:
    pipeline = _build_pipeline()

    resume_result = _process_resume(
        pipeline
    )

    jd_result = _process_jd(
        pipeline
    )

    project_match_result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    ats_result = (
        project_match_result.ats_analysis_result
    )

    analyzer = RecommendationAnalyzer(
        minimum_confidence=0.80,
    )

    result = analyzer.process(
        ats_result
    )

    for recommendation in result.recommendations:
        assert (
            recommendation.confidence
            >= 0.80
        )


# ============================================================================
# EMPTY / VALIDATED RESULT
# ============================================================================


def test_phase6_result_is_fully_validated() -> None:
    pipeline = _build_pipeline()

    resume_result = _process_resume(
        pipeline
    )

    jd_result = _process_jd(
        pipeline
    )

    project_match_result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    ats_result = (
        project_match_result.ats_analysis_result
    )

    analyzer = RecommendationAnalyzer()

    result = analyzer.process(
        ats_result
    )

    result.validate()

    assert (
        result.ats_result
        is ats_result
    )


# ============================================================================
# INVALID INPUT CONTRACT
# ============================================================================


def test_phase6_rejects_non_ats_result() -> None:
    analyzer = RecommendationAnalyzer()

    with pytest.raises(
        TypeError,
        match="ATSResumeAnalysisResult",
    ):
        analyzer.process(
            object()
        )