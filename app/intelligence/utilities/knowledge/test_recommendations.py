"""
Phase 6 Recommendation Integration Tests
=========================================

End-to-end integration coverage for:

    Phase 1
        DocumentInput
            ->
        DocumentKnowledgeProfile

    Phase 2
        JD
            ->
        JDRequirementProfile

    Phase 3.1
        Resume + JD
            ->
        KnowledgeMatchResult

    Phase 3.2
        KnowledgeMatchResult
            ->
        EnrichedKnowledgeMatchResult

    Phase 3.3
        EnrichedKnowledgeMatchResult
            ->
        KnowledgeGapAnalysisResult

    Phase 4
        KnowledgeMatchProfile

    Phase 5
        ATSResumeAnalysisRequest
            ->
        ATSResumeAnalysisResult

    Phase 6
        ATSResumeAnalysisResult
            ->
        RecommendationAnalyzer
            ->
        RecommendationResult

These tests intentionally exercise the real application orchestration
boundary rather than reconstructing Phase 4 or Phase 5 objects manually.

IMPORTANT
---------

This test assumes the production RecommendationAnalyzer exists at:

    app.intelligence.utilities.knowledge.recommendations.recommendation_analyzer

If your project uses a different module path for RecommendationAnalyzer,
change only that import.

The tests preserve and verify the identity contracts established by the
Phase 4, Phase 5, and Phase 6 models.
"""

from __future__ import annotations

from typing import Any

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

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline_result import (
    ProjectMatchResult,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSResumeAnalysisResult,
)

from app.intelligence.utilities.knowledge.recommendations.recommendation_models import (
    Recommendation,
    RecommendationPriority,
    RecommendationResult,
    RecommendationStatus,
    RecommendationSummary,
    RecommendationType,
)

from app.intelligence.utilities.knowledge.recommendations.recommendation_analyzer import (
    RecommendationAnalyzer,
)


# ============================================================================
# TEST DATA
# ============================================================================


RESUME_TEXT = """
John Doe

Professional Summary

Software Engineer with 6 years of experience building backend applications,
REST APIs, cloud services, and data-driven systems.

Experience

Senior Software Engineer
ABC Technologies

- Built Python backend services supporting 2 million requests per month.
- Developed REST APIs using Python and FastAPI.
- Improved API response time by 35 percent.
- Implemented PostgreSQL data models and database integrations.
- Worked with Docker and AWS deployment pipelines.
- Led a team of 4 engineers.

Software Engineer
XYZ Solutions

- Developed backend services using Python.
- Built automated testing pipelines.
- Improved system reliability and monitoring.

Skills

Python
FastAPI
REST APIs
PostgreSQL
Docker
AWS
Git
CI/CD
Automated Testing

Education

Bachelor of Science in Computer Science
University of Technology
"""

JD_TEXT = """
Senior Backend Software Engineer

Professional Summary

We are looking for a Senior Backend Software Engineer to build scalable
backend services and APIs.

Experience

The candidate should have strong backend engineering experience.

Required Skills

Python
FastAPI
REST APIs
PostgreSQL
Docker
AWS
Git
CI/CD

Preferred Skills

Automated Testing
Cloud Architecture
Monitoring
System Design

Responsibilities

- Build scalable backend services.
- Design and maintain REST APIs.
- Work with PostgreSQL databases.
- Deploy services using Docker and AWS.
- Improve application performance.
- Collaborate with engineering teams.

Education

Bachelor's degree in Computer Science or related field.
"""


# ============================================================================
# HELPERS
# ============================================================================


def _build_pipeline() -> ProjectPipeline:
    """
    Build the real ProjectPipeline.

    No Phase 4 or Phase 5 objects are manually reconstructed here.
    """

    return ProjectPipeline()


def _build_resume_result(
    pipeline: ProjectPipeline,
):
    return pipeline.process(
        DocumentInput(
            text=RESUME_TEXT,
            document_type=DocumentType.RESUME,
        )
    )


