"""
Enterprise Target Extractor

Generic Ontology Version

Enterprise V5
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.generic_ontology_extractor import (
    GenericOntologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.target_models import (
    TargetKnowledge,
)


class TargetExtractor(GenericOntologyExtractor):

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "targets"

    knowledge_class = TargetKnowledge

    entity_type = "target"

    ####################################################################
    # TARGET SPECIFIC FIELDS
    ####################################################################

    def extra_fields(
        self,
        entity,
        metadata,
    ):

        return {}