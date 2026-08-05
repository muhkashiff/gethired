"""
Enterprise Ontology Matcher

Enterprise V12

Sentence
      ↓
Ontology Repository
      ↓
EntityMatch
"""

from .extraction_models import EntityMatch


class OntologyMatcher:

    ####################################################################
    # INITIALIZE
    ####################################################################

    def __init__(

        self,

        ontology_repository,

    ):

        self.repository = ontology_repository

    ####################################################################
    # PUBLIC
    ####################################################################

    def match(

        self,

        sentence,

    ):

        """
        Match one sentence against the ontology repository.

        Returns
        -------
        list[EntityMatch]
        """

        matches = []

        resolved_entities = self.repository.resolve(

            sentence.text

        )

        if not resolved_entities:

            return matches

        for entity in resolved_entities:

            matches.append(

                self._create_match(

                    entity

                )

            )

        return matches

    ####################################################################
    # PRIVATE
    ####################################################################

    def _create_match(

        self,

        ontology_entity,

    ):

        return EntityMatch(

            entity_id=ontology_entity.entity_id,

            entity_type=ontology_entity.entity_type,

            canonical=ontology_entity.canonical,

            matched_text=ontology_entity.canonical,

            confidence=getattr(

                ontology_entity,

                "confidence",

                1.0,

            ),

            ontology_source="OntologyRepository",

            metadata=getattr(

                ontology_entity,

                "metadata",

                {},

            ),

        )