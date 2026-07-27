"""
Entity Linker

Links text to ontology using Repository.
"""

from app.intelligence.utilities.knowledge.repository import repository

from .linked_entity import LinkedEntity


class EntityLinker:

    def __init__(self):

        self.repository = repository

    # ----------------------------------------------------------

    def link(self, text):

        if not text:

            return LinkedEntity()

        text = text.strip().lower()

        # ---------------------------------------
        # Alias lookup
        # ---------------------------------------

        alias = self.repository.search_alias(text)

        if alias:

            entity = self.repository.get_entity(alias)

        else:

            entity = self.repository.get_entity(text)

        # ---------------------------------------

        if entity is None:

            return LinkedEntity()

        # ---------------------------------------

        linked = LinkedEntity()

        linked.found = True

        linked.entity_id = entity.entity_id

        linked.canonical = entity.canonical

        linked.category = entity.category

        linked.business_area = entity.business_area

        linked.preferred_direction = entity.preferred_direction

        linked.impact_weight = entity.impact_weight

        linked.business_meaning = entity.business_meaning

        linked.aliases = entity.aliases

        linked.metadata = entity.metadata

        linked.source = "ontology"

        linked.confidence = 1.0

        return linked