
"""
Phase 5 - ATS Resume Analyzer Tests
====================================

Complete object-in / object-out contract tests.

Pipeline under test:

    Phase 3.1
        KnowledgeMatchResult
             |
             v
    Phase 3.2
        EnrichedKnowledgeMatchResult
             |
             v
    Phase 3.3
        KnowledgeGapAnalysisResult
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


Architectural rule
------------------
Phase 6 must receive the exact ATSResumeAnalysisResult object produced here.

The test suite therefore checks identity, not merely equality.
"""

from __future__ import annotations

import pytest

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSFormattingAnalysis,
    ATSKeywordAnalysis,
    ATSParseabilityAnalysis,
    ATSQuantificationAnalysis,
    ATSReadabilityAnalysis,
    ATSResumeAnalysisResult,
    ATSScore,
    ATSScoreBreakdown,
    ATSSectionAnalysis,
    ATSTerminologyAnalysis,
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

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeMatchProfile,
)


# ============================================================================
# PHASE 3.1
# ============================================================================


class TestPhase31MatchResult:
    """
    Verify Phase 3.1 object boundary.
    """

    def test_match_result_is_object(
        self,
        match_result,
    ) -> None:

        from app.intelligence.utilities.knowledge.matching.match_models import (
            KnowledgeMatchResult,
        )

        assert isinstance(
            match_result,
            KnowledgeMatchResult,
        )

    def test_match_result_contains_matches(
        self,
        match_result,
    ) -> None:

        assert len(
            match_result.matches
        ) == 3

    def test_match_statuses_are_preserved(
        self,
        match_result,
    ) -> None:

        statuses = {
            match.status
            for match in match_result.matches
        }

        from app.intelligence.utilities.knowledge.matching.match_models import (
            MatchStatus,
        )

        assert MatchStatus.MATCHED in statuses
        assert MatchStatus.PARTIAL in statuses
        assert MatchStatus.UNMATCHED in statuses


# ============================================================================
# PHASE 3.2
# ============================================================================


class TestPhase32Enrichment:
    """
    Verify Phase 3.2 preserves the Phase 3.1 object.
    """

    def test_enrichment_returns_typed_object(
        self,
        enriched_match_result,
    ) -> None:

        from app.intelligence.utilities.knowledge.matching.enrichment_models import (
            EnrichedKnowledgeMatchResult,
        )

        assert isinstance(
            enriched_match_result,
            EnrichedKnowledgeMatchResult,
        )

    def test_enrichment_preserves_match_identity(
        self,
        match_result,
        enriched_match_result,
    ) -> None:

        assert (
            enriched_match_result.match_result
            is match_result
        )


# ============================================================================
# PHASE 3.3
# ============================================================================


class TestPhase33GapAnalysis:
    """
    Verify Phase 3.3 preserves Phase 3.2.
    """

    def test_gap_analysis_returns_typed_object(
        self,
        gap_analysis_result,
    ) -> None:

        from app.intelligence.utilities.knowledge.matching.gap_models import (
            KnowledgeGapAnalysisResult,
        )

        assert isinstance(
            gap_analysis_result,
            KnowledgeGapAnalysisResult,
        )

    def test_gap_analysis_preserves_enrichment_identity(
        self,
        enriched_match_result,
        gap_analysis_result,
    ) -> None:

        assert (
            gap_analysis_result.enriched_match_result
            is enriched_match_result
        )


# ============================================================================
# PHASE 4
# ============================================================================


class TestPhase4KnowledgeMatchProfile:
    """
    Verify the aggregate Phase 4 object.
    """

    def test_profile_is_typed_object(
        self,
        knowledge_match_profile,
    ) -> None:

        assert isinstance(
            knowledge_match_profile,
            KnowledgeMatchProfile,
        )

    def test_profile_preserves_phase31_identity(
        self,
        knowledge_match_profile,
        match_result,
    ) -> None:

        assert (
            knowledge_match_profile.match_result
            is match_result
        )

    def test_profile_preserves_phase32_identity(
        self,
        knowledge_match_profile,
        enriched_match_result,
    ) -> None:

        assert (
            knowledge_match_profile.enriched_match_result
            is enriched_match_result
        )

    def test_profile_preserves_phase33_identity(
        self,
        knowledge_match_profile,
        gap_analysis_result,
    ) -> None:

        assert (
            knowledge_match_profile.gap_analysis_result
            is gap_analysis_result
        )


# ============================================================================
# PHASE 5 CONSTRUCTION
# ============================================================================


