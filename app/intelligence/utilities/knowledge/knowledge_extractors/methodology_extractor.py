"""
Enterprise Methodology Extractor

Generic Ontology Version

Enterprise V4
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.generic_ontology_extractor import (
    GenericOntologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.methodology_models import (
    MethodologyKnowledge,
)


class MethodologyExtractor(GenericOntologyExtractor):

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "methodologies"

    knowledge_class = MethodologyKnowledge

    entity_type = "methodology"

    ####################################################################
    # METHODOLOGY SPECIFIC FIELDS
    ####################################################################

    def extra_fields(

        self,

        entity,

        metadata,

    ):

        return {

            "framework": metadata.get(

                "framework",

                ""

            ),

            "lifecycle": metadata.get(

                "lifecycle",

                ""

            ),

            "methodology_family": metadata.get(

                "methodology_family",

                ""

            ),

            "agile": metadata.get(

                "agile",

                False,

            ),

            "lean": metadata.get(

                "lean",

                False,

            ),

            "continuous_improvement": metadata.get(

                "continuous_improvement",

                False,

            ),

        }