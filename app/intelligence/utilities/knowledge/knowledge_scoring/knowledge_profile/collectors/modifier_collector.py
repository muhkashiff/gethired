"""
Modifier Collector

Collects linguistic modifiers from the Knowledge Graph.

Examples

Cross Functional

Strategic

Global

Executive

Digital

Enterprise

Future versions

• Executive language detection

• Leadership language

• Innovation language

• ATS keyword strength

• Soft skill scoring
"""

from collections import Counter


class ModifierCollector:

    # -----------------------------------------------------

    def collect(self, graph):

        modifiers = []

        for node in graph.nodes.values():

            if node.node_type != "Modifier":
                continue

            modifiers.append(node)

        return modifiers

    # -----------------------------------------------------

    def frequencies(self, graph):

        counts = Counter()

        for node in self.collect(graph):

            counts[node.canonical] += 1

        return dict(counts)

    # -----------------------------------------------------

    def unique(self, graph):

        unique_modifiers = {}

        for node in self.collect(graph):

            unique_modifiers[node.entity_id] = node

        return list(unique_modifiers.values())

    # -----------------------------------------------------

    def categories(self, graph):

        counts = Counter()

        for node in self.collect(graph):

            counts[node.category] += 1

        return dict(counts)

    # -----------------------------------------------------

    def executive(self, graph):

        """
        Executive modifiers.
        """

        executive_categories = {

            "leadership",
            "executive",
            "strategy",
            "management"

        }

        results = []

        for node in self.collect(graph):

            if node.category.lower() in executive_categories:

                results.append(node)

        return results

    # -----------------------------------------------------

    def strengths(self, graph):

        """
        Returns modifier strengths.
        """

        strengths = []

        for node in self.collect(graph):

            strengths.append(

                {

                    "modifier": node.canonical,

                    "strength": node.metadata.get(

                        "strength",

                        1.0

                    ),

                    "executive_weight": node.metadata.get(

                        "executive_weight",

                        1.0

                    )

                }

            )

        return strengths

    # -----------------------------------------------------

    def summary(self, graph):

        modifiers = self.collect(graph)

        return {

            "count": len(modifiers),

            "categories": self.categories(graph),

            "executive_modifiers": len(

                self.executive(graph)

            )

        }