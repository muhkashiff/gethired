"""
Domain Collector

Collects all Domain nodes from the Knowledge Graph.

This collector provides:

• domain list
• frequency
• business area statistics

Future versions may include

• industry mapping
• domain clustering
• executive weighting
"""

from collections import Counter


class DomainCollector:

    # -----------------------------------------------------

    def collect(self, graph):

        domains = []

        for node in graph.nodes.values():

            if node.node_type != "Domain":
                continue

            domains.append(node)

        return domains

    # -----------------------------------------------------

    def frequencies(self, graph):

        counts = Counter()

        for node in self.collect(graph):

            counts[node.canonical] += 1

        return dict(counts)

    # -----------------------------------------------------

    def business_areas(self, graph):

        counts = Counter()

        for node in self.collect(graph):

            counts[node.business_area] += 1

        return dict(counts)

    # -----------------------------------------------------

    def unique(self, graph):

        unique_domains = {}

        for node in self.collect(graph):

            unique_domains[node.entity_id] = node

        return list(unique_domains.values())

    # -----------------------------------------------------

    def executive_domains(self, graph):

        """
        Returns domains considered
        executive-level.
        """

        executive = []

        executive_business_areas = {

            "leadership",
            "strategy",
            "operations",
            "finance",

        }

        for node in self.collect(graph):

            if node.business_area.lower() in executive_business_areas:

                executive.append(node)

        return executive