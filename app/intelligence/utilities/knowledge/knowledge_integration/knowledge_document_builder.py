"""
Enterprise Knowledge Document Builder
Enterprise V13

Resume text
    ↓
KnowledgeDocument
    ↓
KnowledgeSentence
    ↓
KnowledgeFact
    ↓
KnowledgeInterpretation
"""

from __future__ import annotations

import re
from uuid import uuid4

from app.intelligence.utilities.knowledge.knowledge_models.knowledge_models import (
    KnowledgeDocument,
    KnowledgeSentence,
    KnowledgeFact,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)


class KnowledgeDocumentBuilder:

    # ==================================================================
    # BUILD
    # ==================================================================

    def build(
        self,
        resume_text: str,
        section_metadata=None,
    ) -> KnowledgeDocument:

        text = (
            resume_text
            if isinstance(
                resume_text,
                str,
            )
            else str(
                resume_text or ""
            )
        )

        document = KnowledgeDocument(

            document_id=str(
                uuid4()
            ),

            source="resume",

            raw_text=text,

            confidence=1.0,
        )

        if not text.strip():

            document.build_statistics()

            return document

        sentences = self._split_sentences(
            text
        )

        for index, item in enumerate(
            sentences
        ):

            sentence_text = item["text"]

            start = item["start"]

            end = item["end"]

            sentence = KnowledgeSentence(

                sentence_id=str(
                    uuid4()
                ),

                original_text=sentence_text,

                sentence_index=index,

                start_char=start,

                end_char=end,

                confidence=1.0,
            )

            fact = KnowledgeFact(

                fact_id=str(
                    uuid4()
                ),

                text=sentence_text,

                sentence_index=index,

                start_char=start,

                end_char=end,

                confidence=1.0,

                source="resume",

                interpretation=(
                    KnowledgeInterpretation(
                        confidence=1.0
                    )
                ),
            )

            sentence.add_fact(
                fact
            )

            document.add_sentence(
                sentence
            )

        document.build_statistics()

        return document

    # ==================================================================
    # SENTENCE SPLITTER
    # ==================================================================

    @staticmethod
    def _split_sentences(
        text: str,
    ) -> list[dict]:

        output = []

        pattern = re.compile(
            r"[^.!?\n]+(?:[.!?]+|$)",
            re.MULTILINE,
        )

        for match in pattern.finditer(
            text
        ):

            value = match.group(
                0
            ).strip()

            if not value:

                continue

            output.append({

                "text": value,

                "start": match.start(),

                "end": match.end(),

            })

        return output