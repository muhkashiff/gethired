"""
Enterprise Knowledge Document Builder

Enterprise V7

Converts the output of the existing Resume SectionDetector
into the universal KnowledgeDocument structure.

Pipeline

Resume text
    ↓
SectionDetector
    ↓
sections
    ↓
KnowledgeDocumentBuilder
    ↓
KnowledgeDocument
    ↓
KnowledgeV5Pipeline
    ↓
MatchResult[]
    ↓
SemanticResolver
    ↓
SemanticResolution
    ↓
KnowledgeGraphBuilder
    ↓
KnowledgeGraph
"""

from __future__ import annotations

from typing import Any

from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeDocument,
    KnowledgeSentence,
    KnowledgeFact,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)


class KnowledgeDocumentBuilder:
    """
    Converts detected resume sections into a KnowledgeDocument.

    Important:

    This class does NOT perform ontology matching.

    Ontology matching remains the responsibility of
    KnowledgeV5Pipeline.

    This class is responsible only for converting raw
    section text into the universal knowledge structure.
    """

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self):

        self.section_order = []

    # ==========================================================
    # BUILD
    # ==========================================================

    def build(
        self,
        sections: dict[str, list[str]] | None,
        raw_text: str = "",
    ) -> KnowledgeDocument:

        """
        Build a KnowledgeDocument from detected resume sections.

        Parameters
        ----------
        sections:
            Output of SectionDetector.detect()

        raw_text:
            Original resume text.

        Returns
        -------
        KnowledgeDocument
        """

        document = KnowledgeDocument()

        document.raw_text = raw_text or ""

        if not sections:
            return document

        self.section_order = list(
            sections.keys()
        )

        sentence_index = 0

        for section_name, lines in sections.items():

            if not lines:
                continue

            if isinstance(lines, str):
                lines = [lines]

            for line in lines:

                if not line:
                    continue

                text = str(line).strip()

                if not text:
                    continue

                sentence = self._build_sentence(
                    text=text,
                    section_name=section_name,
                    sentence_index=sentence_index,
                )

                document.sentences.append(
                    sentence
                )

                document.facts.extend(
                    sentence.facts
                )

                sentence_index += 1

        self._build_statistics(
            document
        )

        self._calculate_confidence(
            document
        )

        return document

    # ==========================================================
    # BUILD SENTENCE
    # ==========================================================

    def _build_sentence(
        self,
        text: str,
        section_name: str,
        sentence_index: int,
    ) -> KnowledgeSentence:

        """
        Convert one resume line into a KnowledgeSentence.
        """

        fact = self._build_fact(
            text=text,
            section_name=section_name,
            sentence_index=sentence_index,
        )

        sentence = KnowledgeSentence(
            original_text=text,
            facts=[fact],
            confidence=fact.confidence,
        )

        return sentence

    # ==========================================================
    # BUILD FACT
    # ==========================================================

    def _build_fact(
        self,
        text: str,
        section_name: str,
        sentence_index: int,
    ) -> KnowledgeFact:

        """
        Create the initial KnowledgeFact.

        No ontology resolution happens here.

        The fact is deliberately kept lightweight so that
        the V5 ontology pipeline can perform the actual
        semantic resolution.
        """

        interpretation = (
            KnowledgeInterpretation()
        )

        # ------------------------------------------------------
        # Attach section information where possible
        # ------------------------------------------------------

        self._attach_metadata(
            interpretation,
            {
                "resume_section": section_name,
                "sentence_index": sentence_index,
                "source": "resume",
            },
        )

        fact = KnowledgeFact(
            text=text,
            interpretation=interpretation,
            achievement=False,
            quantified=self._contains_quantity(
                text
            ),
            source="resume",
            confidence=1.0,
        )

        # ------------------------------------------------------
        # Preserve section information directly as well.
        #
        # This is useful if later stages inspect KnowledgeFact
        # without going through KnowledgeInterpretation.
        # ------------------------------------------------------

        self._attach_fact_metadata(
            fact,
            {
                "resume_section": section_name,
                "sentence_index": sentence_index,
            },
        )

        return fact

    # ==========================================================
    # METADATA
    # ==========================================================

    @staticmethod
    def _attach_metadata(
        interpretation: Any,
        metadata: dict,
    ) -> None:

        """
        Safely attach metadata to KnowledgeInterpretation.

        Different versions of KnowledgeInterpretation may not
        expose a metadata field. Therefore this method does not
        assume its existence.
        """

        if hasattr(
            interpretation,
            "metadata",
        ):

            existing = getattr(
                interpretation,
                "metadata",
                None,
            )

            if existing is None:

                try:
                    setattr(
                        interpretation,
                        "metadata",
                        {},
                    )

                    existing = interpretation.metadata

                except Exception:
                    return

            if isinstance(
                existing,
                dict,
            ):

                existing.update(
                    metadata
                )

    # ==========================================================

    @staticmethod
    def _attach_fact_metadata(
        fact: KnowledgeFact,
        metadata: dict,
    ) -> None:

        """
        Safely attach metadata to a KnowledgeFact.
        """

        if not hasattr(
            fact,
            "metadata",
        ):

            try:

                setattr(
                    fact,
                    "metadata",
                    {},
                )

            except Exception:

                return

        existing = getattr(
            fact,
            "metadata",
            None,
        )

        if isinstance(
            existing,
            dict,
        ):

            existing.update(
                metadata
            )

    # ==========================================================
    # QUANTITY DETECTION
    # ==========================================================

    @staticmethod
    def _contains_quantity(
        text: str,
    ) -> bool:

        """
        Lightweight detection of quantitative text.

        This is NOT the ontology numeric resolver.

        It only flags a fact as potentially quantified.

        Examples:

            99%
            70%
            15 years
            20%
            500 units
            $100,000
        """

        if not text:
            return False

        characters = set(
            "0123456789"
        )

        return any(
            char in characters
            for char in text
        )

    # ==========================================================
    # STATISTICS
    # ==========================================================

    @staticmethod
    def _build_statistics(
        document: KnowledgeDocument,
    ) -> None:

        sections = {}

        for sentence in document.sentences:

            for fact in sentence.facts:

                section = ""

                metadata = getattr(
                    fact,
                    "metadata",
                    {},
                )

                if isinstance(
                    metadata,
                    dict,
                ):

                    section = metadata.get(
                        "resume_section",
                        "",
                    )

                if section:

                    sections.setdefault(
                        section,
                        0,
                    )

                    sections[section] += 1

        document.statistics = {

            "sentence_count": len(
                document.sentences
            ),

            "fact_count": len(
                document.facts
            ),

            "sections": sections,

        }

    # ==========================================================
    # DOCUMENT CONFIDENCE
    # ==========================================================

    @staticmethod
    def _calculate_confidence(
        document: KnowledgeDocument,
    ) -> None:

        if not document.facts:

            document.confidence = 0.0

            return

        scores = [

            fact.confidence

            for fact in document.facts

        ]

        document.confidence = round(
            sum(scores) / len(scores),
            2,
        )

    # ==========================================================
    # CONVENIENCE
    # ==========================================================

    def build_from_lines(
        self,
        paragraphs: list[str],
    ) -> KnowledgeDocument:

        """
        Convenience API.

        Runs no section detection itself.

        Use this only when paragraphs have already been
        sectioned externally.
        """

        sections = {
            "header": paragraphs
        }

        return self.build(
            sections=sections,
            raw_text="\n".join(
                paragraphs
            ),
        )