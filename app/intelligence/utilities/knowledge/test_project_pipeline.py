"""
Project Pipeline Tests
======================

Tests the complete ProjectPipeline orchestration boundary.

Covered phases:

    Phase 1
        DocumentInput
            ->
        DocumentProfile

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
        Phase 3 results
            ->
        KnowledgeMatchProfile


The tests intentionally verify orchestration contracts rather than
individual intelligence heuristics.
"""

from __future__ import annotations

import pytest


# ============================================================================
# PROJECT PIPELINE
# ============================================================================

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline import (
    ProjectPipeline,
    ProjectPipelineResult,
    ProjectMatchResult,
    project_pipeline,
)


# ============================================================================
# DOCUMENT LAYER
# ============================================================================

from app.intelligence.utilities.knowledge.documents.document_input import (
    DocumentInput,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.documents.routed_document import (
    RoutedDocument,
)


# ============================================================================
# KNOWLEDGE PIPELINE LAYER
# ============================================================================

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_request import (
    KnowledgePipelineRequest,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_response import (
    KnowledgePipelineResponse,
)


# ============================================================================
# JD REQUIREMENT LAYER
# ============================================================================

from app.intelligence.utilities.knowledge.jd_requirements.requirement_models import (
    JDRequirementProfile,
)


# ============================================================================
# PHASE 3.1
# ============================================================================

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchRequest,
    KnowledgeMatchResult,
)


# ============================================================================
# PHASE 3.2
# ============================================================================

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
)


# ============================================================================
# PHASE 3.3
# ============================================================================

from app.intelligence.utilities.knowledge.matching.gap_models import (
    KnowledgeGapAnalysisResult,
)


# ============================================================================
# PHASE 4
# ============================================================================

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeMatchProfile,
)


# ============================================================================
# TEST DATA
# ============================================================================


RESUME_TEXT = """
Senior Engineering Manager with 10 years of experience leading software
engineering teams.

Led a team of 12 engineers delivering scalable Python services.
Mentored senior engineers and engineering managers.
Managed engineering projects from planning through production delivery.

Strong experience with Python, Django, REST APIs, PostgreSQL and AWS.
Worked closely with product and design teams to deliver customer-facing
platform capabilities.
"""


JD_TEXT = """
Senior Engineering Manager

We are looking for an experienced engineering leader to manage software
engineering teams and deliver scalable products.

Requirements:

- 8+ years of software engineering experience.
- Experience leading engineering teams.
- Experience mentoring engineers and managers.
- Strong Python experience.
- Experience with Django or similar web frameworks.
- Experience designing REST APIs.
- Experience with PostgreSQL or relational databases.
- Experience with AWS or cloud platforms.
- Strong project management experience.
- Excellent communication and collaboration skills.
"""


# ============================================================================
# HELPERS
# ============================================================================


def build_resume_result() -> ProjectPipelineResult:
    """
    Process the test resume through the project pipeline.
    """

    pipeline = ProjectPipeline()

    document = DocumentInput(
        text=RESUME_TEXT,
        document_type=DocumentType.RESUME,
    )

    return pipeline.process(
        document
    )


def build_jd_result() -> ProjectPipelineResult:
    """
    Process the test JD through the project pipeline.
    """

    pipeline = ProjectPipeline()

    document = DocumentInput(
        text=JD_TEXT,
        document_type=DocumentType.JD,
    )

    return pipeline.process(
        document
    )


def build_match_result() -> ProjectMatchResult:
    """
    Process both documents and execute the complete matching pipeline.

    Phase 3.1
        Knowledge Matching

    Phase 3.2
        Evidence Enrichment

    Phase 3.3
        Gap Analysis

    Phase 4
        Knowledge Match Profile
    """

    pipeline = ProjectPipeline()

    resume_result = pipeline.process(
        DocumentInput(
            text=RESUME_TEXT,
            document_type=DocumentType.RESUME,
        )
    )

    jd_result = pipeline.process(
        DocumentInput(
            text=JD_TEXT,
            document_type=DocumentType.JD,
        )
    )

    return pipeline.match(
        resume_result=resume_result,
        jd_result=jd_result,
    )


# ============================================================================
# PHASE 1
# ============================================================================


