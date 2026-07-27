"""
Ontology Repository

Single access point to all ontology entities.
"""

from app.intelligence.utilities.knowledge.knowledge_knowledge.ontology_loader import (
    OntologyLoader,
)


class OntologyRepository:

    def __init__(self):

        self.loader = OntologyLoader()

        self.loader.load_all()

    # ----------------------------------------

    def get(self, entity_id):

        return self.loader.entities.get(entity_id)

    # ----------------------------------------

    def resolve(self, text):

        return self.loader.resolve(text)

    # ----------------------------------------

    def all_entities(self):

        return list(self.loader.entities.values())

    # ----------------------------------------

    def count(self):

        return len(self.loader.entities)