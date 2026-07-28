"""
Knowledge Graph Query Engine

Provides simple APIs for querying a KnowledgeGraph.
"""

from app.intelligence.utilities.knowledge.knowledge_graph.graph_repository import (
    GraphRepository,
)


class GraphQueryEngine:

    def __init__(self, graph):

        self.repository = GraphRepository(graph)

    # -------------------------------------------------

    def actions(self):

        return self.repository.get_nodes_by_type("Action")

    # -------------------------------------------------

    def objects(self):

        return self.repository.get_nodes_by_type("Object")

    # -------------------------------------------------

    def metrics(self):

        return self.repository.get_nodes_by_type("Metric")

    # -------------------------------------------------

    def domains(self):

        return self.repository.get_nodes_by_type("Domain")

    # -------------------------------------------------

    def measurements(self):

        return self.repository.get_nodes_by_type("Measurement")

    # -------------------------------------------------

    def find_entity(self, entity_id):

        return self.repository.find_node(entity_id)

    # -------------------------------------------------

    def relationships(self, entity_id):

        return self.repository.find_relationships(entity_id)

    # -------------------------------------------------

    def connected_entities(self, entity_id):

        edges = self.relationships(entity_id)

        nodes = []

        for edge in edges:

            if edge.source_node == entity_id:

                nodes.append(edge.target_node)

            elif edge.target_node == entity_id:

                nodes.append(edge.source_node)

        return nodes