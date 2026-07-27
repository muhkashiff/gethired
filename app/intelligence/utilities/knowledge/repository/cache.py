"""
Repository Cache

Loads ontology once.

Everything else uses memory.
"""

from dataclasses import dataclass, field


@dataclass
class RepositoryCache:

    actions: dict = field(default_factory=dict)

    objects: dict = field(default_factory=dict)

    metrics: dict = field(default_factory=dict)

    certifications: dict = field(default_factory=dict)

    technologies: dict = field(default_factory=dict)

    aliases: dict = field(default_factory=dict)

    domains: dict = field(default_factory=dict)

    semantics: dict = field(default_factory=dict)

    config: dict = field(default_factory=dict)