def _build_jd_result(
    pipeline: ProjectPipeline,
):
    return pipeline.process(
        DocumentInput(
            text=JD_TEXT,
            document_type=DocumentType.JD,
        )
    )


def _build_project_match_result() -> ProjectMatchResult:
    """
    Execute the complete Phase 1 -> Phase 5 pipeline.
    """

    pipeline = _build_pipeline()

    resume_result = _build_resume_result(
        pipeline
    )

    jd_result = _build_jd_result(
        pipeline
    )

    match_result = pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )

    assert isinstance(
        match_result,
        ProjectMatchResult,
    )

    assert isinstance(
        match_result.ats_analysis_result,
        ATSResumeAnalysisResult,
    )

    return match_result


def _build_ats_result() -> ATSResumeAnalysisResult:
    """
    Execute the real ProjectPipeline through Phase 5.
    """

    project_match_result = (
        _build_project_match_result()
    )

    ats_result = (
        project_match_result.ats_analysis_result
    )

    assert isinstance(
        ats_result,
        ATSResumeAnalysisResult,
    )

    return ats_result


def _build_recommendation_analyzer(
    ats_result: ATSResumeAnalysisResult,
) -> RecommendationAnalyzer:
    """
    Construct the RecommendationAnalyzer using the available Phase 5
    result/policy context.

    This helper intentionally supports analyzers that accept either the
    Phase 5 result or a policy/configuration object in their constructor.

    If the project's RecommendationAnalyzer has a fixed constructor,
    replace this helper with that project's constructor.
    """

    # ------------------------------------------------------------------------
    # Preferred constructor:
    #
    #     RecommendationAnalyzer()
    #
    # This is the cleanest object-in/object-out Phase 6 design.
    # ------------------------------------------------------------------------

    try:
        return RecommendationAnalyzer()
    except TypeError:
        pass

    # ------------------------------------------------------------------------
    # Compatibility path for analyzers that expect a policy.
    # ------------------------------------------------------------------------

    policy = getattr(
        ats_result.request,
        "metadata",
        {},
    ).get(
        "policy"
    )

    try:
        return RecommendationAnalyzer(
            policy=policy,
        )
    except TypeError:
        pass

    # ------------------------------------------------------------------------
    # If the implementation expects the Phase 5 result itself.
    # ------------------------------------------------------------------------

    try:
        return RecommendationAnalyzer(
            ats_result=ats_result,
        )
    except TypeError:
        pass

    raise TypeError(
        "Unable to construct RecommendationAnalyzer using the supported "
        "Phase 6 integration-test constructor patterns. Update "
        "_build_recommendation_analyzer() to match the production "
        "RecommendationAnalyzer constructor."
    )


def _run_recommendations() -> RecommendationResult:
    """
    Execute the real Phase 5 -> Phase 6 recommendation pipeline.
    """

    ats_result = _build_ats_result()

    analyzer = _build_recommendation_analyzer(
        ats_result
    )

    # ------------------------------------------------------------------------
    # Preferred Phase 6 contract:
    #
    #     analyzer.process(ats_result)
    # ------------------------------------------------------------------------

    result = analyzer.process(
        ats_result
    )

    assert isinstance(
        result,
        RecommendationResult,
    )

    return result


# ============================================================================
# PHASE 5 PRECONDITIONS
# ============================================================================


def test_phase_5_produces_valid_ats_result_before_recommendations() -> None:
    """
    Verify that Phase 6 receives a valid, fully constructed Phase 5 result.
    """

    ats_result = _build_ats_result()

    assert isinstance(
        ats_result,
        ATSResumeAnalysisResult,
    )

    assert ats_result.request is not None
    assert ats_result.knowledge_match_profile is not None

    assert (
        ats_result.request.knowledge_match_profile
        is ats_result.knowledge_match_profile
    )

    assert (
        ats_result.resume_profile
        is ats_result.request.resume_profile
    )

    assert (
        ats_result.jd_requirement_profile
        is ats_result.request.jd_requirement_profile
    )

    ats_result.validate()


