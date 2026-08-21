"""
Document Profile Builder
========================

Converts a KnowledgePipelineResponse into a
DocumentKnowledgeProfile.

Object In
---------
KnowledgePipelineResponse

Object Out
----------
DocumentKnowledgeProfile
"""

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_response import (
    KnowledgePipelineResponse,
)

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
)


class DocumentProfileBuilder:
    """
    Builds a document-aware profile from a pipeline response.

    This class does not calculate or modify profile intelligence.
    It only establishes the document-aware profile boundary.
    """

    def build(
        self,
        response: KnowledgePipelineResponse,
    ) -> DocumentKnowledgeProfile:
        """
        Build DocumentKnowledgeProfile.

        Object In
            KnowledgePipelineResponse

        Object Out
            DocumentKnowledgeProfile
        """

        if not isinstance(
            response,
            KnowledgePipelineResponse,
        ):
            raise TypeError(
                "DocumentProfileBuilder.build() "
                "expects a KnowledgePipelineResponse."
            )

        if not response.success:
            raise ValueError(
                "Cannot build DocumentKnowledgeProfile "
                "from an unsuccessful KnowledgePipelineResponse."
            )

        profile = response.knowledge_profile

        if profile is None:
            raise ValueError(
                "KnowledgePipelineResponse does not contain "
                "a KnowledgeProfile."
            )

        return DocumentKnowledgeProfile(
            document_type=response.document_type,
            profile=profile,
            source_result=response.result,
        )