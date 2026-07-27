"""
Knowledge Graph Query Engine

Provides reusable graph queries.

Every future AI module should use this instead
of searching raw resume text.
"""

from collections import defaultdict


class GraphQuery:

    def __init__(self, graph):

        self.graph = graph

        # ------------------------------------------
        # Build lookup dictionaries
        # ------------------------------------------

        self.node_lookup = {}

        for node in graph.nodes:
            self.node_lookup[node.id] = node

        self.outgoing = defaultdict(list)

        self.incoming = defaultdict(list)

        for edge in graph.edges:

            self.outgoing[edge.source].append(edge)

            self.incoming[edge.target].append(edge)

    # ==========================================================
    # Generic
    # ==========================================================

    def nodes(self):

        return self.graph.nodes

    def edges(self):

        return self.graph.edges

    def node_by_label(self, label):

        for node in self.graph.nodes:

            if node.label.lower() == label.lower():

                return node

        return None

    def nodes_by_type(self, node_type):

        return [

            n

            for n in self.graph.nodes

            if n.node_type.lower() == node_type.lower()

        ]

    # ==========================================================
    # Relationship Queries
    # ==========================================================

    def children(self, node):

        result = []

        for edge in self.outgoing[node.id]:

            result.append(self.node_lookup[edge.target])

        return result

    def parents(self, node):

        result = []

        for edge in self.incoming[node.id]:

            result.append(self.node_lookup[edge.source])

        return result

    def relations(self, node):

        result = []

        for edge in self.outgoing[node.id]:

            result.append(

                (

                    edge.relation,

                    self.node_lookup[edge.target],

                )

            )

        return result

    # ==========================================================
    # Resume Intelligence Queries
    # ==========================================================

    def achievements(self):

        return self.nodes_by_type("Action")

    def metrics(self):

        return self.nodes_by_type("Metric")

    def measurements(self):

        return self.nodes_by_type("Measurement")

    def domains(self):

        return self.nodes_by_type("Domain")

    def objects(self):

        return self.nodes_by_type("Object")

    # ==========================================================
    # Domain Search
    # ==========================================================

    def actions_in_domain(self, domain_name):

        result = []

        domain = self.node_by_label(domain_name)

        if domain is None:

            return result

        for edge in self.incoming[domain.id]:

            result.append(

                self.node_lookup[edge.source]

            )

        return result

    # ==========================================================
    # Metric Search
    # ==========================================================

    def metric_value(self, metric_name):

        metric = self.node_by_label(metric_name)

        if metric is None:

            return None

        for edge in self.outgoing[metric.id]:

            if edge.relation == "measured_as":

                return self.node_lookup[edge.target]

        return None

    # ==========================================================
    # Pretty Printing
    # ==========================================================

    def print_graph(self):

        print("=" * 70)

        print("KNOWLEDGE GRAPH")

        print("=" * 70)

        for node in self.graph.nodes:

            print()

            print(f"{node.node_type}: {node.label}")

            for relation, child in self.relations(node):

                print(

                    f"    └── {relation} ---> {child.label}"

                )