
"""
Phase 6 Recommendation Integration Tests
=========================================

Pipeline
--------

    Resume
       |
       v
    Phase 1
       |
       v
    Phase 2
       |
       v
    Phase 3.1 KnowledgeMatchResult
       |
       v
    Phase 3.2 EnrichedKnowledgeMatchResult
       |
       v
    Phase 3.3 KnowledgeGapAnalysisResult
       |
       v
    Phase 4 KnowledgeMatchProfile
       |
       v
    Phase 5 ATSResumeAnalysisResult
       |
       v
    Phase 6 RecommendationAnalyzer
       |
       v
    RecommendationResult
       |
       v
    ProjectMatchResult


Design rules tested
-------------------

1. Phase 6 consumes the exact Phase 5 ATSResumeAnalysisResult object.
2. Phase 6 preserves the exact Phase 5 ATSResumeAnalysisResult identity.
3. Phase 6 preserves the exact Phase 4 KnowledgeMatchProfile identity.
4. Phase 6 exposes the exact Phase 1 resume profile.
5. Phase 6 exposes the exact Phase 2 JDRequirementProfile.
6. Recommendations are typed Recommendation objects.
7. Recommendation IDs are unique.
8. RecommendationSummary exactly matches the recommendations.
9. RecommendationResult.validate() succeeds.
10. ProjectMatchResult contains the RecommendationResult.
11. The final ProjectMatchResult preserves the complete source chain.
12. Minimum-confidence filtering is enforced by the recommendation layer.

IMPORTANT
---------

These are integration tests.

They intentionally use the real ProjectPipeline and real Phase 1-6
objects rather than reconstructing Phase 5 or Phase 4 objects inside
the tests.

The current implementation error:

    TypeError:
    ProjectMatchResult.__init__()
    missing 1 required positional argument:
    'recommendation_result'

is expected to disappear once ProjectPipeline.match() actually executes
Phase 6 and passes:

    recommendation_result=recommendation_result

into ProjectMatchResult.
"""

from __future__ import annotations

from typing import Any

import pytest


# ============================================================================
# PROJECT PIPELINE
# ============================================================================

from app.intelligence.utilities.knowledge.project_pipeline import (
    ProjectPipeline,
    ProjectPipelineResult,
)


# ============================================================================
# DOCUMENT INPUT
# ============================================================================

from app.intelligence.utilities.knowledge.documents.document_input import (
    DocumentInput,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)


# ============================================================================
# PHASE 5
# ============================================================================

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSResumeAnalysisResult,
)


# ============================================================================
# PHASE 6
# ============================================================================

from app.intelligence.utilities.knowledge.recommendations.recommendation_models import (
    Recommendation,
    RecommendationResult,
    RecommendationSummary,
    RecommendationPriority,
    RecommendationStatus,
    RecommendationType,
)


# ============================================================================
# REALISTIC RESUME
# ============================================================================

RESUME_TEXT = """
MUHAMMAD KASHIF

Senior Quality Assurance and Food Safety Professional

Professional Summary

Quality Assurance professional with 6 years of Food Safety experience
and 4 years of Quality Assurance experience. Experienced in HACCP,
FSSC 22000, root cause analysis, internal audits, corrective actions,
preventive actions, production improvement, and data-based decision making.

Experience

Senior Quality Assurance Executive
ABC Foods

- Led HACCP implementation across production operations.
- Improved production yield from 70% to 99% through data-based decision making.
- Reduced quality defects by 25%.
- Conducted root cause analysis for recurring production issues.
- Managed corrective and preventive action programs.
- Conducted internal quality audits.
- Supported FSSC 22000 compliance activities.
- Trained production and quality teams.
- Maintained quality documentation and compliance records.

Skills

Quality Assurance
Food Safety
HACCP
FSSC 22000
Root Cause Analysis
Internal Auditing
CAPA
Corrective Action
Preventive Action
Data Analysis
Quality Management
Production Improvement

Education

Bachelor of Science in Food Science
University of Punjab
""".strip()


