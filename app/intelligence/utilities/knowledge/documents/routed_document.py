"""
Routed Document
===============

Output object produced by DocumentRouter.
"""

from dataclasses import dataclass

from .document_types import (
    DocumentType,
)


@dataclass(frozen=True)
class RoutedDocument:
    """
    Output object produced by DocumentRouter.

    Object In
        DocumentInput

    Object Out
        RoutedDocument
    """

    text: str
    document_type: DocumentType

    @property
    def is_resume(self) -> bool:
        """
        Return True when this is a resume.
        """

        return self.document_type == DocumentType.RESUME

    @property
    def is_jd(self) -> bool:
        """
        Return True when this is a job description.
        """

        return self.document_type == DocumentType.JD