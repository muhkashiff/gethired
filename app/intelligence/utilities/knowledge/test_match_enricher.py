"""
Project Pipeline Tests
======================

Integration tests for the complete ProjectPipeline orchestration boundary.

Current pipeline:

    DocumentInput
        ↓
    DocumentProcessingService
        ↓
    DocumentKnowledgeProfile
        ↓
    JDRequirementProfile [JD only]
        ↓
    KnowledgeMatchResult [match()]
        ↓
    EnrichedKnowledgeMatchResult [match()]

These tests verify orchestration contracts.

They intentionally do NOT test individual extraction or matching
heuristics in detail. Those responsibilities belong to their own
unit/integration test modules.
"""

from __future__ import annotations


# ============================================================================
# IMPORTS
# ============================================================================

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
    ProjectPipelineResult,
    ProjectMatchResult,
)

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchResult,
)

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
)


# ============================================================================
# TEST DATA
# ============================================================================


RESUME_TEXT = """
Senior Software Engineer with 8 years of experience building scalable
backend systems.

Led engineering teams and managed software development projects.

Designed and implemented Python applications using Django and FastAPI.

Built REST APIs, PostgreSQL databases, Redis caching systems, and
Docker-based deployments.

Worked with AWS cloud infrastructure and CI/CD pipelines.

Experience with system architecture, distributed systems, testing,
code reviews, mentoring, and technical leadership.
"""


JD_TEXT = """
Senior Software Engineer

We are looking for a Senior Software Engineer to join our engineering
team.

Requirements:

- 5+ years of software engineering experience.
- Strong Python experience.
- Experience with Django or FastAPI.
- Experience building REST APIs.
- Experience with PostgreSQL.
- Experience with Docker and AWS.
- Experience designing scalable backend systems.
- Experience leading engineering projects and mentoring engineers.
"""


# ============================================================================
# TEST CLASS
# ============================================================================


