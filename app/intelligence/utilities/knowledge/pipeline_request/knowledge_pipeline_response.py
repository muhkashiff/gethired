"""
Knowledge Pipeline Response
===========================

Standardized output object from the Knowledge Pipeline Adapter.

The underlying legacy/enterprise pipeline result is preserved
inside this object rather than being modified.
"""

from dataclasses import dataclass
from typing import Any, Optional

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)


@dataclass(frozen=True)
class KnowledgePipelineResponse:
    """
    Standardized Knowledge Pipeline output.

    Object In
        EnterpriseResumePipelineResult

    Object Out
        KnowledgePipelineResponse
    """

    success: bool
    document_type: DocumentType
    result: Any

    error: Optional[str] = None

    @property
    def knowledge_profile(self) -> Any:
        """
        Return the KnowledgeProfile produced by the
        underlying Enterprise Pipeline.
        """

        if self.result is None:
            return None

        return getattr(
            self.result,
            "knowledge_profile",
            None,
        )

    @property
    def knowledge_document(self) -> Any:
        """
        Return the KnowledgeDocument produced by the
        underlying pipeline.
        """

        if self.result is None:
            return None

        return getattr(
            self.result,
            "knowledge_document",
            None,
        )

    @property
    def business_statements(self) -> list:
        """
        Return business statements from the underlying result.
        """

        if self.result is None:
            return []

        return list(
            getattr(
                self.result,
                "business_statements",
                [],
            )
            or []
        )

    @property
    def semantic_entities(self) -> list:
        """
        Return semantic entities from the underlying result.
        """

        if self.result is None:
            return []

        return list(
            getattr(
                self.result,
                "semantic_entities",
                [],
            )
            or []
        )

    @property
    def knowledge_graph(self) -> Any:
        """
        Return the KnowledgeGraph produced by the pipeline.
        """

        if self.result is None:
            return None

        return getattr(
            self.result,
            "knowledge_graph",
            None,
        )