"""
Shared Knowledge Pipeline pytest fixtures
=========================================

Object-in / object-out test graph.

Phase 3.1
    KnowledgeMatchResult

        ↓

Phase 3.2
    EnrichedKnowledgeMatchResult

        ↓

Phase 3.3
    KnowledgeGapAnalysisResult

        ↓

Phase 4
    KnowledgeMatchProfile

        ↓

Phase 5
    ATSResumeAnalysisRequest

        ↓

Phase 5
    ATSResumeAnalysisResult


IMPORTANT
---------
These fixtures intentionally preserve object identity.

No phase is converted into a dictionary.

The same object produced by one phase is passed into the next phase.
"""

from __future__ import annotations

import pytest

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSResumeAnalysisResult,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_policy import (
    ATSAnalysisPolicy,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_request import (
    ATSResumeAnalysisRequest,
)

from app.intelligence.utilities.knowledge.ats.ats_resume_analyzer import (
    ATSResumeAnalyzer,
)

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.jd_requirements.requirement_models import (
    JDRequirementProfile,
)

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
)

from app.intelligence.utilities.knowledge.matching.gap_analyzer import (
    KnowledgeGapAnalyzer,
)

from app.intelligence.utilities.knowledge.matching.gap_models import (
    KnowledgeGapAnalysisResult,
)

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_builder import (
    KnowledgeMatchProfileBuilder,
)

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeMatchProfile,
)

from app.intelligence.utilities.knowledge.matching.match_enricher import (
    KnowledgeMatchEnricher,
)

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchResult,
    MatchBasis,
    MatchStatus,
    RequirementMatch,
)


# ============================================================================
# TEST INPUT
# ============================================================================


RESUME_TEXT = """
John Smith

Professional Summary

Senior Software Engineer with experience building scalable Python
applications and enterprise systems.

Experience

Senior Software Engineer
ABC Technologies

- Led a team of 8 engineers.
- Improved API performance by 35%.
- Built Python and FastAPI services.
- Designed PostgreSQL data models.
- Managed CI/CD pipelines.
- Mentored junior engineers.

Skills

Python
FastAPI
PostgreSQL
Docker
AWS
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
experience building scalable backend systems.

Requirements

Python
FastAPI
PostgreSQL
Docker
AWS
CI/CD
Git
Pytest
Automation
Backend Development
Kubernetes
"""


# ============================================================================
# PHASE 1/2 DOCUMENT PROFILE OBJECTS
# ============================================================================


@pytest.fixture
def resume_profile() -> DocumentKnowledgeProfile:
    """
    Real DocumentKnowledgeProfile object for the resume side.

    The document profile is intentionally an object.

    No text dictionary is passed into the model.
    """

    # Import lazily to avoid imposing another dependency on every test module.
    from app.intelligence.utilities.knowledge.knowledge_profile import (
        KnowledgeProfile,
    )

    profile = KnowledgeProfile()

    return DocumentKnowledgeProfile(
        document_type=DocumentType.RESUME,
        profile=profile,
    )


@pytest.fixture
def jd_document_profile() -> DocumentKnowledgeProfile:
    """
    Real DocumentKnowledgeProfile object for the JD side.
    """

    from app.intelligence.utilities.knowledge.knowledge_profile import (
        KnowledgeProfile,
    )

    profile = KnowledgeProfile()

    return DocumentKnowledgeProfile(
        document_type=DocumentType.JD,
        profile=profile,
    )


@pytest.fixture
def jd_requirement_profile() -> JDRequirementProfile:
    """
    JD requirement object.

    Phase 3 matching tests supply the authoritative RequirementMatch
    objects explicitly, so this fixture does not fabricate requirements
    from dictionaries.
    """

    return JDRequirementProfile.from_requirements(
        []
    )


# ============================================================================
# PHASE 3.1
# ============================================================================


@pytest.fixture
def match_result() -> KnowledgeMatchResult:
    """
    Real Phase 3.1 KnowledgeMatchResult.
    """

    matches = (
        RequirementMatch(
            requirement_id="req-python",
            requirement_subject="Python",
            requirement_type="skill",
            priority="high",
            status=MatchStatus.MATCHED,
            score=0.95,
            basis=MatchBasis.CANONICAL,
            candidate_entity_ids=(),
            candidate_evidence=(),
            evidence_count=0,
        ),
        RequirementMatch(
            requirement_id="req-fastapi",
            requirement_subject="FastAPI",
            requirement_type="skill",
            priority="high",
            status=MatchStatus.PARTIAL,
            score=0.60,
            basis=MatchBasis.CANONICAL,
            candidate_entity_ids=(),
            candidate_evidence=(),
            evidence_count=0,
        ),
        RequirementMatch(
            requirement_id="req-kubernetes",
            requirement_subject="Kubernetes",
            requirement_type="skill",
            priority="medium",
            status=MatchStatus.UNMATCHED,
            score=0.0,
            basis=MatchBasis.NONE,
            candidate_entity_ids=(),
            candidate_evidence=(),
            evidence_count=0,
        ),
    )

    result = KnowledgeMatchResult.from_matches(
        matches
    )

    assert isinstance(
        result,
        KnowledgeMatchResult,
    )

    return result


# ============================================================================
# PHASE 3.2
# ============================================================================


