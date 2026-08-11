"""
Enterprise Repository
Enterprise V5

Responsibilities

• Load ontology entities
• Load repository relations
• Build entity indexes
• Build relation indexes
• Resolve entities
• Resolve relations
• Support aliases
• Support canonical forms
• Support normalized forms
• Support linguistic forms
• Support technology surface forms
"""

from __future__ import annotations

import json

from pathlib import Path

from .repository_cache import RepositoryCache
from .repository_loader import RepositoryLoader
from .repository_paths import RepositoryPaths
from .relation_repository_record import RelationRepositoryRecord


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

            if not isinstance(
                path,
                Path,
            ):
                continue

            if path.suffix != ".json":
                continue

            ################################################################
            # RELATIONS
            ################################################################

            if path.name == "relations.json":

                self.load_relations(
                    path
                )

                continue

            ################################################################
            # ONTOLOGY
            ################################################################

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
    # LOAD RELATIONS
    ####################################################################

    def load_relations(
        self,
        path: str | Path,
    ) -> None:
        """
        Load relations.json into RelationRepositoryRecord objects.

        relations.json
            ↓
        RelationRepositoryRecord
            ↓
        RepositoryCache
        """

        path = Path(path)

        with open(
            path,
            "r",
            encoding="utf8",
        ) as file:

            raw = json.load(file)

        ################################################################
        # VALIDATE ROOT
        ################################################################

        if not isinstance(
            raw,
            dict,
        ):

            raise ValueError(
                "relations.json must contain a JSON object."
            )

        ################################################################
        # INDEXES
        ################################################################

        relation_index = {}

        relation_type_index = {}

        relation_source_index = {}

        relation_target_index = {}

        ################################################################
        # BUILD RELATION OBJECTS
        ################################################################

        for relation_id, item in raw.items():

            if not isinstance(
                item,
                dict,
            ):

                raise ValueError(
                    f"Relation {relation_id!r} "
                    "must be a JSON object."
                )

            relation = self._build_relation(
                relation_id,
                item,
            )

            ################################################################
            # MASTER RELATION INDEX
            ################################################################

            relation_index[
                relation.relation_id
            ] = relation

            ################################################################
            # TYPE INDEX
            ################################################################

            relation_type = (
                self._normalize_relation_key(
                    relation.relation_type
                )
            )

            if relation_type:

                relation_type_index.setdefault(
                    relation_type,
                    [],
                ).append(
                    relation
                )

            ################################################################
            # SOURCE INDEX
            ################################################################

            source = (
                self._normalize_relation_key(
                    relation.source
                )
            )

            if source:

                relation_source_index.setdefault(
                    source,
                    [],
                ).append(
                    relation
                )

            ################################################################
            # TARGET INDEX
            ################################################################

            target = (
                self._normalize_relation_key(
                    relation.target
                )
            )

            if target:

                relation_target_index.setdefault(
                    target,
                    [],
                ).append(
                    relation
                )

        ################################################################
        # STORE
        ################################################################

        self.cache.relation_indexes[
            "relations"
        ] = relation_index

        self.cache.relation_type_indexes[
            "relations"
        ] = relation_type_index

        self.cache.relation_source_indexes[
            "relations"
        ] = relation_source_index

        self.cache.relation_target_indexes[
            "relations"
        ] = relation_target_index

    ####################################################################
    # BUILD RELATION
    ####################################################################

    @staticmethod
    def _build_relation(
        relation_id,
        item,
    ) -> RelationRepositoryRecord:
        """
        Convert one JSON relation into a
        RelationRepositoryRecord object.
        """

        metadata = {}

        for key, value in item.items():

            if key not in {
                "relation_type",
                "source",
                "target",
                "weight",
                "description",
                "searchable",
                "active",
                "source_name",
                "metadata",
            }:

                metadata[
                    key
                ] = value

        explicit_metadata = item.get(
            "metadata",
            {},
        )

        if not isinstance(
            explicit_metadata,
            dict,
        ):

            raise ValueError(
                f"Metadata for relation "
                f"{relation_id!r} must be a JSON object."
            )

        metadata.update(
            explicit_metadata
        )

        return RelationRepositoryRecord(

            relation_id=str(
                relation_id
            ).strip(),

            relation_type=str(
                item.get(
                    "relation_type",
                    "",
                )
            ).strip(),

            source=str(
                item.get(
                    "source",
                    "",
                )
            ).strip(),

            target=str(
                item.get(
                    "target",
                    "",
                )
            ).strip(),

            weight=Repository._float_value(
                item.get(
                    "weight",
                    1.0,
                )
            ),

            description=str(
                item.get(
                    "description",
                    "",
                )
            ).strip(),

            searchable=Repository._bool_value(
                item.get(
                    "searchable",
                    True,
                )
            ),

            active=Repository._bool_value(
                item.get(
                    "active",
                    True,
                )
            ),

            source_name=str(
                item.get(
                    "source_name",
                    "relations",
                )
            ).strip(),

            metadata=metadata,
        )

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
        # ALIAS
        ############################################################

        entity = self.cache.alias_indexes.get(
            ontology,
            {},
        ).get(
            phrase
        )

        if entity is not None:
            return entity

        ############################################################
        # CANONICAL
        ############################################################

        entity = self.cache.canonical_indexes.get(
            ontology,
            {},
        ).get(
            phrase
        )

        if entity is not None:
            return entity

        ############################################################
        # NORMALIZED
        ############################################################

        entity = self.cache.normalized_indexes.get(
            ontology,
            {},
        ).get(
            phrase
        )

        if entity is not None:
            return entity

        ############################################################
        # LINGUISTIC
        ############################################################

        entity = self.cache.linguistic_indexes.get(
            ontology,
            {},
        ).get(
            phrase
        )

        if entity is not None:
            return entity

        ############################################################
        # SURFACE
        ############################################################

        entity = self.cache.surface_indexes.get(
            ontology,
            {},
        ).get(
            phrase
        )

        if entity is not None:
            return entity

        return None

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

        return self.cache.canonical_indexes.get(
            ontology,
            {},
        ).get(
            phrase
        )

    ####################################################################
    # FIND ENTITY BY ID
    ####################################################################

    def find_entity_by_id(
        self,
        ontology,
        entity_id,
    ):

        ontology = ontology.lower()

        return self.cache.entity_indexes.get(
            ontology,
            {},
        ).get(
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
    # FIND RELATION BY ID
    ####################################################################

    def find_relation(
        self,
        relation_id,
    ):

        if relation_id is None:
            return None

        relation_id = str(
            relation_id
        ).strip()

        if not relation_id:
            return None

        return self.cache.relation_indexes.get(
            "relations",
            {},
        ).get(
            relation_id
        )

    ####################################################################
    # FIND RELATIONS BY TYPE
    ####################################################################

    def find_relations_by_type(
        self,
        relation_type,
    ):

        relation_type = (
            self._normalize_relation_key(
                relation_type
            )
        )

        if not relation_type:
            return []

        return self.cache.relation_type_indexes.get(
            "relations",
            {},
        ).get(
            relation_type,
            [],
        )

    ####################################################################
    # FIND RELATIONS BY SOURCE
    ####################################################################

    def find_relations_by_source(
        self,
        source,
    ):

        source = (
            self._normalize_relation_key(
                source
            )
        )

        if not source:
            return []

        return self.cache.relation_source_indexes.get(
            "relations",
            {},
        ).get(
            source,
            [],
        )

    ####################################################################
    # FIND RELATIONS BY TARGET
    ####################################################################

    def find_relations_by_target(
        self,
        target,
    ):

        target = (
            self._normalize_relation_key(
                target
            )
        )

        if not target:
            return []

        return self.cache.relation_target_indexes.get(
            "relations",
            {},
        ).get(
            target,
            [],
        )

    ####################################################################
    # BUILD SURFACE FORMS
    ####################################################################

    @classmethod
    def _build_surface_forms(
        cls,
        entity,
    ) -> set[str]:

        forms: set[str] = set()

        canonical = cls._normalize_lookup(
            entity.canonical
        )

        if canonical:

            forms.add(
                canonical
            )

        for alias in entity.aliases:

            normalized_alias = (
                cls._normalize_lookup(
                    alias
                )
            )

            if normalized_alias:

                forms.add(
                    normalized_alias
                )

        ################################################################
        # MICROSOFT TECHNOLOGY SHORTENING
        ################################################################

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
    # LINGUISTIC INDEX HELPER
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

        value = value.strip().casefold()

        if not value:
            return

        index[
            value
        ] = entity

    ####################################################################
    # NORMALIZATION
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

    ####################################################################
    # RELATION KEY NORMALIZATION
    ####################################################################

    @staticmethod
    def _normalize_relation_key(
        value,
    ) -> str:

        if not isinstance(
            value,
            str,
        ):

            return ""

        return value.strip().casefold()

    ####################################################################
    # FLOAT
    ####################################################################

    @staticmethod
    def _float_value(
        value,
    ) -> float:

        if value is None:
            return 0.0

        try:

            return float(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            raise ValueError(
                f"Invalid numeric repository "
                f"value: {value!r}"
            )

    ####################################################################
    # BOOLEAN
    ####################################################################

    @staticmethod
    def _bool_value(
        value,
    ) -> bool:

        if isinstance(
            value,
            bool,
        ):

            return value

        if isinstance(
            value,
            str,
        ):

            normalized = (
                value.casefold().strip()
            )

            if normalized in {
                "true",
                "yes",
                "1",
            }:

                return True

            if normalized in {
                "false",
                "no",
                "0",
            }:

                return False

        return bool(value)