"""
Project Pipeline
================

Complete application orchestration pipeline for the Resume Customizer.

The pipeline is intentionally incremental. At the current milestone it
integrates the real shared document/knowledge pipeline through Phase 2:

    DocumentInput
        -> DocumentProcessingService
        -> KnowledgePipelineResponse
        -> DocumentProfileBuilder
        -> DocumentKnowledgeProfile
        -> JDRequirementClassifier (JD only)

Future phases will extend this same pipeline rather than creating separate
pipelines. The existing EnterpriseResumePipeline remains untouched.

Current endpoint:

    RESUME -> DocumentKnowledgeProfile

    JD     -> DocumentKnowledgeProfile
             +
             JDRequirementProfile

The returned ProjectPipelineResult retains every intermediate object so that
integration tests and later phases can inspect the exact objects crossing
module boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

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

from app.intelligence.utilities.knowledge.documents.document_profile_builder import (
    DocumentProfileBuilder,
)

from app.intelligence.utilities.knowledge.documents.document_processing.document_processing_service import (
    DocumentProcessingService,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_request import (
    KnowledgePipelineRequest,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_response import (
    KnowledgePipelineResponse,
)

from app.intelligence.utilities.knowledge.jd_requirements.requirement_classifier import (
    JDRequirementClassifier,
)

from app.intelligence.utilities.knowledge.jd_requirements.requirement_models import (
    JDRequirementProfile,
)


# ============================================================================
# PROJECT PIPELINE RESULT
# ============================================================================


@dataclass(frozen=True)
class ProjectPipelineResult:
    """
    All currently available checkpoints of project_pipeline.

    The purpose of retaining every object is diagnostic visibility.

    Instead of only receiving:

        final_result

    we retain:

        DocumentInput
        RoutedDocument
        KnowledgePipelineRequest
        KnowledgePipelineResponse
        DocumentKnowledgeProfile
        JDRequirementProfile

    This allows later phases to be attached without losing visibility into
    earlier pipeline boundaries.
    """

    document_input: DocumentInput

    routed_document: RoutedDocument

    pipeline_request: KnowledgePipelineRequest

    pipeline_response: KnowledgePipelineResponse

    document_profile: DocumentKnowledgeProfile

    jd_requirement_profile: Optional[
        JDRequirementProfile
    ] = None

    # ------------------------------------------------------------------
    # Convenience properties
    # ------------------------------------------------------------------

    @property
    def is_resume(self) -> bool:
        """
        Return True when this pipeline execution processed a resume.
        """

        return (
            self.document_input.document_type
            == DocumentType.RESUME
        )

    @property
    def is_jd(self) -> bool:
        """
        Return True when this pipeline execution processed a JD.
        """

        return (
            self.document_input.document_type
            == DocumentType.JD
        )

    @property
    def knowledge_profile(self) -> Any:
        """
        Return the underlying Enterprise KnowledgeProfile.

        This is intentionally the original profile wrapped by
        DocumentKnowledgeProfile.
        """

        return self.document_profile.profile


# ============================================================================
# PROJECT PIPELINE
# ============================================================================


class ProjectPipeline:
    """
    Complete project orchestration boundary.

    At the current milestone this class connects:

        DocumentInput
            ↓
        DocumentProcessingService
            ↓
        KnowledgePipelineResponse
            ↓
        DocumentProfileBuilder
            ↓
        DocumentKnowledgeProfile
            ↓
        JDRequirementClassifier [JD only]

    This class does not reimplement:

        - document extraction
        - entity extraction
        - semantic resolution
        - knowledge graph construction
        - KnowledgeProfile construction

    It composes existing project modules.
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
    ) -> None:
        """
        Initialize the project pipeline.

        Dependencies remain injectable so the orchestration layer can be
        tested independently when necessary.
        """

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

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def process(
        self,
        document: DocumentInput,
    ) -> ProjectPipelineResult:
        """
        Run one document through the current project pipeline.

        Object In
        ---------
        DocumentInput

        Object Out
        ----------
        ProjectPipelineResult
        """

        if not isinstance(
            document,
            DocumentInput,
        ):
            raise TypeError(
                "ProjectPipeline.process() expects "
                "a DocumentInput object."
            )

        # =================================================================
        # STEP 1
        # EXISTING DOCUMENT PROCESSING PIPELINE
        # =================================================================

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

        # =================================================================
        # STEP 2
        # RETAIN ROUTING OBJECT
        # =================================================================
        #
        # DocumentProcessingService internally creates these objects.
        #
        # At this stage the service does not expose its internal checkpoints,
        # therefore we reconstruct the immutable boundary objects from the
        # same validated input for diagnostic retention.
        #
        # No intelligence is performed here.
        # =================================================================

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

        # =================================================================
        # STEP 3
        # BUILD DOCUMENT-AWARE PROFILE
        # =================================================================

        document_profile = (
            self.profile_builder.build(
                response
            )
        )

        # =================================================================
        # STEP 4
        # PHASE 2 JD INTERPRETATION
        # =================================================================

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

        # =================================================================
        # STEP 5
        # RETURN COMPLETE CURRENT PIPELINE RESULT
        # =================================================================

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
    Convenience entry point for project_pipeline.

    Example
    -------

        result = project_pipeline(
            text=resume_text,
            document_type=DocumentType.RESUME,
        )
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
# PUBLIC EXPORTS
# ============================================================================


__all__ = [
    "ProjectPipeline",
    "ProjectPipelineResult",
    "project_pipeline",
]