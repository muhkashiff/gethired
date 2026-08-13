"""
Enterprise Match Result

Enterprise V12

Represents one successful semantic match produced by
KnowledgeV5Pipeline.

Pipeline

Sentence
    ↓
Tokenizer
    ↓
NGram
    ↓
Repository
    ↓
Matcher
    ↓
MatchResult
    ↓
SemanticResolver
"""

from __future__ import annotations

from dataclasses import dataclass

from app.intelligence.utilities.knowledge.repository_v5.repository_entity import (
    RepositoryEntity,
)


@dataclass(slots=True)
class MatchResult:

    # ==========================================================
    # REPOSITORY ENTITY
    # ==========================================================

    entity: RepositoryEntity

    # ==========================================================
    # TEXT MATCH
    # ==========================================================

    phrase: str

    matched_alias: str = ""

    is_alias: bool = False

    # ==========================================================
    # CONFIDENCE
    # ==========================================================

    confidence: float = 0.0

    # ==========================================================
    # TOKEN POSITION
    # ==========================================================

    token_index: int = 0

    token_count: int = 0

    # ==========================================================
    # CHARACTER POSITION
    # ==========================================================

    start_char: int = 0

    end_char: int = 0

    # ==========================================================
    # STATEMENT CONTEXT
    #
    # These are optional and preserve backward compatibility.
    # V5 can populate them when processing multiple sentences.
    # ==========================================================

    statement_id: str = "STATEMENT_1"

    sentence_index: int = 0

    # ==========================================================
    # CONVENIENCE PROPERTIES
    # ==========================================================

    @property
    def canonical(self) -> str:

        return self.entity.canonical

    @property
    def entity_id(self) -> str:

        return self.entity.entity_id

    @property
    def entity_type(self) -> str:

        return self.entity.entity_type

    @property
    def category(self) -> str:

        return self.entity.category

    @property
    def business_area(self) -> str:

        return self.entity.business_area

    @property
    def domain(self) -> str:

        return self.entity.domain

    @property
    def impact_weight(self) -> float:

        return self.entity.impact_weight

    # ==========================================================
    # METADATA
    # ==========================================================

    @property
    def metadata(self) -> dict:

        metadata = {}

        entity_metadata = getattr(
            self.entity,
            "metadata",
            None,
        )

        if entity_metadata:

            metadata.update(
                entity_metadata
            )

        metadata.update(
            {
                "statement_id": self.statement_id,
                "sentence_index": self.sentence_index,
                "matched_phrase": self.phrase,
                "matched_alias": self.matched_alias,
                "is_alias": self.is_alias,
            }
        )

        return metadata

    # ==========================================================
    # DEBUG
    # ==========================================================

    def __repr__(self) -> str:

        return (
            "MatchResult("
            f"entity_id={self.entity_id!r}, "
            f"entity_type={self.entity_type!r}, "
            f"canonical={self.canonical!r}, "
            f"phrase={self.phrase!r}, "
            f"confidence={self.confidence:.3f}, "
            f"statement_id={self.statement_id!r}, "
            f"sentence_index={self.sentence_index}, "
            f"tokens=({self.token_index},"
            f"{self.token_count}), "
            f"chars=({self.start_char},"
            f"{self.end_char})"
            ")"
        )