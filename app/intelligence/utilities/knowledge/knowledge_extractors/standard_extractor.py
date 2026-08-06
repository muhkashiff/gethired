"""
Enterprise Standard Extractor
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

            "category": metadata.get(
                "category",
                "",
            ),

            "business_area": metadata.get(
                "business_area",
                "",
            ),

        }