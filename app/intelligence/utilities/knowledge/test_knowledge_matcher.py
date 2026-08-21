"""
Knowledge Matcher + Project Pipeline Integration Tests
=======================================================

Phase 3.1

These tests verify two boundaries independently:

1. KnowledgeMatcher unit boundary

    KnowledgeMatchRequest
            ↓
    KnowledgeMatcher
            ↓
    KnowledgeMatchResult

2. ProjectPipeline integration boundary

    RESUME
        ↓
    ProjectPipeline.process()
        ↓
    ProjectPipelineResult

    JD
        ↓
    ProjectPipeline.process()
        ↓
    ProjectPipelineResult

    ProjectPipelineResult[RESUME]
                +
    ProjectPipelineResult[JD]
                ↓
        ProjectPipeline.match()
                ↓
        ProjectMatchResult

Important
---------
The project pipeline does NOT attach a KnowledgeMatchResult directly to
ProjectPipelineResult.

Matching is intentionally a separate pipeline operation:

    process()
        =
    document processing

    match()
        =
    resume + JD matching
"""

from dataclasses import dataclass

import pytest

from app.intelligence.utilities.knowledge.documents.document_input import (
    DocumentInput,
)

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.jd_requirements.requirement_models import (
    JDRequirement,
    JDRequirementProfile,
    RequirementPriority,
    RequirementType,
)

from app.intelligence.utilities.knowledge.matching.knowledge_matcher import (
    KnowledgeMatcher,
)

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchRequest,
    KnowledgeMatchResult,
    MatchBasis,
    MatchStatus,
)

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline import (
    ProjectPipeline,
)

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline_result import (
    ProjectPipelineResult,
    ProjectMatchResult,
)


# ============================================================================
# TEST DOUBLES
# ============================================================================


@dataclass
class FakeKnowledgeEntity:

    entity_id: str

    canonical: str

    normalized: str = ""

    label: str = ""

    entity_type: str = "skill"


@dataclass
class FakeEntityProfile:

    entities: list


@dataclass
class FakeDomainProfile:

    domains: dict

    business_areas: dict


@dataclass
class FakeStatementProfile:

    statements: list


@dataclass
class FakeKnowledgeProfile:

    entities: FakeEntityProfile

    domains: FakeDomainProfile

    business_statements: FakeStatementProfile


# ============================================================================
# SAMPLE DOCUMENTS
# ============================================================================


JD_TEXT = """
Senior Food Safety Manager

We are seeking a Senior Food Safety Manager with strong HACCP knowledge
and experience managing food safety programs.

Required:
- HACCP
- Food safety management
- Quality assurance
- Team leadership

The successful candidate should have experience working in regulated
food production environments.
"""


RESUME_TEXT = """
Food Safety Manager

Experienced food safety professional with extensive HACCP experience.

Skills:
- HACCP
- Food safety management
- Quality assurance
- Team leadership

Managed food safety programs in regulated food production environments.
"""


# ============================================================================
# HELPERS
# ============================================================================


def build_resume_profile(
    *,
    entities=None,
    domains=None,
    statements=None,
):
    """
    Build the existing document wrapper around a minimal profile-shaped
    test object.

    The matcher only consumes the public DocumentKnowledgeProfile boundary.
    """

    profile = FakeKnowledgeProfile(
        entities=FakeEntityProfile(
            entities=entities or []
        ),
        domains=FakeDomainProfile(
            domains=domains or {},
            business_areas={},
        ),
        business_statements=FakeStatementProfile(
            statements=statements or []
        ),
    )

    return profile


def build_requirement(
    *,
    requirement_id="jdreq:skill:skill-haccp",
    entity_id="SKILL_HACCP",
    subject="HACCP",
    requirement_type=RequirementType.SKILL,
    priority=RequirementPriority.REQUIRED,
    domain="food_safety",
):
    return JDRequirement(
        requirement_id=requirement_id,
        requirement_type=requirement_type,
        priority=priority,
        subject=subject,
        entity_id=entity_id,
        domain=domain,
        evidence="HACCP experience required.",
        source_statement="HACCP experience required.",
        confidence=0.9,
        mandatory=(
            priority
            == RequirementPriority.REQUIRED
        ),
        preferred=(
            priority
            == RequirementPriority.PREFERRED
        ),
    )