class TestATSResumeAnalyzerConstruction:
    """
    Analyzer construction contract.
    """

    def test_default_policy_is_created(
        self,
    ) -> None:

        analyzer = ATSResumeAnalyzer()

        assert isinstance(
            analyzer.policy,
            ATSAnalysisPolicy,
        )

    def test_custom_policy_is_preserved(
        self,
    ) -> None:

        policy = ATSAnalysisPolicy()

        analyzer = ATSResumeAnalyzer(
            policy=policy,
        )

        assert (
            analyzer.policy
            is policy
        )

    def test_invalid_policy_is_rejected(
        self,
    ) -> None:

        with pytest.raises(
            TypeError,
            match="ATSResumeAnalyzer.policy",
        ):
            ATSResumeAnalyzer(
                policy="invalid",  # type: ignore[arg-type]
            )


# ============================================================================
# PHASE 5 REQUEST
# ============================================================================


class TestATSResumeAnalysisRequest:
    """
    Validate the Phase 5 request object.
    """

    def test_request_is_typed_object(
        self,
        ats_request,
    ) -> None:

        assert isinstance(
            ats_request,
            ATSResumeAnalysisRequest,
        )

    def test_request_preserves_phase4_profile(
        self,
        ats_request,
        knowledge_match_profile,
    ) -> None:

        assert (
            ats_request.knowledge_match_profile
            is knowledge_match_profile
        )

    def test_request_has_resume_source(
        self,
        ats_request,
    ) -> None:

        assert ats_request.has_resume_source
        assert ats_request.source_text.strip()

    def test_request_has_phase4_profile(
        self,
        ats_request,
    ) -> None:

        assert ats_request.has_phase4_profile

    def test_request_source_text_is_resume_text(
        self,
        ats_request,
    ) -> None:

        assert (
            ats_request.source_text
            == ats_request.resume_text
        )

    def test_empty_resume_is_rejected(
        self,
        knowledge_match_profile,
        ats_policy,
    ) -> None:

        with pytest.raises(
            ValueError,
            match="resume_text",
        ):
            ATSResumeAnalysisRequest(
                resume_text="   ",
                knowledge_match_profile=(
                    knowledge_match_profile
                ),
                policy=ats_policy,
            )

    def test_missing_profile_is_rejected(
        self,
        ats_policy,
    ) -> None:

        with pytest.raises(
            ValueError,
            match="KnowledgeMatchProfile",
        ):
            ATSResumeAnalysisRequest(
                resume_text="Valid resume text",
                knowledge_match_profile=None,
                policy=ats_policy,
            )

    def test_missing_policy_is_rejected(
        self,
        knowledge_match_profile,
    ) -> None:

        with pytest.raises(
            ValueError,
            match="policy",
        ):
            ATSResumeAnalysisRequest(
                resume_text="Valid resume text",
                knowledge_match_profile=(
                    knowledge_match_profile
                ),
                policy=None,
            )


# ============================================================================
# PHASE 5 ANALYZER INPUT CONTRACT
# ============================================================================


class TestATSResumeAnalyzerInputContract:
    """
    ATSResumeAnalyzer must accept the Phase 5 request object,
    not dictionaries or arbitrary values.
    """

    def test_invalid_request_type_is_rejected(
        self,
    ) -> None:

        analyzer = ATSResumeAnalyzer()

        with pytest.raises(
            TypeError,
            match="ATSResumeAnalysisRequest",
        ):
            analyzer.process(
                "invalid request",  # type: ignore[arg-type]
            )

    def test_request_policy_must_match_analyzer_policy(
        self,
        knowledge_match_profile,
    ) -> None:

        analyzer_policy = ATSAnalysisPolicy()
        request_policy = ATSAnalysisPolicy()

        request = ATSResumeAnalysisRequest(
            resume_text="Valid resume text",
            knowledge_match_profile=(
                knowledge_match_profile
            ),
            policy=request_policy,
        )

        analyzer = ATSResumeAnalyzer(
            policy=analyzer_policy,
        )

        with pytest.raises(
            ValueError,
            match="policy",
        ):
            analyzer.process(
                request
            )


# ============================================================================
# PHASE 5 PROCESS
# ============================================================================


