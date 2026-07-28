"""
Ontology Repository

Central ontology repository.

Loads every ontology/config file once and returns
EntityRecord objects instead of raw JSON whenever possible.

Backward compatibility is preserved.
"""

import json

from app.intelligence.utilities.knowledge.repository.paths import RepositoryPaths
from app.intelligence.utilities.knowledge.repository.cache import RepositoryCache
from app.intelligence.utilities.knowledge.repository.entity_record import EntityRecord


class Repository:

    def __init__(self):

        self.paths = RepositoryPaths()
        self.cache = RepositoryCache()

        self._load()

    # ---------------------------------------------------------

    def _read(self, path):

        with open(path, encoding="utf8") as f:
            return json.load(f)

    # ---------------------------------------------------------

    def _load(self):

        self.cache.actions = self._read(self.paths.actions)

        self.cache.objects = self._read(self.paths.objects)

        self.cache.metrics = self._read(self.paths.metrics)

        self.cache.business_kpis = self._read(
            self.paths.business_kpis
        )

        self.cache.domains = self._read(
            self.paths.domains
        )
        self.cache.impact_dictionary = self._read(
                self.paths.impact_dictionary
            )

        self.cache.domain_reasoning = self._read(
            self.paths.domain_reasoning
        )

        self.cache.certifications = self._read(
            self.paths.certifications
        )

        self.cache.technologies = self._read(
            self.paths.technologies
        )

        self.cache.measurement_patterns = self._read(
            self.paths.measurement_patterns
        )

        self.cache.measurement_semantics = self._read(
            self.paths.measurement_semantics
        )

        self.cache.modifier_dictionary = self._read(
            self.paths.modifier_dictionary
        )

        self.cache.confidence_rules = self._read(
            self.paths.confidence_rules
        )

        self.cache.clause_patterns = self._read(self.paths.clause_patterns)

    # =========================================================
    # Entity Builders
    # =========================================================

    def _entity(self, data, source="ontology"):

        if not data:
            return None

        return EntityRecord(

            entity_id=data.get("entity_id", ""),

            canonical=data.get(
                "canonical",
                data.get("base", "")
            ),

            aliases=data.get("aliases", []),

            category=data.get("category", ""),

            business_area=data.get(
                "business_area",
                ""
            ),

            preferred_direction=data.get(
                "preferred_direction",
                ""
            ),

            impact_weight=float(
                data.get("impact_weight", 1.0)
            ),

            business_meaning=data.get(
                "business_meaning",
                ""
            ),

            source=source,

            metadata=data

        )

    # =========================================================
    # Repository Lookups
    # =========================================================

    def get_action(self, word):

        data = self.cache.actions.get(word)

        return self._entity(data)

    # ---------------------------------------------------------

    def get_object(self, phrase):

        data = self.cache.objects.get(phrase)

        return self._entity(data)

    # ---------------------------------------------------------

    def get_metric(self, phrase):

        data = self.cache.metrics.get(phrase)

        return self._entity(data)

    # ---------------------------------------------------------

    def get_business_kpi(self, phrase):

        data = self.cache.business_kpis.get(phrase)

        return self._entity(data)

    # ---------------------------------------------------------

    def get_certification(self, phrase):

        data = self.cache.certifications.get(phrase)

        return self._entity(data)

    # ---------------------------------------------------------

    def get_technology(self, phrase):

        data = self.cache.technologies.get(phrase)

        return self._entity(data)

    # ---------------------------------------------------------

    def get_domain(self, domain):

        data = self.cache.domains.get(domain)

        return self._entity(data)

    # =========================================================
    # Backward Compatible API
    # =========================================================

    def actions(self):
        return self.cache.actions

    def objects(self):
        return self.cache.objects

    def metrics(self):
        return self.cache.metrics

    def business_kpis(self):
        return self.cache.business_kpis

    def domains(self):
        return self.cache.domains

    def domain_reasoning(self):
        return self.cache.domain_reasoning

    def certifications(self):
        return self.cache.certifications

    def technologies(self):
        return self.cache.technologies

    def measurement_patterns(self):
        return self.cache.measurement_patterns

    def modifier_dictionary(self):
        return self.cache.modifier_dictionary

    def measurement_semantics(self):
        return self.cache.measurement_semantics

    def confidence_rules(self):
        return self.cache.confidence_rules

    def get_dictionary(self, name):

        dictionaries = {

            "actions": self.cache.actions,

            "objects": self.cache.objects,

            "metrics": self.cache.metrics,

            "business_kpis": self.cache.business_kpis,

            "domains": self.cache.domains,

            "domain_reasoning": self.cache.domain_reasoning,

            "certifications": self.cache.certifications,

            "technologies": self.cache.technologies,

            "measurement_patterns": self.cache.measurement_patterns,

            "measurement_semantics": self.cache.measurement_semantics,

            "modifier_dictionary": self.cache.modifier_dictionary,

            "confidence_rules": self.cache.confidence_rules,

            "impact_dictionary": self.cache.impact_dictionary,

        }

        return dictionaries.get(name, {})

    def get_measurement_patterns(self):
        return self.cache.measurement_patterns

    def get_modifier_dictionary(self):
        return self.cache.modifier_dictionary

    def get_domains(self):
        return self.cache.domains


    def get_domain_reasoning(self):
        return self.cache.domain_reasoning

    def get_clause_patterns(self):
        return self.cache.clause_patterns

    def get_impact_dictionary(self):
        return self.cache.impact_dictionary

    