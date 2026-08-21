"""
Document Processing Service
===========================

Application-level orchestration service for document processing.

Architecture:

DocumentInput
      ↓
DocumentProcessingService
      ↓
DocumentRouter
      ↓
RoutedDocument
      ↓
KnowledgePipelineRequest
      ↓
KnowledgePipelineAdapter
      ↓
KnowledgePipelineResponse

IMPORTANT
---------
This service orchestrates existing objects.

It does NOT perform:
- extraction
- semantic reasoning
- entity resolution
- business statement generation
- graph construction
- profile construction
"""

from app.intelligence.utilities.knowledge.documents.document_input import (
    DocumentInput,
)

from app.intelligence.utilities.knowledge.documents.document_router import (
    DocumentRouter,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_request import (
    KnowledgePipelineRequest,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_response import (
    KnowledgePipelineResponse,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_adapter import (
    KnowledgePipelineAdapter,
)


class DocumentProcessingService:
    """
    Coordinates document routing and knowledge processing.

    Object In
        DocumentInput

    Object Out
        KnowledgePipelineResponse
    """

    def __init__(
        self,
        router=None,
        pipeline_adapter=None,
    ) -> None:
        """
        Initialize the processing service.

        Dependencies are injectable so the service can be
        unit tested without executing the real Knowledge Pipeline.
        """

        self.router = (
            router
            if router is not None
            else DocumentRouter()
        )

        self.pipeline_adapter = (
            pipeline_adapter
            if pipeline_adapter is not None
            else KnowledgePipelineAdapter()
        )

    def process(
        self,
        document: DocumentInput,
    ) -> KnowledgePipelineResponse:
        """
        Process one document through the document-processing
        architecture.

        Object In
            DocumentInput

        Object Out
            KnowledgePipelineResponse
        """

        if not isinstance(
            document,
            DocumentInput,
        ):
            raise TypeError(
                "DocumentProcessingService.process() "
                "expects a DocumentInput object."
            )

        # ------------------------------------------------------
        # STEP 1
        # Route document
        # ------------------------------------------------------

        routed_document = self.router.process(
            document
        )

        # ------------------------------------------------------
        # STEP 2
        # Convert routed document into pipeline request
        # ------------------------------------------------------

        pipeline_request = KnowledgePipelineRequest(
            document_text=routed_document.text,
            document_type=routed_document.document_type,
        )

        # ------------------------------------------------------
        # STEP 3
        # Execute existing Knowledge Pipeline
        # ------------------------------------------------------

        pipeline_response = self.pipeline_adapter.process(
            pipeline_request
        )

        # ------------------------------------------------------
        # STEP 4
        # Return standardized response
        # ------------------------------------------------------

        return pipeline_response