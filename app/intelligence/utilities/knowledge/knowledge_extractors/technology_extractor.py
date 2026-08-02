"""
Enterprise Technology Extractor

Generic Ontology Version

Enterprise V4
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.generic_ontology_extractor import (
    GenericOntologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.technology_models import (
    TechnologyKnowledge,
)


class TechnologyExtractor(GenericOntologyExtractor):

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "technologies"

    knowledge_class = TechnologyKnowledge

    entity_type = "technology"

    ####################################################################
    # TECHNOLOGY SPECIFIC FIELDS
    ####################################################################

    def extra_fields(

        self,

        entity,

        metadata,

    ):

        return {

            "vendor": metadata.get(

                "vendor",

                ""

            ),

            "platform": metadata.get(

                "platform",

                ""

            ),

            "technology_family": metadata.get(

                "technology_family",

                ""

            ),

            "version": metadata.get(

                "version",

                ""

            ),

            "cloud_ready": metadata.get(

                "cloud_ready",

                False,

            ),

            "enterprise_level": metadata.get(

                "enterprise_level",

                False,

            ),

        }