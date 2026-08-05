"""
Enterprise Relation Rule Engine

Enterprise V12

Provides reusable relationship-based reasoning.

Knowledge Graph
        ↓
Graph Edge
        ↓
Rule Engine
        ↓
Capability
"""

from dataclasses import dataclass


# ==========================================================
# Rule Definition
# ==========================================================

@dataclass
class RelationRule:

    relation: str

    source_type: str = ""

    target_type: str = ""

    capability: str = ""

    weight: float = 1.0

    confidence: float = 1.0


# ==========================================================
# Rule Engine
# ==========================================================

class RelationRuleEngine:

    def __init__(self):

        self.rules = []

    # -----------------------------------------------------

    def register(self, rule: RelationRule):

        self.rules.append(rule)

    # -----------------------------------------------------

    def register_many(self, rules):

        for rule in rules:

            self.register(rule)

    # -----------------------------------------------------

    def clear(self):

        self.rules.clear()

    # -----------------------------------------------------

    def evaluate(

        self,

        edge,

        source,

        target,

    ):

        """
        Returns all matching rules.
        """

        matched = []

        for rule in self.rules:

            if edge.relation.upper() != rule.relation.upper():

                continue

            if rule.source_type:

                if source.entity_type.lower() != rule.source_type.lower():

                    continue

            if rule.target_type:

                if target.entity_type.lower() != rule.target_type.lower():

                    continue

            matched.append(rule)

        return matched