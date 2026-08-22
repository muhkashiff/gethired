"""
Project Pipeline Result Contracts
=================================

Enterprise project-level result objects.

This module contains result contracts for the application orchestration
pipeline.

The orchestration itself remains in:

    project_pipeline.py


Current result boundaries:

    ProjectPipelineResult
        One document processed through Phase 1 + Phase 2.


    ProjectMatchResult
        One processed resume matched against one processed JD
        through Phase 3, consolidated through Phase 4, analyzed
        through Phase 5 ATS analysis, and processed through Phase 6
        recommendation analysis.


Phase 3
-------

    Phase 3.1
        Knowledge Matching
            ↓
        KnowledgeMatchResult


    Phase 3.2
        Match Evidence / Enrichment
            ↓
        EnrichedKnowledgeMatchResult


    Phase 3.3
        Gap Analysis
            ↓
        KnowledgeGapAnalysisResult


Phase 4
-------

    KnowledgeMatchResult
        +
    EnrichedKnowledgeMatchResult
        +
    KnowledgeGapAnalysisResult
        ↓
    KnowledgeMatchProfile


Phase 5
-------

    KnowledgeMatchProfile
        +
    Resume DocumentKnowledgeProfile
        +
    JDRequirementProfile
        ↓
    ATSResumeAnalysisRequest
        ↓
    ATSResumeAnalyzer
        ↓
    ATSResumeAnalysisResult


Phase 6
-------

    ATSResumeAnalysisResult
        ↓
    RecommendationAnalyzer
        ↓
    RecommendationResult


Complete project match
----------------------

    Resume ProjectPipelineResult
                +
    JD ProjectPipelineResult
                ↓
        Phase 3.1 Matching
                ↓
        Phase 3.2 Enrichment
                ↓
        Phase 3.3 Gap Analysis
                ↓
        Phase 4 KnowledgeMatchProfile
                ↓
        Phase 5 ATS Analysis
                ↓
        Phase 6 Recommendations
                ↓
        ProjectMatchResult


Design principles
-----------------

1. ProjectPipeline remains the application orchestration boundary.

2. Individual intelligence modules remain responsible for their own work.

3. ProjectMatchResult preserves every major Phase 3 boundary.

4. ProjectMatchResult preserves the authoritative Phase 4 profile.

5. ProjectMatchResult preserves the complete Phase 5 ATS result.

6. ProjectMatchResult preserves the complete Phase 6 recommendation result.

7. No intelligence phase is silently discarded.

8. Phase 5 consumes the exact Phase 4 KnowledgeMatchProfile.

9. Phase 5 does not reconstruct matching, enrichment, or gap analysis.

10. Phase 6 consumes the exact Phase 5 ATSResumeAnalysisResult.

11. Phase 6 preserves the exact Phase 5 ATSResumeAnalysisResult identity.

12. Phase 6 preserves the exact Phase 4 KnowledgeMatchProfile identity through
    the Phase 5 result.

13. Downstream phases can consume ProjectMatchResult without rerunning
    Phases 3, 4, 5, or 6.

14. Convenience properties expose authoritative metrics only. They do not
    recalculate intelligence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


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

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
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
# PHASE 3.1 MATCHING LAYER
# ============================================================================

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchRequest,
    KnowledgeMatchResult,
)


# ============================================================================
# PHASE 3.2 ENRICHMENT LAYER
# ============================================================================

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
)


# ============================================================================
# PHASE 3.3 GAP ANALYSIS LAYER
# ============================================================================

from app.intelligence.utilities.knowledge.matching.gap_models import (
    KnowledgeGapAnalysisResult,
)


# ============================================================================
# PHASE 4 MATCH PROFILE
# ============================================================================

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeMatchProfile,
)


# ============================================================================
# PHASE 5 ATS LAYER
# ============================================================================

from app.intelligence.utilities.knowledge.ats.ats_analysis_request import (
    ATSResumeAnalysisRequest,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSResumeAnalysisResult,
)


# ============================================================================
# PHASE 6 RECOMMENDATION LAYER
# ============================================================================

from app.intelligence.utilities.knowledge.recommendations.recommendation_models import (
    RecommendationResult,
)


# ============================================================================
# PROJECT PIPELINE RESULT
# ============================================================================


@dataclass(frozen=True)
class ProjectPipelineResult:
    """
    Complete result of processing one document.

    This is the Phase 1 + Phase 2 application boundary.
    """

    # ------------------------------------------------------------------
    # Original input
    # ------------------------------------------------------------------

    document_input: DocumentInput

    # ------------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------------

    routed_document: RoutedDocument

    # ------------------------------------------------------------------
    # Knowledge pipeline
    # ------------------------------------------------------------------

    pipeline_request: KnowledgePipelineRequest

    pipeline_response: KnowledgePipelineResponse

    # ------------------------------------------------------------------
    # Document-aware knowledge profile
    # ------------------------------------------------------------------

    document_profile: DocumentKnowledgeProfile

    # ------------------------------------------------------------------
    # Phase 2 JD interpretation
    # ------------------------------------------------------------------

    jd_requirement_profile: Optional[
        JDRequirementProfile
    ] = None

    # =========================================================================
    # CONVENIENCE PROPERTIES
    # =========================================================================

    @property
    def is_resume(self) -> bool:
        """Return True when this result represents a resume."""

        return (
            self.document_input.document_type
            == DocumentType.RESUME
        )

    @property
    def is_jd(self) -> bool:
        """Return True when this result represents a job description."""

        return (
            self.document_input.document_type
            == DocumentType.JD
        )

    @property
    def knowledge_profile(self) -> Any:
        """
        Return the underlying Enterprise KnowledgeProfile.

        The original KnowledgeProfile remains untouched.
        """

        return self.document_profile.profile


# ============================================================================
# PROJECT MATCH RESULT
# ============================================================================


@dataclass(frozen=True)
class ProjectMatchResult:
    """
    Complete application-level result for resume-to-JD matching.

    Complete structure:

        resume_result
                +
        jd_result
                ↓
        match_request
                ↓
        match_result
                ↓
        enriched_match_result
                ↓
        gap_analysis_result
                ↓
        knowledge_match_profile
                ↓
        ats_analysis_request
                ↓
        ats_analysis_result
                ↓
        recommendation_result


    The object deliberately retains every major boundary so downstream
    phases do not need to rerun previous intelligence.
    """

    # ------------------------------------------------------------------
    # Processed source results
    # ------------------------------------------------------------------

    resume_result: ProjectPipelineResult

    jd_result: ProjectPipelineResult

    # ------------------------------------------------------------------
    # Phase 3.1 matching boundary
    # ------------------------------------------------------------------

    match_request: KnowledgeMatchRequest

    match_result: KnowledgeMatchResult

    # ------------------------------------------------------------------
    # Phase 3.2 enrichment boundary
    # ------------------------------------------------------------------

    enriched_match_result: EnrichedKnowledgeMatchResult

    # ------------------------------------------------------------------
    # Phase 3.3 gap analysis boundary
    # ------------------------------------------------------------------

    gap_analysis_result: KnowledgeGapAnalysisResult

    # ------------------------------------------------------------------
    # Phase 4 consolidated profile
    # ------------------------------------------------------------------

    knowledge_match_profile: KnowledgeMatchProfile

    # ------------------------------------------------------------------
    # Phase 5 ATS boundary
    # ------------------------------------------------------------------

    ats_analysis_request: ATSResumeAnalysisRequest

    ats_analysis_result: ATSResumeAnalysisResult

    # ------------------------------------------------------------------
    # Phase 6 recommendation boundary
    # ------------------------------------------------------------------

    recommendation_result: RecommendationResult

    def __post_init__(self) -> None:
        """
        Validate the complete Phase 3 -> Phase 4 -> Phase 5 -> Phase 6
        source chain.
        """

        # ------------------------------------------------------------------
        # BASE RESULT VALIDATION
        # ------------------------------------------------------------------

        if not isinstance(
            self.resume_result,
            ProjectPipelineResult,
        ):
            raise TypeError(
                "resume_result must be ProjectPipelineResult."
            )

        if not isinstance(
            self.jd_result,
            ProjectPipelineResult,
        ):
            raise TypeError(
                "jd_result must be ProjectPipelineResult."
            )

        if not isinstance(
            self.match_request,
            KnowledgeMatchRequest,
        ):
            raise TypeError(
                "match_request must be KnowledgeMatchRequest."
            )

        if not isinstance(
            self.match_result,
            KnowledgeMatchResult,
        ):
            raise TypeError(
                "match_result must be KnowledgeMatchResult."
            )

        if not isinstance(
            self.enriched_match_result,
            EnrichedKnowledgeMatchResult,
        ):
            raise TypeError(
                "enriched_match_result must be "
                "EnrichedKnowledgeMatchResult."
            )

        if not isinstance(
            self.gap_analysis_result,
            KnowledgeGapAnalysisResult,
        ):
            raise TypeError(
                "gap_analysis_result must be "
                "KnowledgeGapAnalysisResult."
            )

        if not isinstance(
            self.knowledge_match_profile,
            KnowledgeMatchProfile,
        ):
            raise TypeError(
                "knowledge_match_profile must be "
                "KnowledgeMatchProfile."
            )

        if not isinstance(
            self.ats_analysis_request,
            ATSResumeAnalysisRequest,
        ):
            raise TypeError(
                "ats_analysis_request must be "
                "ATSResumeAnalysisRequest."
            )

        if not isinstance(
            self.ats_analysis_result,
            ATSResumeAnalysisResult,
        ):
            raise TypeError(
                "ats_analysis_result must be "
                "ATSResumeAnalysisResult."
            )

        if not isinstance(
            self.recommendation_result,
            RecommendationResult,
        ):
            raise TypeError(
                "recommendation_result must be "
                "RecommendationResult."
            )

        # ------------------------------------------------------------------
        # PHASE 3.2 -> PHASE 3.1 IDENTITY
        # ------------------------------------------------------------------

        if (
            self.enriched_match_result.match_result
            is not self.match_result
        ):
            raise ValueError(
                "enriched_match_result must reference "
                "the supplied match_result."
            )

        # ------------------------------------------------------------------
        # PHASE 3.3 -> PHASE 3.2 IDENTITY
        # ------------------------------------------------------------------

        if (
            self.gap_analysis_result.enriched_match_result
            is not self.enriched_match_result
        ):
            raise ValueError(
                "gap_analysis_result must reference "
                "the supplied enriched_match_result."
            )

        # ------------------------------------------------------------------
        # PHASE 4 -> PHASE 3.1 IDENTITY
        # ------------------------------------------------------------------

        if (
            self.knowledge_match_profile.match_result
            is not self.match_result
        ):
            raise ValueError(
                "knowledge_match_profile must reference "
                "the supplied match_result."
            )

        # ------------------------------------------------------------------
        # PHASE 4 -> PHASE 3.2 IDENTITY
        # ------------------------------------------------------------------

        if (
            self.knowledge_match_profile.enriched_match_result
            is not self.enriched_match_result
        ):
            raise ValueError(
                "knowledge_match_profile must reference "
                "the supplied enriched_match_result."
            )

        # ------------------------------------------------------------------
        # PHASE 4 -> PHASE 3.3 IDENTITY
        # ------------------------------------------------------------------

        if (
            self.knowledge_match_profile.gap_analysis_result
            is not self.gap_analysis_result
        ):
            raise ValueError(
                "knowledge_match_profile must reference "
                "the supplied gap_analysis_result."
            )

        # ------------------------------------------------------------------
        # PHASE 5 REQUEST -> PHASE 4 IDENTITY
        # ------------------------------------------------------------------

        if (
            self.ats_analysis_request.knowledge_match_profile
            is not self.knowledge_match_profile
        ):
            raise ValueError(
                "ats_analysis_request must reference "
                "the supplied knowledge_match_profile."
            )

        # ------------------------------------------------------------------
        # PHASE 5 REQUEST -> RESUME SOURCE IDENTITY
        # ------------------------------------------------------------------

        if (
            self.ats_analysis_request.resume_profile
            is not self.resume_result.document_profile
        ):
            raise ValueError(
                "ats_analysis_request must reference "
                "the resume_result.document_profile."
            )

        # ------------------------------------------------------------------
        # PHASE 5 REQUEST -> JD REQUIREMENT IDENTITY
        # ------------------------------------------------------------------

        if (
            self.ats_analysis_request.jd_requirement_profile
            is not self.jd_result.jd_requirement_profile
        ):
            raise ValueError(
                "ats_analysis_request must reference "
                "the jd_result.jd_requirement_profile."
            )

        # ------------------------------------------------------------------
        # PHASE 5 RESULT -> REQUEST IDENTITY
        # ------------------------------------------------------------------

        if (
            self.ats_analysis_result.request
            is not self.ats_analysis_request
        ):
            raise ValueError(
                "ats_analysis_result must reference "
                "the supplied ats_analysis_request."
            )

        # ------------------------------------------------------------------
        # PHASE 5 RESULT -> PHASE 4 IDENTITY
        # ------------------------------------------------------------------

        if (
            self.ats_analysis_result.knowledge_match_profile
            is not self.knowledge_match_profile
        ):
            raise ValueError(
                "ats_analysis_result must preserve "
                "the exact Phase 4 KnowledgeMatchProfile."
            )

        # ------------------------------------------------------------------
        # PHASE 6 RESULT -> PHASE 5 IDENTITY
        # ------------------------------------------------------------------

        if (
            self.recommendation_result.ats_result
            is not self.ats_analysis_result
        ):
            raise ValueError(
                "recommendation_result must preserve "
                "the exact Phase 5 ATSResumeAnalysisResult."
            )

        # ------------------------------------------------------------------
        # PHASE 6 RESULT -> PHASE 4 IDENTITY
        # ------------------------------------------------------------------

        if (
            self.recommendation_result.knowledge_match_profile
            is not self.knowledge_match_profile
        ):
            raise ValueError(
                "recommendation_result must preserve "
                "the exact Phase 4 KnowledgeMatchProfile."
            )

        # ------------------------------------------------------------------
        # PHASE 6 INTERNAL VALIDATION
        # ------------------------------------------------------------------

        self.recommendation_result.validate()

    # =========================================================================
    # PHASE 3.1 CONVENIENCE PROPERTIES
    # =========================================================================

    @property
    def total_requirements(self) -> int:
        """Return total JD requirements evaluated by Phase 3.1."""

        return self.match_result.total_requirements

    @property
    def matched_count(self) -> int:
        """Return fully matched requirement count."""

        return self.match_result.matched_count

    @property
    def partial_count(self) -> int:
        """Return partially matched requirement count."""

        return self.match_result.partial_count

    @property
    def unmatched_count(self) -> int:
        """Return unmatched requirement count."""

        return self.match_result.unmatched_count

    @property
    def overall_score(self) -> float:
        """Return overall requirement matching score."""

        return self.match_result.overall_score

    @property
    def confidence(self) -> float:
        """Return Phase 3.1 matching confidence."""

        return self.match_result.confidence

    # =========================================================================
    # PHASE 3.2 CONVENIENCE PROPERTIES
    # =========================================================================

    @property
    def evidence_backed_count(self) -> int:
        """Return the number of requirement matches supported by evidence."""

        return self.enriched_match_result.evidence_backed_count

    @property
    def enrichment_confidence(self) -> float:
        """Return Phase 3.2 enrichment confidence."""

        return self.enriched_match_result.enrichment_confidence

    # =========================================================================
    # PHASE 3.3 CONVENIENCE PROPERTIES
    # =========================================================================

    @property
    def gap_count(self) -> int:
        """Return the total number of requirements with a gap."""

        return (
            self.gap_analysis_result.partial_gap_count
            + self.gap_analysis_result.full_gap_count
        )

    @property
    def no_gap_count(self) -> int:
        """Return the number of requirements without a gap."""

        return self.gap_analysis_result.no_gap_count

    @property
    def partial_gap_count(self) -> int:
        """Return the number of partially covered requirements."""

        return self.gap_analysis_result.partial_gap_count

    @property
    def full_gap_count(self) -> int:
        """Return the number of fully uncovered requirements."""

        return self.gap_analysis_result.full_gap_count

    @property
    def gap_coverage_score(self) -> float:
        """Return the Phase 3.3 requirement coverage score."""

        return self.gap_analysis_result.gap_coverage_score

    @property
    def gap_analysis_confidence(self) -> float:
        """Return Phase 3.3 gap analysis confidence."""

        return self.gap_analysis_result.confidence

    # =========================================================================
    # PHASE 4 CONVENIENCE PROPERTIES
    # =========================================================================

    @property
    def knowledge_match_profile_confidence(self) -> float:
        """Return the Phase 4 KnowledgeMatchProfile confidence."""

        return self.knowledge_match_profile.confidence

    # =========================================================================
    # PHASE 5 CONVENIENCE PROPERTIES
    # =========================================================================

    @property
    def ats_analysis(self) -> ATSResumeAnalysisResult:
        """
        Convenience alias for ats_analysis_result.
        """

        return self.ats_analysis_result

    @property
    def ats_score(self) -> float:
        """Return the final normalized Phase 5 ATS score."""

        return self.ats_analysis_result.ats_score.score

    @property
    def ats_confidence(self) -> float:
        """Return Phase 5 ATS analysis confidence."""

        return self.ats_analysis_result.confidence

    @property
    def ats_keyword_coverage_score(self) -> float:
        """Return the Phase 5 keyword coverage score."""

        return (
            self.ats_analysis_result
            .keyword_analysis
            .keyword_coverage_score
        )

    @property
    def ats_parseability_score(self) -> float:
        """Return the Phase 5 parseability score."""

        return (
            self.ats_analysis_result
            .parseability_analysis
            .parseability_score
        )

    # =========================================================================
    # PHASE 6 CONVENIENCE PROPERTIES
    # =========================================================================

    @property
    def recommendations(self):
        """
        Return the typed Phase 6 recommendations.

        The RecommendationResult remains the authoritative owner of
        recommendation state.
        """

        return self.recommendation_result.recommendations

    @property
    def recommendation_summary(self):
        """
        Return the authoritative Phase 6 recommendation summary.
        """

        return self.recommendation_result.summary

    @property
    def has_recommendations(self) -> bool:
        """
        Return True when Phase 6 produced one or more recommendations.
        """

        return self.recommendation_result.has_recommendations

    @property
    def high_priority_recommendations(self):
        """
        Return the Phase 6 high-priority recommendations.
        """

        return (
            self.recommendation_result
            .high_priority_recommendations()
        )

    @property
    def recommendation_confidence(self) -> float:
        """
        Return the authoritative Phase 6 confidence.

        Phase 6 does not invent a new independent confidence value;
        RecommendationResult delegates confidence to the exact Phase 5
        ATS result.
        """

        return self.recommendation_result.confidence


# ============================================================================
# PUBLIC EXPORTS
# ============================================================================

__all__ = [
    "ProjectPipelineResult",
    "ProjectMatchResult",
]