class TestProjectPipelineProcessing:
    """
    Tests single-document processing.
    """

    def test_resume_processing_returns_project_pipeline_result(
        self,
    ) -> None:

        result = build_resume_result()

        assert isinstance(
            result,
            ProjectPipelineResult,
        )

    def test_resume_result_has_correct_document_identity(
        self,
    ) -> None:

        result = build_resume_result()

        assert result.is_resume is True
        assert result.is_jd is False

        assert (
            result.document_input.document_type
            == DocumentType.RESUME
        )

    def test_resume_result_contains_routing_contract(
        self,
    ) -> None:

        result = build_resume_result()

        assert isinstance(
            result.routed_document,
            RoutedDocument,
        )

        assert (
            result.routed_document.document_type
            == DocumentType.RESUME
        )

        assert (
            result.routed_document.text
            == RESUME_TEXT.strip()
        )

    def test_resume_result_contains_pipeline_request(
        self,
    ) -> None:

        result = build_resume_result()

        assert isinstance(
            result.pipeline_request,
            KnowledgePipelineRequest,
        )

    def test_resume_result_contains_pipeline_response(
        self,
    ) -> None:

        result = build_resume_result()

        assert isinstance(
            result.pipeline_response,
            KnowledgePipelineResponse,
        )

        assert (
            result.pipeline_response.success
            is True
        )

    def test_resume_result_contains_knowledge_profile(
        self,
    ) -> None:

        result = build_resume_result()

        assert result.document_profile is not None

        assert (
            result.knowledge_profile
            is result.document_profile.profile
        )

    def test_resume_does_not_create_jd_requirement_profile(
        self,
    ) -> None:

        result = build_resume_result()

        assert (
            result.jd_requirement_profile
            is None
        )


# ============================================================================
# PHASE 2
# ============================================================================


class TestProjectPipelineJDProcessing:
    """
    Tests JD-specific Phase 2 processing.
    """

    def test_jd_processing_returns_project_pipeline_result(
        self,
    ) -> None:

        result = build_jd_result()

        assert isinstance(
            result,
            ProjectPipelineResult,
        )

    def test_jd_result_has_correct_document_identity(
        self,
    ) -> None:

        result = build_jd_result()

        assert result.is_jd is True
        assert result.is_resume is False

        assert (
            result.document_input.document_type
            == DocumentType.JD
        )

    def test_jd_produces_requirement_profile(
        self,
    ) -> None:

        result = build_jd_result()

        assert (
            result.jd_requirement_profile
            is not None
        )

        assert isinstance(
            result.jd_requirement_profile,
            JDRequirementProfile,
        )

    def test_jd_requirement_profile_contains_requirements(
        self,
    ) -> None:

        result = build_jd_result()

        requirement_profile = (
            result.jd_requirement_profile
        )

        assert requirement_profile is not None

        assert requirement_profile.requirements


# ============================================================================
# PHASE 3.1
# ============================================================================


class TestProjectPipelineMatching:
    """
    Tests Phase 3.1 KnowledgeMatcher integration.
    """

    def test_match_returns_project_match_result(
        self,
    ) -> None:

        result = build_match_result()

        assert isinstance(
            result,
            ProjectMatchResult,
        )

    def test_match_contains_knowledge_match_request(
        self,
    ) -> None:

        result = build_match_result()

        assert isinstance(
            result.match_request,
            KnowledgeMatchRequest,
        )

    def test_match_contains_knowledge_match_result(
        self,
    ) -> None:

        result = build_match_result()

        assert isinstance(
            result.match_result,
            KnowledgeMatchResult,
        )

    def test_match_result_is_derived_from_jd_requirements(
        self,
    ) -> None:

        result = build_match_result()

        requirement_profile = (
            result.jd_result.jd_requirement_profile
        )

        assert requirement_profile is not None

        assert (
            result.match_result.total_requirements
            == len(
                requirement_profile.requirements
            )
        )

        assert (
            len(
                result.match_result.matches
            )
            == len(
                requirement_profile.requirements
            )
        )

    def test_match_preserves_resume_and_jd_results(
        self,
    ) -> None:

        result = build_match_result()

        assert result.resume_result.is_resume
        assert result.jd_result.is_jd

        assert (
            result.resume_result.document_input.text
            == RESUME_TEXT
        )

        assert (
            result.jd_result.document_input.text
            == JD_TEXT
        )


