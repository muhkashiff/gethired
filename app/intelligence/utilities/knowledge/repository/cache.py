"""
Repository Cache

Caches every ontology in memory.

Loaded once by Repository.
"""

from dataclasses import dataclass, field


@dataclass
class RepositoryCache:

    # ----------------------------
    # Ontology
    # ----------------------------

    actions: dict = field(default_factory=dict)

    objects: dict = field(default_factory=dict)

    metrics: dict = field(default_factory=dict)

    business_kpis: dict = field(default_factory=dict)

    domains: dict = field(default_factory=dict)

    domain_reasoning: dict = field(default_factory=dict)

    certifications: dict = field(default_factory=dict)

    technologies: dict = field(default_factory=dict)

    # ----------------------------
    # Semantics
    # ----------------------------

    measurement_semantics: dict = field(default_factory=dict)

    # ----------------------------
    # Config
    # ----------------------------

    modifier_dictionary: dict = field(default_factory=dict)

    confidence_rules: dict = field(default_factory=dict)

    measurement_patterns: dict = field(default_factory=dict)

    aliases: dict = field(default_factory=dict)

    clause_patterns: dict = field(default_factory=dict)

    impact_dictionary: dict = field(default_factory=dict)