# ============================================================================
# REALISTIC JOB DESCRIPTION
# ============================================================================

JD_TEXT = """
QUALITY ASSURANCE LEAD

We are looking for a Quality Assurance Lead to manage food safety,
quality systems, audits, compliance, and continuous improvement.

Required Qualifications

- Minimum 5 years of Food Safety experience.
- At least 4 years of Quality Assurance experience.
- HACCP certification.
- Experience with FSSC 22000.
- Experience with corrective and preventive actions.
- Experience conducting internal quality audits.
- Strong root cause analysis experience.

Preferred Qualifications

- Retail experience.
- Bachelor's degree in Food Science.
- Experience leading quality teams.
- Experience with data-driven continuous improvement.

Responsibilities

- Lead quality assurance activities.
- Manage food safety programs.
- Conduct internal audits.
- Lead corrective and preventive actions.
- Improve production quality.
- Monitor quality metrics.
- Train quality and production personnel.
""".strip()


# ============================================================================
# HELPERS
# ============================================================================


def _assert_score_between_zero_and_one(
    value: Any,
) -> None:
    """
    Assert that a score/confidence value is normalized.
    """

    assert isinstance(
        value,
        (int, float),
    )

    assert 0.0 <= float(value) <= 1.0


def _assert_typed_recommendations(
    result: RecommendationResult,
) -> None:
    """
    Assert that every recommendation is a real typed Recommendation object.
    """

    assert isinstance(
        result.recommendations,
        tuple,
    )

    for recommendation in result.recommendations:
        assert isinstance(
            recommendation,
            Recommendation,
        )

        assert isinstance(
            recommendation.recommendation_type,
            RecommendationType,
        )

        assert isinstance(
            recommendation.priority,
            RecommendationPriority,
        )

        assert isinstance(
            recommendation.status,
            RecommendationStatus,
        )

        _assert_score_between_zero_and_one(
            recommendation.confidence,
        )


def _assert_recommendation_ids_unique(
    result: RecommendationResult,
) -> None:
    """
    Assert unique recommendation IDs.
    """

    ids = tuple(
        recommendation.recommendation_id
        for recommendation in result.recommendations
    )

    assert len(ids) == len(set(ids))


def _assert_summary_matches(
    result: RecommendationResult,
) -> None:
    """
    Recalculate the summary independently and compare it with the result.
    """

    expected = (
        RecommendationSummary.from_recommendations(
            result.recommendations
        )
    )

    assert result.summary == expected


def _assert_phase5_identity_chain(
    project_match_result,
) -> None:
    """
    Validate the Phase 3 -> Phase 4 -> Phase 5 identity chain.
    """

    assert (
        project_match_result.knowledge_match_profile
        is project_match_result.ats_analysis_result.knowledge_match_profile
    )

    assert (
        project_match_result.ats_analysis_result.request
        is project_match_result.ats_analysis_request
    )

    assert (
        project_match_result.ats_analysis_request.knowledge_match_profile
        is project_match_result.knowledge_match_profile
    )

    assert (
        project_match_result.ats_analysis_request.resume_profile
        is project_match_result.resume_result.document_profile
    )

    assert (
        project_match_result.ats_analysis_request.jd_requirement_profile
        is project_match_result.jd_result.jd_requirement_profile
    )


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def pipeline() -> ProjectPipeline:
    """
    Construct the real project pipeline.

    No mocks.
    No fake Phase 4 profile.
    No fake Phase 5 result.
    """

    return ProjectPipeline()


@pytest.fixture
def resume_document() -> DocumentInput:
    """
    Real Phase 1 resume input.
    """

    return DocumentInput(
        text=RESUME_TEXT,
        document_type=DocumentType.RESUME,
    )


@pytest.fixture
def jd_document() -> DocumentInput:
    """
    Real Phase 2 JD input.
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
    Run the real Phase 1 resume processing.
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

    assert result.document_profile is not None

    return result


@pytest.fixture
def processed_jd(
    pipeline: ProjectPipeline,
    jd_document: DocumentInput,
) -> ProjectPipelineResult:
    """
    Run the real Phase 2 JD processing.
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

    assert result.jd_requirement_profile is not None

    return result


