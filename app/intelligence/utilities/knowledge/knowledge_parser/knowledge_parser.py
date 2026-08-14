"""
Enterprise Knowledge Parser

V12 Architecture

Public Entry Point

Pipeline

Raw Text
    ↓
DocumentParser
    ↓
KnowledgeDocument

The rest of the Knowledge Engine starts from here.

Example
-------

parser = KnowledgeParser()

document = parser.parse(text)
"""

from __future__ import annotations

from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeDocument,
)

from .document_parser import DocumentParser


class KnowledgeParser:
    """
    Enterprise Knowledge Parser

    Public parser used by every AI engine.

    Stateless wrapper around DocumentParser.
    """

    ####################################################################
    # Initialization
    ####################################################################

    def __init__(self):

        self.document_parser = DocumentParser()

    ####################################################################
    # Parse
    ####################################################################

    def parse(
        self,
        text: str,
    ) -> KnowledgeDocument:
        """
        Parse raw text into a KnowledgeDocument.

        Parameters
        ----------
        text : str

        Returns
        -------
        KnowledgeDocument
        """

        if text is None:
            text = ""

        text = str(text)

        return self.document_parser.parse(text)

    ####################################################################
    # Alias
    ####################################################################

    def __call__(
        self,
        text: str,
    ) -> KnowledgeDocument:

        return self.parse(text)
    