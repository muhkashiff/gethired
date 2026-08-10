"""
Enterprise Repository Cache
Enterprise V5

Stores every in-memory index used by Repository.

Repository Cache Responsibilities
----------------------------------
• Store entity indexes
• Store canonical indexes
• Store normalized indexes
• Store alias indexes
• Store linguistic-form indexes
• Store configuration indexes
• Store semantic indexes

The cache contains indexes only.

It does not perform matching logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RepositoryCache:
    """
    Enterprise in-memory repository cache.

    The Repository owns the matching behaviour.
    RepositoryCache only stores the indexes required
    by the Repository.

    Index hierarchy:

        ontology
            ↓
        lookup value
            ↓
        RepositoryEntity
    """

    ####################################################################
    # ENTITY INDEXES
    ####################################################################

    # ontology -> entity_id -> RepositoryEntity
    entity_indexes: dict = field(
        default_factory=dict
    )

    # ontology -> canonical -> RepositoryEntity
    canonical_indexes: dict = field(
        default_factory=dict
    )

    # ontology -> normalized -> RepositoryEntity
    normalized_indexes: dict = field(
        default_factory=dict
    )

    # ontology -> alias -> RepositoryEntity
    alias_indexes: dict = field(
        default_factory=dict
    )

    ####################################################################
    # LINGUISTIC INDEXES
    ####################################################################

    # ontology -> linguistic form -> RepositoryEntity
    #
    # Includes:
    #
    #   base
    #   past
    #   gerund
    #   plural
    #   singular
    #   abbreviation
    #   short_name
    #
    # Example:
    #
    # "analyze"    -> Analyze
    # "analyzed"   -> Analyze
    # "analyzing"  -> Analyze
    #
    linguistic_indexes: dict = field(
        default_factory=dict
    )

    ####################################################################
    # INDIVIDUAL LINGUISTIC INDEXES
    ####################################################################

    # These are intentionally kept separate.
    #
    # This allows the Repository to determine exactly
    # which linguistic form produced a match.

    base_indexes: dict = field(
        default_factory=dict
    )

    past_indexes: dict = field(
        default_factory=dict
    )

    gerund_indexes: dict = field(
        default_factory=dict
    )

    plural_indexes: dict = field(
        default_factory=dict
    )

    singular_indexes: dict = field(
        default_factory=dict
    )

    abbreviation_indexes: dict = field(
        default_factory=dict
    )

    short_name_indexes: dict = field(
        default_factory=dict
    )

    ####################################################################
    # CONFIGURATION
    ####################################################################

    # confidence_rules.json
    # modifier_dictionary.json
    # measurement_patterns.json

    config_indexes: dict = field(
        default_factory=dict
    )

    ####################################################################
    # SEMANTIC FILES
    ####################################################################

    semantic_indexes: dict = field(
        default_factory=dict
    )

    ####################################################################
    # OPTIONAL FUTURE CACHE
    ####################################################################

    statistics: dict = field(
        default_factory=dict
    )

    ####################################################################
    # CLEAR
    ####################################################################

    def clear(self) -> None:
        """
        Clear every repository cache index.
        """

        self.entity_indexes.clear()

        self.canonical_indexes.clear()

        self.normalized_indexes.clear()

        self.alias_indexes.clear()

        self.linguistic_indexes.clear()

        self.base_indexes.clear()

        self.past_indexes.clear()

        self.gerund_indexes.clear()

        self.plural_indexes.clear()

        self.singular_indexes.clear()

        self.abbreviation_indexes.clear()

        self.short_name_indexes.clear()

        self.config_indexes.clear()

        self.semantic_indexes.clear()

        self.statistics.clear()