"""
Enterprise Knowledge Document Parser

V12 Architecture

Input
-----
Raw text

Output
------
KnowledgeDocument
"""

from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeDocument,
)

from .clause_segmenter import ClauseSegmenter
from .sentence_parser import SentenceParser


class DocumentParser:

    def __init__(self):

        self.segmenter = ClauseSegmenter()
        self.sentence_parser = SentenceParser()

    # -----------------------------------------------------

    def parse(self, text: str) -> KnowledgeDocument:

        document = KnowledgeDocument()

        document.raw_text = text

        clauses = self.segmenter.segment(text)

        for clause in clauses:

            sentence = self.sentence_parser.parse(clause)

            document.sentences.append(sentence)

            document.facts.extend(sentence.facts)

        document.statistics = {
            "sentences": len(document.sentences),
            "facts": len(document.facts),
        }

        if document.facts:

            document.confidence = (
                sum(f.confidence for f in document.facts)
                / len(document.facts)
            )

        return document