# ============================================================================
# BASIC PHASE 6 INTEGRATION
# ============================================================================


def test_recommendation_analyzer_accepts_exact_phase_5_result() -> None:
    """
    RecommendationAnalyzer must consume the exact Phase 5
    ATSResumeAnalysisResult object.
    """

    ats_result = _build_ats_result()

    analyzer = _build_recommendation_analyzer(
        ats_result
    )

    result = analyzer.process(
        ats_result
    )

    assert isinstance(
        result,
        RecommendationResult,
    )

    assert result.ats_result is ats_result


def test_phase_6_result_preserves_phase_5_identity() -> None:
    """
    Core Phase 6 identity contract:

        result.ats_result is ats_result
    """

    ats_result = _build_ats_result()

    analyzer = _build_recommendation_analyzer(
        ats_result
    )

    result = analyzer.process(
        ats_result
    )

    assert result.ats_result is ats_result


def test_phase_6_preserves_phase_4_knowledge_match_profile_identity() -> None:
    """
    Core cross-phase identity contract:

        result.knowledge_match_profile
            is
        ats_result.knowledge_match_profile
    """

    ats_result = _build_ats_result()

    analyzer = _build_recommendation_analyzer(
        ats_result
    )

    result = analyzer.process(
        ats_result
    )

    assert (
        result.knowledge_match_profile
        is ats_result.knowledge_match_profile
    )


def test_phase_6_preserves_phase_1_resume_profile_identity() -> None:
    """
    Phase 1 resume profile must remain reachable through Phase 6 without
    reconstruction.
    """

    ats_result = _build_ats_result()

    analyzer = _build_recommendation_analyzer(
        ats_result
    )

    result = analyzer.process(
        ats_result
    )

    assert (
        result.resume_profile
        is ats_result.resume_profile
    )


def test_phase_6_preserves_phase_2_jd_requirement_profile_identity() -> None:
    """
    Phase 2 JDRequirementProfile must remain reachable through Phase 6
    without reconstruction.
    """

    ats_result = _build_ats_result()

    analyzer = _build_recommendation_analyzer(
        ats_result
    )

    result = analyzer.process(
        ats_result
    )

    assert (
        result.jd_requirement_profile
        is ats_result.jd_requirement_profile
    )


# ============================================================================
# RECOMMENDATION OBJECT CONTRACT
# ============================================================================


def test_all_recommendations_are_typed_objects() -> None:
    """
    Phase 6 must expose Recommendation objects rather than dictionaries.
    """

    result = _run_recommendations()

    assert isinstance(
        result,
        RecommendationResult,
    )

    for recommendation in result.recommendations:
        assert isinstance(
            recommendation,
            Recommendation,
        )


def test_recommendations_have_unique_ids() -> None:
    """
    RecommendationResult requires globally unique recommendation IDs within
    the result.
    """

    result = _run_recommendations()

    ids = [
        recommendation.recommendation_id
        for recommendation in result.recommendations
    ]

    assert len(ids) == len(
        set(ids)
    )


def test_recommendations_have_valid_core_fields() -> None:
    """
    Every recommendation must contain the required typed fields.
    """

    result = _run_recommendations()

    for recommendation in result.recommendations:

        assert (
            recommendation.recommendation_id.strip()
        )

        assert isinstance(
            recommendation.recommendation_type,
            RecommendationType,
        )

        assert isinstance(
            recommendation.priority,
            RecommendationPriority,
        )

        assert (
            recommendation.title.strip()
        )

        assert (
            recommendation.description.strip()
        )

        assert isinstance(
            recommendation.status,
            RecommendationStatus,
        )

        assert 0.0 <= recommendation.confidence <= 1.0


# ============================================================================
# SUMMARY CONTRACT
# ============================================================================