@pytest.fixture
def project_match_result(
    pipeline: ProjectPipeline,
    processed_resume: ProjectPipelineResult,
    processed_jd: ProjectPipelineResult,
):
    """
    Run the complete real Phase 1 -> Phase 6 project pipeline.

    This is the central integration fixture.

    IMPORTANT:

    Once Phase 6 is correctly connected, this call must return a
    ProjectMatchResult containing recommendation_result.
    """

    result = pipeline.match(
        resume_result=processed_resume,
        jd_result=processed_jd,
    )

    return result


@pytest.fixture
def recommendation_result(
    project_match_result,
) -> RecommendationResult:
    """
    Extract the Phase 6 RecommendationResult from ProjectMatchResult.
    """

    result = project_match_result.recommendation_result

    assert isinstance(
        result,
        RecommendationResult,
    )

    return result


@pytest.fixture
def ats_result(
    project_match_result,
) -> ATSResumeAnalysisResult:
    """
    Extract the exact Phase 5 result carried by ProjectMatchResult.
    """

    result = project_match_result.ats_analysis_result

    assert isinstance(
        result,
        ATSResumeAnalysisResult,
    )

    return result


# ============================================================================
# PHASE 6 RESULT CONTRACT
# ============================================================================


def test_phase6_consumes_exact_phase5_result(
    project_match_result,
) -> None:
    """
    Phase 6 must consume the exact Phase 5 object.

    No reconstructed ATSResumeAnalysisResult is allowed.
    """

    recommendation_result = (
        project_match_result.recommendation_result
    )

    assert isinstance(
        recommendation_result,
        RecommendationResult,
    )

    assert (
        recommendation_result.ats_result
        is project_match_result.ats_analysis_result
    )


def test_phase6_preserves_exact_phase4_profile(
    project_match_result,
) -> None:
    """
    Phase 6 must preserve the exact Phase 4 KnowledgeMatchProfile.
    """

    recommendation_result = (
        project_match_result.recommendation_result
    )

    assert (
        recommendation_result.knowledge_match_profile
        is project_match_result.knowledge_match_profile
    )

    assert (
        recommendation_result.ats_result.knowledge_match_profile
        is project_match_result.knowledge_match_profile
    )


def test_phase6_preserves_exact_resume_profile(
    project_match_result,
) -> None:
    """
    Phase 6 must expose the exact Phase 1 resume profile.

    No reconstruction is permitted.
    """

    recommendation_result = (
        project_match_result.recommendation_result
    )

    assert (
        recommendation_result.resume_profile
        is project_match_result.resume_result.document_profile
    )

    assert (
        recommendation_result.ats_result.resume_profile
        is project_match_result.resume_result.document_profile
    )


def test_phase6_preserves_exact_jd_requirement_profile(
    project_match_result,
) -> None:
    """
    Phase 6 must expose the exact Phase 2 JDRequirementProfile.
    """

    recommendation_result = (
        project_match_result.recommendation_result
    )

    assert (
        recommendation_result.jd_requirement_profile
        is project_match_result.jd_result.jd_requirement_profile
    )

    assert (
        recommendation_result.ats_result.jd_requirement_profile
        is project_match_result.jd_result.jd_requirement_profile
    )


# ============================================================================
# TYPED RECOMMENDATIONS
# ============================================================================


def test_phase6_returns_typed_recommendations(
    recommendation_result: RecommendationResult,
) -> None:
    """
    Every recommendation must be a typed Recommendation object.

    Dictionaries are not accepted at the public Phase 6 boundary.
    """

    _assert_typed_recommendations(
        recommendation_result
    )


# ============================================================================
# SUMMARY
# ============================================================================