def build_document_profile(
    monkeypatch,
    *,
    document_type=DocumentType.RESUME,
    entities=None,
    domains=None,
    statements=None,
):
    """
    Build a DocumentKnowledgeProfile for isolated KnowledgeMatcher tests.

    The strict KnowledgeProfile validation is bypassed only here because
    these tests are testing matcher behavior, not KnowledgeProfile
    construction.
    """

    profile = build_resume_profile(
        entities=entities,
        domains=domains,
        statements=statements,
    )

    monkeypatch.setattr(
        DocumentKnowledgeProfile,
        "__post_init__",
        lambda self: None,
    )

    return DocumentKnowledgeProfile(
        document_type=document_type,
        profile=profile,
    )


# ============================================================================
# KNOWLEDGE MATCHER UNIT TESTS
# ============================================================================


class TestKnowledgeMatcher:

    def test_exact_entity_match(
        self,
        monkeypatch,
    ):

        entity = FakeKnowledgeEntity(
            entity_id="SKILL_HACCP",
            canonical="HACCP",
            normalized="haccp",
        )

        requirement = build_requirement()

        jd_profile = JDRequirementProfile.from_requirements(
            [requirement]
        )

        document_profile = build_document_profile(
            monkeypatch,
            entities=[entity],
        )

        request = KnowledgeMatchRequest(
            resume_profile=document_profile,
            jd_requirement_profile=jd_profile,
        )

        result = KnowledgeMatcher().process(
            request
        )

        assert isinstance(
            result,
            KnowledgeMatchResult,
        )

        assert result.total_requirements == 1

        assert result.matched_count == 1

        assert result.partial_count == 0

        assert result.unmatched_count == 0

        match = result.matches[0]

        assert match.status == MatchStatus.MATCHED

        assert match.basis == MatchBasis.ENTITY_ID

        assert match.score == 1.0

        assert match.evidence_count == 1

        assert (
            "HACCP"
            in match.candidate_evidence
        )

    def test_canonical_match(
        self,
        monkeypatch,
    ):

        entity = FakeKnowledgeEntity(
            entity_id="OTHER_ID",
            canonical="HACCP",
            normalized="haccp",
        )

        requirement = build_requirement(
            entity_id="SKILL_HACCP"
        )

        jd_profile = JDRequirementProfile.from_requirements(
            [requirement]
        )

        document_profile = build_document_profile(
            monkeypatch,
            entities=[entity],
        )

        request = KnowledgeMatchRequest(
            resume_profile=document_profile,
            jd_requirement_profile=jd_profile,
        )

        result = KnowledgeMatcher().process(
            request
        )

        match = result.matches[0]

        assert match.status == MatchStatus.MATCHED

        assert match.basis == MatchBasis.CANONICAL

        assert match.score == 0.95

    def test_domain_produces_partial_match(
        self,
        monkeypatch,
    ):

        requirement = build_requirement(
            entity_id="UNKNOWN",
            subject="Quality Assurance",
            domain="food_safety",
        )

        jd_profile = JDRequirementProfile.from_requirements(
            [requirement]
        )

        document_profile = build_document_profile(
            monkeypatch,
            entities=[],
            domains={
                "food_safety": 0.8
            },
        )

        request = KnowledgeMatchRequest(
            resume_profile=document_profile,
            jd_requirement_profile=jd_profile,
        )

        result = KnowledgeMatcher().process(
            request
        )

        match = result.matches[0]

        assert match.status == MatchStatus.PARTIAL

        assert match.basis == MatchBasis.DOMAIN

        assert match.score == 0.65

        assert match.evidence_count == 1

    def test_unmatched_requirement(
        self,
        monkeypatch,
    ):

        requirement = build_requirement(
            entity_id="SKILL_HACCP",
            subject="HACCP",
        )

        jd_profile = JDRequirementProfile.from_requirements(
            [requirement]
        )

        document_profile = build_document_profile(
            monkeypatch,
            entities=[],
            domains={},
        )

        request = KnowledgeMatchRequest(
            resume_profile=document_profile,
            jd_requirement_profile=jd_profile,
        )

        result = KnowledgeMatcher().process(
            request
        )

        match = result.matches[0]

        assert match.status == MatchStatus.UNMATCHED

        assert match.basis == MatchBasis.NONE

        assert match.score == 0.0

        assert match.evidence_count == 0

    def test_match_result_counters_are_derived(
        self,
        monkeypatch,
    ):

        entities = [
            FakeKnowledgeEntity(
                entity_id="SKILL_HACCP",
                canonical="HACCP",
                normalized="haccp",
            ),
        ]

        requirements = [
            build_requirement(
                requirement_id="req:1",
                entity_id="SKILL_HACCP",
                subject="HACCP",
            ),
            build_requirement(
                requirement_id="req:2",
                entity_id="SKILL_UNKNOWN",
                subject="Six Sigma",
                domain="quality",
            ),
        ]

        jd_profile = JDRequirementProfile.from_requirements(
            requirements
        )

        document_profile = build_document_profile(
            monkeypatch,
            entities=entities,
            domains={},
        )

        request = KnowledgeMatchRequest(
            resume_profile=document_profile,
            jd_requirement_profile=jd_profile,
        )

        result = KnowledgeMatcher().process(
            request
        )

        assert result.total_requirements == 2

        assert result.matched_count == 1

        assert result.partial_count == 0

        assert result.unmatched_count == 1

        assert (
            result.overall_score
            == 0.5
        )

    def test_jd_profile_is_rejected_as_resume(
        self,
    ):

        matcher = KnowledgeMatcher()

        requirement = build_requirement()

        jd_profile = JDRequirementProfile.from_requirements(
            [requirement]
        )

        class FakeJDProfile:

            document_type = DocumentType.JD

        request = KnowledgeMatchRequest(
            resume_profile=FakeJDProfile(),
            jd_requirement_profile=jd_profile,
        )

        with pytest.raises(
            TypeError
        ):

            matcher.process(
                request
            )


