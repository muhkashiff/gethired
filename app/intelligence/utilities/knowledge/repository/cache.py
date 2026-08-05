"""
Enterprise Repository Cache

Stores every ontology only once.

Also stores:

- alias indexes
- entity indexes
- normalized indexes

Version : Enterprise V2
"""

from dataclasses import dataclass, field


@dataclass
class RepositoryCache:

    ####################################################################
    # RAW ONTOLOGIES
    ####################################################################

    actions: dict = field(default_factory=dict)

    targets: dict = field(default_factory=dict)

    metrics: dict = field(default_factory=dict)

    standards: dict = field(default_factory=dict)

    methodologies: dict = field(default_factory=dict)

    skills: dict = field(default_factory=dict)

    technologies: dict = field(default_factory=dict)

    certifications: dict = field(default_factory=dict)

    domains: dict = field(default_factory=dict)

    business_kpis: dict = field(default_factory=dict)

    ####################################################################
    # SEMANTICS
    ####################################################################

    measurement_semantics: dict = field(default_factory=dict)

    impact_dictionary: dict = field(default_factory=dict)

    domain_reasoning: dict = field(default_factory=dict)

    ####################################################################
    # CONFIGURATION
    ####################################################################

    modifier_dictionary: dict = field(default_factory=dict)

    confidence_rules: dict = field(default_factory=dict)

    measurement_patterns: dict = field(default_factory=dict)

    clause_patterns: dict = field(default_factory=dict)

    ####################################################################
    # ENTERPRISE INDEXES
    ####################################################################

    #
    # alias_indexes
    #
    # Example
    #
    # alias_indexes["standards"]["gmp"]
    #
    # → EntityRecord(...)
    #
    alias_indexes: dict = field(default_factory=dict)

    #
    # canonical_indexes
    #
    # canonical_indexes["targets"]
    #
    canonical_indexes: dict = field(default_factory=dict)

    #
    # entity_id indexes
    #
    entity_indexes: dict = field(default_factory=dict)

    #
    # normalized indexes
    #
    normalized_indexes: dict = field(default_factory=dict)

    relations: dict = field(default_factory=dict)