def test_phase6_summary_is_consistent(
    recommendation_result: RecommendationResult,
) -> None:
    """
    RecommendationSummary must exactly represent the recommendations.
    """

    assert isinstance(
        recommendation_result.summary,
        RecommendationSummary,
    )

    _assert_summary_matches(
        recommendation_result
    )


# ============================================================================
# UNIQUE IDS
# ============================================================================


def test_phase6_recommendation_ids_are_unique(
    recommendation_result: RecommendationResult,
) -> None:
    """
    Every recommendation must have a unique ID.
    """

    _assert_recommendation_ids_unique(
        recommendation_result
    )


# ============================================================================
# MINIMUM CONFIDENCE
# ============================================================================


def test_phase6_minimum_confidence_filters_recommendations(
    recommendation_result: RecommendationResult,
) -> None:
    """
    Every returned recommendation must satisfy the minimum confidence
    threshold defined by the Phase 6 implementation.

    The test deliberately does not hard-code an arbitrary threshold.

    Instead, it supports the canonical Phase 6 configuration names:

        minimum_confidence
        min_confidence
        confidence_threshold

    If the analyzer exposes one of these values, every returned
    recommendation must satisfy it.

    If the threshold is not exposed by the analyzer, the result-level
    confidence contract is still checked.
    """

    analyzer = getattr(
        recommendation_result,
        "analyzer",
        None,
    )

    if analyzer is None:
        analyzer = getattr(
            getattr(
                recommendation_result,
                "metadata",
                {},
            ),
            "analyzer",
            None,
        )

    threshold = None

    if analyzer is not None:
        for attribute_name in (
            "minimum_confidence",
            "min_confidence",
            "confidence_threshold",
        ):
            candidate = getattr(
                analyzer,
                attribute_name,
                None,
            )

            if candidate is not None:
                try:
                    threshold = float(candidate)
                except (
                    TypeError,
                    ValueError,
                ):
                    threshold = None

                if threshold is not None:
                    break

    if threshold is None:
        metadata = (
            recommendation_result.metadata
            or {}
        )

        for key in (
            "minimum_confidence",
            "min_confidence",
            "confidence_threshold",
        ):
            candidate = metadata.get(key)

            if candidate is not None:
                try:
                    threshold = float(candidate)
                except (
                    TypeError,
                    ValueError,
                ):
                    threshold = None

                if threshold is not None:
                    break

    if threshold is not None:
        assert 0.0 <= threshold <= 1.0

        for recommendation in (
            recommendation_result.recommendations
        ):
            assert (
                recommendation.confidence
                >= threshold
            )

    for recommendation in (
        recommendation_result.recommendations
    ):
        _assert_score_between_zero_and_one(
            recommendation.confidence
        )


# ============================================================================
# COMPLETE VALIDATION
# ============================================================================


def test_phase6_result_is_fully_validated(
    project_match_result,
    recommendation_result: RecommendationResult,
) -> None:
    """
    Validate the entire Phase 6 object graph.

    This is the final integration contract.
    """

    # ------------------------------------------------------------------------
    # PROJECT RESULT
    # ------------------------------------------------------------------------

    assert project_match_result is not None

    assert (
        project_match_result.recommendation_result
        is recommendation_result
    )

    # ------------------------------------------------------------------------
    # PHASE 5
    # ------------------------------------------------------------------------

    assert isinstance(
        project_match_result.ats_analysis_result,
        ATSResumeAnalysisResult,
    )

    # ------------------------------------------------------------------------
    # PHASE 6
    # ------------------------------------------------------------------------

    assert isinstance(
        recommendation_result,
        RecommendationResult,
    )

    recommendation_result.validate()

    # ------------------------------------------------------------------------
    # EXACT OBJECT IDENTITY
    # ------------------------------------------------------------------------

    assert (
        recommendation_result.ats_result
        is project_match_result.ats_analysis_result
    )

    assert (
        recommendation_result.knowledge_match_profile
        is project_match_result.knowledge_match_profile
    )

    assert (
        recommendation_result.resume_profile
        is project_match_result.resume_result.document_profile
    )

    assert (
        recommendation_result.jd_requirement_profile
        is project_match_result.jd_result.jd_requirement_profile
    )

    # ------------------------------------------------------------------------
    # PHASE 3 -> PHASE 4 -> PHASE 5 CHAIN
    # ------------------------------------------------------------------------

    _assert_phase5_identity_chain(
        project_match_result
    )

    # ------------------------------------------------------------------------
    # RECOMMENDATIONS
    # ------------------------------------------------------------------------

    _assert_typed_recommendations(
        recommendation_result
    )

    _assert_recommendation_ids_unique(
        recommendation_result
    )

    _assert_summary_matches(
        recommendation_result
    )

    # ------------------------------------------------------------------------
    # CONFIDENCE
    # ------------------------------------------------------------------------

    _assert_score_between_zero_and_one(
        recommendation_result.confidence
    )


