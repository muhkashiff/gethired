
"""
Phase 6 Recommendation Integration Tests
=========================================

The Phase-6 test deliberately does NOT manufacture Phase-4 or Phase-5
objects.

The test uses the real pipeline:

    DocumentInput (RESUME)
            |
            v
    ProjectPipeline.process()
            |
            v
    ProjectPipelineResult
            |
            +----------------------+
            |                      |
            v                      v
    DocumentKnowledgeProfile   JDRequirementProfile
            |                      |
            +----------+-----------+
                       |
                       v
              ProjectPipeline.match()
                       |
                       v
              ProjectMatchResult
                       |
                       v
             ATSResumeAnalysisResult
                       |
                       v
             RecommendationAnalyzer
                       |
                       v
             RecommendationResult

IMPORTANT
---------
This file is an integration test for Phase 6.

It intentionally does NOT:

    - create a fake KnowledgeProfile
    - create a fake KnowledgeMatchProfile
    - create a fake DocumentKnowledgeProfile
    - manually create RequirementMatch objects
    - manually create KnowledgeMatchResult
    - manually create EnrichedKnowledgeMatchResult
    - manually create KnowledgeGapAnalysisResult
    - manually create ATSResumeAnalysisResult
    - patch RecommendationAnalyzer
    - monkeypatch the pipeline
    - use dictionaries as Phase-4/5 substitutes

The only object created by this test at the Phase-6 boundary is the real
RecommendationAnalyzer.

Phase 6 receives the exact ATSResumeAnalysisResult produced by Phase 5.
"""

from __future__ import annotations

import pytest

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline import (
    ProjectPipeline,
)

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline_result import (
    ProjectPipelineResult,
)

from app.intelligence.utilities.knowledge.documents.document_input import (
    DocumentInput,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSResumeAnalysisResult,
)

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeMatchProfile,
)

from app.intelligence.utilities.knowledge.recommendations.recommendation_analyzer import (
    RecommendationAnalyzer,
)

from app.intelligence.utilities.knowledge.recommendations.recommendation_models import (
    Recommendation,
    RecommendationResult,
)


# ============================================================================
# REAL TEST INPUTS
# ============================================================================

RESUME_TEXT = """
JOHN DOE

Professional Summary

Senior Python Backend Engineer with 7+ years of experience building
scalable backend systems and enterprise applications.

Experience

Senior Python Backend Engineer
ABC Technologies

- Built Python backend services for enterprise applications.
- Developed REST APIs using FastAPI.
- Designed PostgreSQL data models.
- Improved API performance by 35%.
- Led a team of 8 engineers.
- Managed CI/CD pipelines.
- Worked with Docker and AWS.
- Mentored junior engineers.

Education

Bachelor of Science in Computer Science

Skills

Python
FastAPI
PostgreSQL
REST APIs
Docker
AWS
CI/CD
Git
Pytest
Backend Development
"""

JD_TEXT = """
Senior Python Backend Engineer

Professional Summary

We are looking for a Senior Python Backend Engineer with strong experience
building scalable backend applications.

Experience

The candidate should have experience developing Python backend services,
REST APIs, FastAPI applications, PostgreSQL databases, Docker containers,
AWS infrastructure, CI/CD pipelines, and automated testing.

Skills

Python
FastAPI
PostgreSQL
REST APIs
Docker
AWS
CI/CD
Git
Pytest
Kubernetes
Redis

Education

Bachelor's degree in Computer Science or a related field.
"""


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture(scope="module")
def pipeline() -> ProjectPipeline:
    """
    Use the real project pipeline.

    No fake pipeline and no mocked phase objects are used.
    """
    return ProjectPipeline()


@pytest.fixture(scope="module")
def resume_document() -> DocumentInput:
    """
    Real Phase-1/2 resume input object.
    """
    return DocumentInput(
        text=RESUME_TEXT,
        document_type=DocumentType.RESUME,
    )


@pytest.fixture(scope="module")
def jd_document() -> DocumentInput:
    """
    Real Phase-1/2 JD input object.
    """
    return DocumentInput(
        text=JD_TEXT,
        document_type=DocumentType.JD,
    )


@pytest.fixture(scope="module")
def resume_result(
    pipeline: ProjectPipeline,
    resume_document: DocumentInput,
) -> ProjectPipelineResult:
    """
    Execute the real resume pipeline.

    The resulting ProjectPipelineResult owns the exact
    DocumentKnowledgeProfile that must later be carried into
    Phase 5.
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
        result.document_profile
        is not None
    )

    return result


@pytest.fixture(scope="module")
def jd_result(
    pipeline: ProjectPipeline,
    jd_document: DocumentInput,
) -> ProjectPipelineResult:
    """
    Execute the real JD pipeline.

    No JD profile is fabricated for the recommendation test.
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
        result.jd_requirement_profile
        is not None
    )

    return result


