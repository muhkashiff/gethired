"""
Enterprise Ontology Repository
==============================

Version : 3.0

Responsibilities
----------------
✓ Load ontology files
✓ Validate schema
✓ Normalize entities
✓ Build alias indexes
✓ Build ID indexes
✓ Build category indexes
✓ Build business area indexes
✓ Build domain indexes
✓ Build relationship indexes
✓ Provide unified lookup APIs
✓ Preserve backward compatibility
"""

from __future__ import annotations

import json
from collections import defaultdict

from app.intelligence.utilities.knowledge.repository.paths import RepositoryPaths
from app.intelligence.utilities.knowledge.repository.cache import RepositoryCache
from app.intelligence.utilities.knowledge.repository.entity_record import EntityRecord


class Repository:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.paths = RepositoryPaths()

        self.cache = RepositoryCache()

        # Enterprise Indexes
        self.alias_indexes = {}
        self.id_indexes = {}
        self.category_indexes = {}
        self.business_area_indexes = {}
        self.domain_indexes = {}
        self.relationship_indexes = {}

        self._load()

        self._build_indexes()

    ####################################################################
    # JSON READER
    ####################################################################

    def _read(self, path):

        with open(path, encoding="utf-8") as f:

            return json.load(f)

    ####################################################################
    # LOAD ALL KNOWLEDGE FILES
    ####################################################################

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

        self.cache.domain_reasoning = self._read(
            self.paths.domain_reasoning
        )

        self.cache.certifications = self._read(
            self.paths.certifications
        )

        self.cache.standards = self._read(
            self.paths.standards
        )

        self.cache.skills = self._read(
            self.paths.skills
        )

        self.cache.methodologies = self._read(
            self.paths.methodologies
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

        self.cache.impact_dictionary = self._read(
            self.paths.impact_dictionary
        )

        self.cache.clause_patterns = self._read(
            self.paths.clause_patterns
        )

        # Optional Files

        try:
            self.cache.relations = self._read(
                self.paths.relations
            )
        except Exception:
            self.cache.relations = {}

    ####################################################################
    # ENTITY VALIDATION
    ####################################################################

    def _validate_entity(self, data):

        if not isinstance(data, dict):

            return False

        # canonical is mandatory

        if "canonical" not in data:

            return False

        return True

    ####################################################################
    # ENTITY NORMALIZATION
    ####################################################################

    def _entity(self, data, source="ontology"):

        if not data:

            return None

        if not self._validate_entity(data):

            return None

        return EntityRecord(

            entity_id=data.get(
                "entity_id",
                ""
            ),

            canonical=data.get(
                "canonical",
                data.get("base", "")
            ),

            aliases=data.get(
                "aliases",
                []
            ),

            category=data.get(
                "category",
                ""
            ),

            business_area=data.get(
                "business_area",
                ""
            ),

            preferred_direction=data.get(
                "preferred_direction",
                ""
            ),

            impact_weight=float(
                data.get(
                    "impact_weight",
                    1.0
                )
            ),

            business_meaning=data.get(
                "business_meaning",
                ""
            ),

            metadata=data,

            source=source

        )
        ####################################################################
    # ENTERPRISE INDEX BUILDER
    ####################################################################

    def _build_indexes(self):

        """
        Build all enterprise lookup indexes.

        This executes only once during Repository startup.
        """

        ontology_tables = {

            "actions": self.cache.actions,

            "objects": self.cache.objects,

            "metrics": self.cache.metrics,

            "business_kpis": self.cache.business_kpis,

            "domains": self.cache.domains,

            "skills": self.cache.skills,

            "technologies": self.cache.technologies,

            "methodologies": self.cache.methodologies,

            "standards": self.cache.standards,

            "certifications": self.cache.certifications

        }

        for ontology_name, table in ontology_tables.items():

            alias_index = {}

            id_index = {}

            category_index = defaultdict(list)

            business_area_index = defaultdict(list)

            domain_index = defaultdict(list)

            canonical_index = {}

            ##############################################################

            for key, entity in table.items():

                if not isinstance(entity, dict):

                    continue

                record = self._entity(entity)

                if record is None:

                    continue

                ##########################################################
                # Entity ID Index
                ##########################################################

                if record.entity_id:

                    id_index[
                        record.entity_id
                    ] = record

                ##########################################################
                # Canonical Index
                ##########################################################

                if record.canonical:

                    canonical_index[
                        record.canonical.lower()
                    ] = record

                    alias_index[
                        record.canonical.lower()
                    ] = record

                ##########################################################
                # Alias Index
                ##########################################################

                for alias in record.aliases:

                    alias_index[
                        alias.lower()
                    ] = record

                ##########################################################
                # Original JSON Key
                ##########################################################

                alias_index[
                    key.lower()
                ] = record

                ##########################################################
                # Category Index
                ##########################################################

                if record.category:

                    category_index[
                        record.category
                    ].append(record)

                ##########################################################
                # Business Area Index
                ##########################################################

                if record.business_area:

                    business_area_index[
                        record.business_area
                    ].append(record)

                ##########################################################
                # Domain Index
                ##########################################################

                domain = record.metadata.get(
                    "domain"
                )

                if domain:

                    domain_index[
                        domain
                    ].append(record)

            ##############################################################

            self.alias_indexes[
                ontology_name
            ] = alias_index

            self.id_indexes[
                ontology_name
            ] = id_index

            self.category_indexes[
                ontology_name
            ] = category_index

            self.business_area_indexes[
                ontology_name
            ] = business_area_index

            self.domain_indexes[
                ontology_name
            ] = domain_index

        ##############################################################
        # Build Relations
        ##############################################################

        self._build_relation_index()
    ####################################################################
    # GENERIC ENTITY LOOKUP
    ####################################################################

    def find_entity(self, ontology_name, phrase):
        """
        Generic entity lookup.

        Examples
        --------
        repo.find_entity("skills", "Lean")

        repo.find_entity("technologies", "Python")

        repo.find_entity("methodologies", "Kaizen")
        """

        if phrase is None:
            return None

        alias_index = self.alias_indexes.get(
            ontology_name,
            {}
        )

        return alias_index.get(
            str(phrase).lower()
        )

    ####################################################################
    # LOOKUP BY ENTITY ID
    ####################################################################

    def find_entity_by_id(self,
                          ontology_name,
                          entity_id):

        if entity_id is None:
            return None

        return self.id_indexes.get(
            ontology_name,
            {}
        ).get(entity_id)

    ####################################################################
    # LOOKUP BY CATEGORY
    ####################################################################

    def find_by_category(self,
                         ontology_name,
                         category):

        return self.category_indexes.get(
            ontology_name,
            {}
        ).get(category, [])

    ####################################################################
    # LOOKUP BY BUSINESS AREA
    ####################################################################

    def find_by_business_area(self,
                              ontology_name,
                              business_area):

        return self.business_area_indexes.get(
            ontology_name,
            {}
        ).get(business_area, [])

    ####################################################################
    # LOOKUP BY DOMAIN
    ####################################################################

    def find_by_domain(self,
                       ontology_name,
                       domain):

        return self.domain_indexes.get(
            ontology_name,
            {}
        ).get(domain, [])

    ####################################################################
    # RELATION LOOKUP
    ####################################################################

    def get_relations(self,
                      entity_id):

        return self.relationship_indexes.get(
            entity_id,
            [])

    ####################################################################
    # SEARCH ACROSS ALL ONTOLOGIES
    ####################################################################

    def search(self, phrase):

        phrase = str(phrase).lower()

        for ontology_name, alias_index in self.alias_indexes.items():

            entity = alias_index.get(phrase)

            if entity:

                return ontology_name, entity

        return None, None

    ####################################################################
    # ENTITY EXISTENCE
    ####################################################################

    def exists(self,
               ontology_name,
               phrase):

        return self.find_entity(
            ontology_name,
            phrase
        ) is not None

    ####################################################################
    # GET ALL ENTITIES
    ####################################################################

    def get_all_entities(self,
                         ontology_name):

        return list(

            self.id_indexes.get(

                ontology_name,

                {}

            ).values()

        )
    ####################################################################
    # BACKWARD COMPATIBLE LOOKUPS
    ####################################################################

    def get_action(self, phrase):
        return self.find_entity("actions", phrase)

    def get_object(self, phrase):
        return self.find_entity("objects", phrase)

    def get_metric(self, phrase):
        return self.find_entity("metrics", phrase)

    def get_business_kpi(self, phrase):
        return self.find_entity("business_kpis", phrase)

    def get_domain(self, phrase):
        return self.find_entity("domains", phrase)

    def get_skill(self, phrase):
        return self.find_entity("skills", phrase)

    def get_methodology(self, phrase):
        return self.find_entity("methodologies", phrase)

    def get_standard(self, phrase):
        return self.find_entity("standards", phrase)

    def get_certification(self, phrase):
        return self.find_entity("certifications", phrase)

    def get_technology(self, phrase):
        return self.find_entity("technologies", phrase)