class TestProjectPipeline:
    """
    Integration tests for the complete ProjectPipeline.

    Pipeline responsibilities verified here:

        Phase 1
            DocumentInput
                →
            DocumentKnowledgeProfile

        Phase 2
            JD
                →
            JDRequirementProfile

        Phase 3.1
            Resume + JD
                →
            KnowledgeMatchResult

        Phase 3.2
            KnowledgeMatchResult
                +
            Resume profile
                +
            JD requirements
                →
            EnrichedKnowledgeMatchResult
    """

    # ========================================================================
    # PHASE 1
    # ========================================================================

    def test_resume_process_produces_project_pipeline_result(
        self,
    ) -> None:
        """
        Verify that a resume can pass through the document pipeline.
        """

        pipeline = ProjectPipeline()

        document_input = DocumentInput(
            text=RESUME_TEXT,
            document_type=DocumentType.RESUME,
        )

        result = pipeline.process(
            document_input
        )

        assert isinstance(
            result,
            ProjectPipelineResult,
        )

        assert (
            result.pipeline_response.success
            is True
        )

        assert (
            result.document_profile
            is not None
        )

        assert (
            result.document_profile.is_resume
            is True
        )

        assert (
            result.document_profile.is_jd
            is False
        )

        # Resume processing must not create JD requirements.

        assert (
            result.jd_requirement_profile
            is None
        )

    # ========================================================================
    # PHASE 2
    # ========================================================================

    def test_jd_process_produces_requirement_profile(
        self,
    ) -> None:
        """
        Verify that JD processing automatically performs Phase 2.
        """

        pipeline = ProjectPipeline()

        document_input = DocumentInput(
            text=JD_TEXT,
            document_type=DocumentType.JD,
        )

        result = pipeline.process(
            document_input
        )

        assert isinstance(
            result,
            ProjectPipelineResult,
        )

        assert (
            result.pipeline_response.success
            is True
        )

        assert (
            result.document_profile.is_jd
            is True
        )

        assert (
            result.document_profile.is_resume
            is False
        )

        assert (
            result.jd_requirement_profile
            is not None
        )

        assert (
            result.jd_requirement_profile.requirements
        ), (
            "JD produced zero requirements."
        )

    # ========================================================================
    # PHASE 3.1 + 3.2
    # ========================================================================

    def test_match_produces_complete_phase_3_result(
        self,
    ) -> None:
        """
        Verify the complete matching pipeline.

        Expected:

            Resume
                +
            JD
                ↓
            KnowledgeMatchResult
                ↓
            EnrichedKnowledgeMatchResult
                ↓
            ProjectMatchResult
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

        result = pipeline.match(
            resume_result=resume_result,
            jd_result=jd_result,
        )

        assert isinstance(
            result,
            ProjectMatchResult,
        )

        # ----------------------------------------------------------------
        # PHASE 3.1
        # ----------------------------------------------------------------

        assert isinstance(
            result.match_result,
            KnowledgeMatchResult,
        )

        assert (
            result.match_result.total_requirements
            == len(
                jd_result.jd_requirement_profile.requirements
            )
        )

        # ----------------------------------------------------------------
        # PHASE 3.2
        # ----------------------------------------------------------------

        assert (
            result.enriched_match_result
            is not None
        )

        assert isinstance(
            result.enriched_match_result,
            EnrichedKnowledgeMatchResult,
        )

        assert (
            result.enriched_match_result.match_result
            is result.match_result
        )

    # ========================================================================
    # PHASE 3.1 REQUIREMENT INVARIANT
    # ========================================================================

    def test_every_requirement_receives_one_match(
        self,
    ) -> None:
        """
        Verify the Phase 3.1 invariant:

            one JD requirement
                →
            one RequirementMatch
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

        result = pipeline.match(
            resume_result,
            jd_result,
        )

        requirements = (
            jd_result
            .jd_requirement_profile
            .requirements
        )

        matches = (
            result
            .match_result
            .matches
        )

        assert len(matches) == len(
            requirements
        )

        assert (
            result.match_result.total_requirements
            == len(requirements)
        )

    # ========================================================================
    # PHASE 3.2 MATCH COUNT INVARIANT
    # ========================================================================

    def test_enriched_match_count_matches_atomic_match_count(
        self,
    ) -> None:
        """
        Phase 3.2 must enrich every Phase 3.1 match.

        It must not create or remove requirements.
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

        result = pipeline.match(
            resume_result,
            jd_result,
        )

        atomic_matches = (
            result.match_result.matches
        )

        enriched_matches = (
            result
            .enriched_match_result
            .matches
        )

        assert len(
            enriched_matches
        ) == len(
            atomic_matches
        )

        assert (
            result
            .enriched_match_result
            .total_requirements
            == result
            .match_result
            .total_requirements
        )

    # ========================================================================
    # PHASE 3.2 EVIDENCE CONTRACT
    # ========================================================================

    def test_enriched_matches_retain_original_match(
        self,
    ) -> None:
        """
        Verify that enrichment does not replace the original
        RequirementMatch.

        Every enriched match must retain its Phase 3.1 match object.
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

        result = pipeline.match(
            resume_result,
            jd_result,
        )

        atomic_matches = (
            result.match_result.matches
        )

        enriched_matches = (
            result
            .enriched_match_result
            .matches
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

    # ========================================================================
    # RESUME-ONLY CONTRACT
    # ========================================================================

    def test_resume_only_does_not_create_jd_or_match_result(
        self,
    ) -> None:
        """
        A resume by itself must not create JD interpretation or matching.

        Matching requires an explicit JD result.
        """

        pipeline = ProjectPipeline()

        result = pipeline.process(
            DocumentInput(
                text=RESUME_TEXT,
                document_type=DocumentType.RESUME,
            )
        )

        assert isinstance(
            result,
            ProjectPipelineResult,
        )

        assert (
            result.is_resume
            is True
        )

        assert (
            result.is_jd
            is False
        )

        assert (
            result.jd_requirement_profile
            is None
        )

        # The document result itself does not contain a match result.

        assert not hasattr(
            result,
            "knowledge_match_result",
        )

    # ========================================================================
    # INVALID RESUME INPUT
    # ========================================================================

    def test_match_rejects_jd_as_resume(
        self,
    ) -> None:
        """
        match() must reject a JD supplied as resume_result.
        """

        pipeline = ProjectPipeline()

        jd_result = pipeline.process(
            DocumentInput(
                text=JD_TEXT,
                document_type=DocumentType.JD,
            )
        )

        resume_result = pipeline.process(
            DocumentInput(
                text=RESUME_TEXT,
                document_type=DocumentType.RESUME,
            )
        )

        try:

            pipeline.match(
                resume_result=jd_result,
                jd_result=resume_result,
            )

        except TypeError as exc:

            assert (
                "resume_result"
                in str(exc)
            )

        else:

            raise AssertionError(
                "ProjectPipeline.match() "
                "accepted a JD as resume_result."
            )

    # ========================================================================
    # INVALID JD INPUT
    # ========================================================================

    def test_match_rejects_resume_as_jd(
        self,
    ) -> None:
        """
        match() must reject a resume supplied as jd_result.
        """

        pipeline = ProjectPipeline()

        resume_result = pipeline.process(
            DocumentInput(
                text=RESUME_TEXT,
                document_type=DocumentType.RESUME,
            )
        )

        try:

            pipeline.match(
                resume_result=resume_result,
                jd_result=resume_result,
            )

        except TypeError as exc:

            assert (
                "jd_result"
                in str(exc)
            )

        else:

            raise AssertionError(
                "ProjectPipeline.match() "
                "accepted a resume as jd_result."
            )

    # ========================================================================
    # RESULT SOURCE VISIBILITY
    # ========================================================================

    def test_project_match_result_retains_source_results(
        self,
    ) -> None:
        """
        ProjectMatchResult must retain both processed source results.
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

        result = pipeline.match(
            resume_result,
            jd_result,
        )

        assert (
            result.resume_result
            is resume_result
        )

        assert (
            result.jd_result
            is jd_result
        )

    # ========================================================================
    # COUNTER CONSISTENCY
    # ========================================================================

    def test_match_result_counters_are_consistent(
        self,
    ) -> None:
        """
        Verify that the project-level result exposes the same counters
        as KnowledgeMatchResult.
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

        result = pipeline.match(
            resume_result,
            jd_result,
        )

        match_result = (
            result.match_result
        )

        assert (
            result.total_requirements
            == match_result.total_requirements
        )

        assert (
            result.matched_count
            == match_result.matched_count
        )

        assert (
            result.partial_count
            == match_result.partial_count
        )

        assert (
            result.unmatched_count
            == match_result.unmatched_count
        )

        assert (
            result.overall_score
            == match_result.overall_score
        )

        assert (
            result.confidence
            == match_result.confidence
        )

    # ========================================================================
    # ENRICHMENT EVIDENCE
    # ========================================================================

    def test_enrichment_produces_traceable_evidence_when_available(
        self,
    ) -> None:
        """
        Verify the Phase 3.2 evidence boundary.

        Evidence may legitimately be empty for an individual match,
        depending on the matcher basis and available profile data.

        The important contract is that all evidence objects are structured
        MatchEvidence objects and enrichment does not alter the atomic match.
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

        result = pipeline.match(
            resume_result,
            jd_result,
        )

        enriched_result = (
            result.enriched_match_result
        )

        for enriched_match in (
            enriched_result.matches
        ):

            assert (
                enriched_match.match
                in result.match_result.matches
            )

            assert (
                enriched_match.evidence_count
                == len(
                    enriched_match.evidence
                )
            )

            for evidence in (
                enriched_match.evidence
            ):

                assert evidence.source
                assert evidence.evidence
                assert evidence.basis
                assert (
                    0.0
                    <= evidence.confidence
                    <= 1.0
                )