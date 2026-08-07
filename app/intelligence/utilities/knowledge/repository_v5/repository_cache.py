"""
Enterprise Repository Cache

Stores every in-memory index used by Repository.
"""

from dataclasses import dataclass, field


@dataclass
class RepositoryCache:

    ############################################################
    # ENTITY INDEXES
    ############################################################

    # ontology -> entity_id -> RepositoryEntity
    entity_indexes: dict = field(default_factory=dict)

    # ontology -> canonical -> RepositoryEntity
    canonical_indexes: dict = field(default_factory=dict)

    # ontology -> normalized -> RepositoryEntity
    normalized_indexes: dict = field(default_factory=dict)

    # ontology -> alias -> RepositoryEntity
    alias_indexes: dict = field(default_factory=dict)

    ############################################################
    # CONFIG FILES
    ############################################################

    #confidence_rules.json
    #modifier_dictionary.json
    #measurement_patterns.json
    config_indexes: dict = field(default_factory=dict)

    ############################################################
    # SEMANTIC FILES
    ############################################################

    semantic_indexes: dict = field(default_factory=dict)

    ############################################################
    # OPTIONAL FUTURE CACHE
    ############################################################

    statistics: dict = field(default_factory=dict)

    ############################################################

    def clear(self):

        self.entity_indexes.clear()

        self.canonical_indexes.clear()

        self.normalized_indexes.clear()

        self.alias_indexes.clear()

        self.config_indexes.clear()

        self.semantic_indexes.clear()

        self.statistics.clear()