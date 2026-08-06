"""
Enterprise Object Extractor

Generic Ontology Version

Enterprise V4
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.generic_ontology_extractor import (
    GenericOntologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.object_models import (
    ObjectKnowledge,
)


class ObjectExtractor(GenericOntologyExtractor):

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "targets"

    knowledge_class = ObjectKnowledge

    entity_type = "target"

    ####################################################################
    # OBJECT SPECIFIC FIELDS
    ####################################################################

    def extra_fields(

        self,

        entity,

        metadata,

    ):

        return {}