# ============================================================================
# PROJECT PIPELINE PHASE 3 INTEGRATION TESTS
# ============================================================================


class TestProjectPipelineMatching:

    def test_jd_pipeline_produces_match_result(
        self,
    ) -> None:
        """
        Verify the complete Phase 3 boundary.

        Important:
        process() produces ProjectPipelineResult.

        match() produces ProjectMatchResult.

        Matching is therefore NOT expected to exist directly on the
        single-document ProjectPipelineResult.
        """

        pipeline = ProjectPipeline()

        resume_input = DocumentInput(
            text=RESUME_TEXT,
            document_type=DocumentType.RESUME,
        )

        jd_input = DocumentInput(
            text=JD_TEXT,
            document_type=DocumentType.JD,
        )

        resume_result = pipeline.process(
            resume_input
        )

        jd_result = pipeline.process(
            jd_input
        )

        # --------------------------------------------------------------
        # RESUME PIPELINE CONTRACT
        # --------------------------------------------------------------

        assert isinstance(
            resume_result,
            ProjectPipelineResult,
        )

        assert (
            resume_result.pipeline_response.success
            is True
        )

        assert (
            resume_result.document_profile.is_resume
            is True
        )

        assert (
            resume_result.jd_requirement_profile
            is None
        )

        # --------------------------------------------------------------
        # JD PIPELINE CONTRACT
        # --------------------------------------------------------------

        assert isinstance(
            jd_result,
            ProjectPipelineResult,
        )

        assert (
            jd_result.pipeline_response.success
            is True
        )

        assert (
            jd_result.document_profile.is_jd
            is True
        )

        assert (
            jd_result.jd_requirement_profile
            is not None
        )

        assert (
            jd_result.jd_requirement_profile.requirements
        ), (
            "JD produced zero requirements."
        )

        # --------------------------------------------------------------
        # PHASE 3 MATCHING
        # --------------------------------------------------------------

        project_match = pipeline.match(
            resume_result=resume_result,
            jd_result=jd_result,
        )

        assert isinstance(
            project_match,
            ProjectMatchResult,
        )

        assert isinstance(
            project_match.match_result,
            KnowledgeMatchResult,
        )

        assert (
            project_match.match_result.total_requirements
            == len(
                jd_result.jd_requirement_profile.requirements
            )
        )

    def test_jd_matching_result_is_derived_from_requirements(
        self,
    ) -> None:
        """
        Verify the Phase 3.1 invariant:

            one JDRequirement
                ->
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

        project_match = pipeline.match(
            resume_result,
            jd_result,
        )

        requirement_profile = (
            jd_result.jd_requirement_profile
        )

        match_result = (
            project_match.match_result
        )

        assert requirement_profile is not None

        assert (
            len(match_result.matches)
            == len(
                requirement_profile.requirements
            )
        )

        requirement_ids = {
            requirement.requirement_id
            for requirement
            in requirement_profile.requirements
        }

        match_requirement_ids = {
            match.requirement_id
            for match
            in match_result.matches
        }

        assert (
            match_requirement_ids
            == requirement_ids
        )

    def test_resume_only_pipeline_does_not_create_jd_matching(
        self,
    ) -> None:
        """
        Resume-only processing must not create JD interpretation
        or matching output.
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
            result.document_profile.is_resume
            is True
        )

        assert (
            result.document_profile.is_jd
            is False
        )

        assert (
            result.jd_requirement_profile
            is None
        )

        # Matching does not exist on a single-document result.
        assert not hasattr(
            result,
            "knowledge_match_result",
        )

    def test_match_result_counters_are_consistent(
        self,
    ) -> None:
        """
        Verify that the ProjectPipeline exposes the exact
        KnowledgeMatchResult produced by KnowledgeMatcher.
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

        project_match = pipeline.match(
            resume_result,
            jd_result,
        )

        match_result = (
            project_match.match_result
        )

        assert (
            match_result.total_requirements
            == (
                match_result.matched_count
                + match_result.partial_count
                + match_result.unmatched_count
            )
        )

        assert (
            match_result.total_requirements
            == len(
                match_result.matches
            )
        )

        assert (
            0.0
            <= match_result.overall_score
            <= 1.0
        )

        assert (
            0.0
            <= match_result.confidence
            <= 1.0
        )

    def test_every_match_has_requirement_identity(
        self,
    ) -> None:
        """
        Every atomic match must retain enough requirement identity
        to trace it back to Phase 2.
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

        project_match = pipeline.match(
            resume_result,
            jd_result,
        )

        match_result = (
            project_match.match_result
        )

        assert match_result.matches

        for match in match_result.matches:

            assert (
                match.requirement_id
            )

            assert (
                match.requirement_subject
            )

            assert (
                match.requirement_type
            )

            assert (
                match.priority
            )

            assert isinstance(
                match.status,
                MatchStatus,
            )

            assert isinstance(
                match.basis,
                MatchBasis,
            )

            assert (
                0.0
                <= match.score
                <= 1.0
            )