# ============================================================================
# ADDITIONAL OBJECT-IN / OBJECT-OUT CONTRACT TEST
# ============================================================================


def test_phase6_result_exposes_phase5_score_and_confidence(
    recommendation_result: RecommendationResult,
) -> None:
    """
    Phase 6 must not duplicate or mutate Phase 5 scoring.

    Its score/confidence properties must come from the exact Phase 5 result.
    """

    assert (
        recommendation_result.score
        is recommendation_result.ats_result.ats_score
    )

    assert (
        recommendation_result.confidence
        == recommendation_result.ats_result.confidence
    )

    _assert_score_between_zero_and_one(
        recommendation_result.score.score
    )

    _assert_score_between_zero_and_one(
        recommendation_result.score.confidence
    )

    _assert_score_between_zero_and_one(
        recommendation_result.confidence
    )


# ============================================================================
# FILTERING CONTRACTS
# ============================================================================


def test_phase6_high_priority_filter_returns_only_high_priority_items(
    recommendation_result: RecommendationResult,
) -> None:
    """
    high_priority_recommendations() must return only CRITICAL/HIGH items.
    """

    high_priority = (
        recommendation_result.high_priority_recommendations()
    )

    for recommendation in high_priority:
        assert recommendation.priority in (
            RecommendationPriority.CRITICAL,
            RecommendationPriority.HIGH,
        )

        assert recommendation.is_high_priority is True


def test_phase6_type_filter_returns_only_requested_type(
    recommendation_result: RecommendationResult,
) -> None:
    """
    recommendations_of_type() must return only the requested type.
    """

    for recommendation_type in RecommendationType:
        filtered = (
            recommendation_result.recommendations_of_type(
                recommendation_type
            )
        )

        for recommendation in filtered:
            assert (
                recommendation.recommendation_type
                == recommendation_type
            )


# ============================================================================
# ACTIONABLE STATUS CONTRACT
# ============================================================================


def test_phase6_actionable_recommendations_are_typed_and_valid(
    recommendation_result: RecommendationResult,
) -> None:
    """
    Every actionable recommendation must satisfy the Recommendation model.
    """

    actionable = tuple(
        recommendation
        for recommendation
        in recommendation_result.recommendations
        if recommendation.is_actionable
    )

    for recommendation in actionable:
        assert isinstance(
            recommendation,
            Recommendation,
        )

        assert (
            recommendation.status
            == RecommendationStatus.ACTIONABLE
        )

        assert recommendation.title
        assert recommendation.description

        _assert_score_between_zero_and_one(
            recommendation.confidence
        )


# ============================================================================
# RESULT METADATA CONTRACT
# ============================================================================


def test_phase6_metadata_is_a_dictionary(
    recommendation_result: RecommendationResult,
) -> None:
    """
    RecommendationResult metadata must remain a typed aggregate metadata
    dictionary and must not replace the primary object graph.
    """

    assert isinstance(
        recommendation_result.metadata,
        dict,
    )

    assert (
        recommendation_result.ats_result
        is not None
    )

    assert (
        recommendation_result.knowledge_match_profile
        is recommendation_result.ats_result.knowledge_match_profile
    )


