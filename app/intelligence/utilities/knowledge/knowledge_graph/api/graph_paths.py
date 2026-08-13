"""
Enterprise Graph Paths

Enterprise Version

Provides path-finding algorithms over KnowledgeGraph.

Responsibilities
----------------
• Find shortest path
• Find all paths
• Respect graph direction
• Prevent cycles
• Support depth limits
• Return node IDs as paths

The KnowledgeGraph remains responsible for storage.
GraphPaths is responsible only for path algorithms.
"""

from collections import deque


class GraphPaths:

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, graph):

        self.graph = graph

    # ==========================================================
    # SHORTEST PATH
    # ==========================================================

    def shortest_path(
        self,
        source,
        target,
    ):
        """
        Find the shortest directed path.

        Example:

            ACTION
              |
              | affects
              ↓
             KPI
              |
              | measured_by
              ↓
          MEASUREMENT

        Returns:

            [
                "ACTION_1",
                "KPI_1",
                "MEASUREMENT_1",
            ]

        Returns [] when no path exists.
        """

        if self.graph is None:
            return []

        if not source or not target:
            return []

        if (
            self.graph.get_node(source)
            is None
        ):
            return []

        if (
            self.graph.get_node(target)
            is None
        ):
            return []

        if source == target:
            return [source]

        queue = deque()

        queue.append(
            [source]
        )

        visited = {
            source
        }

        while queue:

            path = queue.popleft()

            current = path[-1]

            # --------------------------------------------------
            # IMPORTANT
            #
            # Use KnowledgeGraph's public edge collection
            # instead of requiring an outgoing_edges()
            # method that does not exist.
            # --------------------------------------------------

            for edge in self.graph.get_edges():

                if edge.source_id != current:
                    continue

                next_node = edge.target_id

                if next_node in visited:
                    continue

                new_path = (
                    path
                    + [next_node]
                )

                if next_node == target:

                    return new_path

                visited.add(
                    next_node
                )

                queue.append(
                    new_path
                )

        return []

    # ==========================================================
    # ALL PATHS
    # ==========================================================

    def all_paths(
        self,
        source,
        target,
        max_depth=10,
    ):
        """
        Find all directed paths between two nodes.

        Parameters
        ----------
        source:
            Starting node ID.

        target:
            Destination node ID.

        max_depth:
            Maximum number of edges allowed
            in a path.

        Returns
        -------
        list[list[str]]

        Example:

            [
                [
                    "ACTION_1",
                    "KPI_1",
                ],
                [
                    "ACTION_1",
                    "METRIC_1",
                    "MEASUREMENT_1",
                ],
            ]
        """

        if self.graph is None:
            return []

        if not source or not target:
            return []

        if (
            self.graph.get_node(source)
            is None
        ):
            return []

        if (
            self.graph.get_node(target)
            is None
        ):
            return []

        if max_depth < 0:
            return []

        if source == target:
            return [
                [source]
            ]

        results = []

        self._dfs_all_paths(
            current=source,
            target=target,
            path=[source],
            results=results,
            max_depth=max_depth,
        )

        return results

    # ==========================================================
    # ALL PATHS DFS
    # ==========================================================

    def _dfs_all_paths(
        self,
        current,
        target,
        path,
        results,
        max_depth,
    ):
        """
        Recursive depth-first path search.

        The current path is used as the cycle guard.

        A node may appear in different paths but may
        not appear twice inside the same path.
        """

        # ------------------------------------------------------
        # Depth protection
        # ------------------------------------------------------

        if (
            len(path) - 1
            >= max_depth
        ):
            return

        # ------------------------------------------------------
        # Explore outgoing edges
        # ------------------------------------------------------

        for edge in self.graph.get_edges():

            if edge.source_id != current:
                continue

            next_node = edge.target_id

            # --------------------------------------------------
            # Cycle protection
            # --------------------------------------------------

            if next_node in path:
                continue

            new_path = (
                path
                + [next_node]
            )

            # --------------------------------------------------
            # Target reached
            # --------------------------------------------------

            if next_node == target:

                results.append(
                    new_path
                )

                continue

            # --------------------------------------------------
            # Continue traversal
            # --------------------------------------------------

            self._dfs_all_paths(
                current=next_node,
                target=target,
                path=new_path,
                results=results,
                max_depth=max_depth,
            )

    # ==========================================================
    # UNDIRECTED SHORTEST PATH
    # ==========================================================

    def shortest_undirected_path(
        self,
        source,
        target,
    ):
        """
        Find shortest path while allowing traversal
        in both directions.

        This is intentionally separate from shortest_path().

        shortest_path()
            = directed

        shortest_undirected_path()
            = bidirectional
        """

        if self.graph is None:
            return []

        if not source or not target:
            return []

        if (
            self.graph.get_node(source)
            is None
        ):
            return []

        if (
            self.graph.get_node(target)
            is None
        ):
            return []

        if source == target:
            return [source]

        queue = deque()

        queue.append(
            [source]
        )

        visited = {
            source
        }

        while queue:

            path = queue.popleft()

            current = path[-1]

            for edge in self.graph.get_edges():

                next_node = None

                if edge.source_id == current:

                    next_node = (
                        edge.target_id
                    )

                elif edge.target_id == current:

                    next_node = (
                        edge.source_id
                    )

                if next_node is None:
                    continue

                if next_node in visited:
                    continue

                new_path = (
                    path
                    + [next_node]
                )

                if next_node == target:

                    return new_path

                visited.add(
                    next_node
                )

                queue.append(
                    new_path
                )

        return []

    # ==========================================================
    # PATH EXISTS
    # ==========================================================

    def exists(
        self,
        source,
        target,
    ):
        """
        Return True when a directed path exists.
        """

        return bool(
            self.shortest_path(
                source,
                target,
            )
        )

    # ==========================================================
    # PATH LENGTH
    # ==========================================================

    def path_length(
        self,
        source,
        target,
    ):
        """
        Return number of edges in shortest path.

        Returns -1 when no path exists.
        """

        path = self.shortest_path(
            source,
            target,
        )

        if not path:
            return -1

        return len(path) - 1