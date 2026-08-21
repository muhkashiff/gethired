"""
Document Router
===============

Routes incoming documents according to their declared document type.

Architecture

DocumentInput
      ↓
DocumentRouter
      ↓
RoutedDocument

The router does NOT perform knowledge extraction.
"""

from app.intelligence.utilities.knowledge.documents.document_input import (
    DocumentInput,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.documents.routed_document import (
    RoutedDocument,
)


class DocumentRouter:
    """
    Route a document into the Enterprise Knowledge architecture.

    Responsibilities
    ----------------
    - Validate the incoming document object.
    - Normalize the document type.
    - Produce a RoutedDocument.

    Non-responsibilities
    -------------------
    - Text extraction
    - Sentence parsing
    - Entity extraction
    - Knowledge graph construction
    - Knowledge profile construction
    """

    def process(
        self,
        document: DocumentInput,
    ) -> RoutedDocument:
        """
        Process one DocumentInput.

        Object In
            DocumentInput

        Object Out
            RoutedDocument
        """

        if not isinstance(
            document,
            DocumentInput,
        ):
            raise TypeError(
                "DocumentRouter.process() expects "
                "a DocumentInput object."
            )

        return RoutedDocument(
            text=document.text.strip(),
            document_type=document.document_type,
        )