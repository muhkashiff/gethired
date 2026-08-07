"""
Enterprise Match Result

Stage 3 Output

This object represents a successful match between
an NGram produced by the Tokenizer and an
entity loaded from the Repository.

Pipeline

Sentence
    ↓
Tokenizer
    ↓
NGram
    ↓
Repository
    ↓
MatchResult
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.repository_v5.repository_entity import RepositoryEntity


@dataclass(slots=True)
class MatchResult:

    ####################################################################
    # Repository Entity
    ####################################################################

    entity: RepositoryEntity

    ####################################################################
    # Text matched
    ####################################################################

    phrase: str

    matched_alias: str = ""

    is_alias: bool = False

    ####################################################################
    # Confidence
    ####################################################################

    confidence: float = 0.0

    ####################################################################
    # Token positions
    ####################################################################

    token_index: int = 0

    token_count: int = 0

    ####################################################################
    # Character positions
    ####################################################################

    start_char: int = 0

    end_char: int = 0

    ####################################################################
    # Convenience Properties
    ####################################################################

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

    ####################################################################
    # Debug
    ####################################################################

    def __repr__(self):

        return (
            "MatchResult("
            f"entity_id='{self.entity.entity_id}', "
            f"canonical='{self.entity.canonical}', "
            f"phrase='{self.phrase}', "
            f"confidence={self.confidence:.3f}, "
            f"tokens=({self.token_index},{self.token_count}), "
            f"chars=({self.start_char},{self.end_char})"
            ")"
        )