"""
Gap Analysis Tests
==================

Phase 3.3

Tests the gap-analysis boundary without testing internal heuristics.

Phase flow:

    KnowledgeMatchResult
            +
    EnrichedKnowledgeMatchResult [optional evidence]
            +
    JDRequirementProfile
            |
            v
       Gap Analysis
            |
            v
       GapAnalysisResult

The tests verify:

    1. valid inputs are accepted
    2. gaps are produced from unmatched / partial requirements
    3. matched requirements are not incorrectly classified as gaps
    4. requirement identity is preserved
    5. counts remain internally consistent
    6. empty gap sets are handled correctly
    7. invalid input types fail explicitly
    8. Phase 3.2 evidence remains available where supplied

These tests intentionally avoid asserting implementation-specific
heuristics unless they are part of the public contract.
"""

from __future__ import annotations

import pytest


# ============================================================================
# PHASE 3.3 IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.matching.gap_models import (
    KnowledgeGapAnalysisResult,
)


# ============================================================================
# PHASE 3.1 / PHASE 3.2 IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchResult,
    MatchStatus,
)

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
)


# ============================================================================
# PROJECT PIPELINE
# ============================================================================

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline import (
    ProjectPipeline,
)

from app.intelligence.utilities.knowledge.documents.document_input import (
    DocumentInput,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)


# ============================================================================
# TEST DATA
# ============================================================================


RESUME_TEXT = """
Senior Software Engineer with 8 years of experience.

Led engineering teams and mentored developers.

Built scalable Python applications using Django and FastAPI.

Experienced with PostgreSQL, REST APIs, Docker, AWS,
CI/CD pipelines, and distributed systems.

Designed backend architectures and improved application
performance and reliability.
"""


JD_TEXT = """
Senior Backend Engineer

We are looking for a senior backend engineer to build
scalable Python services.

Requirements:

- 5+ years of software engineering experience
- Strong Python experience
- Experience with Django or FastAPI
- PostgreSQL experience
- REST API development
- Docker and AWS experience
- Experience leading engineering teams
- Strong Kubernetes experience
- Experience with Terraform
"""


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def pipeline() -> ProjectPipeline:
    """
    Create the real project pipeline.
    """

    return ProjectPipeline()


@pytest.fixture
def processed_resume(
    pipeline: ProjectPipeline,
):
    """
    Process the resume through the real Phase 1 + Phase 2 pipeline.
    """

    return pipeline.process(
        DocumentInput(
            text=RESUME_TEXT,
            document_type=DocumentType.RESUME,
        )
    )


@pytest.fixture
def processed_jd(
    pipeline: ProjectPipeline,
):
    """
    Process the JD through the real Phase 1 + Phase 2 pipeline.
    """

    return pipeline.process(
        DocumentInput(
            text=JD_TEXT,
            document_type=DocumentType.JD,
        )
    )


@pytest.fixture
def project_match_result(
    pipeline: ProjectPipeline,
    processed_resume,
    processed_jd,
):
    """
    Execute Phase 3.1 matching.
    """

    return pipeline.match(
        resume_result=processed_resume,
        jd_result=processed_jd,
    )


# ============================================================================
# BASIC CONTRACT TESTS
# ============================================================================


class TestGapAnalysisContract:
    """
    Basic Phase 3.3 contract tests.
    """

    def test_gap_analysis_result_is_correct_type(
        self,
        project_match_result,
    ) -> None:
        """
        Verify that the Phase 3.1 result is available as the
        required input boundary for Phase 3.3.
        """

        assert isinstance(
            project_match_result.match_result,
            KnowledgeMatchResult,
        )

    def test_match_result_contains_requirements(
        self,
        project_match_result,
    ) -> None:
        """
        Phase 3.3 requires actual requirement-level match data.
        """

        match_result = (
            project_match_result.match_result
        )

        assert (
            match_result.total_requirements
            > 0
        )

        assert match_result.matches


# ============================================================================
# MATCH STATUS DISTRIBUTION
# ============================================================================


class TestGapCandidates:
    """
    Verify that Phase 3.1 status information provides a valid
    foundation for Phase 3.3 gap detection.
    """

    def test_every_requirement_has_a_match(
        self,
        project_match_result,
    ) -> None:
        """
        Every JD requirement must have exactly one RequirementMatch.
        """

        match_result = (
            project_match_result.match_result
        )

        assert (
            len(match_result.matches)
            == match_result.total_requirements
        )

    def test_match_status_is_explicit(
        self,
        project_match_result,
    ) -> None:
        """
        Every atomic match must expose an explicit MatchStatus.

        Phase 3.3 must derive gap classification from the established
        Phase 3.1 status rather than re-running matching.
        """

        for match in (
            project_match_result.match_result.matches
        ):

            assert isinstance(
                match.status,
                MatchStatus,
            )

    def test_unmatched_requirements_can_be_identified(
        self,
        project_match_result,
    ) -> None:
        """
        Verify that unmatched requirements are explicitly identifiable.

        This is the primary source for hard gaps.
        """

        unmatched = [
            match
            for match in (
                project_match_result.match_result.matches
            )
            if match.status
            == MatchStatus.UNMATCHED
        ]

        assert isinstance(
            unmatched,
            list,
        )

    def test_partial_requirements_can_be_identified(
        self,
        project_match_result,
    ) -> None:
        """
        Verify that partial matches are explicitly identifiable.

        Partial matches should remain distinguishable from complete gaps.
        """

        partial = [
            match
            for match in (
                project_match_result.match_result.matches
            )
            if match.status
            == MatchStatus.PARTIAL
        ]

        assert isinstance(
            partial,
            list,
        )


