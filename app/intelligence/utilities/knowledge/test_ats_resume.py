"""
ATS Resume Analyzer Tests
=========================

Phase 5 - ATS Resume Analysis

Architecture
------------

    DocumentKnowledgeProfile
             +
    JDRequirementProfile
             +
    KnowledgeMatchProfile
             |
             v
    ATSResumeAnalysisRequest
             |
             v
    ATSResumeAnalyzer
             |
             v
    ATSResumeAnalysisResult

The tests intentionally preserve the real Phase 3 -> Phase 4
identity chain.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest


# ============================================================================
# PHASE 5
# ============================================================================

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSKeywordAnalysis,
    ATSScore,
    ATSScoreBreakdown,
    ATSSectionAnalysis,
    ATSFormattingAnalysis,
    ATSReadabilityAnalysis,
    ATSTerminologyAnalysis,
    ATSQuantificationAnalysis,
    ATSParseabilityAnalysis,
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


# ============================================================================
# DOCUMENT MODELS
# ============================================================================

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile import (
    KnowledgeProfile,
)


# ============================================================================
# JD MODELS
# ============================================================================

from app.intelligence.utilities.knowledge.jd_requirements.requirement_models import (
    JDRequirementProfile,
)


# ============================================================================
# MATCHING MODELS
# ============================================================================

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchResult,
    MatchBasis,
    MatchStatus,
    RequirementMatch,
)

from app.intelligence.utilities.knowledge.matching.match_enricher import (
    KnowledgeMatchEnricher,
)

from app.intelligence.utilities.knowledge.matching.gap_analyzer import (
    KnowledgeGapAnalyzer,
)

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_builder import (
    KnowledgeMatchProfileBuilder,
)

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeMatchProfile,
)


# ============================================================================
# TEST SOURCE OBJECTS
# ============================================================================


@dataclass
class FakeKnowledgeDocument:
    """
    Minimal source document compatible with the real Phase 5 source lookup.

    This is NOT a fake KnowledgeMatchProfile.

    It represents the existing KnowledgeDocument source contract used by
    DocumentKnowledgeProfile.source_result.
    """

    raw_text: str

    facts: list[Any]


@dataclass
class FakePipelineResult:
    """
    Minimal pipeline result wrapper.

    The real project exposes knowledge_document through the pipeline
    result. This fixture only supplies the fields Phase 5 consumes.
    """

    knowledge_document: FakeKnowledgeDocument


# ============================================================================
# RESUME
# ============================================================================


RESUME_TEXT = """
John Smith

Professional Summary

Senior Software Engineer with experience building scalable Python
applications and enterprise systems.

Experience

Senior Software Engineer
ABC Technologies

Led a team of 8 engineers.
Improved API performance by 35%.
Built Python and FastAPI services.
Designed PostgreSQL data models.
Managed CI/CD pipelines.
Mentored junior engineers.

Skills

Python
FastAPI
PostgreSQL
Docker
AWS
CI/CD

Education