@pytest.fixture(scope="module")
def project_match(
    pipeline: ProjectPipeline,
    resume_result: ProjectPipelineResult,
    jd_result: ProjectPipelineResult,
):
    """
    Execute the REAL Phase-3 -> Phase-4 -> Phase-5 pipeline.

    This is the critical fixture.

    Phase 6 does not construct any upstream object itself.
    """
    result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    return result


@pytest.fixture(scope="module")
def ats_result(
    project_match,
) -> ATSResumeAnalysisResult:
    """
    Extract the exact Phase-5 ATS result produced by the pipeline.

    No ATSResumeAnalysisResult is constructed here.
    """
    result = project_match.ats_analysis_result

    assert isinstance(
        result,
        ATSResumeAnalysisResult,
    )

    return result


@pytest.fixture(scope="module")
def analyzer() -> RecommendationAnalyzer:
    """
    Construct the real Phase-6 application service.
    """
    return RecommendationAnalyzer()


@pytest.fixture(scope="module")
def recommendation_result(
    analyzer: RecommendationAnalyzer,
    ats_result: ATSResumeAnalysisResult,
) -> RecommendationResult:
    """
    Send the EXACT Phase-5 object directly into Phase 6.
    """
    result = analyzer.process(
        ats_result
    )

    assert isinstance(
        result,
        RecommendationResult,
    )

    return result


# ============================================================================
# PIPELINE BOUNDARY
# ============================================================================

class TestPhase6PipelineBoundary:
    """
    Verify that Phase 6 receives the actual Phase-5 object produced by
    the real pipeline.
    """

    def test_project_match_contains_phase5_result(
        self,
        project_match,
    ) -> None:

        assert isinstance(
            project_match.ats_analysis_result,
            ATSResumeAnalysisResult,
        )

    def test_phase5_result_contains_real_phase4_profile(
        self,
        ats_result: ATSResumeAnalysisResult,
    ) -> None:

        assert isinstance(
            ats_result.knowledge_match_profile,
            KnowledgeMatchProfile,
        )

    def test_phase5_result_preserves_phase4_profile_identity(
        self,
        ats_result: ATSResumeAnalysisResult,
    ) -> None:

        assert (
            ats_result.knowledge_match_profile
            is ats_result.request.knowledge_match_profile
        )

    def test_phase5_result_preserves_resume_profile_identity(
        self,
        ats_result: ATSResumeAnalysisResult,
        resume_result: ProjectPipelineResult,
    ) -> None:

        assert (
            ats_result.request.resume_profile
            is resume_result.document_profile
        )

    def test_phase5_result_has_real_jd_profile(
        self,
        ats_result: ATSResumeAnalysisResult,
        jd_result: ProjectPipelineResult,
    ) -> None:

        assert (
            ats_result.request.jd_requirement_profile
            is jd_result.jd_requirement_profile
        )


# ============================================================================
# RECOMMENDATION ANALYZER
# ============================================================================

class TestRecommendationAnalyzerIntegration:
    """
    Test RecommendationAnalyzer against the actual Phase-5 output.
    """

    def test_analyzer_accepts_real_phase5_object(
        self,
        analyzer: RecommendationAnalyzer,
        ats_result: ATSResumeAnalysisResult,
    ) -> None:

        result = analyzer.process(
            ats_result
        )

        assert isinstance(
            result,
            RecommendationResult,
        )

    def test_result_preserves_exact_phase5_identity(
        self,
        recommendation_result: RecommendationResult,
        ats_result: ATSResumeAnalysisResult,
    ) -> None:

        assert (
            recommendation_result.ats_result
            is ats_result
        )

    def test_recommendations_are_typed_objects(
        self,
        recommendation_result: RecommendationResult,
    ) -> None:

        for recommendation in (
            recommendation_result.recommendations
        ):
            assert isinstance(
                recommendation,
                Recommendation,
            )

    def test_recommendations_are_not_dictionaries(
        self,
        recommendation_result: RecommendationResult,
    ) -> None:

        for recommendation in (
            recommendation_result.recommendations
        ):
            assert not isinstance(
                recommendation,
                dict,
            )

    def test_recommendations_are_immutable_tuple(
        self,
        recommendation_result: RecommendationResult,
    ) -> None:

        assert isinstance(
            recommendation_result.recommendations,
            tuple,
        )

    def test_recommendation_ids_are_unique(
        self,
        recommendation_result: RecommendationResult,
    ) -> None:

        ids = [
            recommendation.recommendation_id
            for recommendation in (
                recommendation_result.recommendations
            )
        ]

        assert len(ids) == len(set(ids))