def test_recommendation_summary_is_present_and_consistent() -> None:
    """
    RecommendationResult must contain a summary that exactly matches the
    recommendation collection.
    """

    result = _run_recommendations()

    assert isinstance(
        result.summary,
        RecommendationSummary,
    )

    expected_summary = (
        RecommendationSummary.from_recommendations(
            result.recommendations
        )
    )

    assert (
        result.summary
        == expected_summary
    )


def test_summary_total_matches_recommendation_count() -> None:
    """
    The summary total must equal the number of recommendations.
    """

    result = _run_recommendations()

    assert result.summary is not None

    assert (
        result.summary.total
        == len(result.recommendations)
    )


def test_summary_priority_counts_match_recommendations() -> None:
    """
    Verify all priority counters.
    """

    result = _run_recommendations()

    assert result.summary is not None

    assert (
        result.summary.critical
        == sum(
            1
            for item in result.recommendations
            if item.priority
            == RecommendationPriority.CRITICAL
        )
    )

    assert (
        result.summary.high
        == sum(
            1
            for item in result.recommendations
            if item.priority
            == RecommendationPriority.HIGH
        )
    )

    assert (
        result.summary.medium
        == sum(
            1
            for item in result.recommendations
            if item.priority
            == RecommendationPriority.MEDIUM
        )
    )

    assert (
        result.summary.low
        == sum(
            1
            for item in result.recommendations
            if item.priority
            == RecommendationPriority.LOW
        )
    )


def test_summary_type_counts_match_recommendations() -> None:
    """
    Verify all Phase 6 recommendation-type counters.
    """

    result = _run_recommendations()

    assert result.summary is not None

    assert (
        result.summary.keyword_count
        == sum(
            1
            for item in result.recommendations
            if item.recommendation_type
            == RecommendationType.KEYWORD
        )
    )

    assert (
        result.summary.section_count
        == sum(
            1
            for item in result.recommendations
            if item.recommendation_type
            == RecommendationType.SECTION
        )
    )

    assert (
        result.summary.formatting_count
        == sum(
            1
            for item in result.recommendations
            if item.recommendation_type
            == RecommendationType.FORMATTING
        )
    )

    assert (
        result.summary.readability_count
        == sum(
            1
            for item in result.recommendations
            if item.recommendation_type
            == RecommendationType.READABILITY
        )
    )

    assert (
        result.summary.terminology_count
        == sum(
            1
            for item in result.recommendations
            if item.recommendation_type
            == RecommendationType.TERMINOLOGY
        )
    )

    assert (
        result.summary.quantification_count
        == sum(
            1
            for item in result.recommendations
            if item.recommendation_type
            == RecommendationType.QUANTIFICATION
        )
    )

    assert (
        result.summary.parseability_count
        == sum(
            1
            for item in result.recommendations
            if item.recommendation_type
            == RecommendationType.PARSEABILITY
        )
    )

    assert (
        result.summary.knowledge_gap_count
        == sum(
            1
            for item in result.recommendations
            if item.recommendation_type
            == RecommendationType.KNOWLEDGE_GAP
        )
    )


# ============================================================================
# FILTERING CONTRACT
# ============================================================================


def test_recommendations_of_type_returns_only_requested_type() -> None:
    """
    Verify RecommendationResult.recommendations_of_type().
    """

    result = _run_recommendations()

    for recommendation_type in RecommendationType:

        filtered = (
            result.recommendations_of_type(
                recommendation_type
            )
        )

        for recommendation in filtered:
            assert (
                recommendation.recommendation_type
                == recommendation_type
            )


def test_high_priority_recommendations_returns_only_high_or_critical() -> None:
    """
    Verify RecommendationResult.high_priority_recommendations().
    """

    result = _run_recommendations()

    high_priority = (
        result.high_priority_recommendations()
    )

    for recommendation in high_priority:
        assert recommendation.priority in (
            RecommendationPriority.CRITICAL,
            RecommendationPriority.HIGH,
        )

        assert recommendation.is_high_priority


