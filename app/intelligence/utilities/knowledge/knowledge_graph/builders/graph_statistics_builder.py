"""
Enterprise Graph Statistics Builder

Computes graph analytics after graph construction.

Runs AFTER

    All Builders

Runs BEFORE

    Graph Optimizer

Enterprise V7
"""

from collections import Counter


class GraphStatisticsBuilder:

    ####################################################################
    # BUILD
    ####################################################################

    def build(

        self,

        graph,

    ):

        stats = graph.statistics

        # -----------------------------------------------------
        # Entity Distribution
        # -----------------------------------------------------

        stats.entity_counts = Counter(

            node.entity_type

            for node in graph.get_nodes()

        )

        # -----------------------------------------------------
        # Category Distribution
        # -----------------------------------------------------

        stats.category_counts = Counter(

            node.category

            for node in graph.get_nodes()

            if node.category

        )

        # -----------------------------------------------------
        # Business Areas
        # -----------------------------------------------------

        stats.business_area_counts = Counter(

            node.business_area

            for node in graph.get_nodes()

            if node.business_area

        )

        # -----------------------------------------------------
        # Domain Distribution
        # -----------------------------------------------------

        stats.domain_counts = Counter(

            node.domain

            for node in graph.get_nodes()

            if node.domain

        )

        # -----------------------------------------------------
        # Relationship Distribution
        # -----------------------------------------------------

        stats.relation_counts = Counter(

            edge.relation

            for edge in graph.get_edges()

        )

        # -----------------------------------------------------
        # Degree Statistics
        # -----------------------------------------------------

        degrees = [

            len(node.incoming_edges)

            + len(node.outgoing_edges)

            for node in graph.get_nodes()

        ]

        if degrees:

            stats.max_degree = max(degrees)

            stats.min_degree = min(degrees)

            stats.average_degree = round(

                sum(degrees)

                / len(degrees),

                2,

            )

        # -----------------------------------------------------
        # Density
        # -----------------------------------------------------

        node_count = len(graph.get_nodes())

        edge_count = len(graph.get_edges())

        if node_count > 1:

            stats.density = round(

                edge_count

                /

                (

                    node_count

                    * (node_count - 1)

                ),

                4,

            )

        # -----------------------------------------------------
        # Connected Components
        # -----------------------------------------------------

        stats.connected_components = (

            self._connected_components(

                graph,

            )

        )

        return stats

    ####################################################################
    # Connected Components
    ####################################################################

    def _connected_components(

        self,

        graph,

    ):

        visited = set()

        components = 0

        for node in graph.get_nodes():

            if node.node_id in visited:

                continue

            components += 1

            stack = [node]

            while stack:

                current = stack.pop()

                if current.node_id in visited:

                    continue

                visited.add(

                    current.node_id

                )

                neighbors = graph.neighbors(

                    current.node_id

                )

                stack.extend(neighbors)

        return components