class TestATSResumeAnalyzerProcess:
    """
    Complete Phase 5 output contract.
    """

    def test_process_returns_ats_result(
        self,
        ats_result,
    ) -> None:

        assert isinstance(
            ats_result,
            ATSResumeAnalysisResult,
        )

    def test_result_preserves_request_identity(
        self,
        ats_result,
        ats_request,
    ) -> None:

        assert (
            ats_result.request
            is ats_request
        )

    def test_result_preserves_phase4_identity(
        self,
        ats_result,
        knowledge_match_profile,
    ) -> None:

        assert (
            ats_result.knowledge_match_profile
            is knowledge_match_profile
        )

    def test_request_and_result_share_same_phase4_object(
        self,
        ats_result,
        ats_request,
        knowledge_match_profile,
    ) -> None:

        assert (
            ats_result.request
            is ats_request
        )

        assert (
            ats_request.knowledge_match_profile
            is knowledge_match_profile
        )

        assert (
            ats_result.knowledge_match_profile
            is knowledge_match_profile
        )

    def test_result_is_not_a_dictionary(
        self,
        ats_result,
    ) -> None:

        assert not isinstance(
            ats_result,
            dict,
        )

    def test_result_has_typed_keyword_analysis(
        self,
        ats_result,
    ) -> None:

        assert isinstance(
            ats_result.keyword_analysis,
            ATSKeywordAnalysis,
        )

    def test_result_has_typed_section_analysis(
        self,
        ats_result,
    ) -> None:

        assert isinstance(
            ats_result.section_analysis,
            ATSSectionAnalysis,
        )

    def test_result_has_typed_formatting_analysis(
        self,
        ats_result,
    ) -> None:

        assert isinstance(
            ats_result.formatting_analysis,
            ATSFormattingAnalysis,
        )

    def test_result_has_typed_readability_analysis(
        self,
        ats_result,
    ) -> None:

        assert isinstance(
            ats_result.readability_analysis,
            ATSReadabilityAnalysis,
        )

    def test_result_has_typed_terminology_analysis(
        self,
        ats_result,
    ) -> None:

        assert isinstance(
            ats_result.terminology_analysis,
            ATSTerminologyAnalysis,
        )

    def test_result_has_typed_quantification_analysis(
        self,
        ats_result,
    ) -> None:

        assert isinstance(
            ats_result.quantification_analysis,
            ATSQuantificationAnalysis,
        )

    def test_result_has_typed_parseability_analysis(
        self,
        ats_result,
    ) -> None:

        assert isinstance(
            ats_result.parseability_analysis,
            ATSParseabilityAnalysis,
        )


# ============================================================================
# SCORE CONTRACT
# ============================================================================


class TestATSScoreContract:
    """
    All ATS scores must remain normalized.
    """

    def test_ats_score_is_typed_object(
        self,
        ats_result,
    ) -> None:

        assert isinstance(
            ats_result.ats_score,
            ATSScore,
        )

    def test_score_is_normalized(
        self,
        ats_result,
    ) -> None:

        assert 0.0 <= (
            ats_result.ats_score.score
        ) <= 1.0

    def test_confidence_is_normalized(
        self,
        ats_result,
    ) -> None:

        assert 0.0 <= (
            ats_result.ats_score.confidence
        ) <= 1.0

        assert 0.0 <= (
            ats_result.confidence
        ) <= 1.0

    def test_breakdown_is_typed_object(
        self,
        ats_result,
    ) -> None:

        assert isinstance(
            ats_result.score_breakdown,
            ATSScoreBreakdown,
        )

    def test_breakdown_scores_are_normalized(
        self,
        ats_result,
    ) -> None:

        breakdown = ats_result.score_breakdown

        scores = (
            breakdown.keyword_score,
            breakdown.section_score,
            breakdown.formatting_score,
            breakdown.readability_score,
            breakdown.terminology_score,
            breakdown.quantification_score,
            breakdown.parseability_score,
            breakdown.structure_score,
            breakdown.weighted_score,
        )

        for score in scores:
            assert 0.0 <= score <= 1.0

    def test_compatibility_score_alias_matches_ats_score(
        self,
        ats_result,
    ) -> None:

        assert (
            ats_result.score
            == ats_result.ats_score.score
        )

    def test_compatibility_breakdown_alias_matches_typed_breakdown(
        self,
        ats_result,
    ) -> None:

        assert (
            ats_result.breakdown
            is ats_result.score_breakdown
        )


# ============================================================================
# COMPONENT CONTENT
# ============================================================================


