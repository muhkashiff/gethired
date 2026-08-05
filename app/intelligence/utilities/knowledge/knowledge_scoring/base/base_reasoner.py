"""
Enterprise Base Reasoner

Enterprise V12

Provides reusable graph reasoning utilities.

Every reasoning engine inherits from this class.

KnowledgeGraph
        ↓
BaseReasoner
        ↓
Specialized Reasoner
"""

from abc import ABC, abstractmethod


class BaseReasoner(ABC):

    def __init__(self):

        self.graph = None

    # =====================================================
    # Entry Point
    # =====================================================

    @abstractmethod
    def reason(self, graph):
        """
        Every child implements this.
        """
        raise NotImplementedError()

    # =====================================================
    # Validation
    # =====================================================

    def validate_graph(self, graph):

        if graph is None:

            raise ValueError("KnowledgeGraph cannot be None.")

        self.graph = graph

        return True

    # =====================================================
    # Graph Access
    # =====================================================

    def nodes(self):

        return self.graph.get_nodes()

    def edges(self):

        return self.graph.get_edges()

    # =====================================================
    # Node Lookup
    # =====================================================

    def node(self, node_id):

        return self.graph.get_node(node_id)

    # =====================================================
    # Entity Filters
    # =====================================================

    def entities(self, entity_type):

        return self.graph.find_by_type(entity_type)

    def actions(self):

        return self.entities("Action")

    def targets(self):

        return self.entities("Target")

    def objects(self):

        return self.entities("Object")

    def metrics(self):

        return self.entities("Metric")

    def measurements(self):

        return self.entities("Measurement")

    def standards(self):

        return self.entities("Standard")

    def methodologies(self):

        return self.entities("Methodology")

    def domains(self):

        return self.entities("Domain")

    def skills(self):

        return self.entities("Skill")

    # =====================================================
    # Relation Filters
    # =====================================================

    def relations(self, relation):

        return self.graph.relations(relation)

    # =====================================================
    # Graph Traversal
    # =====================================================

    def successors(self, node):

        if node is None:

            return []

        return self.graph.successors(node.node_id)

    def predecessors(self, node):

        if node is None:

            return []

        return self.graph.predecessors(node.node_id)

    def neighbors(self, node):

        if node is None:

            return []

        return self.graph.neighbors(node.node_id)

    # =====================================================
    # Relationship Helpers
    # =====================================================

    def outgoing_relations(self, node):

        if node is None:

            return []

        return node.outgoing_edges

    def incoming_relations(self, node):

        if node is None:

            return []

        return node.incoming_edges

    # =====================================================
    # Relation Navigation
    # =====================================================

    def source_node(self, edge):

        return self.node(edge.source_id)

    def target_node(self, edge):

        return self.node(edge.target_id)

    # =====================================================
    # Find Relations For Node
    # =====================================================

    def find_outgoing(self, node, relation=None):

        output = []

        for edge in self.outgoing_relations(node):

            if relation is None:

                output.append(edge)

            elif edge.relation.upper() == relation.upper():

                output.append(edge)

        return output

    def find_incoming(self, node, relation=None):

        output = []

        for edge in self.incoming_relations(node):

            if relation is None:

                output.append(edge)

            elif edge.relation.upper() == relation.upper():

                output.append(edge)

        return output

    # =====================================================
    # Graph Statistics
    # =====================================================

    def node_count(self):

        return len(self.nodes())

    def edge_count(self):

        return len(self.edges())

    # =====================================================
    # Confidence Utility
    # =====================================================

    def average_confidence(self, values):

        if not values:

            return 0.0

        return round(

            sum(values) / len(values),

            2,

        )
    