# ============================================================================
# PROJECT PIPELINE VALIDATION TESTS
# ============================================================================


class TestProjectPipelineValidation:

    def test_match_rejects_non_pipeline_resume(
        self,
    ) -> None:

        pipeline = ProjectPipeline()

        jd_result = pipeline.process(
            DocumentInput(
                text=JD_TEXT,
                document_type=DocumentType.JD,
            )
        )

        with pytest.raises(
            TypeError
        ):

            pipeline.match(
                resume_result="not-a-pipeline-result",
                jd_result=jd_result,
            )

    def test_match_rejects_jd_as_resume(
        self,
    ) -> None:

        pipeline = ProjectPipeline()

        jd_result = pipeline.process(
            DocumentInput(
                text=JD_TEXT,
                document_type=DocumentType.JD,
            )
        )

        with pytest.raises(
            TypeError
        ):

            pipeline.match(
                resume_result=jd_result,
                jd_result=jd_result,
            )

    def test_match_rejects_resume_as_jd(
        self,
    ) -> None:

        pipeline = ProjectPipeline()

        resume_result = pipeline.process(
            DocumentInput(
                text=RESUME_TEXT,
                document_type=DocumentType.RESUME,
            )
        )

        with pytest.raises(
            TypeError
        ):

            pipeline.match(
                resume_result=resume_result,
                jd_result=resume_result,
            )

    def test_match_requires_jd_requirement_profile(
        self,
    ) -> None:
        """
        Protect the Phase 2 -> Phase 3 boundary.

        A JD must have a JDRequirementProfile before matching can start.
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

        # Create a deliberately invalid boundary object by replacing
        # the JD requirement profile with None.

        invalid_jd_result = ProjectPipelineResult(
            document_input=jd_result.document_input,
            routed_document=jd_result.routed_document,
            pipeline_request=jd_result.pipeline_request,
            pipeline_response=jd_result.pipeline_response,
            document_profile=jd_result.document_profile,
            jd_requirement_profile=None,
        )

        with pytest.raises(
            ValueError
        ):

            pipeline.match(
                resume_result=resume_result,
                jd_result=invalid_jd_result,
            )