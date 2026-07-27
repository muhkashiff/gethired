"""
Knowledge Repository

Loads all dictionaries once.

Every parser/reasoner/linker
should use this instead of json.load().
"""

import json

from .paths import CONFIG
from .paths import ONTOLOGY
from .paths import SEMANTICS


class KnowledgeRepository:

    def __init__(self):

        self._cache = {}

    # ---------------------------------------------------------

    def _load(self, folder, filename):

        key = f"{folder.name}/{filename}"

        if key not in self._cache:

            path = folder / filename

            with open(path, encoding="utf8") as f:

                self._cache[key] = json.load(f)

        return self._cache[key]

    # =========================================================
    # CONFIG
    # =========================================================

    def clause_patterns(self):

        return self._load(CONFIG, "clause_patterns.json")

    def measurement_patterns(self):
    
            return self._load(CONFIG, "measurement_patterns.json")

    def confidence_rules(self):

        return self._load(CONFIG, "confidence_rules.json")

    def parser_rules(self):

        return self._load(CONFIG, "parser_rules.json")

    def modifier_dictionary(self):

        return self._load(CONFIG, "modifier_dictionary.json")

    def scoring_rules(self):

        return self._load(CONFIG, "scoring_rules.json")

    # =========================================================
    # SEMANTICS
    # =========================================================

    def measurement_semantics(self):

        return self._load(SEMANTICS, "measurement_semantics.json")

    def achievement_patterns(self):

        return self._load(SEMANTICS, "achievement_patterns.json")

    def executive_patterns(self):

        return self._load(SEMANTICS, "executive_patterns.json")

    def direction_semantics(self):

        return self._load(SEMANTICS, "direction_semantics.json")

    def impact_rules(self):

        return self._load(SEMANTICS, "impact_rules.json")

    # =========================================================
    # ONTOLOGY
    # =========================================================

    def actions(self):

        return self._load(ONTOLOGY, "actions.json")

    def objects(self):

        return self._load(ONTOLOGY, "objects.json")

    def certifications(self):

        return self._load(ONTOLOGY, "certifications.json")

    def technologies(self):

        return self._load(ONTOLOGY, "technologies.json")

    def business_kpis(self):

        return self._load(ONTOLOGY, "business_kpis.json")

    def metrics(self):

        return self._load(ONTOLOGY, "metrics_dictionary.json")

    def domains(self):

        return self._load(ONTOLOGY, "domains_reasonings.json")