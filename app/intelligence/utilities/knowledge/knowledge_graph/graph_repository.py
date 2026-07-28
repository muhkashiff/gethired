"""
Knowledge Graph Repository

Provides fast lookup over graph nodes and edges.

Every future module (ATS, RAG, Narrative, Intelligence)
uses this repository instead of directly walking the graph.
"""

from collections import defaultdict


class GraphRepository:

    def __init__(self, graph):

        self.graph = graph

        self.node_index = {}
        self.node_type_index = defaultdict(list)
        self.edge_index = defaultdict(list)

        self._build_indexes()

    # ---------------------------------------------------------

    def _build_indexes(self):

        for node in self.graph.nodes:

            self.node_index[node.entity_id] = node

            self.node_type_index[node.node_type].append(node)

        for edge in self.graph.edges:

            self.edge_index[edge.source_node].append(edge)

            self.edge_index[edge.target_node].append(edge)

    # ---------------------------------------------------------
    # Node Queries
    # ---------------------------------------------------------

    def find_node(self, entity_id):

        return self.node_index.get(entity_id)

    # ---------------------------------------------------------

    def get_nodes_by_type(self, node_type):

        return self.node_type_index.get(node_type, [])

    # ---------------------------------------------------------

    def get_all_nodes(self):

        return self.graph.nodes

    # ---------------------------------------------------------
    # Edge Queries
    # ---------------------------------------------------------

    def find_relationships(self, entity_id):

        return self.edge_index.get(entity_id, [])

    # ---------------------------------------------------------

    def get_all_edges(self):

        return self.graph.edges

    # ---------------------------------------------------------

    def connected_nodes(self, entity_id):

        nodes = []

        for edge in self.find_relationships(entity_id):

            if edge.source_node == entity_id:

                node = self.find_node(edge.target_node)

            else:

                node = self.find_node(edge.source_node)

            if node:

                nodes.append(node)

        return nodes