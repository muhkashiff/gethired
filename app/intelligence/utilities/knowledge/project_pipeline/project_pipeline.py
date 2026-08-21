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

ProjectPipeline remains the single application orchestration boundary.

Individual intelligence modules remain responsible for their own work.

This module only composes those modules.
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

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_response import (
    KnowledgePipelineResponse,
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
    ) -> None:

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

        self.jd_requirement_classifier = (
            jd_requirement_classifier
            if jd_requirement_classifier is not None
            else JDRequirementClassifier()
        )

        self.knowledge_matcher = (
            knowledge_matcher
            if knowledge_matcher is not None
            else KnowledgeMatcher()
        )

        self.knowledge_match_enricher = (
            knowledge_match_enricher
            if knowledge_match_enricher is not None
            else KnowledgeMatchEnricher()
        )

        self.gap_analyzer = (
            gap_analyzer
            if gap_analyzer is not None
            else KnowledgeGapAnalyzer()
        )

        self.knowledge_match_profile_builder = (
            knowledge_match_profile_builder
            if knowledge_match_profile_builder is not None
            else KnowledgeMatchProfileBuilder()
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

        if not isinstance(
            document,
            DocumentInput,
        ):
            raise TypeError(
                "ProjectPipeline.process() expects "
                "a DocumentInput object."
            )

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

        routed_document = RoutedDocument(
            text=document.text.strip(),
            document_type=document.document_type,
        )

        pipeline_request = KnowledgePipelineRequest(
            document_text=(
                routed_document.text
            ),
            document_type=(
                routed_document.document_type
            ),
        )

        document_profile = (
            self.profile_builder.build(
                response
            )
        )

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

        return ProjectPipelineResult(
            document_input=document,

            routed_document=routed_document,

            pipeline_request=pipeline_request,

            pipeline_response=response,

            document_profile=document_profile,

            jd_requirement_profile=(
                jd_requirement_profile
            ),
        )

    # =========================================================================
    # PHASE 3 + PHASE 4
    # =========================================================================

    def match(
        self,
        resume_result: ProjectPipelineResult,
        jd_result: ProjectPipelineResult,
    ) -> ProjectMatchResult:
        """
        Execute the complete Phase 3 + Phase 4 pipeline.

        Phase 3.1
            KnowledgeMatchResult

        Phase 3.2
            EnrichedKnowledgeMatchResult

        Phase 3.3
            KnowledgeGapAnalysisResult

        Phase 4
            KnowledgeMatchProfile
        """

        # =================================================================
        # VALIDATE RESUME
        # =================================================================

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

        # =================================================================
        # VALIDATE JD
        # =================================================================

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

        # =================================================================
        # REQUIRE PHASE 2
        # =================================================================

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

        # =================================================================
        # PHASE 3.1
        # =================================================================

        match_request = KnowledgeMatchRequest(
            resume_profile=(
                resume_result.document_profile
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

        # =================================================================
        # PHASE 3.2
        # =================================================================

        enriched_match_result = (
            self.knowledge_match_enricher.process(
                match_result=match_result,
                resume_profile=(
                    resume_result.document_profile
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

        # =================================================================
        # PHASE 3.3
        # =================================================================

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

        # =================================================================
        # PHASE 4
        # =================================================================
        #
        # IMPORTANT:
        #
        # The exact objects generated by Phases 3.1, 3.2 and 3.3 are passed
        # directly into Phase 4.
        #
        # Phase 4 does not rerun any intelligence.
        # =================================================================

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

        # =================================================================
        # FINAL SOURCE IDENTITY VALIDATION
        # =================================================================

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

        # =================================================================
        # RETURN COMPLETE PROJECT RESULT
        # =================================================================

        return ProjectMatchResult(
            resume_result=resume_result,

            jd_result=jd_result,

            match_request=match_request,

            match_result=match_result,

            enriched_match_result=(
                enriched_match_result
            ),

            gap_analysis_result=(
                gap_analysis_result
            ),

            knowledge_match_profile=(
                knowledge_match_profile
            ),
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


__all__ = [
    "ProjectPipeline",
    "ProjectPipelineResult",
    "ProjectMatchResult",
    "project_pipeline",
]