# ============================================================================
# PHASE 5 -> PHASE 6 IDENTITY
# ============================================================================

class TestPhase5ToPhase6Identity:
    """
    These tests are more important than synthetic recommendation fixtures.

    They verify that Phase 6 is consuming the real object produced by Phase 5.
    """

    def test_same_phase5_object_is_given_to_analyzer(
        self,
        analyzer: RecommendationAnalyzer,
        ats_result: ATSResumeAnalysisResult,
    ) -> None:

        result = analyzer.process(
            ats_result
        )

        assert (
            result.ats_result
            is ats_result
        )

    def test_phase4_profile_survives_into_phase6(
        self,
        recommendation_result: RecommendationResult,
        ats_result: ATSResumeAnalysisResult,
    ) -> None:

        assert (
            recommendation_result.ats_result.knowledge_match_profile
            is ats_result.knowledge_match_profile
        )

    def test_phase5_request_survives_into_phase6(
        self,
        recommendation_result: RecommendationResult,
        ats_result: ATSResumeAnalysisResult,
    ) -> None:

        assert (
            recommendation_result.ats_result.request
            is ats_result.request
        )


# ============================================================================
# RECOMMENDATION CONTENT
# ============================================================================

class TestRecommendationSignals:
    """
    These tests verify recommendations generated from the REAL ATS result.

    We do not manufacture ATSKeywordAnalysis, ATSSectionAnalysis,
    ATSFormattingAnalysis, etc.
    """

    def test_missing_keywords_drive_keyword_recommendation_when_present(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendation_result: RecommendationResult,
    ) -> None:

        missing_keywords = (
            ats_result.keyword_analysis.missing_keywords
        )

        keyword_recommendations = tuple(
            recommendation
            for recommendation in (
                recommendation_result.recommendations
            )
            if recommendation.source_component
            == "keyword_analysis"
        )

        if missing_keywords:
            assert keyword_recommendations
        else:
            assert not keyword_recommendations

    def test_missing_sections_drive_section_recommendation_when_present(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendation_result: RecommendationResult,
    ) -> None:

        missing_sections = (
            ats_result.section_analysis.missing_sections
        )

        section_recommendations = tuple(
            recommendation
            for recommendation in (
                recommendation_result.recommendations
            )
            if recommendation.source_component
            == "section_analysis"
        )

        if missing_sections:
            assert section_recommendations
        else:
            assert not section_recommendations

    def test_formatting_signals_are_based_on_real_phase5_analysis(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendation_result: RecommendationResult,
    ) -> None:

        formatting = (
            ats_result.formatting_analysis
        )

        has_formatting_problem = any(
            (
                formatting.has_complex_layout,
                formatting.has_tables,
                formatting.has_columns,
                formatting.has_graphics,
            )
        )

        formatting_recommendations = tuple(
            recommendation
            for recommendation in (
                recommendation_result.recommendations
            )
            if recommendation.source_component
            == "formatting_analysis"
        )

        if has_formatting_problem:
            assert formatting_recommendations
        else:
            assert not formatting_recommendations

    def test_readability_signal_is_based_on_real_phase5_analysis(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendation_result: RecommendationResult,
    ) -> None:

        readability = (
            ats_result.readability_analysis
        )

        readability_recommendations = tuple(
            recommendation
            for recommendation in (
                recommendation_result.recommendations
            )
            if recommendation.source_component
            == "readability_analysis"
        )

        if readability.long_sentence_count > 0:
            assert readability_recommendations
        else:
            assert not readability_recommendations

    def test_terminology_signal_is_based_on_real_phase5_analysis(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendation_result: RecommendationResult,
    ) -> None:

        missing_terms = (
            ats_result.terminology_analysis.missing_terms
        )

        terminology_recommendations = tuple(
            recommendation
            for recommendation in (
                recommendation_result.recommendations
            )
            if recommendation.source_component
            == "terminology_analysis"
        )

        if missing_terms:
            assert terminology_recommendations
        else:
            assert not terminology_recommendations

    def test_quantification_signal_is_based_on_real_phase5_analysis(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendation_result: RecommendationResult,
    ) -> None:

        score = (
            ats_result.quantification_analysis
            .quantification_score
        )

        quantification_recommendations = tuple(
            recommendation
            for recommendation in (
                recommendation_result.recommendations
            )
            if recommendation.source_component
            == "quantification_analysis"
        )

        if score < 0.70:
            assert quantification_recommendations
        else:
            assert not quantification_recommendations

    def test_parseability_signal_is_based_on_real_phase5_analysis(
        self,
        ats_result: ATSResumeAnalysisResult,
        recommendation_result: RecommendationResult,
    ) -> None:

        parseability = (
            ats_result.parseability_analysis
        )

        parseability_recommendations = tuple(
            recommendation
            for recommendation in (
                recommendation_result.recommendations
            )
            if recommendation.source_component
            == "parseability_analysis"
        )

        if parseability.parseable:
            assert not parseability_recommendations
        else:
            assert parseability_recommendations


