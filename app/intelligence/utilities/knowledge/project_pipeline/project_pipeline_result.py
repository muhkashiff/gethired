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
        through the complete Phase 3 pipeline and consolidated
        into the Phase 4 KnowledgeMatchProfile.


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


    Complete Phase 3
            ↓
        ProjectMatchResult


Phase 4
-------

    ProjectMatchResult
            |
            +-- KnowledgeMatchProfile


Architecture
------------

Single document:

    DocumentInput
        ↓
    ProjectPipeline
        ↓
    ProjectPipelineResult


Complete matching:

    ProjectPipelineResult [RESUME]
                +
    ProjectPipelineResult [JD]
                ↓
          ProjectPipeline.match()
                ↓
        Phase 3.1 KnowledgeMatcher
                ↓
        KnowledgeMatchResult
                ↓
        Phase 3.2 KnowledgeMatchEnricher
                ↓
        EnrichedKnowledgeMatchResult
                ↓
        Phase 3.3 GapAnalyzer
                ↓
        KnowledgeGapAnalysisResult
                ↓
        Phase 4 KnowledgeMatchProfile
                ↓
        ProjectMatchResult


Design principles
-----------------

1. ProjectPipeline remains the application orchestration boundary.

2. Individual intelligence modules remain responsible for their own work.

3. ProjectMatchResult preserves every major Phase 3 boundary.

4. No Phase 3 result is silently discarded.

5. Phase 4 can consume ProjectMatchResult without having to rerun
   matching, enrichment, or gap analysis.

6. The original KnowledgeMatchResult remains available for traceability.

7. The original EnrichedKnowledgeMatchResult remains available for
   evidence-level inspection.

8. Gap analysis remains a Phase 3.3 concern and is attached to the
   complete ProjectMatchResult.

9. KnowledgeMatchProfile remains the Phase 4 consolidated representation.

10. ProjectMatchResult exposes Phase 4 profile metrics through convenience
    properties without recalculating them.
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
# PROJECT PIPELINE RESULT
# ============================================================================


@dataclass(frozen=True)
class ProjectPipelineResult:
    """
    Complete result of processing one document.

    This is the Phase 1 + Phase 2 application boundary.

    ------------------------------------------------------------------------
    Resume
    ------------------------------------------------------------------------

        DocumentInput
            ↓
        ProjectPipelineResult
            └── document_profile


    ------------------------------------------------------------------------
    Job Description
    ------------------------------------------------------------------------

        DocumentInput
            ↓
        ProjectPipelineResult
            ├── document_profile
            └── jd_requirement_profile


    Object In
        DocumentInput


    Object Out
        ProjectPipelineResult


    Important
    ---------

    Gap analysis does NOT belong here.

    Gap analysis requires both:

        Resume
        +
        JD
        +
        Phase 3.1 match
        +
        Phase 3.2 enrichment

    Therefore Phase 3.3 belongs to ProjectMatchResult.
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
        """
        Return True when this result represents a resume.
        """

        return (
            self.document_input.document_type
            == DocumentType.RESUME
        )

    @property
    def is_jd(self) -> bool:
        """
        Return True when this result represents a job description.
        """

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

    This object preserves the complete Phase 3 chain and the Phase 4
    KnowledgeMatchProfile.

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

    def __post_init__(self) -> None:
        """
        Validate the complete Phase 3 -> Phase 4 source chain.
        """

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

    # =========================================================================
    # PHASE 3.1 CONVENIENCE PROPERTIES
    # =========================================================================

    @property
    def total_requirements(self) -> int:
        """
        Return total JD requirements evaluated by Phase 3.1.
        """

        return self.match_result.total_requirements

    @property
    def matched_count(self) -> int:
        """
        Return fully matched requirement count.
        """

        return self.match_result.matched_count

    @property
    def partial_count(self) -> int:
        """
        Return partially matched requirement count.
        """

        return self.match_result.partial_count

    @property
    def unmatched_count(self) -> int:
        """
        Return unmatched requirement count.
        """

        return self.match_result.unmatched_count

    @property
    def overall_score(self) -> float:
        """
        Return overall requirement matching score.
        """

        return self.match_result.overall_score

    @property
    def confidence(self) -> float:
        """
        Return Phase 3.1 matching confidence.
        """

        return self.match_result.confidence

    # =========================================================================
    # PHASE 3.2 CONVENIENCE PROPERTIES
    # =========================================================================

    @property
    def evidence_backed_count(self) -> int:
        """
        Return the number of requirement matches supported by evidence.
        """

        return (
            self.enriched_match_result.evidence_backed_count
        )

    @property
    def enrichment_confidence(self) -> float:
        """
        Return Phase 3.2 enrichment confidence.
        """

        return (
            self.enriched_match_result.enrichment_confidence
        )

    # =========================================================================
    # PHASE 3.3 CONVENIENCE PROPERTIES
    # =========================================================================

    @property
    def gap_count(self) -> int:
        """
        Return the total number of requirements with a gap.

        A gap is either:

            PARTIAL
            FULL

        The authoritative Phase 3.3 counters remain owned by
        KnowledgeGapAnalysisResult.
        """

        return (
            self.gap_analysis_result.partial_gap_count
            + self.gap_analysis_result.full_gap_count
        )

    @property
    def no_gap_count(self) -> int:
        """
        Return the number of requirements without a gap.
        """

        return self.gap_analysis_result.no_gap_count

    @property
    def partial_gap_count(self) -> int:
        """
        Return the number of partially covered requirements.
        """

        return self.gap_analysis_result.partial_gap_count

    @property
    def full_gap_count(self) -> int:
        """
        Return the number of fully uncovered requirements.
        """

        return self.gap_analysis_result.full_gap_count

    @property
    def gap_coverage_score(self) -> float:
        """
        Return the Phase 3.3 requirement coverage score.
        """

        return self.gap_analysis_result.gap_coverage_score

    @property
    def gap_analysis_confidence(self) -> float:
        """
        Return Phase 3.3 gap analysis confidence.
        """

        return self.gap_analysis_result.confidence

    # =========================================================================
    # PHASE 4 CONVENIENCE PROPERTIES
    # =========================================================================

    @property
    def knowledge_match_profile_confidence(self) -> float:
        """
        Return the Phase 4 KnowledgeMatchProfile confidence.

        This is a direct exposure of the profile's public ``confidence``
        contract. No confidence value is recalculated here.
        """

        return self.knowledge_match_profile.confidence


# ============================================================================
# PUBLIC EXPORTS
# ============================================================================


__all__ = [
    "ProjectPipelineResult",
    "ProjectMatchResult",
]