"""
Enterprise Repository V2

Single source of truth for every ontology.

Responsibilities
----------------
✓ Load every ontology once
✓ Create EntityRecord objects
✓ Build alias indexes
✓ Generic entity lookup
✓ Backward compatibility
✓ Future relations support

Version : Enterprise V2
"""

from __future__ import annotations

import json
import re

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

        self._load()

    ####################################################################
    # FILE READER
    ####################################################################

    def _read(self, path):

        with open(path, encoding="utf8") as f:

            return json.load(f)

    ####################################################################
    # NORMALIZATION
    ####################################################################

    def normalize(self, text: str) -> str:

        if text is None:

            return ""

        text = text.lower()

        text = re.sub(

            r"[^a-z0-9 ]",

            " ",

            text

        )

        text = re.sub(

            r"\s+",

            " ",

            text

        )

        return text.strip()

    ####################################################################
    # ENTITY BUILDER
    ####################################################################

    def _entity(

        self,

        data,

        ontology,

        source="ontology",

    ):

        if not data:

            return None

        return EntityRecord(

            entity_id=data.get(

                "entity_id",

                ""

            ),

            canonical=data.get(

                "canonical",

                data.get(

                    "base",

                    ""

                )

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

            source=source,

            metadata=data,

        )

    ####################################################################
    # LOAD EVERYTHING
    ####################################################################

    def _load(self):

        """
        Loads every ontology.

        Index building happens later.
        """

        self.cache.actions = self._read(

            self.paths.actions

        )

        self.cache.objects = self._read(

            self.paths.objects

        )

        self.cache.metrics = self._read(

            self.paths.metrics

        )

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

        self.cache.clause_patterns = self._read(

            self.paths.clause_patterns

        )

        self.cache.impact_dictionary = self._read(

            self.paths.impact_dictionary

        )

        self.cache.skills = self._read(

            self.paths.skills

        )

        self.cache.methodologies = self._read(

            self.paths.methodologies

        )

        self.cache.standards = self._read(

            self.paths.standards

        )
        ############################################################
            # RELATIONS
        ############################################################
        
        self._load_relations()
        
        ############################################################
        # BUILD ENTERPRISE INDEXES
        ############################################################
        
        self._build_indexes()

    ####################################################################
    # BUILD ONE ALIAS INDEX
    ####################################################################

    def _build_alias_index(

        self,

        ontology_name,

        ontology,

    ):

        alias_index = {}

        canonical_index = {}

        entity_index = {}

        normalized_index = {}

        for _, data in ontology.items():

            entity = self._entity(

                data,

                ontology_name,

            )

            if entity is None:

                continue

            ########################################################
            # Entity ID
            ########################################################

            entity_index[

                entity.entity_id

            ] = entity

            ########################################################
            # Canonical
            ########################################################

            canonical = entity.canonical

            canonical_index[

                canonical.lower()

            ] = entity

            normalized_index[

                self.normalize(canonical)

            ] = entity

            ########################################################
            # Aliases
            ########################################################

            for alias in entity.aliases:

                alias_index[

                    alias.lower()

                ] = entity

                normalized_index[

                    self.normalize(alias)

                ] = entity

        ############################################################

        self.cache.alias_indexes[

            ontology_name

        ] = alias_index

        self.cache.canonical_indexes[

            ontology_name

        ] = canonical_index

        self.cache.entity_indexes[

            ontology_name

        ] = entity_index

        self.cache.normalized_indexes[

            ontology_name

        ] = normalized_index

    ####################################################################
    # BUILD ALL INDEXES
    ####################################################################

    def _build_indexes(self):

        self._build_alias_index(

            "actions",

            self.cache.actions,

        )

        self._build_alias_index(

            "objects",

            self.cache.objects,

        )

        self._build_alias_index(

            "metrics",

            self.cache.metrics,

        )

        self._build_alias_index(

            "business_kpis",

            self.cache.business_kpis,

        )

        self._build_alias_index(

            "domains",

            self.cache.domains,

        )

        self._build_alias_index(

            "certifications",

            self.cache.certifications,

        )

        self._build_alias_index(

            "technologies",

            self.cache.technologies,

        )

        self._build_alias_index(

            "skills",

            self.cache.skills,

        )

        self._build_alias_index(

            "methodologies",

            self.cache.methodologies,

        )

        self._build_alias_index(

            "standards",

            self.cache.standards,

        )

    ####################################################################
    # LOAD RELATIONS
    ####################################################################

    def _load_relations(self):

        try:

            self.cache.relations = self._read(

                self.paths.relations

            )

        except Exception:

            self.cache.relations = {}

    ####################################################################
    # FIND ENTITY
    ####################################################################

    def find_entity(

        self,

        ontology,

        phrase,

    ):

        if phrase is None:

            return None

        ontology = ontology.lower()

        phrase = phrase.strip()

        alias_index = self.cache.alias_indexes.get(

            ontology,

            {}

        )

        canonical_index = self.cache.canonical_indexes.get(

            ontology,

            {}

        )

        normalized_index = self.cache.normalized_indexes.get(

            ontology,

            {}

        )

        ##########################################################

        entity = alias_index.get(

            phrase.lower()

        )

        if entity:

            return entity

        ##########################################################

        entity = canonical_index.get(

            phrase.lower()

        )

        if entity:

            return entity

        ##########################################################

        entity = normalized_index.get(

            self.normalize(phrase)

        )

        if entity:

            return entity

        ##########################################################

        return None
    ####################################################################
    # FIND ENTITY EXACT
    ####################################################################

    def find_entity_exact(

        self,

        ontology,

        phrase,

    ):

        if phrase is None:

            return None

        ontology = ontology.lower()

        canonical_index = self.cache.canonical_indexes.get(

            ontology,

            {}

        )

        return canonical_index.get(

            phrase.lower()

        )
    ####################################################################
    # FIND ENTITY BY ID
    ####################################################################

    def find_entity_by_id(

        self,

        ontology,

        entity_id,

    ):

        ontology = ontology.lower()

        entity_index = self.cache.entity_indexes.get(

            ontology,

            {}

        )

        return entity_index.get(entity_id)
    ####################################################################
    # FIND MULTIPLE ENTITIES
    ####################################################################

    def find_entities(

        self,

        ontology,

        phrases,

    ):

        results = []

        seen = set()

        for phrase in phrases:

            entity = self.find_entity(

                ontology,

                phrase

            )

            if entity is None:

                continue

            if entity.entity_id in seen:

                continue

            seen.add(

                entity.entity_id

            )

            results.append(entity)

        return results
    ####################################################################
    # RETURN RAW ONTOLOGY
    ####################################################################

    def ontology(

        self,

        ontology_name,

    ):

        return getattr(

            self.cache,

            ontology_name,

            {}

        )
    ####################################################################
    # BACKWARD COMPATIBILITY
    ####################################################################

    def get_action(self, phrase):

        return self.find_entity(

            "actions",

            phrase

        )

    # ---------------------------------------------------------

    def get_object(self, phrase):

        return self.find_entity(

            "objects",

            phrase

        )

    # ---------------------------------------------------------

    def get_metric(self, phrase):

        return self.find_entity(

            "metrics",

            phrase

        )

    # ---------------------------------------------------------

    def get_standard(self, phrase):

        return self.find_entity(

            "standards",

            phrase

        )

    # ---------------------------------------------------------

    def get_methodology(self, phrase):

        return self.find_entity(

            "methodologies",

            phrase

        )

    # ---------------------------------------------------------

    def get_skill(self, phrase):

        return self.find_entity(

            "skills",

            phrase

        )

    # ---------------------------------------------------------

    def get_domain(self, phrase):

        return self.find_entity(

            "domains",

            phrase

        )

    # ---------------------------------------------------------

    def get_certification(self, phrase):

        return self.find_entity(

            "certifications",

            phrase

        )

    # ---------------------------------------------------------

    def get_technology(self, phrase):

        return self.find_entity(

            "technologies",

            phrase

        )

    # ---------------------------------------------------------

    def get_business_kpi(self, phrase):

        return self.find_entity(

            "business_kpis",

            phrase

        )
    ####################################################################
    # RELATIONS
    ####################################################################

    def get_relations(self):

        return self.cache.relations


    # ---------------------------------------------------------

    def get_relation(

        self,

        relation_name,

    ):

        return self.cache.relations.get(

            relation_name,

            {}

        )
    ####################################################################
    # RAW DICTIONARIES
    ####################################################################

    def get_dictionary(

        self,

        name,

    ):

        return getattr(

            self.cache,

            name,

            {}

        )

        ####################################################################
    # KNOWLEDGE DICTIONARIES
    ####################################################################

    def get_clause_patterns(self):

        return self.cache.clause_patterns


    def get_measurement_patterns(self):

        return self.cache.measurement_patterns


    def get_measurement_semantics(self):

        return self.cache.measurement_semantics


    def get_modifier_dictionary(self):

        return self.cache.modifier_dictionary


    def get_confidence_rules(self):

        return self.cache.confidence_rules


    def get_domain_reasoning(self):

        return self.cache.domain_reasoning


    def get_impact_dictionary(self):

        return self.cache.impact_dictionary
    
    ####################################################################
    # REPOSITORY SUMMARY
    ####################################################################

    def summary(self):

        return {

            "actions": len(self.cache.actions),

            "objects": len(self.cache.objects),

            "metrics": len(self.cache.metrics),

            "standards": len(self.cache.standards),

            "methodologies": len(self.cache.methodologies),

            "skills": len(self.cache.skills),

            "technologies": len(self.cache.technologies),

            "certifications": len(self.cache.certifications),

            "domains": len(self.cache.domains),

            "business_kpis": len(self.cache.business_kpis),

        }