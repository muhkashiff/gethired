"""
Project Pipeline
================

Complete application orchestration pipeline for the Resume Customizer.

Current phases:

    Phase 1
        DocumentInput
            ->
        DocumentKnowledgeProfile

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
        KnowledgeMatchResult
            +
        EnrichedKnowledgeMatchResult
            +
        KnowledgeGapAnalysisResult
            ->
        KnowledgeMatchProfile

    Phase 5
        KnowledgeMatchProfile
            +
        original Resume source
            +
        ATSAnalysisPolicy
            ->
        ATSResumeAnalysisRequest
            ->
        ATSResumeAnalysisResult

ProjectPipeline remains the single application orchestration boundary.

Individual intelligence modules remain responsible for their own work.

This module only composes those modules.

IMPORTANT PHASE 5 CONTRACT
--------------------------

ATSResumeAnalysisRequest now exposes exactly these constructor fields:

    resume_text
    knowledge_match_profile
    resume_profile        # Phase 1 resume profile
    jd_requirement_profile # Phase 2 JD profile
    metadata

The policy is owned by the analyzer and the pipeline, but it is NOT part
of the request object.  The request carries the source text and the
Phase 4 profile; the policy is supplied separately to the analyzer.

The Phase 1 resume DocumentKnowledgeProfile and Phase 2
JDRequirementProfile are preserved both as explicit fields and inside
request.metadata for traceability.

The authoritative original resume source is passed through the actual
resume_text field of ATSResumeAnalysisRequest.

The exact Phase 4 KnowledgeMatchProfile is passed through the actual
knowledge_match_profile field.
"""

from __future__ import annotations

from typing import Optional


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

from app.intelligence.utilities.knowledge.documents.document_profile_builder import (
    DocumentProfileBuilder,
)

from app.intelligence.utilities.knowledge.documents.document_processing.document_processing_service import (
    DocumentProcessingService,
)


# ============================================================================
# KNOWLEDGE PIPELINE LAYER
# ============================================================================

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_request import (
    KnowledgePipelineRequest,
)


# ============================================================================
# JD REQUIREMENT LAYER
# ============================================================================

from app.intelligence.utilities.knowledge.jd_requirements.requirement_classifier import (
    JDRequirementClassifier,
)

from app.intelligence.utilities.knowledge.jd_requirements.requirement_models import (
    JDRequirementProfile,
)


# ============================================================================
# PHASE 3.1
# ============================================================================

from app.intelligence.utilities.knowledge.matching.knowledge_matcher import (
    KnowledgeMatcher,
)

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchRequest,
    KnowledgeMatchResult,
)


# ============================================================================
# PHASE 3.2
# ============================================================================

from app.intelligence.utilities.knowledge.matching.match_enricher import (
    KnowledgeMatchEnricher,
)

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
)


# ============================================================================
# PHASE 3.3
# ============================================================================

from app.intelligence.utilities.knowledge.matching.gap_analyzer import (
    KnowledgeGapAnalyzer,
)

from app.intelligence.utilities.knowledge.matching.gap_models import (
    KnowledgeGapAnalysisResult,
)


# ============================================================================
# PHASE 4
# ============================================================================

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_builder import (
    KnowledgeMatchProfileBuilder,
)

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeMatchProfile,
)


# ============================================================================
# PHASE 5
# ============================================================================

from app.intelligence.utilities.knowledge.ats.ats_analysis_request import (
    ATSResumeAnalysisRequest,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSResumeAnalysisResult,
)

