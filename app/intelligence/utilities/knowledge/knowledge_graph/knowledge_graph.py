"""
Enterprise Knowledge Graph

Stores all nodes and edges.

Provides an Enterprise Graph API.

Enterprise V6
"""

from collections import defaultdict

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphNode,
    GraphEdge,
    GraphStatistics,
)


class KnowledgeGraph:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.nodes = {}

        self.edges = []

        self.statistics = GraphStatistics()

    ####################################################################
    # ADD NODE
    ####################################################################

    def add_node(self, node: GraphNode):

        if node.node_id in self.nodes:

            return self.nodes[node.node_id]

        self.nodes[node.node_id] = node

        self.statistics.node_count += 1

        self.statistics.entity_counts[node.entity_type] = (

            self.statistics.entity_counts.get(
                node.entity_type,
                0,
            ) + 1

        )

        return node

    ####################################################################
    # ADD EDGE
    ####################################################################

    def add_edge(self, edge: GraphEdge):

        self.edges.append(edge)

        self.statistics.edge_count += 1

        self.statistics.relation_counts[edge.relation] = (

            self.statistics.relation_counts.get(
                edge.relation,
                0,
            ) + 1

        )

        if edge.source_id in self.nodes:

            self.nodes[edge.source_id].outgoing_edges.append(edge)

        if edge.target_id in self.nodes:

            self.nodes[edge.target_id].incoming_edges.append(edge)

    ####################################################################
    # BASIC API
    ####################################################################

    def get_node(self, node_id):

        return self.nodes.get(node_id)

    def get_nodes(self):

        return list(self.nodes.values())

    def get_edges(self):

        return self.edges

    ####################################################################
    # TYPE FILTERS
    ####################################################################

    def find_by_type(self, entity_type):

        entity_type = entity_type.lower()

        return [

            node

            for node in self.nodes.values()

            if node.entity_type.lower() == entity_type

        ]

    ####################################################################
    # SHORTCUTS
    ####################################################################

    def actions(self):

        return self.find_by_type("action")

    def objects(self):

        return self.find_by_type("object")

    def domains(self):

        return self.find_by_type("domain")

    def standards(self):

        return self.find_by_type("standard")

    def skills(self):

        return self.find_by_type("skill")

    def metrics(self):

        return self.find_by_type("metric")

    def measurements(self):

        return self.find_by_type("measurement")

    def methodologies(self):

        return self.find_by_type("methodology")

    ####################################################################
    # CATEGORY FILTER
    ####################################################################

    def category(self, category):

        category = category.lower()

        return [

            node

            for node in self.nodes.values()

            if node.category.lower() == category

        ]

    ####################################################################
    # BUSINESS AREA FILTER
    ####################################################################

    def business_area(self, area):

        area = area.lower()

        return [

            node

            for node in self.nodes.values()

            if node.business_area.lower() == area

        ]

    ####################################################################
    # RELATION FILTER
    ####################################################################

    def relations(self, relation):

        relation = relation.lower()

        return [

            edge

            for edge in self.edges

            if edge.relation.lower() == relation

        ]

    ####################################################################
    # GRAPH TRAVERSAL
    ####################################################################

    def successors(self, node_id):

        node = self.get_node(node_id)

        if node is None:

            return []

        output = []

        for edge in node.outgoing_edges:

            target = self.get_node(edge.target_id)

            if target:

                output.append(target)

        return output

    ####################################################################

    def predecessors(self, node_id):

        node = self.get_node(node_id)

        if node is None:

            return []

        output = []

        for edge in node.incoming_edges:

            source = self.get_node(edge.source_id)

            if source:

                output.append(source)

        return output

    ####################################################################

    def neighbors(self, node_id):

        return (

            self.successors(node_id)

            +

            self.predecessors(node_id)

        )

    ####################################################################
    # COUNTS
    ####################################################################

    def count(self, entity_type):

        return len(

            self.find_by_type(entity_type)

        )

    ####################################################################
    # GRAPH SUMMARY
    ####################################################################

    def summary(self):

        return {

            "nodes": self.statistics.node_count,

            "edges": self.statistics.edge_count,

            "entities": self.statistics.entity_counts,

            "relations": self.statistics.relation_counts,

        }

    ####################################################################

    def get_statistics(self):

        return self.statistics