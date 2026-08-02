"""
Enterprise Action Extractor

Generic Ontology Version

Enterprise V4
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.generic_ontology_extractor import (
    GenericOntologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.action_models import (
    ActionKnowledge,
)


class ActionExtractor(GenericOntologyExtractor):

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "actions"

    knowledge_class = ActionKnowledge

    entity_type = "action"

    ####################################################################
    # ACTION-SPECIFIC FIELDS
    ####################################################################

    def extra_fields(

        self,

        entity,

        metadata,

    ):

        return {

            "base": metadata.get(

                "base",

                entity.canonical,

            ),

            "gerund": metadata.get(

                "gerund",

                "",

            ),

            "clause_candidate": True,

        }