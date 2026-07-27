import json
from pathlib import Path


class AliasRepository:

    def __init__(self):

        self.entities = {}

        self.alias_lookup = {}

        self._load()

    # --------------------------------------------------

    def _load(self):

        folder = (
            Path(__file__).resolve().parent.parent
            / "knowledge_knowledge"
            /"ontology"
        )

        files = [

            "business_kpis.json",

            "actions.json",

            "objects.json",

            "domains_reasoning.json",

            "metrics_dictionary.json",

            "certifications.json",

            "technologies.json",

        ]

        for file in files:

            path = folder / file

            if not path.exists():
                continue

            with open(path, encoding="utf8") as f:

                data = json.load(f)

            self._index(data)

    # --------------------------------------------------

    def _index(self, data):

        for _, group in data.items():

            if isinstance(group, dict):

                for key, entity in group.items():

                    if not isinstance(entity, dict):
                        continue

                    canonical = entity.get("canonical")

                    if not canonical:
                        continue

                    entity_id = entity.get("id", canonical)

                    self.entities[entity_id] = entity

                    aliases = entity.get("aliases", [])

                    aliases.append(canonical)

                    for alias in aliases:

                        self.alias_lookup[alias.lower()] = entity_id

    # --------------------------------------------------

    def lookup(self, text):

        entity_id = self.alias_lookup.get(text.lower())

        if entity_id:

            return self.entities[entity_id]

        return None