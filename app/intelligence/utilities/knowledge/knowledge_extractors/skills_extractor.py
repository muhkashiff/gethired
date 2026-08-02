"""
Enterprise Skills Extractor

Generic Ontology Version

Enterprise V4
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.generic_ontology_extractor import (
    GenericOntologyExtractor,
)

from app.parser.parsed_models import Skill


class SkillsExtractor(GenericOntologyExtractor):

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "skills"

    entity_type = "skill"

    # Skill uses ATS model instead of Knowledge model
    knowledge_class = Skill

    ####################################################################
    # BACKWARD COMPATIBILITY
    ####################################################################

    def extract(self, sentence):

        return self.extract_all(sentence)

    ####################################################################
    # SKILL IMPLEMENTATION
    ####################################################################

    def extract_all(self, sentence):

        matches = self.lookup_sentence(

            self.ontology_name,

            sentence,

        )

        skills = []

        for match in matches:

            entity = match["entity"]

            metadata = entity.metadata

            skills.append(

                Skill(

                    name=entity.canonical,

                    category=entity.category,

                    level=metadata.get(

                        "level",

                        ""

                    ),

                    years=None,

                    confidence=match["confidence"],

                    matched=False,

                    score=0.0,

                    raw_text=match["phrase"],

                    normalized_name=self.normalize(

                        entity.canonical

                    )

                )

            )

        return skills