@pytest.fixture
def enriched_match_result(
    match_result: KnowledgeMatchResult,
    resume_profile: DocumentKnowledgeProfile,
    jd_requirement_profile: JDRequirementProfile,
) -> EnrichedKnowledgeMatchResult:
    """
    Real Phase 3.2 enrichment result.
    """

    result = KnowledgeMatchEnricher().process(
        match_result=match_result,
        resume_profile=resume_profile,
        jd_requirement_profile=jd_requirement_profile,
    )

    assert isinstance(
        result,
        EnrichedKnowledgeMatchResult,
    )

    # Phase 3.2 must preserve Phase 3.1 identity.
    assert (
        result.match_result
        is match_result
    )

    return result


# ============================================================================
# PHASE 3.3
# ============================================================================


@pytest.fixture
def gap_analysis_result(
    enriched_match_result: EnrichedKnowledgeMatchResult,
) -> KnowledgeGapAnalysisResult:
    """
    Real Phase 3.3 gap analysis result.
    """

    result = KnowledgeGapAnalyzer().process(
        enriched_match_result
    )

    assert isinstance(
        result,
        KnowledgeGapAnalysisResult,
    )

    # Phase 3.3 must preserve Phase 3.2 identity.
    assert (
        result.enriched_match_result
        is enriched_match_result
    )

    return result


# ============================================================================
# PHASE 4
# ============================================================================


@pytest.fixture
def knowledge_match_profile(
    match_result: KnowledgeMatchResult,
    enriched_match_result: EnrichedKnowledgeMatchResult,
    gap_analysis_result: KnowledgeGapAnalysisResult,
) -> KnowledgeMatchProfile:
    """
    Real Phase 4 KnowledgeMatchProfile.

    This is the canonical object passed into Phase 5.
    """

    profile = KnowledgeMatchProfileBuilder().process(
        match_result=match_result,
        enriched_match_result=enriched_match_result,
        gap_analysis_result=gap_analysis_result,
    )

    assert isinstance(
        profile,
        KnowledgeMatchProfile,
    )

    # ------------------------------------------------------------------
    # PHASE 4 SOURCE IDENTITY
    # ------------------------------------------------------------------

    assert (
        profile.match_result
        is match_result
    )

    assert (
        profile.enriched_match_result
        is enriched_match_result
    )

    assert (
        profile.gap_analysis_result
        is gap_analysis_result
    )

    return profile


# ============================================================================
# PHASE 5 POLICY
# ============================================================================


@pytest.fixture
def ats_policy() -> ATSAnalysisPolicy:
    """
    Shared Phase 5 policy object.
    """

    return ATSAnalysisPolicy()


# ============================================================================
# PHASE 5 REQUEST
# ============================================================================


@pytest.fixture
def ats_request(
    knowledge_match_profile: KnowledgeMatchProfile,
    ats_policy: ATSAnalysisPolicy,
) -> ATSResumeAnalysisRequest:
    """
    Real Phase 5 input object.

    KnowledgeMatchProfile is passed directly.

    No dictionary conversion occurs.
    """

    request = ATSResumeAnalysisRequest(
        resume_text=RESUME_TEXT,
        knowledge_match_profile=knowledge_match_profile,
        policy=ats_policy,
    )

    assert isinstance(
        request,
        ATSResumeAnalysisRequest,
    )

    assert (
        request.knowledge_match_profile
        is knowledge_match_profile
    )

    assert request.has_resume_source
    assert request.has_phase4_profile

    return request


# ============================================================================
# PHASE 5 RESULT
# ============================================================================


@pytest.fixture
def ats_result(
    ats_request: ATSResumeAnalysisRequest,
    knowledge_match_profile: KnowledgeMatchProfile,
    ats_policy: ATSAnalysisPolicy,
) -> ATSResumeAnalysisResult:
    """
    Real Phase 5 output object.

    This is the object Phase 6 must consume directly.
    """

    analyzer = ATSResumeAnalyzer(
        policy=ats_policy,
    )

    result = analyzer.process(
        ats_request
    )

    assert isinstance(
        result,
        ATSResumeAnalysisResult,
    )

    # ------------------------------------------------------------------
    # PHASE 5 SOURCE IDENTITY
    # ------------------------------------------------------------------

    assert (
        result.request
        is ats_request
    )

    assert (
        result.knowledge_match_profile
        is knowledge_match_profile
    )

    assert (
        result.request.knowledge_match_profile
        is knowledge_match_profile
    )

    # ------------------------------------------------------------------
    # TYPED ATS COMPONENTS
    # ------------------------------------------------------------------

    assert result.keyword_analysis is not None
    assert result.section_analysis is not None
    assert result.formatting_analysis is not None
    assert result.readability_analysis is not None
    assert result.terminology_analysis is not None
    assert result.quantification_analysis is not None
    assert result.parseability_analysis is not None

    # ------------------------------------------------------------------
    # SCORE CONTRACT
    # ------------------------------------------------------------------

    assert 0.0 <= result.ats_score.score <= 1.0
    assert 0.0 <= result.ats_score.confidence <= 1.0
    assert 0.0 <= result.confidence <= 1.0

    return result


# ============================================================================
# PHASE 5 REQUEST BUILDER HELPER
# ============================================================================


@pytest.fixture
def build_ats_request():
    """
    Factory fixture for creating additional valid Phase 5 request objects.
    """

    def _build(
        *,
        profile: KnowledgeMatchProfile,
        policy: ATSAnalysisPolicy,
        resume_text: str = RESUME_TEXT,
    ) -> ATSResumeAnalysisRequest:

        return ATSResumeAnalysisRequest(
            resume_text=resume_text,
            knowledge_match_profile=profile,
            policy=policy,
        )

    return _build

