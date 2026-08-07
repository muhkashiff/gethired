from pathlib import Path

from .repository_cache import RepositoryCache
from .repository_loader import RepositoryLoader
from .repository_paths import RepositoryPaths


class Repository:

    ############################################################

    def __init__(self):

        self.cache = RepositoryCache()

        self.loader = RepositoryLoader()

        self.paths = RepositoryPaths()

        self.load_everything()

    ############################################################

    def load_everything(self):

        for ontology_name, path in vars(self.paths).items():

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

    ############################################################

    def load_ontology(

        self,

        ontology_name,

        path,

    ):

        entities = self.loader.load(

            ontology_name,

            path,

        )

        alias_index = {}

        canonical_index = {}

        normalized_index = {}

        entity_index = {}

        ########################################################

        for entity in entities:

            entity_index[entity.entity_id] = entity

            canonical_index[

                entity.canonical.lower()

            ] = entity

            normalized_index[

                entity.normalized

            ] = entity

            for alias in entity.aliases:

                alias_index[

                    alias.lower()

                ] = entity

        ########################################################

        self.cache.alias_indexes[ontology_name] = alias_index

        self.cache.canonical_indexes[ontology_name] = canonical_index

        self.cache.normalized_indexes[ontology_name] = normalized_index

        self.cache.entity_indexes[ontology_name] = entity_index

    ############################################################
    # FIND ENTITY
    ############################################################

    def find_entity(

        self,

        ontology,

        phrase,

    ):

        if phrase is None:

            return None

        ontology = ontology.lower()

        phrase = phrase.strip()

        alias_index = self.cache.alias_indexes.get(
            ontology,
            {},
        )

        canonical_index = self.cache.canonical_indexes.get(
            ontology,
            {},
        )

        normalized_index = self.cache.normalized_indexes.get(
            ontology,
            {},
        )

        ########################################################

        entity = alias_index.get(
            phrase.lower()
        )

        if entity:
            return entity

        ########################################################

        entity = canonical_index.get(
            phrase.lower()
        )

        if entity:
            return entity

        ########################################################

        normalized = phrase.lower()

        entity = normalized_index.get(
            normalized
        )

        if entity:
            return entity

        ########################################################

        return None


    ############################################################
    # FIND EXACT
    ############################################################

    def find_entity_exact(

        self,

        ontology,

        phrase,

    ):

        ontology = ontology.lower()

        canonical_index = self.cache.canonical_indexes.get(
            ontology,
            {},
        )

        return canonical_index.get(
            phrase.lower()
        )


    ############################################################
    # FIND BY ID
    ############################################################

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

        return entity_index.get(entity_id)


    ############################################################
    # FIND MANY
    ############################################################

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

            seen.add(entity.entity_id)

            results.append(entity)

        return results