def test_actionable_property_matches_status() -> None:
    """
    Verify Recommendation.is_actionable().
    """

    result = _run_recommendations()

    for recommendation in result.recommendations:

        if (
            recommendation.status
            == RecommendationStatus.ACTIONABLE
        ):
            assert recommendation.is_actionable

        else:
            assert not recommendation.is_actionable


# ============================================================================
# PHASE 5 DATA PRESERVATION
# ============================================================================


def test_phase_5_score_is_preserved_by_phase_6() -> None:
    """
    Phase 6 must not replace or reconstruct the Phase 5 ATS score.
    """

    ats_result = _build_ats_result()

    analyzer = _build_recommendation_analyzer(
        ats_result
    )

    result = analyzer.process(
        ats_result
    )

    assert (
        result.score
        is ats_result.ats_score
    )


def test_phase_5_confidence_is_preserved_by_phase_6() -> None:
    """
    Phase 6 confidence must be the same confidence produced by Phase 5.
    """

    ats_result = _build_ats_result()

    analyzer = _build_recommendation_analyzer(
        ats_result
    )

    result = analyzer.process(
        ats_result
    )

    assert (
        result.confidence
        == ats_result.confidence
    )


def test_phase_5_request_is_preserved_through_phase_6() -> None:
    """
    Phase 6 must retain the exact Phase 5 request through ats_result.
    """

    ats_result = _build_ats_result()

    analyzer = _build_recommendation_analyzer(
        ats_result
    )

    result = analyzer.process(
        ats_result
    )

    assert (
        result.ats_result.request
        is ats_result.request
    )


# ============================================================================
# FULL OBJECT-GRAPH VALIDATION
# ============================================================================


def test_complete_phase_1_to_phase_6_object_graph_validates() -> None:
    """
    Full integration test.

    This is the most important test in this file.

    It verifies that the complete object graph survives:

        Phase 1
        Phase 2
        Phase 3.1
        Phase 3.2
        Phase 3.3
        Phase 4
        Phase 5
        Phase 6
    """

    project_match_result = (
        _build_project_match_result()
    )

    ats_result = (
        project_match_result.ats_analysis_result
    )

    analyzer = _build_recommendation_analyzer(
        ats_result
    )

    recommendation_result = analyzer.process(
        ats_result
    )

    # ------------------------------------------------------------------------
    # Aggregate types
    # ------------------------------------------------------------------------

    assert isinstance(
        project_match_result,
        ProjectMatchResult,
    )

    assert isinstance(
        ats_result,
        ATSResumeAnalysisResult,
    )

    assert isinstance(
        recommendation_result,
        RecommendationResult,
    )

    # ------------------------------------------------------------------------
    # Phase 5 identity
    # ------------------------------------------------------------------------

    assert (
        recommendation_result.ats_result
        is ats_result
    )

    # ------------------------------------------------------------------------
    # Phase 4 identity
    # ------------------------------------------------------------------------

    assert (
        recommendation_result.knowledge_match_profile
        is project_match_result.knowledge_match_profile
    )

    assert (
        recommendation_result.knowledge_match_profile
        is ats_result.knowledge_match_profile
    )

    # ------------------------------------------------------------------------
    # Phase 3.1 / 3.2 / 3.3 identity remains reachable through Phase 4
    # ------------------------------------------------------------------------

    assert (
        project_match_result.knowledge_match_profile.match_result
        is project_match_result.match_result
    )

    assert (
        project_match_result.knowledge_match_profile.enriched_match_result
        is project_match_result.enriched_match_result
    )

    assert (
        project_match_result.knowledge_match_profile.gap_analysis_result
        is project_match_result.gap_analysis_result
    )

    # ------------------------------------------------------------------------
    # Phase 1 identity
    # ------------------------------------------------------------------------

    assert (
        recommendation_result.resume_profile
        is project_match_result.resume_result.document_profile
    )

    # ------------------------------------------------------------------------
    # Phase 2 identity
    # ------------------------------------------------------------------------

    assert (
        recommendation_result.jd_requirement_profile
        is project_match_result.jd_result.jd_requirement_profile
    )

    # ------------------------------------------------------------------------
    # Phase 5 request identity
    # ------------------------------------------------------------------------

    assert (
        ats_result.request
        is project_match_result.ats_analysis_request
    )

    # ------------------------------------------------------------------------
    # Recommendation objects
    # ------------------------------------------------------------------------

    for recommendation in recommendation_result.recommendations:
        assert isinstance(
            recommendation,
            Recommendation,
        )

    # ------------------------------------------------------------------------
    # Final validation
    # ------------------------------------------------------------------------

    recommendation_result.validate()


