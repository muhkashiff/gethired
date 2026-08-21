"""
Knowledge Pipeline Adapter
===========================

Provides the new object-oriented interface to the existing
EnterpriseResumePipeline.

IMPORTANT
---------
The existing EnterpriseResumePipeline is intentionally NOT modified.

This adapter translates:

    KnowledgePipelineRequest
            ↓
    EnterpriseResumePipeline.run(text)
            ↓
    EnterpriseResumePipelineResult
            ↓
    KnowledgePipelineResponse
"""

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_request import (
    KnowledgePipelineRequest,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_response import (
    KnowledgePipelineResponse,
)

from app.intelligence.utilities.knowledge.enterprise_resume_pipeline import (
    EnterpriseResumePipeline,
)


class KnowledgePipelineAdapter:
    """
    Object-oriented boundary around the existing Enterprise Pipeline.

    Responsibilities
    ----------------
    1. Accept KnowledgePipelineRequest.
    2. Validate the request.
    3. Call the existing pipeline.
    4. Convert its result into KnowledgePipelineResponse.

    Non-responsibilities
    --------------------
    - Knowledge extraction
    - Semantic resolution
    - Business statement generation
    - Knowledge graph construction
    - Knowledge profile construction
    """

    def __init__(
        self,
        pipeline=None,
    ) -> None:
        """
        Initialize the adapter.

        Parameters
        ----------
        pipeline:
            Optional existing EnterpriseResumePipeline instance.

        Dependency injection is used so that the adapter can be
        independently unit tested.
        """

        self.pipeline = (
            pipeline
            if pipeline is not None
            else EnterpriseResumePipeline()
        )

    def process(
        self,
        request: KnowledgePipelineRequest,
    ) -> KnowledgePipelineResponse:
        """
        Process one KnowledgePipelineRequest.

        Object In
            KnowledgePipelineRequest

        Object Out
            KnowledgePipelineResponse
        """

        if not isinstance(
            request,
            KnowledgePipelineRequest,
        ):
            raise TypeError(
                "KnowledgePipelineAdapter.process() "
                "expects a KnowledgePipelineRequest."
            )

        try:
            result = self.pipeline.run(
                request.document_text
            )

            return KnowledgePipelineResponse(
                success=bool(
                    getattr(
                        result,
                        "success",
                        False,
                    )
                ),
                document_type=request.document_type,
                result=result,
                error=getattr(
                    result,
                    "error",
                    None,
                ),
            )

        except Exception as exc:

            return KnowledgePipelineResponse(
                success=False,
                document_type=request.document_type,
                result=None,
                error=f"{type(exc).__name__}: {exc}",
            )