from app.intelligence.utilities.knowledge.ats.ats_resume_analyzer import (
    ATSResumeAnalyzer,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_policy import (
    ATSAnalysisPolicy,
)


# ============================================================================
# PROJECT RESULT LAYER
# ============================================================================

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline_result import (
    ProjectPipelineResult,
    ProjectMatchResult,
)


# ============================================================================
# PROJECT PIPELINE
# ============================================================================


class ProjectPipeline:
    """
    Complete application orchestration boundary.

    process()
        DocumentInput
            ->
        ProjectPipelineResult

    match()
        ProjectPipelineResult [RESUME]
            +
        ProjectPipelineResult [JD]
            ->
        Phase 3.1
            ->
        Phase 3.2
            ->
        Phase 3.3
            ->
        Phase 4
            ->
        Phase 5
            ->
        ProjectMatchResult
    """

    def __init__(
        self,
        processing_service: Optional[
            DocumentProcessingService
        ] = None,
        profile_builder: Optional[
            DocumentProfileBuilder
        ] = None,
        jd_requirement_classifier: Optional[
            JDRequirementClassifier
        ] = None,
        knowledge_matcher: Optional[
            KnowledgeMatcher
        ] = None,
        knowledge_match_enricher: Optional[
            KnowledgeMatchEnricher
        ] = None,
        gap_analyzer: Optional[
            KnowledgeGapAnalyzer
        ] = None,
        knowledge_match_profile_builder: Optional[
            KnowledgeMatchProfileBuilder
        ] = None,
        ats_resume_analyzer: Optional[
            ATSResumeAnalyzer
        ] = None,
        ats_analysis_policy: Optional[
            ATSAnalysisPolicy
        ] = None,
    ) -> None:

        # =====================================================================
        # DOCUMENT SERVICES
        # =====================================================================

        self.processing_service = (
            processing_service
            if processing_service is not None
            else DocumentProcessingService()
        )

        self.profile_builder = (
            profile_builder
            if profile_builder is not None
            else DocumentProfileBuilder()
        )

        # =====================================================================
        # PHASE 2
        # =====================================================================

        self.jd_requirement_classifier = (
            jd_requirement_classifier
            if jd_requirement_classifier is not None
            else JDRequirementClassifier()
        )

        # =====================================================================
        # PHASE 3.1
        # =====================================================================

        self.knowledge_matcher = (
            knowledge_matcher
            if knowledge_matcher is not None
            else KnowledgeMatcher()
        )

        # =====================================================================
        # PHASE 3.2
        # =====================================================================

        self.knowledge_match_enricher = (
            knowledge_match_enricher
            if knowledge_match_enricher is not None
            else KnowledgeMatchEnricher()
        )

        # =====================================================================
        # PHASE 3.3
        # =====================================================================

        self.gap_analyzer = (
            gap_analyzer
            if gap_analyzer is not None
            else KnowledgeGapAnalyzer()
        )

        # =====================================================================
        # PHASE 4
        # =====================================================================

        self.knowledge_match_profile_builder = (
            knowledge_match_profile_builder
            if knowledge_match_profile_builder is not None
            else KnowledgeMatchProfileBuilder()
        )

        # =====================================================================
        # PHASE 5
        # =====================================================================
        #
        # The policy is owned by the pipeline and analyzer.  It is NOT part of
        # the ATSResumeAnalysisRequest.  The request only carries the source
        # text and the Phase 4 profile.  The policy is used by the analyzer.
        #
        # If an ATSResumeAnalyzer is injected, we use its policy.  Otherwise,
        # we create a default policy and a corresponding analyzer.
        # =====================================================================

        if (
            ats_resume_analyzer is not None
            and ats_analysis_policy is not None
        ):
            raise ValueError(
                "Provide either ats_resume_analyzer or "
                "ats_analysis_policy, not both."
            )

        if ats_resume_analyzer is not None:

            self.ats_resume_analyzer = (
                ats_resume_analyzer
            )

            analyzer_policy = getattr(
                ats_resume_analyzer,
                "policy",
                None,
            )

            if not isinstance(
                analyzer_policy,
                ATSAnalysisPolicy,
            ):
                raise TypeError(
                    "An injected ATSResumeAnalyzer must expose "
                    "a valid ATSAnalysisPolicy through its "
                    "'policy' attribute when no explicit "
                    "ats_analysis_policy is supplied."
                )

            self.ats_analysis_policy = (
                analyzer_policy
            )

        else:

            self.ats_analysis_policy = (
                ats_analysis_policy
                if ats_analysis_policy is not None
                else ATSAnalysisPolicy()
            )

            self.ats_resume_analyzer = (
                ATSResumeAnalyzer(
                    policy=self.ats_analysis_policy,
                )
            )

        # =====================================================================
        # FINAL POLICY VALIDATION
        # =====================================================================

        if not isinstance(
            self.ats_analysis_policy,
            ATSAnalysisPolicy,
        ):
            raise TypeError(
                "ProjectPipeline requires a valid "
                "ATSAnalysisPolicy for Phase 5."
            )

    # =========================================================================
    # PHASE 1 + PHASE 2
    # =========================================================================

    def process(
        self,
        document: DocumentInput,
    ) -> ProjectPipelineResult:
        """
        Process one document through Phase 1 and Phase 2.
        """

        # =====================================================================
        # VALIDATE INPUT
        # =====================================================================

        if not isinstance(
            document,
            DocumentInput,
        ):
            raise TypeError(
                "ProjectPipeline.process() expects "
                "a DocumentInput object."
            )

        # =====================================================================
        # DOCUMENT PROCESSING
        # =====================================================================

        response = (
            self.processing_service.process(
                document
            )
        )

        if not response.success:

            message = (
                response.error
                or "Knowledge Pipeline failed."
            )

            raise RuntimeError(
                message
            )

        # =====================================================================
        # ROUTED DOCUMENT
        # =====================================================================

        routed_document = RoutedDocument(
            text=document.text.strip(),
            document_type=document.document_type,
        )

        # =====================================================================
        # KNOWLEDGE PIPELINE REQUEST
        # =====================================================================

        pipeline_request = KnowledgePipelineRequest(
            document_text=routed_document.text,
            document_type=routed_document.document_type,
        )

        # =====================================================================
        # DOCUMENT KNOWLEDGE PROFILE
        # =====================================================================

        document_profile = (
            self.profile_builder.build(
                response
            )
        )

        # =====================================================================
        # PHASE 2 JD REQUIREMENT PROFILE
        # =====================================================================

        jd_requirement_profile = None

        if (
            document.document_type
            == DocumentType.JD
        ):

            jd_requirement_profile = (
                self.jd_requirement_classifier.process(
                    document_profile
                )
            )

            if not isinstance(
                jd_requirement_profile,
                JDRequirementProfile,
            ):
                raise TypeError(
                    "JDRequirementClassifier.process() "
                    "must return a JDRequirementProfile."
                )

        # =====================================================================
        # PROJECT PIPELINE RESULT
        # =====================================================================

        return ProjectPipelineResult(
            document_input=document,
            routed_document=routed_document,
            pipeline_request=pipeline_request,
            pipeline_response=response,
            document_profile=document_profile,
            jd_requirement_profile=jd_requirement_profile,
        )

    # =========================================================================
    # PHASE 3 + PHASE 4 + PHASE 5
    # =========================================================================

    def match(
        self,
        resume_result: ProjectPipelineResult,
        jd_result: ProjectPipelineResult,
    ) -> ProjectMatchResult:
        """
        Execute the complete resume-to-JD intelligence pipeline.

        Phase 3.1
            KnowledgeMatchResult

        Phase 3.2
            EnrichedKnowledgeMatchResult

        Phase 3.3
            KnowledgeGapAnalysisResult

        Phase 4
            KnowledgeMatchProfile

        Phase 5
            ATSResumeAnalysisRequest
                ->
            ATSResumeAnalysisResult

        Phase 5 receives:

            1. Exact original resume source text
            2. Exact Phase 4 KnowledgeMatchProfile
            3. Exact Phase 1 resume profile through metadata
            4. Exact Phase 2 JDRequirementProfile through metadata

        The ATSAnalysisPolicy is owned by the pipeline and analyzer, but it is
        NOT part of the request.  The analyzer uses its own policy.

        No Phase 3 or Phase 4 object is reconstructed.
        """

        # =====================================================================
        # VALIDATE RESUME RESULT
        # =====================================================================

        if not isinstance(
            resume_result,
            ProjectPipelineResult,
        ):
            raise TypeError(
                "ProjectPipeline.match() expects "
                "resume_result to be a ProjectPipelineResult."
            )

        if not resume_result.is_resume:
            raise TypeError(
                "ProjectPipeline.match() requires "
                "resume_result to represent a RESUME."
            )

        # =====================================================================
        # VALIDATE JD RESULT
        # =====================================================================

        if not isinstance(
            jd_result,
            ProjectPipelineResult,
        ):
            raise TypeError(
                "ProjectPipeline.match() expects "
                "jd_result to be a ProjectPipelineResult."
            )

        if not jd_result.is_jd:
            raise TypeError(
                "ProjectPipeline.match() requires "
                "jd_result to represent a JD."
            )

        # =====================================================================
        # VALIDATE ORIGINAL RESUME SOURCE
        # =====================================================================
        #
        # This is the authoritative Phase 5 source.
        #
        # It comes directly from the original DocumentInput.
        #
        # We deliberately do NOT reconstruct it from:
        #
        #     document_profile
        #     knowledge_match_profile
        #     enriched_match_result
        #
        # =====================================================================

        resume_text = (
            resume_result.document_input.text
        )

        if not isinstance(
            resume_text,
            str,
        ):
            raise TypeError(
                "ProjectPipeline.match() requires "
                "resume_result.document_input.text "
                "to be a string."
            )

        if not resume_text.strip():
            raise ValueError(
                "ProjectPipeline.match() requires "
                "the resume document source to be non-empty."
            )

        # =====================================================================
        # VALIDATE RESUME DOCUMENT PROFILE
        # =====================================================================

        resume_profile = (
            resume_result.document_profile
        )

        if resume_profile is None:
            raise ValueError(
                "ProjectPipeline.match() requires "
                "the resume result to contain a "
                "DocumentKnowledgeProfile."
            )

        # =====================================================================
        # REQUIRE PHASE 2 JD PROFILE
        # =====================================================================

        jd_requirement_profile = (
            jd_result.jd_requirement_profile
        )

        if not isinstance(
            jd_requirement_profile,
            JDRequirementProfile,
        ):
            raise ValueError(
                "ProjectPipeline.match() requires "
                "the JD result to contain a "
                "JDRequirementProfile."
            )

        # =====================================================================
        # PHASE 3.1
        # =====================================================================

        match_request = KnowledgeMatchRequest(
            resume_profile=(
                resume_profile
            ),
            jd_requirement_profile=(
                jd_requirement_profile
            ),
        )

        match_result = (
            self.knowledge_matcher.process(
                match_request
            )
        )

        if not isinstance(
            match_result,
            KnowledgeMatchResult,
        ):
            raise TypeError(
                "KnowledgeMatcher.process() "
                "must return a KnowledgeMatchResult."
            )

        # =====================================================================
        # PHASE 3.2
        # =====================================================================

        enriched_match_result = (
            self.knowledge_match_enricher.process(
                match_result=match_result,
                resume_profile=(
                    resume_profile
                ),
                jd_requirement_profile=(
                    jd_requirement_profile
                ),
            )
        )

        if not isinstance(
            enriched_match_result,
            EnrichedKnowledgeMatchResult,
        ):
            raise TypeError(
                "KnowledgeMatchEnricher.process() "
                "must return an "
                "EnrichedKnowledgeMatchResult."
            )

        # =====================================================================
        # PHASE 3.3
        # =====================================================================

        gap_analysis_result = (
            self.gap_analyzer.process(
                enriched_match_result
            )
        )

        if not isinstance(
            gap_analysis_result,
            KnowledgeGapAnalysisResult,
        ):
            raise TypeError(
                "GapAnalyzer.process() "
                "must return a "
                "KnowledgeGapAnalysisResult."
            )

        # =====================================================================
        # PHASE 4
        # =====================================================================

        knowledge_match_profile = (
            self.knowledge_match_profile_builder.process(
                match_result=match_result,
                enriched_match_result=(
                    enriched_match_result
                ),
                gap_analysis_result=(
                    gap_analysis_result
                ),
            )
        )

        if not isinstance(
            knowledge_match_profile,
            KnowledgeMatchProfile,
        ):
            raise TypeError(
                "KnowledgeMatchProfileBuilder.process() "
                "must return a KnowledgeMatchProfile."
            )

        # =====================================================================
        # PHASE 4 SOURCE IDENTITY VALIDATION
        # =====================================================================

        if (
            knowledge_match_profile.match_result
            is not match_result
        ):
            raise ValueError(
                "Phase 4 KnowledgeMatchProfile must "
                "preserve the exact Phase 3.1 match_result."
            )

        if (
            knowledge_match_profile.enriched_match_result
            is not enriched_match_result
        ):
            raise ValueError(
                "Phase 4 KnowledgeMatchProfile must "
                "preserve the exact Phase 3.2 "
                "enriched_match_result."
            )

        if (
            knowledge_match_profile.gap_analysis_result
            is not gap_analysis_result
        ):
            raise ValueError(
                "Phase 4 KnowledgeMatchProfile must "
                "preserve the exact Phase 3.3 "
                "gap_analysis_result."
            )

        # =====================================================================
        # PHASE 5 POLICY
        # =====================================================================

        ats_analysis_policy = (
            self.ats_analysis_policy
        )

        if not isinstance(
            ats_analysis_policy,
            ATSAnalysisPolicy,
        ):
            raise TypeError(
                "ProjectPipeline.match() requires "
                "self.ats_analysis_policy to be an "
                "ATSAnalysisPolicy."
            )

        # =====================================================================
        # PHASE 5 METADATA
        # =====================================================================
        #
        # Metadata contains source objects that are not primary constructor
        # fields of ATSResumeAnalysisRequest.
        #
        # IMPORTANT:
        #
        # These are the EXACT objects produced earlier in the pipeline.
        #
        # No reconstruction occurs here.
        # =====================================================================

        ats_metadata = {
            # -----------------------------------------------------------------
            # AUTHORITATIVE ORIGINAL RESUME SOURCE
            # -----------------------------------------------------------------

            "resume_text": resume_text,
            "resume_source": resume_text,
            "source_text": resume_text,
            "document_text": resume_text,

            # -----------------------------------------------------------------
            # AUTHORITATIVE SOURCE TYPE
            # -----------------------------------------------------------------

            "source_document_type": (
                DocumentType.RESUME
            ),

            # -----------------------------------------------------------------
            # EXACT PHASE 1 RESUME PROFILE
            # -----------------------------------------------------------------

            "resume_profile": resume_profile,

            # -----------------------------------------------------------------
            # EXACT PHASE 2 JD REQUIREMENT PROFILE
            # -----------------------------------------------------------------

            "jd_requirement_profile": (
                jd_requirement_profile
            ),

            # -----------------------------------------------------------------
            # EXACT PHASE 4 PROFILE
            #
            # This is duplicated into metadata intentionally only for
            # traceability. The authoritative Phase 4 object is still the
            # dedicated knowledge_match_profile constructor field.
            # -----------------------------------------------------------------

            "knowledge_match_profile": (
                knowledge_match_profile
            ),

            # -----------------------------------------------------------------
            # EXACT PHASE 5 POLICY
            #
            # The policy is not part of the request's primary fields, but we
            # keep it in metadata for traceability and debugging.
            # -----------------------------------------------------------------

            "policy": ats_analysis_policy,
        }

        # =====================================================================
        # PHASE 5 METADATA VALIDATION
        # =====================================================================

        authoritative_resume_source = (
            ats_metadata.get("resume_text")
        )

        if not isinstance(
            authoritative_resume_source,
            str,
        ):
            raise TypeError(
                "Phase 5 ATS metadata must contain "
                "resume_text as a string."
            )

        if not authoritative_resume_source.strip():
            raise ValueError(
                "Phase 5 ATS metadata must contain "
                "a non-empty resume source."
            )

        # =====================================================================
        # PHASE 5 SOURCE IDENTITY VALIDATION
        # =====================================================================

        if (
            ats_metadata.get("resume_profile")
            is not resume_profile
        ):
            raise ValueError(
                "Phase 5 ATS metadata must preserve "
                "the exact resume DocumentKnowledgeProfile."
            )

        if (
            ats_metadata.get("jd_requirement_profile")
            is not jd_requirement_profile
        ):
            raise ValueError(
                "Phase 5 ATS metadata must preserve "
                "the exact JDRequirementProfile."
            )

        if (
            ats_metadata.get("knowledge_match_profile")
            is not knowledge_match_profile
        ):
            raise ValueError(
                "Phase 5 ATS metadata must preserve "
                "the exact Phase 4 KnowledgeMatchProfile."
            )

        if (
            ats_metadata.get("policy")
            is not ats_analysis_policy
        ):
            raise ValueError(
                "Phase 5 ATS metadata must preserve "
                "the exact ATSAnalysisPolicy."
            )

        # =====================================================================
        # CONSTRUCT ACTUAL PHASE 5 REQUEST
        # =====================================================================
        #
        # ATSResumeAnalysisRequest now defines:
        #
        #     resume_text
        #     knowledge_match_profile
        #     resume_profile          # Phase 1 profile
        #     jd_requirement_profile   # Phase 2 profile
        #     metadata
        #
        # The policy is NOT a constructor argument.  It is used by the
        # analyzer (which already has it) and optionally included in metadata.
        # =====================================================================

        ats_analysis_request = ATSResumeAnalysisRequest(
            resume_text=resume_text,
            knowledge_match_profile=knowledge_match_profile,
            resume_profile=resume_profile,          # explicit Phase 1 profile
            jd_requirement_profile=jd_requirement_profile,  # explicit Phase 2 profile
            metadata=ats_metadata,
        )

        # =====================================================================
        # PHASE 5 REQUEST STRUCTURAL VALIDATION
        # =====================================================================

        if not isinstance(
            ats_analysis_request,
            ATSResumeAnalysisRequest,
        ):
            raise TypeError(
                "Phase 5 must produce an "
                "ATSResumeAnalysisRequest."
            )

        # =====================================================================
        # PHASE 5 REQUEST SOURCE IDENTITY VALIDATION
        # =====================================================================

        if (
            ats_analysis_request.resume_text
            != resume_text
        ):
            raise ValueError(
                "Phase 5 request must preserve "
                "the exact original resume source text."
            )

        if (
            ats_analysis_request.knowledge_match_profile
            is not knowledge_match_profile
        ):
            raise ValueError(
                "Phase 5 request must preserve the exact "
                "Phase 4 KnowledgeMatchProfile."
            )

        # =====================================================================
        # PHASE 5 REQUEST METADATA VALIDATION
        # =====================================================================

        request_metadata = (
            ats_analysis_request.metadata
        )

        if not isinstance(
            request_metadata,
            dict,
        ):
            raise TypeError(
                "ATSResumeAnalysisRequest must expose "
                "a metadata dictionary."
            )

        if (
            request_metadata.get("resume_text")
            != resume_text
        ):
            raise ValueError(
                "Phase 5 request metadata must preserve "
                "the exact original resume source text."
            )

        if (
            request_metadata.get("resume_profile")
            is not resume_profile
        ):
            raise ValueError(
                "Phase 5 request metadata must preserve "
                "the exact resume DocumentKnowledgeProfile."
            )

        if (
            request_metadata.get("jd_requirement_profile")
            is not jd_requirement_profile
        ):
            raise ValueError(
                "Phase 5 request metadata must preserve "
                "the exact JDRequirementProfile."
            )

        if (
            request_metadata.get("knowledge_match_profile")
            is not knowledge_match_profile
        ):
            raise ValueError(
                "Phase 5 request metadata must preserve "
                "the exact Phase 4 KnowledgeMatchProfile."
            )

        if (
            request_metadata.get("policy")
            is not ats_analysis_policy
        ):
            raise ValueError(
                "Phase 5 request metadata must preserve "
                "the exact ATSAnalysisPolicy."
            )

        # =====================================================================
        # PHASE 5 ATS ANALYSIS
        # =====================================================================

        ats_analysis_result = (
            self.ats_resume_analyzer.process(
                ats_analysis_request
            )
        )

        if not isinstance(
            ats_analysis_result,
            ATSResumeAnalysisResult,
        ):
            raise TypeError(
                "ATSResumeAnalyzer.process() "
                "must return an ATSResumeAnalysisResult."
            )

        # =====================================================================
        # PHASE 5 RESULT SOURCE IDENTITY VALIDATION
        # =====================================================================

        if (
            ats_analysis_result.request
            is not ats_analysis_request
        ):
            raise ValueError(
                "Phase 5 ATS result must preserve "
                "the exact ATSResumeAnalysisRequest."
            )

        if (
            ats_analysis_result.knowledge_match_profile
            is not knowledge_match_profile
        ):
            raise ValueError(
                "Phase 5 ATS result must preserve "
                "the exact Phase 4 KnowledgeMatchProfile."
            )

        # =====================================================================
        # FINAL PROJECT RESULT
        # =====================================================================

        return ProjectMatchResult(
            resume_result=resume_result,
            jd_result=jd_result,
            match_request=match_request,
            match_result=match_result,
            enriched_match_result=enriched_match_result,
            gap_analysis_result=gap_analysis_result,
            knowledge_match_profile=knowledge_match_profile,
            ats_analysis_request=ats_analysis_request,
            ats_analysis_result=ats_analysis_result,
        )


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================


def project_pipeline(
    text: str,
    document_type: DocumentType,
    *,
    pipeline: Optional[
        ProjectPipeline
    ] = None,
) -> ProjectPipelineResult:
    """
    Convenience entry point for single-document processing.

    Matching remains explicit through:

        ProjectPipeline.match()
    """

    document = DocumentInput(
        text=text,
        document_type=document_type,
    )

    runner = (
        pipeline
        if pipeline is not None
        else ProjectPipeline()
    )

    return runner.process(
        document
    )


# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    "ProjectPipeline",
    "ProjectPipelineResult",
    "ProjectMatchResult",
    "project_pipeline",
]