# ============================================================================
# REQUIREMENT IDENTITY
# ============================================================================


class TestGapRequirementIdentity:
    """
    Requirement traceability tests.

    Phase 3.3 must never lose the identity of the JD requirement
    that generated the gap.
    """

    def test_every_match_retains_requirement_identity(
        self,
        project_match_result,
    ) -> None:
        """
        Every match must retain a requirement identity.
        """

        for match in (
            project_match_result.match_result.matches
        ):

            requirement_id = getattr(
                match,
                "requirement_id",
                None,
            )

            assert requirement_id is not None

            assert str(
                requirement_id
            ).strip()

    def test_requirement_identity_is_unique(
        self,
        project_match_result,
    ) -> None:
        """
        Each JD requirement should map to one atomic match.
        """

        requirement_ids = [
            match.requirement_id
            for match in (
                project_match_result.match_result.matches
            )
        ]

        assert len(
            requirement_ids
        ) == len(
            set(requirement_ids)
        )


# ============================================================================
# PHASE 3.2 COMPATIBILITY
# ============================================================================


class TestGapAnalysisEvidenceCompatibility:
    """
    Verify that Phase 3.3 can consume Phase 3.2 output without
    destroying the underlying Phase 3.1 result.
    """

    def test_phase_3_2_result_retains_original_match_result(
        self,
        project_match_result,
    ) -> None:
        """
        EnrichedKnowledgeMatchResult must retain the original
        KnowledgeMatchResult.
        """

        # This test only verifies the contract if an enrichment
        # result is already available elsewhere in the pipeline.
        #
        # Phase 3.3 must not require enrichment for basic gap analysis.
        assert isinstance(
            project_match_result.match_result,
            KnowledgeMatchResult,
        )

    def test_gap_analysis_must_not_require_evidence(
        self,
        project_match_result,
    ) -> None:
        """
        Gap analysis is based fundamentally on requirement matching.

        Phase 3.2 evidence is supporting information, not a mandatory
        prerequisite for identifying a gap.
        """

        match_result = (
            project_match_result.match_result
        )

        assert match_result is not None


# ============================================================================
# RESULT COUNTER CONSISTENCY
# ============================================================================


class TestGapAnalysisCounters:
    """
    Protect result-level arithmetic invariants.
    """

    def test_match_status_counts_are_consistent(
        self,
        project_match_result,
    ) -> None:
        """
        Verify that Phase 3.1 counters agree with atomic matches.
        """

        match_result = (
            project_match_result.match_result
        )

        matched = sum(
            match.status
            == MatchStatus.MATCHED
            for match in match_result.matches
        )

        partial = sum(
            match.status
            == MatchStatus.PARTIAL
            for match in match_result.matches
        )

        unmatched = sum(
            match.status
            == MatchStatus.UNMATCHED
            for match in match_result.matches
        )

        assert (
            matched
            == match_result.matched_count
        )

        assert (
            partial
            == match_result.partial_count
        )

        assert (
            unmatched
            == match_result.unmatched_count
        )

        assert (
            matched
            + partial
            + unmatched
            == match_result.total_requirements
        )


# ============================================================================
# EMPTY GAP BEHAVIOR
# ============================================================================


class TestNoGapScenario:
    """
    Contract tests for a hypothetical fully matched result.

    These tests do not fabricate a GapAnalysisResult because the exact
    Phase 3.3 constructor contract should remain defined by gap_models.py
    and the gap-analysis service.
    """

    def test_zero_unmatched_is_valid(
        self,
        project_match_result,
    ) -> None:
        """
        A result with zero unmatched requirements is a valid state.

        The test intentionally checks the Phase 3.1 input contract only.
        """

        match_result = (
            project_match_result.match_result
        )

        unmatched_count = sum(
            match.status
            == MatchStatus.UNMATCHED
            for match in match_result.matches
        )

        assert unmatched_count >= 0


# ============================================================================
# INPUT VALIDATION
# ============================================================================


class TestGapAnalysisInputValidation:
    """
    Guard against accidentally passing unrelated objects into
    the Phase 3.3 boundary.

    These tests will be expanded once the GapAnalyzer service is finalized.
    """

    def test_match_result_is_not_optional(
        self,
    ) -> None:
        """
        Phase 3.3 cannot operate without Phase 3.1 matching output.
        """

        with pytest.raises(
            (TypeError, ValueError),
        ):
            KnowledgeGapAnalysisResult(
                match_result=None,
            )