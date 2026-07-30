"""
Knowledge Paths

Single source of truth
for every ontology/config path.
"""

from pathlib import Path


CURRENT = Path(__file__).resolve().parent

KNOWLEDGE_ROOT = CURRENT.parent

DATA_ROOT = KNOWLEDGE_ROOT / "knowledge_knowledge"

CONFIG = DATA_ROOT / "config"

ONTOLOGY = DATA_ROOT / "ontology"

SEMANTICS = DATA_ROOT / "semantics"


class RepositoryPaths:

    def __init__(self):

        # -------------------
        # Ontology
        # -------------------

        self.actions = ONTOLOGY / "actions.json"

        self.objects = ONTOLOGY / "objects.json"

        self.metrics = ONTOLOGY / "metrics_dictionary.json"

        self.business_kpis = ONTOLOGY / "business_kpis.json"

        self.domains = ONTOLOGY / "domains.json"

        self.domain_reasoning = ONTOLOGY / "domain_reasoning.json"

        self.certifications = ONTOLOGY / "certifications.json"

        self.technologies = ONTOLOGY / "technologies.json"

        self.impact_dictionary = ONTOLOGY/ "impact_dictionary.json"

        self.skills = ONTOLOGY / "skills.json"

        self.methodologies = ONTOLOGY / "methodologies.json"
    
        # -------------------
        # Config
        # -------------------

        self.measurement_patterns = CONFIG / "measurement_patterns.json"

        self.modifier_dictionary = CONFIG / "modifier_dictionary.json"

        self.confidence_rules = CONFIG / "confidence_rules.json"

        # -------------------
        # Semantics
        # -------------------

        self.measurement_semantics = (
            SEMANTICS / "measurement_semantics.json"
        )

        self.clause_patterns = (
            SEMANTICS / "clause_patterns.json"
                )

        