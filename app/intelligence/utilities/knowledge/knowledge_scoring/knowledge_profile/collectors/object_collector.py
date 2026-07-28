"""
Object Collector

Collects all Object nodes from the Knowledge Graph.

Later this collector can:

• group duplicate objects
• merge aliases
• rank important resume entities
• build object statistics

Currently it simply returns every Object node.
"""

from collections import Counter


class ObjectCollector:

    def collect(self, graph):

        objects = []

        for node in graph.nodes.values():

            if node.node_type != "Object":
                continue

            objects.append(node)

        return objects

    # -----------------------------------------------------

    def frequencies(self, graph):

        counts = Counter()

        for node in self.collect(graph):

            counts[node.canonical] += 1

        return dict(counts)

    # -----------------------------------------------------

    def unique(self, graph):

        unique_objects = {}

        for node in self.collect(graph):

            unique_objects[node.entity_id] = node

        return list(unique_objects.values())