# ============================================================================
# NO DICTIONARY RECOMMENDATIONS
# ============================================================================


def test_phase6_public_recommendations_are_never_dicts(
    recommendation_result: RecommendationResult,
) -> None:
    """
    The public Phase 6 result must expose Recommendation objects.

    Compatibility conversion is allowed internally by the model boundary,
    but the resulting public collection must contain typed objects.
    """

    assert all(
        not isinstance(
            recommendation,
            dict,
        )
        for recommendation
        in recommendation_result.recommendations
    )

    assert all(
        isinstance(
            recommendation,
            Recommendation,
        )
        for recommendation
        in recommendation_result.recommendations
    )


# ============================================================================
# FINAL SOURCE-CHAIN TEST
# ============================================================================


def test_phase6_complete_source_chain(
    project_match_result,
) -> None:
    """
    Final identity test:

        Phase 1 resume profile
                |
                v
        Phase 4 KnowledgeMatchProfile
                |
                v
        Phase 5 ATSResumeAnalysisResult
                |
                v
        Phase 6 RecommendationResult
                |
                v
        ProjectMatchResult
    """

    recommendation_result = (
        project_match_result.recommendation_result
    )

    ats_result = (
        project_match_result.ats_analysis_result
    )

    knowledge_match_profile = (
        project_match_result.knowledge_match_profile
    )

    resume_profile = (
        project_match_result.resume_result.document_profile
    )

    jd_requirement_profile = (
        project_match_result.jd_result.jd_requirement_profile
    )

    # Phase 6 -> Phase 5
    assert (
        recommendation_result.ats_result
        is ats_result
    )

    # Phase 6 -> Phase 4
    assert (
        recommendation_result.knowledge_match_profile
        is knowledge_match_profile
    )

    # Phase 6 -> Phase 1
    assert (
        recommendation_result.resume_profile
        is resume_profile
    )

    # Phase 6 -> Phase 2
    assert (
        recommendation_result.jd_requirement_profile
        is jd_requirement_profile
    )

    # Phase 5 -> Phase 4
    assert (
        ats_result.knowledge_match_profile
        is knowledge_match_profile
    )

    # Phase 5 -> request
    assert (
        ats_result.request
        is project_match_result.ats_analysis_request
    )

    # Phase 5 request -> Phase 4
    assert (
        project_match_result.ats_analysis_request
        .knowledge_match_profile
        is knowledge_match_profile
    )

    # Phase 5 request -> Phase 1
    assert (
        project_match_result.ats_analysis_request
        .resume_profile
        is resume_profile
    )

    # Phase 5 request -> Phase 2
    assert (
        project_match_result.ats_analysis_request
        .jd_requirement_profile
        is jd_requirement_profile
    )

    # Final project result -> Phase 6
    assert (
        project_match_result.recommendation_result
        is recommendation_result
    )


# ============================================================================
# EXPECTED TEST COUNT
# ============================================================================

"""
Expected tests in this file:

1.  test_phase6_consumes_exact_phase5_result
2.  test_phase6_preserves_exact_phase4_profile
3.  test_phase6_preserves_exact_resume_profile
4.  test_phase6_preserves_exact_jd_requirement_profile
5.  test_phase6_returns_typed_recommendations
6.  test_phase6_summary_is_consistent
7.  test_phase6_recommendation_ids_are_unique
8.  test_phase6_minimum_confidence_filters_recommendations
9.  test_phase6_result_is_fully_validated
10. test_phase6_result_exposes_phase5_score_and_confidence
11. test_phase6_high_priority_filter_returns_only_high_priority_items
12. test_phase6_type_filter_returns_only_requested_type
13. test_phase6_actionable_recommendations_are_typed_and_valid
14. test_phase6_metadata_is_a_dictionary
15. test_phase6_public_recommendations_are_never_dicts
16. test_phase6_complete_source_chain

Run:

    pytest test_recom_integ.py -v

or, if this file is inside the knowledge package:

    pytest app/intelligence/utilities/knowledge/test_recom_integ.py -v
"""

