"""
Enterprise Ontology Matcher

Enterprise V5

Responsibilities
----------------
• Exact Alias Match
• Canonical Match
• Normalized Match
• Repository Lookup

This class NEVER performs fuzzy matching.
That is delegated to fuzzy.py
"""

from __future__ import annotations

from typing import Optional


class Matcher:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(

        self,

        repository,

        tokenizer,

    ):


        self.repository = repository

        self.tokenizer = tokenizer

    ####################################################################
    # LOOKUP
    ####################################################################

    def lookup(

        self,

        ontology: str,

        phrase: str,

    ):

        """
        Complete lookup pipeline.

        Exact Alias

            ↓

        Canonical

            ↓

        Normalized
        """

        if not phrase:

            return None

        ontology = ontology.lower()

        ############################################################

        alias_index = self.repository.cache.alias_indexes.get(

            ontology,

            {},

        )

        canonical_index = self.repository.cache.canonical_indexes.get(

            ontology,

            {},

        )

        normalized_index = self.repository.cache.normalized_indexes.get(

            ontology,

            {},

        )

        ############################################################
        # Alias Lookup
        ############################################################

        entity = alias_index.get(

            phrase.lower()

        )

        if entity:

            return entity

        ############################################################
        # Canonical Lookup
        ############################################################

        entity = canonical_index.get(

            phrase.lower()

        )

        if entity:

            return entity

        ############################################################
        # Normalized Lookup
        ############################################################

        normalized = self.tokenizer.normalize(

            phrase

        )

        entity = normalized_index.get(

            normalized

        )

        if entity:

            return entity

        ############################################################

        return None

    ####################################################################
    # EXACT
    ####################################################################

    def exact(

        self,

        ontology,

        phrase,

    ):

        return self.lookup(

            ontology,

            phrase,

        )

    ####################################################################
    # EXISTS
    ####################################################################

    def exists(

        self,

        ontology,

        phrase,

    ):

        return (

            self.lookup(

                ontology,

                phrase,

            )

            is not None

        )

    ####################################################################
    # ENTITY BY ID
    ####################################################################

    def entity_by_id(

        self,

        ontology,

        entity_id,

    ):

        ontology = ontology.lower()

        entity_index = self.repository.cache.entity_indexes.get(

            ontology,

            {},

        )

        return entity_index.get(

            entity_id

        )

    ####################################################################
    # ALL MATCHES
    ####################################################################

    def lookup_many(

        self,

        ontology,

        phrases,

    ):

        results = []

        seen = set()

        for phrase in phrases:

            entity = self.lookup(

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
    # DEBUG
    ####################################################################

    def debug_lookup(

        self,

        ontology,

        phrase,

    ):

        entity = self.lookup(

            ontology,

            phrase,

        )

        if entity:

            print(

                f"[FOUND] {phrase} -> "

                f"{entity.canonical}"

            )

        else:

            print(

                f"[MISS] {phrase}"

            )

        return entity