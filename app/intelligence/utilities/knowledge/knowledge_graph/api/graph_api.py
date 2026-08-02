"""
Enterprise Graph API

This is the ONLY public interface that every engine
should use.

Nothing outside the graph package should directly
access

    graph.nodes
    graph.edges

All interaction must happen through GraphAPI.

Enterprise Version
"""

from .graph_query_api import GraphQueryAPI
from .graph_filters import GraphFilters
from .graph_traversal import GraphTraversal
from .graph_neighbors import GraphNeighbors
from .graph_paths import GraphPaths
from .graph_statistics import GraphStatisticsAPI
from .graph_validation import GraphValidation
from .graph_search import GraphSearch


class GraphAPI:

    def __init__(self, graph):

        self.graph = graph

        self.query = GraphQueryAPI(graph)

        self.filters = GraphFilters(graph)

        self.traversal = GraphTraversal(graph)

        self.neighbors_api = GraphNeighbors(graph)

        self.paths_api = GraphPaths(graph)

        self.statistics_api = GraphStatisticsAPI(graph)

        self.validation_api = GraphValidation(graph)

        self.search_api = GraphSearch(graph)

    # =====================================================
    # Node Collections
    # =====================================================

    def nodes(self):
        return self.query.nodes()

    def edges(self):
        return self.query.edges()

    def actions(self):
        return self.query.actions()

    def metrics(self):
        return self.query.metrics()

    def measurements(self):
        return self.query.measurements()

    def objects(self):
        return self.query.objects()

    def domains(self):
        return self.query.domains()

    def standards(self):
        return self.query.standards()

    def skills(self):
        return self.query.skills()

    def methodologies(self):
        return self.query.methodologies()

    # =====================================================
    # Generic Queries
    # =====================================================

    def node(self, node_id):
        return self.query.node(node_id)

    def edge(self, edge_id):
        return self.query.edge(edge_id)

    def find(self, **kwargs):
        return self.query.find(**kwargs)

    # =====================================================
    # Filters
    # =====================================================

    def by_category(self, category):
        return self.filters.by_category(category)

    def by_business_area(self, business_area):
        return self.filters.by_business_area(business_area)

    def by_domain(self, domain):
        return self.filters.by_domain(domain)

    def by_type(self, entity_type):
        return self.filters.by_type(entity_type)

    # =====================================================
    # Graph Traversal
    # =====================================================

    def neighbors(self, node_id):
        return self.neighbors_api.neighbors(node_id)

    def parents(self, node_id):
        return self.neighbors_api.parents(node_id)

    def children(self, node_id):
        return self.neighbors_api.children(node_id)

    def connected(self, node_id):
        return self.neighbors_api.connected(node_id)

    # =====================================================
    # Paths
    # =====================================================

    def shortest_path(self, source, target):
        return self.paths_api.shortest_path(source, target)

    def all_paths(self, source, target):
        return self.paths_api.all_paths(source, target)

    # =====================================================
    # Search
    # =====================================================

    def search(self, text):
        return self.search_api.search(text)

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):
        return self.statistics_api.statistics()

    # =====================================================
    # Validation
    # =====================================================

    def validate(self):
        return self.validation_api.validate()