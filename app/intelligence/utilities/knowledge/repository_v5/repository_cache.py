"""
Enterprise Repository Cache
Enterprise V5

Stores every in-memory index used by Repository.
"""

from dataclasses import dataclass, field


@dataclass
class RepositoryCache:

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
    # SURFACE FORMS
    ####################################################################

    # ontology -> surface form -> RepositoryEntity
    #
    # Examples:
    #
    # "Azure"       -> Microsoft Azure
    # "Power BI"    -> Microsoft Power BI
    # "Excel"       -> Microsoft Excel
    #
    # This is important because the text appearing in a resume
    # does not always equal the canonical repository name.
    ####################################################################

    surface_indexes: dict = field(
        default_factory=dict
    )

    ####################################################################
    # LINGUISTIC INDEX
    ####################################################################

    # ontology -> linguistic form -> RepositoryEntity
    #
    # Used for:
    #
    # base
    # past
    # gerund
    # plural
    # singular
    # abbreviation
    # short_name
    ####################################################################

    linguistic_indexes: dict = field(
        default_factory=dict
    )

    ####################################################################
    # INDIVIDUAL LINGUISTIC INDEXES
    ####################################################################

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
    # CONFIG FILES
    ####################################################################

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

        self.entity_indexes.clear()

        self.canonical_indexes.clear()

        self.normalized_indexes.clear()

        self.alias_indexes.clear()

        self.surface_indexes.clear()

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