# ============================================================================
# DETERMINISM
# ============================================================================

class TestRecommendationDeterminism:
    """
    RecommendationAnalyzer must produce deterministic output for the same
    Phase-5 object.
    """

    def test_same_phase5_input_produces_same_ids(
        self,
        analyzer: RecommendationAnalyzer,
        ats_result: ATSResumeAnalysisResult,
    ) -> None:

        first = analyzer.process(
            ats_result
        )

        second = analyzer.process(
            ats_result
        )

        first_ids = tuple(
            recommendation.recommendation_id
            for recommendation in first.recommendations
        )

        second_ids = tuple(
            recommendation.recommendation_id
            for recommendation in second.recommendations
        )

        assert first_ids == second_ids

    def test_same_phase5_input_produces_same_count(
        self,
        analyzer: RecommendationAnalyzer,
        ats_result: ATSResumeAnalysisResult,
    ) -> None:

        first = analyzer.process(
            ats_result
        )

        second = analyzer.process(
            ats_result
        )

        assert (
            len(first.recommendations)
            == len(second.recommendations)
        )


# ============================================================================
# CONFIDENCE
# ============================================================================

class TestRecommendationConfidence:
    """
    Recommendations inherit confidence from the real Phase-5 result.
    """

    def test_recommendation_confidence_is_normalized(
        self,
        recommendation_result: RecommendationResult,
    ) -> None:

        for recommendation in (
            recommendation_result.recommendations
        ):
            assert 0.0 <= recommendation.confidence <= 1.0

    def test_recommendation_confidence_matches_phase5_confidence(
        self,
        recommendation_result: RecommendationResult,
        ats_result: ATSResumeAnalysisResult,
    ) -> None:

        for recommendation in (
            recommendation_result.recommendations
        ):
            assert (
                recommendation.confidence
                == ats_result.confidence
            )


# ============================================================================
# COMPLETE PHASE 6 SCENARIO
# ============================================================================

@pytest.mark.integration
def test_complete_phase_6_real_pipeline(
    pipeline: ProjectPipeline,
    resume_document: DocumentInput,
    jd_document: DocumentInput,
) -> None:
    """
    Complete real-object Phase-1 -> Phase-6 test.

    No intermediate Phase-3/4/5 object is fabricated.

    The only explicit Phase-6 call is:

        RecommendationAnalyzer.process(
            project_match.ats_analysis_result
        )
    """

    # ------------------------------------------------------------------------
    # PHASE 1 / PHASE 2
    # ------------------------------------------------------------------------

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

    # ------------------------------------------------------------------------
    # PHASE 3 / PHASE 4 / PHASE 5
    # ------------------------------------------------------------------------

    project_match = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    ats_result = (
        project_match.ats_analysis_result
    )

    assert isinstance(
        ats_result,
        ATSResumeAnalysisResult,
    )

    # Critical source-chain identity checks.
    assert (
        ats_result.request.resume_profile
        is resume_result.document_profile
    )

    assert (
        ats_result.request.jd_requirement_profile
        is jd_result.jd_requirement_profile
    )

    assert (
        ats_result.knowledge_match_profile
        is ats_result.request.knowledge_match_profile
    )

    # ------------------------------------------------------------------------
    # PHASE 6
    # ------------------------------------------------------------------------

    analyzer = RecommendationAnalyzer()

    recommendation_result = analyzer.process(
        ats_result
    )

    assert isinstance(
        recommendation_result,
        RecommendationResult,
    )

    # Phase 6 must preserve the exact Phase-5 object.
    assert (
        recommendation_result.ats_result
        is ats_result
    )

    # All outputs must be typed recommendations.
    assert all(
        isinstance(
            recommendation,
            Recommendation,
        )
        for recommendation in (
            recommendation_result.recommendations
        )
    )

    # No dictionary-oriented public output.
    assert all(
        not isinstance(
            recommendation,
            dict,
        )
        for recommendation in (
            recommendation_result.recommendations
        )
    )

    # IDs must remain deterministic and unique.
    ids = tuple(
        recommendation.recommendation_id
        for recommendation in (
            recommendation_result.recommendations
        )
    )

    assert len(ids) == len(set(ids))

    # Final aggregate validation.
    recommendation_result.validate()

