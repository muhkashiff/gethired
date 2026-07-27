import json
from pathlib import Path

from app.intelligence.utilities.knowledge.knowledge_knowledge.ontology_models import (
    OntologyEntity,
)


class OntologyLoader:

    def __init__(self):

        self.entities = {}

        self.alias_lookup = {}

    # -----------------------------------------------------

    def load_file(self, filename):

        folder = (
            Path(__file__).resolve().parent
            / "data"
        )

        path = folder / filename

        with open(path, encoding="utf8") as f:

            try:

                data = json.load(f)

            except json.JSONDecodeError:

                data = {}

        self._index(data)

    # -----------------------------------------------------

    def load_all(self):

        files = [

            "actions.json",

            "objects.json",

            "metrics_dictionary.json",

            "business_kpis.json",

            "domain_reasoning.json",

            "certifications.json",

            "technologies.json"

        ]

        for file in files:

            try:

                self.load_file(file)

            except FileNotFoundError:

                continue

    # -----------------------------------------------------

    def _index(self, data):

        for _, entity in data.items():

            ontology = OntologyEntity(

                id=entity.get("id", ""),

                canonical=entity.get("canonical", ""),

                aliases=entity.get("aliases", []),

                category=entity.get("category", ""),

                business_area=entity.get("business_area", ""),

                description=entity.get("description", ""),

                metadata=entity

            )

            self.entities[ontology.id] = ontology

            self.alias_lookup[ontology.canonical.lower()] = ontology.id

            for alias in ontology.aliases:

                self.alias_lookup[alias.lower()] = ontology.id

    # -----------------------------------------------------

    def resolve(self, text):

        entity_id = self.alias_lookup.get(text.lower())

        if entity_id is None:

            return None

        return self.entities[entity_id]