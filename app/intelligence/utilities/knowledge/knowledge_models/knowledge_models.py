"""
Enterprise Knowledge Models

Enterprise V13

Pipeline
--------

Resume
    ↓
KnowledgeDocument
    ↓
KnowledgeSentence
    ↓
KnowledgeFact
    ↓
KnowledgeInterpretation
    ↓
SemanticEntity
    ↓
BusinessStatement
    ↓
KnowledgeGraph
"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)


# ============================================================================
# KNOWLEDGE FACT
# ============================================================================


@dataclass
class KnowledgeFact:
    """
    Atomic unit of resume knowledge.

    One KnowledgeFact represents one meaningful statement
    extracted from a resume.

    The interpretation is always created.

    The semantic resolver will later populate:

        interpretation.semantic_entities
    """

    # ------------------------------------------------------------------------
    # SOURCE TEXT
    # ------------------------------------------------------------------------

    text: str = ""

    source: str = "resume"

    # ------------------------------------------------------------------------
    # INTERPRETATION
    # ------------------------------------------------------------------------

    interpretation: KnowledgeInterpretation = field(
        default_factory=KnowledgeInterpretation
    )

    # ------------------------------------------------------------------------
    # BUSINESS FLAGS
    # ------------------------------------------------------------------------

    achievement: bool = False

    quantified: bool = False

    # ------------------------------------------------------------------------
    # CONFIDENCE
    # ------------------------------------------------------------------------

    confidence: float = 0.0

    # ------------------------------------------------------------------------
    # IDENTIFICATION
    # ------------------------------------------------------------------------

    fact_id: str = ""

    sentence_index: int = -1

    fact_index: int = -1

    # ------------------------------------------------------------------------
    # METADATA
    # ------------------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================================
    # HELPERS
    # =========================================================================

    @property
    def has_interpretation(self) -> bool:

        return (
            self.interpretation is not None
        )

    @property
    def semantic_entities(self):

        if self.interpretation is None:

            return []

        return (
            self.interpretation.semantic_entities
        )

    @property
    def semantic_entity_count(self) -> int:

        return len(
            self.semantic_entities
        )

    @property
    def has_semantic_entities(self) -> bool:

        return (
            self.semantic_entity_count > 0
        )

    def __repr__(self) -> str:

        return (
            "KnowledgeFact("
            f"id={self.fact_id!r}, "
            f"text={self.text[:60]!r}, "
            f"semantic_entities="
            f"{self.semantic_entity_count}, "
            f"achievement="
            f"{self.achievement!r}"
            ")"
        )


# ============================================================================
# KNOWLEDGE SENTENCE
# ============================================================================


@dataclass
class KnowledgeSentence:
    """
    Parsed resume sentence.

    A sentence may contain one or more KnowledgeFacts.
    """

    # ------------------------------------------------------------------------
    # SOURCE
    # ------------------------------------------------------------------------

    original_text: str = ""

    sentence_index: int = -1

    # ------------------------------------------------------------------------
    # FACTS
    # ------------------------------------------------------------------------

    facts: list[KnowledgeFact] = field(
        default_factory=list
    )

    # ------------------------------------------------------------------------
    # CONFIDENCE
    # ------------------------------------------------------------------------

    confidence: float = 0.0

    # ------------------------------------------------------------------------
    # METADATA
    # ------------------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # =========================================================================
    # HELPERS
    # =========================================================================

    @property
    def fact_count(self) -> int:

        return len(
            self.facts
        )

    def add_fact(
        self,
        fact: KnowledgeFact,
    ) -> None:

        if fact is None:

            return

        self.facts.append(
            fact
        )

    def __repr__(self) -> str:

        return (
            "KnowledgeSentence("
            f"index={self.sentence_index}, "
            f"facts={len(self.facts)}"
            ")"
        )


# ============================================================================
# KNOWLEDGE DOCUMENT
# ============================================================================


@dataclass
class KnowledgeDocument:
    """
    Complete structured representation of a resume.

    The document contains:

        sentences
        facts
        statistics
        confidence

    It is the object passed from extraction into
    semantic resolution.
    """

    # ------------------------------------------------------------------------
    # SENTENCES
    # ------------------------------------------------------------------------

    sentences: list[KnowledgeSentence] = field(
        default_factory=list
    )

    # ------------------------------------------------------------------------
    # FLATTENED FACTS
    # ------------------------------------------------------------------------

    facts: list[KnowledgeFact] = field(
        default_factory=list
    )

    # ------------------------------------------------------------------------
    # DOCUMENT METADATA
    # ------------------------------------------------------------------------

    statistics: dict[str, Any] = field(
        default_factory=dict
    )

    confidence: float = 0.0

    raw_text: str = ""

    source: str = "resume"

    # ------------------------------------------------------------------------
    # FLAGS
    # ------------------------------------------------------------------------

    parsed: bool = False

    # =========================================================================
    # ADD SENTENCE
    # =========================================================================

    def add_sentence(
        self,
        sentence: KnowledgeSentence,
    ) -> None:

        if sentence is None:

            return

        self.sentences.append(
            sentence
        )

    # =========================================================================
    # ADD FACT
    # =========================================================================

    def add_fact(
        self,
        fact: KnowledgeFact,
    ) -> None:

        if fact is None:

            return

        self.facts.append(
            fact
        )

    # =========================================================================
    # REBUILD FACT INDEX
    # =========================================================================

    def rebuild_fact_index(self) -> None:
        """
        Rebuild the flattened facts list from sentences.

        This prevents the common failure where sentences contain
        facts but KnowledgeDocument.facts remains empty.
        """

        flattened = []

        for sentence in self.sentences:

            if sentence is None:

                continue

            for fact in sentence.facts:

                if fact is None:

                    continue

                flattened.append(
                    fact
                )

        self.facts = flattened

    # =========================================================================
    # FACT COUNT
    # =========================================================================

    @property
    def fact_count(self) -> int:

        return len(
            self.facts
        )

    # =========================================================================
    # SENTENCE COUNT
    # =========================================================================

    @property
    def sentence_count(self) -> int:

        return len(
            self.sentences
        )

    # =========================================================================
    # SEMANTIC ENTITY COUNT
    # =========================================================================

    @property
    def semantic_entity_count(self) -> int:

        total = 0

        for fact in self.facts:

            if fact is None:

                continue

            total += (
                fact.semantic_entity_count
            )

        return total

    # =========================================================================
    # FACTS WITH INTERPRETATION
    # =========================================================================

    @property
    def facts_with_interpretation(self) -> int:

        return sum(
            1
            for fact in self.facts
            if (
                fact is not None
                and fact.has_interpretation
            )
        )

    # =========================================================================
    # FACTS WITH ENTITIES
    # =========================================================================

    @property
    def facts_with_entities(self) -> int:

        return sum(
            1
            for fact in self.facts
            if (
                fact is not None
                and fact.has_semantic_entities
            )
        )

    # =========================================================================
    # DIAGNOSTICS
    # =========================================================================

    def diagnostic(self) -> dict[str, Any]:
        """
        Return diagnostic information used by the enterprise
        pipeline test.
        """

        return {
            "sentences": self.sentence_count,
            "facts": self.fact_count,
            "facts_with_interpretation": (
                self.facts_with_interpretation
            ),
            "facts_with_entities": (
                self.facts_with_entities
            ),
            "semantic_entities": (
                self.semantic_entity_count
            ),
            "confidence": self.confidence,
            "parsed": self.parsed,
        }

    # =========================================================================
    # REPR
    # =========================================================================

    def __repr__(self) -> str:

        return (
            "KnowledgeDocument("
            f"sentences={self.sentence_count}, "
            f"facts={self.fact_count}, "
            f"facts_with_entities="
            f"{self.facts_with_entities}, "
            f"semantic_entities="
            f"{self.semantic_entity_count}, "
            f"confidence={self.confidence}"
            ")"
        )


# ============================================================================
# EXPORTS
# ============================================================================


__all__ = [
    "KnowledgeFact",
    "KnowledgeSentence",
    "KnowledgeDocument",
]