# ============================================================================
# NEGATIVE CONTRACT TESTS
# ============================================================================


def test_recommendation_result_rejects_duplicate_ids() -> None:
    """
    Verify the Phase 6 aggregate rejects duplicate recommendation IDs.
    """

    ats_result = _build_ats_result()

    recommendation_a = Recommendation(
        recommendation_id="duplicate-id",
        recommendation_type=RecommendationType.KEYWORD,
        priority=RecommendationPriority.HIGH,
        title="Add missing keyword",
        description="Add the missing keyword to the resume.",
    )

    recommendation_b = Recommendation(
        recommendation_id="duplicate-id",
        recommendation_type=RecommendationType.SECTION,
        priority=RecommendationPriority.MEDIUM,
        title="Improve section",
        description="Improve the resume section structure.",
    )

    with pytest.raises(
        ValueError,
        match="recommendation IDs must be unique",
    ):
        RecommendationResult(
            ats_result=ats_result,
            recommendations=(
                recommendation_a,
                recommendation_b,
            ),
        )


def test_recommendation_result_rejects_invalid_ats_input() -> None:
    """
    RecommendationResult must accept only ATSResumeAnalysisResult.
    """

    with pytest.raises(
        TypeError,
        match="ats_result",
    ):
        RecommendationResult(
            ats_result=object(),
        )


def test_recommendation_rejects_invalid_confidence() -> None:
    """
    Recommendation confidence must remain within [0, 1].
    """

    with pytest.raises(
        ValueError,
        match="between 0.0 and 1.0",
    ):
        Recommendation(
            recommendation_id="invalid-confidence",
            recommendation_type=RecommendationType.GENERAL,
            priority=RecommendationPriority.LOW,
            title="Invalid confidence",
            description="This recommendation has invalid confidence.",
            confidence=2.0,
        )


# ============================================================================
# RESULT SANITY
# ============================================================================


def test_recommendation_result_reports_has_recommendations_correctly() -> None:
    """
    Verify the aggregate convenience property.
    """

    result = _run_recommendations()

    assert (
        result.has_recommendations
        == bool(result.recommendations)
    )


def test_recommendation_result_can_be_validated_multiple_times() -> None:
    """
    Validation should remain stable and idempotent.
    """

    result = _run_recommendations()

    result.validate()
    result.validate()
    result.validate()


# ============================================================================
# OPTIONAL QUALITY ASSERTION
# ============================================================================


def test_phase_6_produces_at_least_one_actionable_recommendation_when_needed() -> None:
    """
    This assertion is intentionally conditional.

    The test does not invent a requirement that Phase 6 must always produce
    recommendations. If Phase 6 produces recommendations, they must be valid
    typed actionable objects when their status says ACTIONABLE.

    If the implementation produces zero recommendations for the supplied
    resume/JD pair, the test remains valid because an empty recommendation
    result is a supported Phase-6 state.
    """

    result = _run_recommendations()

    actionable = tuple(
        recommendation
        for recommendation in result.recommendations
        if recommendation.status
        == RecommendationStatus.ACTIONABLE
    )

    for recommendation in actionable:
        assert recommendation.is_actionable
        assert recommendation.title
        assert recommendation.description


# ============================================================================
# PYTEST ENTRY POINT
# ============================================================================


if __name__ == "__main__":
    pytest.main(
        [
            __file__,
            "-v",
        ]
    )