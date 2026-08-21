"""
Knowledge Pipeline Request
==========================

Object entering the Knowledge Pipeline Adapter.

Architecture:

RoutedDocument
      ↓
KnowledgePipelineRequest
      ↓
KnowledgePipelineAdapter
"""

from dataclasses import dataclass

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)


@dataclass(frozen=True)
class KnowledgePipelineRequest:
    """
    Immutable request object for the Enterprise Knowledge Pipeline.

    Object In
        RoutedDocument

    Object Out
        KnowledgePipelineRequest
    """

    document_text: str
    document_type: DocumentType

    def __post_init__(self) -> None:
        """Validate the request."""

        if not isinstance(self.document_text, str):
            raise TypeError(
                "KnowledgePipelineRequest.document_text "
                "must be a string."
            )

        if not self.document_text.strip():
            raise ValueError(
                "KnowledgePipelineRequest.document_text "
                "cannot be empty."
            )

        if not isinstance(
            self.document_type,
            DocumentType,
        ):
            raise TypeError(
                "KnowledgePipelineRequest.document_type "
                "must be a DocumentType."
            )