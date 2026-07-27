"""
Entity Linker

Normalizes extracted entities into one canonical ontology.

Responsibilities
----------------
1. Resolve aliases.
2. Assign stable IDs.
3. Remove duplicate spellings.
4. Attach ontology metadata.
"""

from app.intelligence.utilities.knowledge.knowledge_linker.alias_repository import (
    AliasRepository,
)

from app.intelligence.utilities.knowledge.knowledge_linker.entity_models import (
    LinkedEntity,
)


class EntityLinker:

    def __init__(self):

        self.repository = AliasRepository()

    # ------------------------------------------------------

    def link(self, knowledge):

        """
        Accepts one extracted knowledge object.

        Returns
        -------
        LinkedEntity
        """

        if not getattr(knowledge, "found", False):

            return LinkedEntity()

        original = ""

        if hasattr(knowledge, "canonical") and knowledge.canonical:

            original = knowledge.canonical

        elif hasattr(knowledge, "original"):

            original = knowledge.original

        elif hasattr(knowledge, "metric"):

            original = knowledge.metric

        if not original:

            return LinkedEntity()

        entity = self.repository.lookup(original)

        if entity is None:

            return LinkedEntity(

                found=True,

                entity_id=original.upper().replace(" ", "_"),

                canonical=original,

                category=getattr(knowledge, "category", ""),

                business_area="",

                confidence=getattr(knowledge, "confidence", 0.8),

            )

        return LinkedEntity(

            found=True,

            entity_id=entity.get("id", entity["canonical"]),

            canonical=entity["canonical"],

            category=entity.get("category", ""),

            business_area=entity.get("business_area", ""),

            confidence=getattr(knowledge, "confidence", 0.95),

            aliases=entity.get("aliases", []),

            metadata=entity,

        )

    # ------------------------------------------------------

    def link_fact(self, fact):

        """
        Link every entity inside a KnowledgeFact.
        """

        fact.linked_action = self.link(fact.action)

        fact.linked_object = self.link(fact.object)

        fact.linked_metric = self.link(fact.metric)

        return fact