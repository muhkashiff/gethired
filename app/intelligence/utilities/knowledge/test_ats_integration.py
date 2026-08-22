"""
ATS / Project Pipeline Integration Tests
========================================

Complete integration coverage for:

    Phase 1
        DocumentInput
            |
            v
    ProjectPipeline.process()
            |
            v
    ProjectPipelineResult
            |
            v
    Phase 3
        KnowledgeMatchResult
            |
            v
    Phase 4
        KnowledgeMatchProfile
            |
            v
    Phase 5
        ATSResumeAnalysisRequest
            |
            v
        ATSResumeAnalyzer
            |
            v
        ATSResumeAnalysisResult

Important
---------

This test module intentionally does NOT depend on pytest fixtures from
another test module.

It creates its own ProjectPipeline instance and its own DocumentInput
objects.

No mocks.
No monkeypatching.
No fake ATS result.
No fake KnowledgeMatchProfile.
No direct construction of the Phase 4 profile for the main integration path.

The purpose is to verify that the real project pipeline can carry a real
resume and JD all the way through ATS analysis.
"""

from __future__ import annotations

import pytest


# ============================================================================
# PROJECT PIPELINE IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline import (
    ProjectPipeline,
)

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline_result import (
    ProjectPipelineResult,
    ProjectMatchResult,
)


# ============================================================================
# DOCUMENT IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.documents.document_input import (
    DocumentInput,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)


# ============================================================================
# PHASE 4 IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeMatchProfile,
)