# ============================================================================
# PHASE 3.2
# ============================================================================


class TestProjectPipelineEnrichment:
    """
    Tests Phase 3.2 KnowledgeMatchEnricher integration.
    """

    def test_match_contains_enriched_match_result(
        self,
    ) -> None:

        result = build_match_result()

        assert isinstance(
            result.enriched_match_result,
            EnrichedKnowledgeMatchResult,
        )

    def test_enriched_result_retains_original_match_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.enriched_match_result.match_result
            is result.match_result
        )

    def test_enriched_result_has_same_requirement_count(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.enriched_match_result.total_requirements
            == result.match_result.total_requirements
        )

        assert (
            len(
                result.enriched_match_result.matches
            )
            == len(
                result.match_result.matches
            )
        )

    def test_enriched_matches_preserve_atomic_matches(
        self,
    ) -> None:

        result = build_match_result()

        atomic_matches = (
            result.match_result.matches
        )

        enriched_matches = (
            result.enriched_match_result.matches
        )

        assert len(
            atomic_matches
        ) == len(
            enriched_matches
        )

        for atomic, enriched in zip(
            atomic_matches,
            enriched_matches,
        ):

            assert (
                enriched.match
                is atomic
            )

    def test_enrichment_confidence_is_valid(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            0.0
            <= result.enriched_match_result.enrichment_confidence
            <= 1.0
        )

        for enriched_match in (
            result.enriched_match_result.matches
        ):

            assert (
                0.0
                <= enriched_match.enrichment_confidence
                <= 1.0
            )

    def test_evidence_backed_count_is_consistent(
        self,
    ) -> None:

        result = build_match_result()

        enriched_matches = (
            result.enriched_match_result.matches
        )

        expected = sum(
            item.evidence_count > 0
            for item in enriched_matches
        )

        assert (
            result.enriched_match_result.evidence_backed_count
            == expected
        )


# ============================================================================
# PHASE 3.3
# ============================================================================


class TestProjectPipelineGapAnalysis:
    """
    Tests Phase 3.3 GapAnalyzer integration.
    """

    def test_match_contains_gap_analysis_result(
        self,
    ) -> None:

        result = build_match_result()

        assert isinstance(
            result.gap_analysis_result,
            KnowledgeGapAnalysisResult,
        )

    def test_gap_analysis_preserves_requirement_count(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.gap_analysis_result.total_requirements
            == result.match_result.total_requirements
        )

    def test_gap_analysis_counters_are_consistent(
        self,
    ) -> None:

        result = build_match_result()

        gap_result = (
            result.gap_analysis_result
        )

        assert (
            gap_result.no_gap_count
            + gap_result.partial_gap_count
            + gap_result.full_gap_count
            == gap_result.total_requirements
        )

    def test_gap_analysis_score_is_valid(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            0.0
            <= result.gap_analysis_result.gap_coverage_score
            <= 1.0
        )

    def test_gap_analysis_confidence_is_valid(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            0.0
            <= result.gap_analysis_result.confidence
            <= 1.0
        )


# ============================================================================
# PHASE 4
# ============================================================================


class TestProjectPipelineKnowledgeMatchProfile:
    """
    Tests Phase 4 KnowledgeMatchProfile integration.
    """

    def test_match_contains_knowledge_match_profile(
        self,
    ) -> None:

        result = build_match_result()

        assert isinstance(
            result.knowledge_match_profile,
            KnowledgeMatchProfile,
        )

    def test_knowledge_match_profile_preserves_match_result(
        self,
    ) -> None:

        result = build_match_result()

        profile = (
            result.knowledge_match_profile
        )

        assert (
            profile.match_result
            is result.match_result
        )

    def test_knowledge_match_profile_preserves_enriched_result(
        self,
    ) -> None:

        result = build_match_result()

        profile = (
            result.knowledge_match_profile
        )

        assert (
            profile.enriched_match_result
            is result.enriched_match_result
        )

    def test_knowledge_match_profile_preserves_gap_analysis_result(
        self,
    ) -> None:

        result = build_match_result()

        profile = (
            result.knowledge_match_profile
        )

        assert (
            profile.gap_analysis_result
            is result.gap_analysis_result
        )

    def test_knowledge_match_profile_requirement_count_is_consistent(
        self,
    ) -> None:

        result = build_match_result()

        profile = (
            result.knowledge_match_profile
        )

        assert (
            profile.total_requirements
            == result.match_result.total_requirements
        )

    def test_knowledge_match_profile_confidence_is_valid(
        self,
    ) -> None:

        result = build_match_result()

        profile = (
            result.knowledge_match_profile
        )

        assert (
            0.0
            <= profile.confidence
            <= 1.0
        )


