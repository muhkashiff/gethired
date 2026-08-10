"""
Enterprise Repository
Enterprise V5

Responsibilities

• Load ontology entities
• Build indexes
• Resolve entities
• Support aliases
• Support canonical forms
• Support normalized forms
• Support linguistic forms
• Support technology surface forms
"""

from __future__ import annotations

from pathlib import Path

from .repository_cache import RepositoryCache
from .repository_loader import RepositoryLoader
from .repository_paths import RepositoryPaths


class Repository:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self) -> None:

        self.cache = RepositoryCache()

        self.loader = RepositoryLoader()

        self.paths = RepositoryPaths()

        self.load_everything()

    ####################################################################
    # LOAD EVERYTHING
    ####################################################################

    def load_everything(self) -> None:

        for ontology_name, path in vars(
            self.paths
        ).items():

            if not isinstance(path, Path):
                continue

            if path.suffix != ".json":
                continue

            if path.parent.name != "ontology":
                continue

            self.load_ontology(
                ontology_name,
                path,
            )

    ####################################################################
    # LOAD ONTOLOGY
    ####################################################################

    def load_ontology(
        self,
        ontology_name,
        path,
    ) -> None:

        entities = self.loader.load(
            ontology_name,
            path,
        )

        alias_index = {}

        canonical_index = {}

        normalized_index = {}

        entity_index = {}

        linguistic_index = {}

        surface_index = {}

        base_index = {}

        past_index = {}

        gerund_index = {}

        plural_index = {}

        singular_index = {}

        abbreviation_index = {}

        short_name_index = {}

        ################################################################
        # BUILD INDEXES
        ################################################################

        for entity in entities:

            ############################################################
            # ENTITY
            ############################################################

            entity_index[
                entity.entity_id
            ] = entity

            ############################################################
            # CANONICAL
            ############################################################

            canonical = self._normalize_lookup(
                entity.canonical
            )

            if canonical:

                canonical_index[
                    canonical
                ] = entity

            ############################################################
            # NORMALIZED
            ############################################################

            normalized = self._normalize_lookup(
                entity.normalized
            )

            if normalized:

                normalized_index[
                    normalized
                ] = entity

            ############################################################
            # ALIASES
            ############################################################

            for alias in entity.aliases:

                value = self._normalize_lookup(
                    alias
                )

                if not value:
                    continue

                alias_index[
                    value
                ] = entity

            ############################################################
            # SURFACE FORMS
            ############################################################

            for surface in self._build_surface_forms(
                entity
            ):

                surface_index[
                    surface
                ] = entity

            ############################################################
            # LINGUISTIC FORMS
            ############################################################

            self._index_linguistic_form(
                linguistic_index,
                entity.base,
                entity,
            )

            self._index_linguistic_form(
                base_index,
                entity.base,
                entity,
            )

            self._index_linguistic_form(
                linguistic_index,
                entity.past,
                entity,
            )

            self._index_linguistic_form(
                past_index,
                entity.past,
                entity,
            )

            self._index_linguistic_form(
                linguistic_index,
                entity.gerund,
                entity,
            )

            self._index_linguistic_form(
                gerund_index,
                entity.gerund,
                entity,
            )

            self._index_linguistic_form(
                linguistic_index,
                entity.plural,
                entity,
            )

            self._index_linguistic_form(
                plural_index,
                entity.plural,
                entity,
            )

            self._index_linguistic_form(
                linguistic_index,
                entity.singular,
                entity,
            )

            self._index_linguistic_form(
                singular_index,
                entity.singular,
                entity,
            )

            self._index_linguistic_form(
                linguistic_index,
                entity.abbreviation,
                entity,
            )

            self._index_linguistic_form(
                abbreviation_index,
                entity.abbreviation,
                entity,
            )

            self._index_linguistic_form(
                linguistic_index,
                entity.short_name,
                entity,
            )

            self._index_linguistic_form(
                short_name_index,
                entity.short_name,
                entity,
            )

        ################################################################
        # STORE INDEXES
        ################################################################

        ontology_name = ontology_name.lower()

        self.cache.entity_indexes[
            ontology_name
        ] = entity_index

        self.cache.canonical_indexes[
            ontology_name
        ] = canonical_index

        self.cache.normalized_indexes[
            ontology_name
        ] = normalized_index

        self.cache.alias_indexes[
            ontology_name
        ] = alias_index

        self.cache.surface_indexes[
            ontology_name
        ] = surface_index

        self.cache.linguistic_indexes[
            ontology_name
        ] = linguistic_index

        self.cache.base_indexes[
            ontology_name
        ] = base_index

        self.cache.past_indexes[
            ontology_name
        ] = past_index

        self.cache.gerund_indexes[
            ontology_name
        ] = gerund_index

        self.cache.plural_indexes[
            ontology_name
        ] = plural_index

        self.cache.singular_indexes[
            ontology_name
        ] = singular_index

        self.cache.abbreviation_indexes[
            ontology_name
        ] = abbreviation_index

        self.cache.short_name_indexes[
            ontology_name
        ] = short_name_index

    ####################################################################
    # FIND ENTITY
    ####################################################################

    def find_entity(
        self,
        ontology,
        phrase,
    ):

        if phrase is None:
            return None

        ontology = ontology.lower()

        phrase = self._normalize_lookup(
            phrase
        )

        if not phrase:
            return None

        ############################################################
        # 1. ALIAS
        ############################################################

        alias_index = self.cache.alias_indexes.get(
            ontology,
            {},
        )

        entity = alias_index.get(
            phrase
        )

        if entity is not None:
            return entity

        ############################################################
        # 2. CANONICAL
        ############################################################

        canonical_index = self.cache.canonical_indexes.get(
            ontology,
            {},
        )

        entity = canonical_index.get(
            phrase
        )

        if entity is not None:
            return entity

        ############################################################
        # 3. NORMALIZED
        ############################################################

        normalized_index = self.cache.normalized_indexes.get(
            ontology,
            {},
        )

        entity = normalized_index.get(
            phrase
        )

        if entity is not None:
            return entity

        ############################################################
        # 4. LINGUISTIC FORM
        ############################################################

        linguistic_index = self.cache.linguistic_indexes.get(
            ontology,
            {},
        )

        entity = linguistic_index.get(
            phrase
        )

        if entity is not None:
            return entity

        ############################################################
        # 5. SURFACE FORM
        ############################################################

        surface_index = self.cache.surface_indexes.get(
            ontology,
            {},
        )

        entity = surface_index.get(
            phrase
        )

        if entity is not None:
            return entity

        ############################################################
        # NO MATCH
        ############################################################

        return None

    ####################################################################
    # BUILD SURFACE FORMS
    ####################################################################

    @classmethod
    def _build_surface_forms(
        cls,
        entity,
    ) -> set[str]:

        forms: set[str] = set()

        ############################################################
        # CANONICAL
        ############################################################

        canonical = cls._normalize_lookup(
            entity.canonical
        )

        if canonical:

            forms.add(
                canonical
            )

        ############################################################
        # ALIASES
        ############################################################

        for alias in entity.aliases:

            normalized_alias = cls._normalize_lookup(
                alias
            )

            if normalized_alias:

                forms.add(
                    normalized_alias
                )

        ############################################################
        # VENDOR-PREFIXED TECHNOLOGY NAMES
        ############################################################

        #
        # Examples:
        #
        # Microsoft Azure
        #       -> azure
        #
        # Microsoft Excel
        #       -> excel
        #
        # Microsoft Power BI
        #       -> power bi
        #
        # This is deliberately limited to "Microsoft"
        # rather than arbitrary substring matching.
        #

        words = canonical.split()

        if len(words) >= 2:

            vendor_prefixes = {
                "microsoft",
            }

            if words[0] in vendor_prefixes:

                shortened = " ".join(
                    words[1:]
                )

                if shortened:

                    forms.add(
                        shortened
                    )

        return forms

    ####################################################################
    # FIND ENTITY EXACT
    ####################################################################

    def find_entity_exact(
        self,
        ontology,
        phrase,
    ):

        ontology = ontology.lower()

        phrase = self._normalize_lookup(
            phrase
        )

        canonical_index = self.cache.canonical_indexes.get(
            ontology,
            {},
        )

        return canonical_index.get(
            phrase
        )

    ####################################################################
    # FIND BY ID
    ####################################################################

    def find_entity_by_id(
        self,
        ontology,
        entity_id,
    ):

        ontology = ontology.lower()

        entity_index = self.cache.entity_indexes.get(
            ontology,
            {},
        )

        return entity_index.get(
            entity_id
        )

    ####################################################################
    # FIND MANY
    ####################################################################

    def find_entities(
        self,
        ontology,
        phrases,
    ):

        results = []

        seen = set()

        for phrase in phrases:

            entity = self.find_entity(
                ontology,
                phrase,
            )

            if entity is None:
                continue

            if entity.entity_id in seen:
                continue

            seen.add(
                entity.entity_id
            )

            results.append(
                entity
            )

        return results

    ####################################################################
    # PRIVATE INDEX HELPER
    ####################################################################

    @staticmethod
    def _index_linguistic_form(
        index,
        value,
        entity,
    ) -> None:

        if not isinstance(
            value,
            str,
        ):
            return

        value = value.strip().lower()

        if not value:
            return

        index[
            value
        ] = entity

    ####################################################################
    # PRIVATE NORMALIZATION
    ####################################################################

    @staticmethod
    def _normalize_lookup(
        value,
    ) -> str:

        if not isinstance(
            value,
            str,
        ):
            return ""

        return " ".join(
            value.casefold().split()
        )