# ============================================================================
# PHASE 5 IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSResumeAnalysisResult,
    ATSScore,
    ATSScoreBreakdown,
    ATSKeywordAnalysis,
    ATSSectionAnalysis,
    ATSFormattingAnalysis,
    ATSReadabilityAnalysis,
    ATSTerminologyAnalysis,
    ATSQuantificationAnalysis,
    ATSParseabilityAnalysis,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_request import (
    ATSResumeAnalysisRequest,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_policy import (
    ATSAnalysisPolicy,
)

from app.intelligence.utilities.knowledge.ats.ats_resume_analyzer import (
    ATSResumeAnalyzer,
)


# ============================================================================
# TEST INPUTS
# ============================================================================

RESUME_TEXT = """
JOHN DOE

Professional Summary

Senior Python Software Engineer with 7+ years of experience building
scalable backend systems, REST APIs, PostgreSQL applications, Docker
deployments, AWS infrastructure, CI/CD pipelines, automated testing,
and cloud-based services.

Experience

Senior Python Software Engineer
Acme Technologies
2020 - Present

- Built Python backend services serving more than 1,000,000 requests per day.
- Improved REST API response time by 35%.
- Designed and maintained Django and FastAPI services.
- Optimized PostgreSQL queries and reduced database latency by 40%.
- Built automated CI/CD deployment pipelines.
- Containerized applications using Docker.
- Deployed production services to AWS.
- Increased automated test coverage to 90%.
- Reduced production defects by 30%.
- Mentored junior software engineers.
- Worked with Git-based development workflows.
- Built SQL queries and database integrations.
- Developed backend automation systems.

Software Engineer
Example Corporation
2017 - 2020

- Developed Python backend applications.
- Built REST APIs.
- Maintained PostgreSQL databases.
- Created automated tests using Pytest.
- Supported CI/CD pipelines.
- Worked with Docker and AWS.

Education

Bachelor of Science in Computer Science

Skills

Python
Django
FastAPI
PostgreSQL
SQL
Docker
AWS
REST APIs
CI/CD
Git
Pytest
Automation
Backend Development
"""


JD_TEXT = """
Senior Python Backend Engineer

Professional Summary

We are looking for a Senior Python Backend Engineer with strong
experience building scalable backend systems and production APIs.

Experience

- Develop backend services using Python.
- Build and maintain REST APIs.
- Work with Django and FastAPI.
- Design and optimize PostgreSQL databases.
- Write SQL queries.
- Deploy applications using Docker.
- Deploy and operate services on AWS.
- Maintain CI/CD pipelines.
- Write automated tests using Pytest.
- Work with Git.
- Build automation solutions.
- Develop scalable backend systems.

Education

Bachelor's degree in Computer Science or a related field.

Skills

Python
Django
FastAPI
PostgreSQL
SQL
REST APIs
Docker
AWS
CI/CD
Git
Pytest
Automation
Backend Development
"""


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def pipeline() -> ProjectPipeline:
    """
    Create a completely fresh real ProjectPipeline.

    This fixture is deliberately defined inside this test module so that
    pytest does not depend on conftest.py or another test module.
    """
    return ProjectPipeline()


@pytest.fixture
def resume_document() -> DocumentInput:
    """
    Real resume DocumentInput.
    """
    return DocumentInput(
        text=RESUME_TEXT,
        document_type=DocumentType.RESUME,
    )


@pytest.fixture
def jd_document() -> DocumentInput:
    """
    Real JD DocumentInput.
    """
    return DocumentInput(
        text=JD_TEXT,
        document_type=DocumentType.JD,
    )


@pytest.fixture
def processed_resume(
    pipeline: ProjectPipeline,
    resume_document: DocumentInput,
) -> ProjectPipelineResult:
    """
    Run the real pipeline through document processing for the resume.
    """
    result = pipeline.process(
        resume_document
    )

    assert isinstance(
        result,
        ProjectPipelineResult,
    )

    assert result.is_resume

    assert (
        result.document_input
        is resume_document
    )

    assert (
        result.document_input.text.strip()
        == RESUME_TEXT.strip()
    )

    return result


@pytest.fixture
def processed_jd(
    pipeline: ProjectPipeline,
    jd_document: DocumentInput,
) -> ProjectPipelineResult:
    """
    Run the real pipeline through document processing for the JD.
    """
    result = pipeline.process(
        jd_document
    )

    assert isinstance(
        result,
        ProjectPipelineResult,
    )

    assert result.is_jd

    assert (
        result.document_input
        is jd_document
    )

    assert (
        result.document_input.text.strip()
        == JD_TEXT.strip()
    )

    assert (
        result.jd_requirement_profile
        is not None
    )

    return result


@pytest.fixture
def project_match(
    pipeline: ProjectPipeline,
    processed_resume: ProjectPipelineResult,
    processed_jd: ProjectPipelineResult,
) -> ProjectMatchResult:
    """
    Run the real Phase 3 -> Phase 4 -> Phase 5 pipeline.

    This is the central integration fixture.
    """
    result = pipeline.match(
        resume_result=processed_resume,
        jd_result=processed_jd,
    )

    assert isinstance(
        result,
        ProjectMatchResult,
    )

    return result


# ============================================================================
# BASIC PIPELINE TEST
# ============================================================================


def test_pipeline_fixture_is_real(
    pipeline: ProjectPipeline,
) -> None:
    """
    Confirm the integration fixture is the real ProjectPipeline.
    """
    assert isinstance(
        pipeline,
        ProjectPipeline,
    )


# ============================================================================
# PHASE 1 -> PHASE 2
# ============================================================================


def test_resume_document_reaches_project_pipeline(
    pipeline: ProjectPipeline,
    resume_document: DocumentInput,
) -> None:
    """
    Verify:

        DocumentInput(RESUME)
            ->
        ProjectPipeline.process()
            ->
        ProjectPipelineResult
    """
    result = pipeline.process(
        resume_document
    )

    assert isinstance(
        result,
        ProjectPipelineResult,
    )

    assert result.is_resume

    assert result.document_input is resume_document

    assert (
        result.document_input.document_type
        is DocumentType.RESUME
    )

    assert (
        result.document_input.text.strip()
    )


def test_jd_document_reaches_project_pipeline(
    pipeline: ProjectPipeline,
    jd_document: DocumentInput,
) -> None:
    """
    Verify:

        DocumentInput(JD)
            ->
        ProjectPipeline.process()
            ->
        ProjectPipelineResult
    """
    result = pipeline.process(
        jd_document
    )

    assert isinstance(
        result,
        ProjectPipelineResult,
    )

    assert result.is_jd

    assert result.document_input is jd_document

    assert (
        result.document_input.document_type
        is DocumentType.JD
    )

    assert (
        result.document_input.text.strip()
    )

    assert (
        result.jd_requirement_profile
        is not None
    )


# ============================================================================
# SOURCE TEXT CONTRACT
# ============================================================================


def test_processed_resume_preserves_original_source(
    processed_resume: ProjectPipelineResult,
) -> None:
    """
    The original resume text must remain available at the pipeline
    boundary.

    This test is important because Phase 5 must analyze the actual
    resume text rather than an empty derived source.
    """
    assert (
        processed_resume.document_input.text.strip()
    )

    assert (
        processed_resume.document_input.text.strip()
        == RESUME_TEXT.strip()
    )


def test_processed_jd_preserves_original_source(
    processed_jd: ProjectPipelineResult,
) -> None:
    """
    The original JD text must remain available at the pipeline boundary.
    """
    assert (
        processed_jd.document_input.text.strip()
    )

    assert (
        processed_jd.document_input.text.strip()
        == JD_TEXT.strip()
    )


# ============================================================================
# PHASE 3 + PHASE 4
# ============================================================================


def test_project_match_is_created(
    project_match: ProjectMatchResult,
) -> None:
    """
    Phase 3 + Phase 4 must produce a real ProjectMatchResult.
    """
    assert isinstance(
        project_match,
        ProjectMatchResult,
    )


def test_project_match_contains_knowledge_profile(
    project_match: ProjectMatchResult,
) -> None:
    """
    Phase 4 must produce a real KnowledgeMatchProfile.
    """
    profile = project_match.knowledge_match_profile

    assert isinstance(
        profile,
        KnowledgeMatchProfile,
    )


def test_phase_4_profile_is_not_fake(
    project_match: ProjectMatchResult,
) -> None:
    """
    Verify the profile contains the actual Phase 4 result objects.
    """
    profile = project_match.knowledge_match_profile

    assert profile.match_result is not None

    assert (
        profile.enriched_match_result
        is not None
    )

    assert (
        profile.gap_analysis_result
        is not None
    )


# ============================================================================
# PHASE 5 REQUEST
# ============================================================================


def test_ats_request_exists(
    project_match: ProjectMatchResult,
) -> None:
    """
    Phase 5 request must be available after pipeline.match().
    """
    request = project_match.ats_analysis_request

    assert isinstance(
        request,
        ATSResumeAnalysisRequest,
    )


def test_ats_request_preserves_phase_4_profile(
    project_match: ProjectMatchResult,
) -> None:
    """
    ATSResumeAnalysisRequest must contain the exact Phase 4 profile.
    """
    request = project_match.ats_analysis_request

    assert (
        request.knowledge_match_profile
        is project_match.knowledge_match_profile
    )


def test_ats_request_has_resume_profile(
    project_match: ProjectMatchResult,
) -> None:
    """
    ATS request must contain a real resume profile.
    """
    request = project_match.ats_analysis_request

    assert request.resume_profile is not None

    assert request.resume_profile.is_resume


def test_ats_request_has_jd_requirement_profile(
    project_match: ProjectMatchResult,
) -> None:
    """
    ATS request must contain the JD requirement profile.
    """
    request = project_match.ats_analysis_request

    assert (
        request.jd_requirement_profile
        is not None
    )


def test_ats_request_contains_non_empty_resume_source(
    project_match: ProjectMatchResult,
) -> None:
    """
    Critical regression test.

    The previous integration failure was:

        ATSResumeAnalysisRequest resume source must not be empty.

    The request reaching Phase 5 must therefore expose the original
    resume text through its request.source_text property.
    """
    request = project_match.ats_analysis_request

    # The request's source_text is the authoritative source for Phase 5.
    assert request.source_text.strip() == RESUME_TEXT.strip()


# ============================================================================
# PHASE 5 RESULT
# ============================================================================


def test_ats_analysis_is_attached_to_project_match(
    project_match: ProjectMatchResult,
) -> None:
    """
    ProjectMatchResult must contain the final ATS analysis result.
    """
    ats_result = project_match.ats_analysis

    assert isinstance(
        ats_result,
        ATSResumeAnalysisResult,
    )


def test_ats_result_preserves_exact_request(
    project_match: ProjectMatchResult,
) -> None:
    """
    ATSResumeAnalysisResult must retain the exact request object.
    """
    ats_result = project_match.ats_analysis

    request = project_match.ats_analysis_request

    assert (
        ats_result.request
        is request
    )


def test_ats_result_preserves_exact_phase_4_profile(
    project_match: ProjectMatchResult,
) -> None:
    """
    The final ATS result must preserve the exact Phase 4 profile.
    """
    ats_result = project_match.ats_analysis

    assert (
        ats_result.knowledge_match_profile
        is project_match.knowledge_match_profile
    )


def test_ats_result_preserves_source_profiles(
    project_match: ProjectMatchResult,
) -> None:
    """
    Verify the final ATS request still contains the original source
    profiles.
    """
    ats_result = project_match.ats_analysis

    request = ats_result.request

    assert request.resume_profile is not None

    assert (
        request.resume_profile.is_resume
    )

    assert (
        request.jd_requirement_profile
        is not None
    )


# ============================================================================
# ATS SCORE
# ============================================================================


def test_ats_score_is_normalized(
    project_match: ProjectMatchResult,
) -> None:
    """
    ATS final score must be within [0, 1].
    """
    ats_result = project_match.ats_analysis

    assert isinstance(
        ats_result.ats_score,
        ATSScore,
    )

    assert (
        0.0
        <= ats_result.ats_score.score
        <= 1.0
    )

    assert (
        0.0
        <= ats_result.ats_score.confidence
        <= 1.0
    )


def test_ats_score_matches_breakdown(
    project_match: ProjectMatchResult,
) -> None:
    """
    Final ATS score must equal the normalized weighted breakdown.
    """
    ats_result = project_match.ats_analysis

    assert isinstance(
        ats_result.score_breakdown,
        ATSScoreBreakdown,
    )

    expected = (
        ats_result.score_breakdown.weighted_score
    )

    assert (
        ats_result.ats_score.score
        == expected
    )


def test_all_ats_scores_are_normalized(
    project_match: ProjectMatchResult,
) -> None:
    """
    Every normalized ATS score must be in [0, 1].
    """
    ats_result = project_match.ats_analysis

    scores = (
        ats_result.ats_score.score,
        ats_result.score_breakdown.keyword_score,
        ats_result.score_breakdown.section_score,
        ats_result.score_breakdown.formatting_score,
        ats_result.score_breakdown.readability_score,
        ats_result.score_breakdown.terminology_score,
        ats_result.score_breakdown.quantification_score,
        ats_result.score_breakdown.parseability_score,
        ats_result.score_breakdown.structure_score,
        ats_result.keyword_analysis.keyword_coverage_score,
        ats_result.section_analysis.section_completeness_score,
        ats_result.formatting_analysis.formatting_score,
        ats_result.readability_analysis.readability_score,
        ats_result.terminology_analysis.terminology_score,
        ats_result.quantification_analysis.quantification_score,
        ats_result.parseability_analysis.parseability_score,
        ats_result.confidence,
    )

    for score in scores:
        assert 0.0 <= score <= 1.0


# ============================================================================
# KEYWORD ANALYSIS
# ============================================================================


def test_ats_keyword_analysis_is_available(
    project_match: ProjectMatchResult,
) -> None:
    """
    Keyword analysis must be present and structurally valid.
    """
    analysis = (
        project_match.ats_analysis
        .keyword_analysis
    )

    assert isinstance(
        analysis,
        ATSKeywordAnalysis,
    )

    assert isinstance(
        analysis.required_keywords,
        tuple,
    )

    assert isinstance(
        analysis.matched_keywords,
        tuple,
    )

    assert isinstance(
        analysis.missing_keywords,
        tuple,
    )

    assert isinstance(
        analysis.additional_keywords,
        tuple,
    )


def test_ats_keyword_sets_are_consistent(
    project_match: ProjectMatchResult,
) -> None:
    """
    Matched and missing keywords must be subsets of required keywords.
    """
    analysis = (
        project_match.ats_analysis
        .keyword_analysis
    )

    required = set(
        analysis.required_keywords
    )

    matched = set(
        analysis.matched_keywords
    )

    missing = set(
        analysis.missing_keywords
    )

    assert matched.issubset(
        required
    )

    assert missing.issubset(
        required
    )

    assert not (
        matched & missing
    )


# ============================================================================
# SECTION ANALYSIS
# ============================================================================


def test_ats_section_analysis_is_available(
    project_match: ProjectMatchResult,
) -> None:
    """
    Section analysis must be present.
    """
    analysis = (
        project_match.ats_analysis
        .section_analysis
    )

    assert isinstance(
        analysis,
        ATSSectionAnalysis,
    )

    assert isinstance(
        analysis.detected_sections,
        tuple,
    )

    assert isinstance(
        analysis.missing_sections,
        tuple,
    )

    assert isinstance(
        analysis.section_order_valid,
        bool,
    )


# ============================================================================
# FORMATTING ANALYSIS
# ============================================================================


def test_ats_formatting_analysis_is_available(
    project_match: ProjectMatchResult,
) -> None:
    """
    Formatting analysis must be present.
    """
    analysis = (
        project_match.ats_analysis
        .formatting_analysis
    )

    assert isinstance(
        analysis,
        ATSFormattingAnalysis,
    )

    assert isinstance(
        analysis.has_complex_layout,
        bool,
    )

    assert isinstance(
        analysis.has_tables,
        bool,
    )

    assert isinstance(
        analysis.has_columns,
        bool,
    )

    assert isinstance(
        analysis.has_graphics,
        bool,
    )


# ============================================================================
# READABILITY ANALYSIS
# ============================================================================


def test_ats_readability_analysis_is_available(
    project_match: ProjectMatchResult,
) -> None:
    """
    Readability analysis must be present.
    """
    analysis = (
        project_match.ats_analysis
        .readability_analysis
    )

    assert isinstance(
        analysis,
        ATSReadabilityAnalysis,
    )

    assert (
        analysis.estimated_word_count
        >= 0
    )

    assert (
        analysis.long_sentence_count
        >= 0
    )

    assert (
        analysis.average_sentence_length
        >= 0.0
    )


# ============================================================================
# TERMINOLOGY ANALYSIS
# ============================================================================


def test_ats_terminology_analysis_is_available(
    project_match: ProjectMatchResult,
) -> None:
    """
    Terminology analysis must be present.
    """
    analysis = (
        project_match.ats_analysis
        .terminology_analysis
    )

    assert isinstance(
        analysis,
        ATSTerminologyAnalysis,
    )

    assert isinstance(
        analysis.aligned_terms,
        tuple,
    )

    assert isinstance(
        analysis.missing_terms,
        tuple,
    )


# ============================================================================
# QUANTIFICATION ANALYSIS
# ============================================================================


def test_ats_quantification_analysis_is_available(
    project_match: ProjectMatchResult,
) -> None:
    """
    Quantification analysis must be present.
    """
    analysis = (
        project_match.ats_analysis
        .quantification_analysis
    )

    assert isinstance(
        analysis,
        ATSQuantificationAnalysis,
    )

    assert (
        analysis.quantified_achievement_count
        >= 0
    )

    assert (
        analysis.quantified_bullet_count
        >= 0
    )


# ============================================================================
# PARSEABILITY ANALYSIS
# ============================================================================


def test_ats_parseability_analysis_is_available(
    project_match: ProjectMatchResult,
) -> None:
    """
    Parseability analysis must be present.
    """
    analysis = (
        project_match.ats_analysis
        .parseability_analysis
    )

    assert isinstance(
        analysis,
        ATSParseabilityAnalysis,
    )

    assert isinstance(
        analysis.parseable,
        bool,
    )

    assert (
        analysis.extraction_warning_count
        == len(
            analysis.warnings
        )
    )


# ============================================================================
# CONFIDENCE
# ============================================================================


def test_ats_confidence_is_normalized(
    project_match: ProjectMatchResult,
) -> None:
    """
    Final ATS confidence must be normalized.
    """
    confidence = (
        project_match.ats_analysis
        .confidence
    )

    assert 0.0 <= confidence <= 1.0


# ============================================================================
# POLICY
# ============================================================================


def test_default_ats_policy_is_valid() -> None:
    """
    Verify the default Phase 5 policy.
    """
    policy = ATSAnalysisPolicy()

    assert isinstance(
        policy,
        ATSAnalysisPolicy,
    )

    assert (
        len(
            policy.required_sections
        )
        > 0
    )

    assert (
        policy.max_line_length
        > 0
    )

    assert (
        policy.minimum_quantifications
        >= 0
    )

    assert (
        abs(
            sum(
                policy.score_weights.values()
            )
            - 1.0
        )
        < 1e-9
    )


# ============================================================================
# DIRECT ATS RESULT CONTRACT
# ============================================================================


def test_ats_result_component_types(
    project_match: ProjectMatchResult,
) -> None:
    """
    Verify every Phase 5 observation object has the correct concrete type.
    """
    result = project_match.ats_analysis

    assert isinstance(
        result,
        ATSResumeAnalysisResult,
    )

    assert isinstance(
        result.ats_score,
        ATSScore,
    )

    assert isinstance(
        result.score_breakdown,
        ATSScoreBreakdown,
    )

    assert isinstance(
        result.keyword_analysis,
        ATSKeywordAnalysis,
    )

    assert isinstance(
        result.section_analysis,
        ATSSectionAnalysis,
    )

    assert isinstance(
        result.formatting_analysis,
        ATSFormattingAnalysis,
    )

    assert isinstance(
        result.readability_analysis,
        ATSReadabilityAnalysis,
    )

    assert isinstance(
        result.terminology_analysis,
        ATSTerminologyAnalysis,
    )

    assert isinstance(
        result.quantification_analysis,
        ATSQuantificationAnalysis,
    )

    assert isinstance(
        result.parseability_analysis,
        ATSParseabilityAnalysis,
    )


# ============================================================================
# COMPLETE END-TO-END TEST
# ============================================================================


@pytest.mark.integration
def test_complete_project_pipeline_through_phase_5(
    pipeline: ProjectPipeline,
    resume_document: DocumentInput,
    jd_document: DocumentInput,
) -> None:
    """
    Complete end-to-end integration test.

    Pipeline:

        DocumentInput RESUME
            |
            v
        ProjectPipeline.process()
            |
            v
        ProjectPipelineResult RESUME

        DocumentInput JD
            |
            v
        ProjectPipeline.process()
            |
            v
        ProjectPipelineResult JD

            |
            v

        ProjectPipeline.match()
            |
            +----------------------------+
            |                            |
            v                            v
        Phase 3                     Phase 4
        matching                    profile
            |                            |
            +-------------+--------------+
                          |
                          v
                        Phase 5
                          |
                          v
                 ATSResumeAnalysisResult
    """

    # ------------------------------------------------------------------
    # PHASE 1 / PHASE 2
    # ------------------------------------------------------------------

    resume_result = pipeline.process(
        resume_document
    )

    jd_result = pipeline.process(
        jd_document
    )

    assert isinstance(
        resume_result,
        ProjectPipelineResult,
    )

    assert isinstance(
        jd_result,
        ProjectPipelineResult,
    )

    assert resume_result.is_resume
    assert jd_result.is_jd

    assert (
        resume_result.document_input
        is resume_document
    )

    assert (
        jd_result.document_input
        is jd_document
    )

    assert (
        resume_result.document_input.text.strip()
    )

    assert (
        jd_result.document_input.text.strip()
    )

    assert (
        jd_result.jd_requirement_profile
        is not None
    )

    # ------------------------------------------------------------------
    # PHASE 3 / PHASE 4 / PHASE 5
    # ------------------------------------------------------------------

    match_result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    assert isinstance(
        match_result,
        ProjectMatchResult,
    )

    # ------------------------------------------------------------------
    # PHASE 4
    # ------------------------------------------------------------------

    profile = (
        match_result.knowledge_match_profile
    )

    assert isinstance(
        profile,
        KnowledgeMatchProfile,
    )

    assert (
        profile.match_result
        is not None
    )

    assert (
        profile.enriched_match_result
        is not None
    )

    assert (
        profile.gap_analysis_result
        is not None
    )

    # ------------------------------------------------------------------
    # PHASE 5 REQUEST
    # ------------------------------------------------------------------

    request = (
        match_result.ats_analysis_request
    )

    assert isinstance(
        request,
        ATSResumeAnalysisRequest,
    )

    assert (
        request.knowledge_match_profile
        is profile
    )

    assert (
        request.resume_profile
        is not None
    )

    assert (
        request.resume_profile.is_resume
    )

    assert (
        request.jd_requirement_profile
        is not None
    )

    # ------------------------------------------------------------------
    # CRITICAL SOURCE CONTRACT
    # ------------------------------------------------------------------

    # The authoritative source text is available directly on the request.
    # No need to drill into source_result (which may not exist on the profile).
    assert request.source_text.strip() == resume_document.text.strip()

    # ------------------------------------------------------------------
    # PHASE 5 RESULT
    # ------------------------------------------------------------------

    ats_result = (
        match_result.ats_analysis
    )

    assert isinstance(
        ats_result,
        ATSResumeAnalysisResult,
    )

    assert (
        ats_result.request
        is request
    )

    assert (
        ats_result.knowledge_match_profile
        is profile
    )

    # ------------------------------------------------------------------
    # SCORE
    # ------------------------------------------------------------------

    assert (
        0.0
        <= ats_result.ats_score.score
        <= 1.0
    )

    assert (
        0.0
        <= ats_result.ats_score.confidence
        <= 1.0
    )

    assert (
        ats_result.ats_score.score
        == ats_result.score_breakdown.weighted_score
    )

    # ------------------------------------------------------------------
    # COMPONENTS
    # ------------------------------------------------------------------

    assert isinstance(
        ats_result.keyword_analysis,
        ATSKeywordAnalysis,
    )

    assert isinstance(
        ats_result.section_analysis,
        ATSSectionAnalysis,
    )

    assert isinstance(
        ats_result.formatting_analysis,
        ATSFormattingAnalysis,
    )

    assert isinstance(
        ats_result.readability_analysis,
        ATSReadabilityAnalysis,
    )

    assert isinstance(
        ats_result.terminology_analysis,
        ATSTerminologyAnalysis,
    )

    assert isinstance(
        ats_result.quantification_analysis,
        ATSQuantificationAnalysis,
    )

    assert isinstance(
        ats_result.parseability_analysis,
        ATSParseabilityAnalysis,
    )

    # ------------------------------------------------------------------
    # FINAL CONFIDENCE
    # ------------------------------------------------------------------

    assert (
        0.0
        <= ats_result.confidence
        <= 1.0
    )