"""
Enterprise Graph Query API

Provides all graph retrieval operations.

This module NEVER performs graph traversal.

It only returns graph objects.

Everything else builds on top of this.

Enterprise Version
"""

from collections import defaultdict


class GraphQueryAPI:

    def __init__(self, graph):

        self.graph = graph

    # =====================================================
    # BASIC COLLECTIONS
    # =====================================================

    def nodes(self):
        return list(self.graph.nodes.values())

    def edges(self):
        return self.graph.edges

    # =====================================================
    # SINGLE OBJECT LOOKUP
    # =====================================================

    def node(self, node_id):

        return self.graph.nodes.get(node_id)

    def edge(self, edge_id):

        for edge in self.graph.edges:

            if edge.edge_id == edge_id:

                return edge

        return None

    # =====================================================
    # GENERIC FILTER
    # =====================================================

    def find(self, **kwargs):

        results = []

        for node in self.nodes():

            match = True

            for key, value in kwargs.items():

                if getattr(node, key, None) != value:

                    match = False
                    break

            if match:

                results.append(node)

        return results

    # =====================================================
    # ENTITY TYPES
    # =====================================================

    def by_entity_type(self, entity_type):

        return [

            node

            for node in self.nodes()

            if node.entity_type.lower() == entity_type.lower()

        ]

    def actions(self):

        return self.by_entity_type("action")

    def objects(self):

        return self.by_entity_type("object")

    def metrics(self):

        return self.by_entity_type("metric")

    def measurements(self):

        return self.by_entity_type("measurement")

    def domains(self):

        return self.by_entity_type("domain")

    def standards(self):

        return self.by_entity_type("standard")

    def skills(self):

        return self.by_entity_type("skill")

    def methodologies(self):

        return self.by_entity_type("methodology")

    def technologies(self):

        return self.by_entity_type("technology")

    def tools(self):

        return self.by_entity_type("tool")

    def industries(self):

        return self.by_entity_type("industry")

    # =====================================================
    # CATEGORY
    # =====================================================

    def by_category(self, category):

        return [

            node

            for node in self.nodes()

            if node.category.lower() == category.lower()

        ]

    # =====================================================
    # DOMAIN
    # =====================================================

    def by_domain(self, domain):

        return [

            node

            for node in self.nodes()

            if node.domain.lower() == domain.lower()

        ]

    # =====================================================
    # BUSINESS AREA
    # =====================================================

    def by_business_area(self, business_area):

        return [

            node

            for node in self.nodes()

            if node.business_area.lower()

            == business_area.lower()

        ]

    # =====================================================
    # LABEL SEARCH
    # =====================================================

    def by_label(self, label):

        return [

            node

            for node in self.nodes()

            if node.label.lower() == label.lower()

        ]

    def contains(self, text):

        text = text.lower()

        return [

            node

            for node in self.nodes()

            if text in node.label.lower()

            or text in node.canonical.lower()

        ]

    # =====================================================
    # GROUPING
    # =====================================================

    def group_by_entity_type(self):

        groups = defaultdict(list)

        for node in self.nodes():

            groups[node.entity_type].append(node)

        return dict(groups)

    def group_by_category(self):

        groups = defaultdict(list)

        for node in self.nodes():

            groups[node.category].append(node)

        return dict(groups)

    def group_by_business_area(self):

        groups = defaultdict(list)

        for node in self.nodes():

            groups[node.business_area].append(node)

        return dict(groups)

    # =====================================================
    # EXISTENCE
    # =====================================================

    def exists(self, node_id):

        return node_id in self.graph.nodes

    # =====================================================
    # COUNTS
    # =====================================================

    def node_count(self):

        return len(self.graph.nodes)

    def edge_count(self):

        return len(self.graph.edges)