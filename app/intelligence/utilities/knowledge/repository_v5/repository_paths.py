"""
Knowledge Paths

Single source of truth
for every ontology/config/semantic path.
"""

from pathlib import Path


CURRENT = Path(__file__).resolve().parent

# knowledge/
KNOWLEDGE_ROOT = CURRENT.parent

# knowledge/repository_v5/
DATA_ROOT = KNOWLEDGE_ROOT / "repository_v5"

CONFIG = DATA_ROOT / "config"

ONTOLOGY = DATA_ROOT / "ontology"

SEMANTICS = DATA_ROOT / "semantics"


class RepositoryPaths:

    ####################################################################
    # ONTOLOGY
    ####################################################################

    def __init__(self):

        self.actions = (
            ONTOLOGY / "actions.json"
        )

        self.targets = (
            ONTOLOGY / "targets.json"
        )

        self.metrics = (
            ONTOLOGY / "metrics.json"
        )

        self.business_kpis = (
            ONTOLOGY / "business_kpis.json"
        )

        self.domains = (
            ONTOLOGY / "domains.json"
        )

        self.domain_reasoning = (
            ONTOLOGY / "domain_reasoning.json"
        )

        self.certifications = (
            ONTOLOGY / "certifications.json"
        )

        self.technologies = (
            ONTOLOGY / "technologies.json"
        )

        self.impact_dictionary = (
            ONTOLOGY / "impact_dictionary.json"
        )

        self.skills = (
            ONTOLOGY / "skills.json"
        )

        self.methodologies = (
            ONTOLOGY / "methodologies.json"
        )

        self.standards = (
            ONTOLOGY / "standards.json"
        )

        ################################################################
        # RELATIONS
        ################################################################

        self.relations = (
            ONTOLOGY / "relations.json"
        )

        ####################################################################
        # CONFIG
        ####################################################################

        self.measurement_patterns = (
            CONFIG / "measurement_patterns.json"
        )

        self.modifier_dictionary = (
            CONFIG / "modifier_dictionary.json"
        )

        self.confidence_rules = (
            CONFIG / "confidence_rules.json"
        )

        ####################################################################
        # SEMANTICS
        ####################################################################

        self.measurement_semantics = (
            SEMANTICS / "measurement_semantics.json"
        )

        self.clause_patterns = (
            SEMANTICS / "clause_patterns.json"
        )