# ============================================================================
# CONVENIENCE PROPERTIES
# ============================================================================


class TestProjectMatchResultProperties:
    """
    Tests convenience counters exposed by ProjectMatchResult.
    """

    def test_total_requirements_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.total_requirements
            == result.match_result.total_requirements
        )

    def test_matched_count_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.matched_count
            == result.match_result.matched_count
        )

    def test_partial_count_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.partial_count
            == result.match_result.partial_count
        )

    def test_unmatched_count_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.unmatched_count
            == result.match_result.unmatched_count
        )

    def test_overall_score_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.overall_score
            == result.match_result.overall_score
        )

    def test_confidence_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.confidence
            == result.match_result.confidence
        )

    def test_gap_count_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.gap_count
            == (
                result.gap_analysis_result.partial_gap_count
                + result.gap_analysis_result.full_gap_count
            )
        )

    def test_no_gap_count_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.no_gap_count
            == result.gap_analysis_result.no_gap_count
        )

    def test_partial_gap_count_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.partial_gap_count
            == result.gap_analysis_result.partial_gap_count
        )

    def test_full_gap_count_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.full_gap_count
            == result.gap_analysis_result.full_gap_count
        )

    def test_gap_coverage_score_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.gap_coverage_score
            == result.gap_analysis_result.gap_coverage_score
        )

    def test_gap_analysis_confidence_matches_underlying_result(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.gap_analysis_confidence
            == result.gap_analysis_result.confidence
        )

    def test_knowledge_match_profile_is_exposed(
        self,
    ) -> None:

        result = build_match_result()

        assert isinstance(
            result.knowledge_match_profile,
            KnowledgeMatchProfile,
        )

    def test_knowledge_match_profile_confidence_is_exposed(
        self,
    ) -> None:

        result = build_match_result()

        assert (
            result.knowledge_match_profile_confidence
            == result.knowledge_match_profile.confidence
        )


# ============================================================================
# VALIDATION
# ============================================================================


class TestProjectPipelineValidation:
    """
    Tests defensive validation at the orchestration boundary.
    """

    def test_process_rejects_invalid_input(
        self,
    ) -> None:

        pipeline = ProjectPipeline()

        with pytest.raises(
            TypeError,
            match="DocumentInput",
        ):

            pipeline.process(
                "not a DocumentInput"
            )

    def test_match_rejects_invalid_resume_result(
        self,
    ) -> None:

        pipeline = ProjectPipeline()

        jd_result = build_jd_result()

        with pytest.raises(
            TypeError,
            match="resume_result",
        ):

            pipeline.match(
                resume_result="invalid",
                jd_result=jd_result,
            )

    def test_match_rejects_invalid_jd_result(
        self,
    ) -> None:

        pipeline = ProjectPipeline()

        resume_result = build_resume_result()

        with pytest.raises(
            TypeError,
            match="jd_result",
        ):

            pipeline.match(
                resume_result=resume_result,
                jd_result="invalid",
            )

    def test_match_rejects_jd_passed_as_resume(
        self,
    ) -> None:

        pipeline = ProjectPipeline()

        jd_result = build_jd_result()

        with pytest.raises(
            TypeError,
            match="RESUME",
        ):

            pipeline.match(
                resume_result=jd_result,
                jd_result=jd_result,
            )

    def test_match_rejects_resume_passed_as_jd(
        self,
    ) -> None:

        pipeline = ProjectPipeline()

        resume_result = build_resume_result()

        with pytest.raises(
            TypeError,
            match="JD",
        ):

            pipeline.match(
                resume_result=resume_result,
                jd_result=resume_result,
            )


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================