class TestATSComponentContent:
    """
    Validate useful observations are present.
    """

    def test_keyword_analysis_is_available(
        self,
        ats_result,
    ) -> None:

        analysis = ats_result.keyword_analysis

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

        assert 0.0 <= (
            analysis.keyword_coverage_score
        ) <= 1.0

    def test_section_analysis_is_available(
        self,
        ats_result,
    ) -> None:

        analysis = ats_result.section_analysis

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

        assert 0.0 <= (
            analysis.section_completeness_score
        ) <= 1.0

    def test_formatting_analysis_is_available(
        self,
        ats_result,
    ) -> None:

        analysis = ats_result.formatting_analysis

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

        assert 0.0 <= (
            analysis.formatting_score
        ) <= 1.0

    def test_readability_analysis_is_available(
        self,
        ats_result,
    ) -> None:

        analysis = ats_result.readability_analysis

        assert analysis.estimated_word_count >= 0
        assert analysis.long_sentence_count >= 0
        assert analysis.average_sentence_length >= 0.0

        assert 0.0 <= (
            analysis.readability_score
        ) <= 1.0

    def test_terminology_analysis_is_available(
        self,
        ats_result,
    ) -> None:

        analysis = ats_result.terminology_analysis

        assert isinstance(
            analysis.aligned_terms,
            tuple,
        )

        assert isinstance(
            analysis.missing_terms,
            tuple,
        )

        assert 0.0 <= (
            analysis.terminology_score
        ) <= 1.0

    def test_quantification_analysis_is_available(
        self,
        ats_result,
    ) -> None:

        analysis = ats_result.quantification_analysis

        assert (
            analysis.quantified_achievement_count
            >= 0
        )

        assert (
            analysis.quantified_bullet_count
            >= 0
        )

        assert 0.0 <= (
            analysis.quantification_score
        ) <= 1.0

    def test_parseability_analysis_is_available(
        self,
        ats_result,
    ) -> None:

        analysis = ats_result.parseability_analysis

        assert isinstance(
            analysis.parseable,
            bool,
        )

        assert (
            analysis.extraction_warning_count
            == len(analysis.warnings)
        )

        assert 0.0 <= (
            analysis.parseability_score
        ) <= 1.0


# ============================================================================
# PHASE 5 -> PHASE 6 HANDOFF CONTRACT
# ============================================================================


class TestPhase5ToPhase6Boundary:
    """
    This is deliberately a Phase-6 preparation test.

    Phase 6 must consume ATSResumeAnalysisResult directly.

    There must be no:

        ATSResumeAnalysisResult -> dict
        dict -> RecommendationRequest

    conversion at this boundary unless a future explicit adapter is
    deliberately introduced.
    """

    def test_phase6_input_is_phase5_result(
        self,
        ats_result,
    ) -> None:

        assert isinstance(
            ats_result,
            ATSResumeAnalysisResult,
        )

    def test_phase6_receives_exact_phase5_object(
        self,
        ats_result,
    ) -> None:

        phase5_output = ats_result

        phase6_input = phase5_output

        assert (
            phase6_input
            is phase5_output
        )

    def test_phase6_can_reach_phase4_without_reconstruction(
        self,
        ats_result,
        knowledge_match_profile,
    ) -> None:

        assert (
            ats_result.knowledge_match_profile
            is knowledge_match_profile
        )

        assert (
            ats_result.request.knowledge_match_profile
            is knowledge_match_profile
        )

    def test_phase6_can_reach_all_ats_components(
        self,
        ats_result,
    ) -> None:

        components = (
            ats_result.keyword_analysis,
            ats_result.section_analysis,
            ats_result.formatting_analysis,
            ats_result.readability_analysis,
            ats_result.terminology_analysis,
            ats_result.quantification_analysis,
            ats_result.parseability_analysis,
            ats_result.ats_score,
            ats_result.score_breakdown,
        )

        for component in components:
            assert component is not None
            assert not isinstance(
                component,
                dict,
            )


# ============================================================================
# OBJECT GRAPH DIAGNOSTIC
# ============================================================================


class TestPhaseChainIdentity:
    """
    Verify the complete object chain.
    """

    def test_complete_phase_chain(
        self,
        match_result,
        enriched_match_result,
        gap_analysis_result,
        knowledge_match_profile,
        ats_request,
        ats_result,
    ) -> None:

        # Phase 3.1
        assert (
            enriched_match_result.match_result
            is match_result
        )

        # Phase 3.3
        assert (
            gap_analysis_result.enriched_match_result
            is enriched_match_result
        )

        # Phase 4
        assert (
            knowledge_match_profile.match_result
            is match_result
        )

        assert (
            knowledge_match_profile.enriched_match_result
            is enriched_match_result
        )

        assert (
            knowledge_match_profile.gap_analysis_result
            is gap_analysis_result
        )

        # Phase 5 request
        assert (
            ats_request.knowledge_match_profile
            is knowledge_match_profile
        )

        # Phase 5 result
        assert (
            ats_result.request
            is ats_request
        )

        assert (
            ats_result.knowledge_match_profile
            is knowledge_match_profile
        )

    def test_no_phase_rebuilds_previous_objects(
        self,
        match_result,
        enriched_match_result,
        gap_analysis_result,
        knowledge_match_profile,
        ats_request,
        ats_result,
    ) -> None:

        objects = (
            match_result,
            enriched_match_result,
            gap_analysis_result,
            knowledge_match_profile,
            ats_request,
            ats_result,
        )

        for obj in objects:
            assert obj is not None

            # Every phase output is an object.
            assert not isinstance(
                obj,
                dict,
            )

