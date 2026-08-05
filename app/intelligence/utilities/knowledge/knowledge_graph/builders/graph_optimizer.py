"""
Enterprise Graph Optimizer

Optimizes graph before reasoning.

Runs AFTER

    Graph Validator

Runs BEFORE

    Reasoning Pipeline

Enterprise V7
"""

from collections import OrderedDict


class GraphOptimizer:

    ####################################################################
    # BUILD
    ####################################################################

    def build(

        self,

        graph,

    ):

        self._remove_duplicate_edges(graph)

        self._normalize_metadata(graph)

        self._sort_edges(graph)

        self._sort_nodes(graph)

        self._update_statistics(graph)

        return graph

    ####################################################################
    # REMOVE DUPLICATE EDGES
    ####################################################################

    def _remove_duplicate_edges(

        self,

        graph,

    ):

        unique = OrderedDict()

        for edge in graph.edges:

            unique[edge.edge_id] = edge

        graph.edges = list(

            unique.values()

        )

    ####################################################################
    # NORMALIZE METADATA
    ####################################################################

    def _normalize_metadata(

        self,

        graph,

    ):

        for node in graph.get_nodes():

            if node.metadata is None:

                node.metadata = {}

                continue

            normalized = {}

            for key, value in node.metadata.items():

                if key is None:

                    continue

                normalized[str(key).lower()] = value

            node.metadata = normalized

    ####################################################################
    # SORT EDGES
    ####################################################################

    def _sort_edges(

        self,

        graph,

    ):

        graph.edges.sort(

            key=lambda edge: (

                edge.source_id,

                edge.relation,

                edge.target_id,

            )

        )

    ####################################################################
    # SORT NODES
    ####################################################################

    def _sort_nodes(

        self,

        graph,

    ):

        graph.nodes = dict(

            sorted(

                graph.nodes.items(),

                key=lambda item: item[0],

            )

        )

    ####################################################################
    # UPDATE STATISTICS
    ####################################################################

    def _update_statistics(

        self,

        graph,

    ):

        graph.statistics.node_count = len(

            graph.nodes

        )

        graph.statistics.edge_count = len(

            graph.edges

        )

        graph.statistics.optimized = True