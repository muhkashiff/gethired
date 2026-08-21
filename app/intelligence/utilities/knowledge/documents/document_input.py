"""
Document Input
==============

Object entering the Document Router.
"""

from dataclasses import dataclass

from .document_types import (
    DocumentType,
)


@dataclass(frozen=True)
class DocumentInput:
    """
    Input object for document routing.

    Object In
        ↓
    DocumentRouter
    """

    text: str
    document_type: DocumentType

    def __post_init__(self) -> None:
        """
        Validate the immutable input object.
        """

        if not isinstance(self.text, str):
            raise TypeError(
                "DocumentInput.text must be a string."
            )

        if not self.text.strip():
            raise ValueError(
                "DocumentInput.text cannot be empty."
            )

        if not isinstance(
            self.document_type,
            DocumentType,
        ):
            raise TypeError(
                "DocumentInput.document_type must be "
                "an instance of DocumentType."
            )