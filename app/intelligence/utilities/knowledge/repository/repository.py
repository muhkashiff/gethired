"""
Knowledge Repository

Single source of truth
for the entire AI engine.
"""

import json
from pathlib import Path

from .cache import RepositoryCache
from .entity_record import EntityRecord


ROOT = Path(__file__).resolve().parents[1]

ONTOLOGY = ROOT / "knowledge_knowledge" / "ontology"
SEMANTICS = ROOT / "knowledge_knowledge" / "semantics"
CONFIG = ROOT / "knowledge_knowledge" / "config"


class Repository:

    def __init__(self):

        self.cache = RepositoryCache()

        self.load_all()

    # -------------------------------------------------------
    # Utilities
    # -------------------------------------------------------

    def normalize_key(self, text: str) -> str:
        """
        Normalize keys for reliable lookups.
        """

        return (
            text.lower()
            .strip()
            .replace("_", " ")
        )

    # -------------------------------------------------------

    def _load_json(self, folder: Path, filename: str):

        path = folder / filename

        if not path.exists():
            return {}

        with open(path, encoding="utf8") as f:
            return json.load(f)

    # -------------------------------------------------------
    # Load Everything
    # -------------------------------------------------------

    def load_all(self):

        self.cache.actions = self._load_json(
            ONTOLOGY,
            "actions.json"
        )

        self.cache.objects = self._load_json(
            ONTOLOGY,
            "objects.json"
        )

        self.cache.metrics = self._load_json(
            ONTOLOGY,
            "business_kpis.json"
        )

        self.cache.certifications = self._load_json(
            ONTOLOGY,
            "certifications.json"
        )

        self.cache.technologies = self._load_json(
            ONTOLOGY,
            "technologies.json"
        )

        self.cache.aliases = self._load_json(
            ONTOLOGY,
            "aliases.json"
        )

        self.cache.domains = self._load_json(
            ONTOLOGY,
            "domains.json"
        )

        self.cache.semantics = self._load_json(
            SEMANTICS,
            "measurement_semantics.json"
        )

        self.cache.config = {}

    # -------------------------------------------------------

    def reload(self):

        self.load_all()

    # -------------------------------------------------------
    # Generic Access
    # -------------------------------------------------------

    def get_dictionary(self, name):

        return getattr(self.cache, name)

    # -------------------------------------------------------

    def get_object(self, key):

        return self.cache.objects.get(
            self.normalize_key(key)
        )

    # -------------------------------------------------------

    def get_metric(self, key):

        return self.cache.metrics.get(
            self.normalize_key(key)
        )

    # -------------------------------------------------------

    def get_action(self, key):

        return self.cache.actions.get(
            self.normalize_key(key)
        )

    # -------------------------------------------------------

    def get_certification(self, key):

        return self.cache.certifications.get(
            self.normalize_key(key)
        )

    # -------------------------------------------------------

    def get_technology(self, key):

        return self.cache.technologies.get(
            self.normalize_key(key)
        )

    # -------------------------------------------------------

    def get_semantics(self):

        return self.cache.semantics

    # -------------------------------------------------------
    # Alias Search
    # -------------------------------------------------------

    def search_alias(self, text):

        text = self.normalize_key(text)

        alias = self.cache.aliases.get(text)

        if alias is None:
            return None

        if isinstance(alias, dict):
            return alias.get("canonical", text)

        return alias

    # -------------------------------------------------------
    # Universal Entity Lookup
    # -------------------------------------------------------

    def get_entity(self, canonical):

        canonical = self.normalize_key(canonical)

        entity = {}

        # ------------------------
        # Merge Objects
        # ------------------------

        if canonical in self.cache.objects:

            entity.update(
                self.cache.objects[canonical]
            )

        # ------------------------
        # Merge KPIs
        # ------------------------

        if canonical in self.cache.metrics:

            entity.update(
                self.cache.metrics[canonical]
            )

        # ------------------------
        # Merge Certifications
        # ------------------------

        if canonical in self.cache.certifications:

            entity.update(
                self.cache.certifications[canonical]
            )

        # ------------------------
        # Merge Technologies
        # ------------------------

        if canonical in self.cache.technologies:

            entity.update(
                self.cache.technologies[canonical]
            )

        # ------------------------

        if not entity:

            return None

        return self.merge_entity(
            canonical,
            entity
        )

    # -------------------------------------------------------
    # Merge Into Universal Entity
    # -------------------------------------------------------

    def merge_entity(self, key, entity):

        record = EntityRecord()

        record.entity_id = entity.get(
            "entity_id",
            key.upper().replace(" ", "_")
        )

        record.canonical = entity.get(
            "canonical",
            key.title()
        )

        record.category = entity.get(
            "category",
            ""
        )

        record.business_area = entity.get(
            "business_area",
            ""
        )

        record.preferred_direction = entity.get(
            "preferred_direction",
            ""
        )

        record.impact_weight = entity.get(
            "impact_weight",
            0
        )

        record.business_meaning = entity.get(
            "business_meaning",
            ""
        )

        record.aliases = entity.get(
            "aliases",
            []
        )

        record.source = "ontology"

        record.metadata = entity

        return record