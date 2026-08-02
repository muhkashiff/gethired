"""
Enterprise Generic Ontology Extractor

All ontology extractors inherit from this class.

Supported ontologies

- actions
- objects
- metrics
- standards
- methodologies
- technologies
- certifications
- skills

Enterprise V4
"""

from abc import ABC

from app.intelligence.utilities.knowledge.knowledge_extractors.base_extractor import (
    BaseExtractor,
)


class GenericOntologyExtractor(

    BaseExtractor,

    ABC,

):

    ####################################################################
    # MUST BE OVERRIDDEN
    ####################################################################

    ontology_name = ""

    knowledge_class = None

    entity_type = ""

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(

        self,

        repository=None,

    ):

        super().__init__(repository)

    ####################################################################
    # BACKWARD COMPATIBLE
    ####################################################################

    def extract(

        self,

        sentence,

    ):

        entities = self.extract_all(

            sentence

        )

        if entities:

            return entities[0]

        return self.knowledge_class()

        ####################################################################
    # MAIN
    ####################################################################

    def extract_all(

        self,

        sentence,

    ):

        candidates = self.extract_candidates(

            ontology=self.ontology_name,

            sentence=sentence,

        )

        results = []

        for candidate in candidates:

            entity = candidate["entity"]

            metadata = entity.metadata

            obj = self.knowledge_class()

            # Populate all common ontology fields
            obj = self.populate_entity(

                obj,

                candidate,

            )

            # Populate ontology-specific fields
            extras = self.extra_fields(

                entity,

                metadata,

            )

            for key, value in extras.items():

                setattr(obj, key, value)

            results.append(obj)

        return results

    ####################################################################
    # TO BE OVERRIDDEN
    ####################################################################

    def extra_fields(

        self,

        entity,

        metadata,

    ):

        """
        Child extractors override this.

        Return only ontology-specific fields.

        Example

        Action

            base
            gerund

        Standard

            publisher
            version

        Metric

            preferred_direction
            business_meaning

        """

        return {}