class TestProjectPipelineConvenienceFunction:
    """
    Tests project_pipeline().
    """

    def test_project_pipeline_returns_project_pipeline_result(
        self,
    ) -> None:

        result = project_pipeline(
            text=RESUME_TEXT,
            document_type=DocumentType.RESUME,
        )

        assert isinstance(
            result,
            ProjectPipelineResult,
        )

    def test_project_pipeline_preserves_document_type(
        self,
    ) -> None:

        result = project_pipeline(
            text=JD_TEXT,
            document_type=DocumentType.JD,
        )

        assert result.is_jd is True
        assert result.is_resume is False

        assert (
            result.jd_requirement_profile
            is not None
        )


# ============================================================================
# END-TO-END CONTRACT
# ============================================================================


class TestProjectPipelineEndToEnd:
    """
    Final architectural contract test.

    Complete pipeline:

        Resume
            ↓
        ProjectPipelineResult
            +
        JD
            ↓
        ProjectPipelineResult
            ↓
        Phase 3.1 KnowledgeMatchResult
            ↓
        Phase 3.2 EnrichedKnowledgeMatchResult
            ↓
        Phase 3.3 KnowledgeGapAnalysisResult
            ↓
        Phase 4 KnowledgeMatchProfile
            ↓
        ProjectMatchResult
    """

    def test_complete_project_pipeline_contract(
        self,
    ) -> None:

        pipeline = ProjectPipeline()

        resume_result = pipeline.process(
            DocumentInput(
                text=RESUME_TEXT,
                document_type=DocumentType.RESUME,
            )
        )

        jd_result = pipeline.process(
            DocumentInput(
                text=JD_TEXT,
                document_type=DocumentType.JD,
            )
        )

        # --------------------------------------------------------------
        # PHASE 1
        # --------------------------------------------------------------

        assert isinstance(
            resume_result,
            ProjectPipelineResult,
        )

        assert isinstance(
            jd_result,
            ProjectPipelineResult,
        )

        # --------------------------------------------------------------
        # PHASE 2
        # --------------------------------------------------------------

        assert (
            jd_result.jd_requirement_profile
            is not None
        )

        # --------------------------------------------------------------
        # PHASE 3.1
        # --------------------------------------------------------------

        match_result = pipeline.match(
            resume_result=resume_result,
            jd_result=jd_result,
        )

        assert isinstance(
            match_result,
            ProjectMatchResult,
        )

        assert isinstance(
            match_result.match_result,
            KnowledgeMatchResult,
        )

        # --------------------------------------------------------------
        # PHASE 3.2
        # --------------------------------------------------------------

        assert isinstance(
            match_result.enriched_match_result,
            EnrichedKnowledgeMatchResult,
        )

        # --------------------------------------------------------------
        # PHASE 3.3
        # --------------------------------------------------------------

        assert isinstance(
            match_result.gap_analysis_result,
            KnowledgeGapAnalysisResult,
        )

        # --------------------------------------------------------------
        # PHASE 4
        # --------------------------------------------------------------

        assert isinstance(
            match_result.knowledge_match_profile,
            KnowledgeMatchProfile,
        )

        # --------------------------------------------------------------
        # TRACEABILITY
        # --------------------------------------------------------------

        assert (
            match_result.enriched_match_result.match_result
            is match_result.match_result
        )

        assert (
            match_result.knowledge_match_profile.match_result
            is match_result.match_result
        )

        assert (
            match_result.knowledge_match_profile.enriched_match_result
            is match_result.enriched_match_result
        )

        assert (
            match_result.knowledge_match_profile.gap_analysis_result
            is match_result.gap_analysis_result
        )

        # --------------------------------------------------------------
        # REQUIREMENT INTEGRITY
        # --------------------------------------------------------------

        assert (
            match_result.enriched_match_result.total_requirements
            == match_result.total_requirements
        )

        assert (
            match_result.gap_analysis_result.total_requirements
            == match_result.total_requirements
        )

        assert (
            match_result.knowledge_match_profile.total_requirements
            == match_result.total_requirements
        )

        # --------------------------------------------------------------
        # PHASE 4 CONFIDENCE
        # --------------------------------------------------------------

        assert (
            0.0
            <= match_result.knowledge_match_profile.confidence
            <= 1.0
        )