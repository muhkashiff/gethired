"""
Impact Repository

Loads business impact rules.

This keeps the Impact Engine completely
independent from storage.

Future

JSON

Ontology

Knowledge Base

Neo4j

Graph Database

REST API

No changes required to Impact Engine.
"""

from app.intelligence.utilities.knowledge.repository.repository import (
    Repository,
)


class ImpactRepository:

    def __init__(self):

        self.repository = Repository()

    # -----------------------------------------------------

    def get_rules(self):

        return self.repository.get_dictionary("impact_dictionary")

    # -----------------------------------------------------

    def get_metric(self, metric):

        rules = self.get_rules()

        return rules.get(metric)

    # -----------------------------------------------------

    def has_metric(self, metric):

        rules = self.get_rules()

        return metric in rules