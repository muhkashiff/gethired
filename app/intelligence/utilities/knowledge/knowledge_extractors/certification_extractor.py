"""
Enterprise Certification Extractor

Generic Ontology Version

Enterprise V4
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.generic_ontology_extractor import (
    GenericOntologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.certification_models import (
    CertificationKnowledge,
)


class CertificationExtractor(GenericOntologyExtractor):

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "certifications"

    knowledge_class = CertificationKnowledge

    entity_type = "certification"

    ####################################################################
    # CERTIFICATION SPECIFIC FIELDS
    ####################################################################

    def extra_fields(

        self,

        entity,

        metadata,

    ):

        return {

            "issuing_body": metadata.get(

                "issuing_body",

                ""

            ),

            "validity": metadata.get(

                "validity",

                ""

            ),

            "accredited": metadata.get(

                "accredited",

                False,

            ),

            "certificate_level": metadata.get(

                "certificate_level",

                ""

            ),

            "renewable": metadata.get(

                "renewable",

                False,

            ),

            "international": metadata.get(

                "international",

                False,

            ),

        }