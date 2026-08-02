"""
Enterprise Standard Extractor

Generic Ontology Version

Enterprise V4
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.generic_ontology_extractor import (
    GenericOntologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.standard_models import (
    StandardKnowledge,
)


class StandardExtractor(GenericOntologyExtractor):

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "standards"

    knowledge_class = StandardKnowledge

    entity_type = "standard"

    ####################################################################
    # STANDARD SPECIFIC FIELDS
    ####################################################################

    def extra_fields(

        self,

        entity,

        metadata,

    ):

        return {

            "publisher": metadata.get(

                "publisher",

                ""

            ),

            "version": metadata.get(

                "version",

                ""

            ),

            "standard_family": metadata.get(

                "standard_family",

                ""

            ),

            "scope": metadata.get(

                "scope",

                ""

            ),

            "certifiable": metadata.get(

                "certifiable",

                False,

            ),

            "food_safety_standard": metadata.get(

                "food_safety_standard",

                False,

            ),

            "quality_standard": metadata.get(

                "quality_standard",

                False,

            ),

        }