Bachelor of Science in Computer Science
"""


# ============================================================================
# RESUME PROFILE
# ============================================================================


@pytest.fixture
def resume_profile() -> DocumentKnowledgeProfile:
    """
    Build a real DocumentKnowledgeProfile.

    No KnowledgeMatchProfile subclassing is used.
    """

    knowledge_profile = KnowledgeProfile()

    source_document = FakeKnowledgeDocument(
        raw_text=RESUME_TEXT,
        facts=[],
    )

    source_result = FakePipelineResult(
        knowledge_document=source_document,
    )

    return DocumentKnowledgeProfile(
        document_type=DocumentType.RESUME,
        profile=knowledge_profile,
        source_result=source_result,
    )


# ============================================================================
# JD PROFILE
# ============================================================================


@pytest.fixture
def jd_requirement_profile() -> JDRequirementProfile:
    """
    Build an empty but valid JDRequirementProfile.

    Phase 5 only requires the established Phase 2 contract.
    """

    return JDRequirementProfile.from_requirements(
        []
    )


# ============================================================================
# PHASE 4 PROFILE
# ============================================================================


@pytest.fixture
def knowledge_match_profile(
    resume_profile: DocumentKnowledgeProfile,
    jd_requirement_profile: JDRequirementProfile,
) -> KnowledgeMatchProfile:
    """
    Build the actual Phase 3 -> Phase 4 chain.
    """

    requirement_matches = [
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
    ]

    # ------------------------------------------------------------------------
    # Phase 3.1
    # ------------------------------------------------------------------------

    match_result = KnowledgeMatchResult.from_matches(
        requirement_matches
    )

    # ------------------------------------------------------------------------
    # Phase 3.2
    # ------------------------------------------------------------------------

    enriched_match_result = (
        KnowledgeMatchEnricher().process(
            match_result=match_result,
            resume_profile=resume_profile,
            jd_requirement_profile=jd_requirement_profile,
        )
    )

    # ------------------------------------------------------------------------
    # Phase 3.3
    # ------------------------------------------------------------------------

    gap_analysis_result = (
        KnowledgeGapAnalyzer().process(
            enriched_match_result
        )
    )

    # ------------------------------------------------------------------------
    # Phase 4
    # ------------------------------------------------------------------------

    profile = (
        KnowledgeMatchProfileBuilder().process(
            match_result=match_result,
            enriched_match_result=enriched_match_result,
            gap_analysis_result=gap_analysis_result,
        )
    )

    # ------------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------------

    assert profile.match_result is match_result

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
# REQUEST
# ============================================================================


@pytest.fixture
def ats_request(
    knowledge_match_profile: KnowledgeMatchProfile,
    resume_profile: DocumentKnowledgeProfile,
    jd_requirement_profile: JDRequirementProfile,
) -> ATSResumeAnalysisRequest:

    return ATSResumeAnalysisRequest(
        knowledge_match_profile=knowledge_match_profile,
        resume_profile=resume_profile,
        jd_requirement_profile=jd_requirement_profile,
    )


# ============================================================================
# CONSTRUCTION
# ============================================================================


class TestATSResumeAnalyzerConstruction:

    def test_default_policy_is_created(self) -> None:

        analyzer = ATSResumeAnalyzer()

        assert isinstance(
            analyzer.policy,
            ATSAnalysisPolicy,
        )

    def test_custom_policy_is_preserved(self) -> None:

        policy = ATSAnalysisPolicy()

        analyzer = ATSResumeAnalyzer(
            policy=policy,
        )

        assert analyzer.policy is policy

    def test_invalid_policy_is_rejected(self) -> None:

        with pytest.raises(
            TypeError,
            match="ATSResumeAnalyzer.policy",
        ):
            ATSResumeAnalyzer(
                policy="invalid",  # type: ignore[arg-type]
            )


# ============================================================================
# REQUEST VALIDATION
# ============================================================================


class TestATSResumeAnalyzerRequestValidation:

    def test_invalid_request_type_is_rejected(
        self,
    ) -> None:

        analyzer = ATSResumeAnalyzer()

        with pytest.raises(
            TypeError,
            match="ATSResumeAnalysisRequest",
        ):
            analyzer.process(
                "invalid",  # type: ignore[arg-type]
            )

    def test_non_resume_profile_is_rejected(
        self,
        knowledge_match_profile: KnowledgeMatchProfile,
        jd_requirement_profile: JDRequirementProfile,
    ) -> None:

        jd_profile = DocumentKnowledgeProfile(
            document_type=DocumentType.JD,
            profile=KnowledgeProfile(),
        )

        request = ATSResumeAnalysisRequest(
            knowledge_match_profile=knowledge_match_profile,
            resume_profile=jd_profile,
            jd_requirement_profile=jd_requirement_profile,
        )

        analyzer = ATSResumeAnalyzer()

        with pytest.raises(
            ValueError,
            match="resume_profile",
        ):
            analyzer.process(
                request
            )

    def test_empty_resume_source_is_rejected(
        self,
        knowledge_match_profile: KnowledgeMatchProfile,
        jd_requirement_profile: JDRequirementProfile,
    ) -> None:

        empty_document = FakeKnowledgeDocument(
            raw_text="   ",
            facts=[],
        )

        empty_result = FakePipelineResult(
            knowledge_document=empty_document,
        )

        empty_resume_profile = DocumentKnowledgeProfile(
            document_type=DocumentType.RESUME,
            profile=KnowledgeProfile(),
            source_result=empty_result,
        )

        request = ATSResumeAnalysisRequest(
            knowledge_match_profile=knowledge_match_profile,
            resume_profile=empty_resume_profile,
            jd_requirement_profile=jd_requirement_profile,
        )

        analyzer = ATSResumeAnalyzer()

        with pytest.raises(
            ValueError,
            match="resume source",
        ):
            analyzer.process(
                request
            )


# ============================================================================
# PROCESS
# ============================================================================


class TestATSResumeAnalyzerProcess:

    def test_process_returns_ats_analysis_result(
        self,
        ats_request: ATSResumeAnalysisRequest,
    ) -> None:

        analyzer = ATSResumeAnalyzer()

        result = analyzer.process(
            ats_request
        )

        assert isinstance(
            result,
            ATSResumeAnalysisResult,
        )

    def test_result_preserves_request_identity(
        self,
        ats_request: ATSResumeAnalysisRequest,
    ) -> None:

        analyzer = ATSResumeAnalyzer()

        result = analyzer.process(
            ats_request
        )

        assert (
            result.request
            is ats_request
        )

    def test_result_preserves_phase_4_profile_identity(
        self,
        ats_request: ATSResumeAnalysisRequest,
        knowledge_match_profile: KnowledgeMatchProfile,
    ) -> None:

        analyzer = ATSResumeAnalyzer()

        result = analyzer.process(
            ats_request
        )

        assert (
            result.knowledge_match_profile
            is knowledge_match_profile
        )

        assert (
            result.request.knowledge_match_profile
            is knowledge_match_profile
        )

    def test_result_contains_all_analysis_dimensions(
        self,
        ats_request: ATSResumeAnalysisRequest,
    ) -> None:

        result = ATSResumeAnalyzer().process(
            ats_request
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

    def test_scores_are_normalized(
        self,
        ats_request: ATSResumeAnalysisRequest,
    ) -> None:

        result = ATSResumeAnalyzer().process(
            ats_request
        )

        assert 0.0 <= result.ats_score.score <= 1.0

        assert (
            0.0
            <= result.ats_score.confidence
            <= 1.0
        )

        assert (
            0.0
            <= result.score_breakdown.weighted_score
            <= 1.0
        )

        assert (
            0.0
            <= result.confidence
            <= 1.0
        )

    def test_keyword_analysis_uses_phase_4_requirements(
        self,
        ats_request: ATSResumeAnalysisRequest,
    ) -> None:

        result = ATSResumeAnalyzer().process(
            ats_request
        )

        required = (
            result
            .keyword_analysis
            .required_keywords
        )

        assert "Python" in required
        assert "FastAPI" in required
        assert "Kubernetes" in required

    def test_section_analysis_uses_resume_source(
        self,
        ats_request: ATSResumeAnalysisRequest,
    ) -> None:

        result = ATSResumeAnalyzer().process(
            ats_request
        )

        detected = (
            result
            .section_analysis
            .detected_sections
        )

        assert "Professional Summary" in detected
        assert "Experience" in detected
        assert "Skills" in detected
        assert "Education" in detected

    def test_quantification_analysis_detects_source_facts_or_numbers(
        self,
        ats_request: ATSResumeAnalysisRequest,
    ) -> None:

        result = ATSResumeAnalyzer().process(
            ats_request
        )

        assert (
            result
            .quantification_analysis
            .quantified_bullet_count
            >= 1
        )

    def test_parseability_is_true_for_valid_resume_source(
        self,
        ats_request: ATSResumeAnalysisRequest,
    ) -> None:

        result = ATSResumeAnalyzer().process(
            ats_request
        )

        assert (
            result
            .parseability_analysis
            .parseable
            is True
        )

        assert (
            result
            .parseability_analysis
            .parseability_score
            == 1.0
        )


# ============================================================================
# RESULT CONTRACT
# ============================================================================


class TestATSResumeAnalysisResultContract:

    def test_result_is_immutable(
        self,
        ats_request: ATSResumeAnalysisRequest,
    ) -> None:

        result = ATSResumeAnalyzer().process(
            ats_request
        )

        with pytest.raises(
            AttributeError
        ):
            result.confidence = 0.5  # type: ignore[misc]

    def test_request_metadata_is_independent(
        self,
        ats_request: ATSResumeAnalysisRequest,
    ) -> None:

        result = ATSResumeAnalyzer().process(
            ats_request
        )

        assert result.request is ats_request

        assert result.metadata == {}


# ============================================================================
# POLICY
# ============================================================================


class TestATSAnalysisPolicy:

    def test_default_policy_has_normalized_weights(
        self,
    ) -> None:

        policy = ATSAnalysisPolicy()

        assert set(
            policy.score_weights.keys()
        ) == {
            "keyword",
            "section",
            "formatting",
            "readability",
            "terminology",
            "quantification",
            "parseability",
        }

        assert sum(
            policy.score_weights.values()
        ) == pytest.approx(
            1.0
        )

    def test_invalid_weights_are_rejected(
        self,
    ) -> None:

        with pytest.raises(
            ValueError,
            match="sum to 1.0",
        ):
            ATSAnalysisPolicy(
                score_weights={
                    "keyword": 1.0,
                    "section": 0.0,
                    "formatting": 0.0,
                    "readability": 0.0,
                    "terminology": 0.0,
                    "quantification": 0.0,
                    "parseability": 1.0,
                }
            )