"""
Enterprise Graph Path Algorithms

Responsible for all graph traversal.

Used by:
    • Leadership Engine
    • Achievement Engine
    • Seniority Engine
    • Semantic Reasoning
    • Explainability
    • Recommendation Engine
"""

from collections import deque


class GraphPaths:

    def __init__(self, graph):

        self.graph = graph

    # ============================================================
    # Breadth First Search
    # ============================================================

    def bfs(self, start_node_id):

        visited = set()

        queue = deque([start_node_id])

        order = []

        while queue:

            node = queue.popleft()

            if node in visited:
                continue

            visited.add(node)

            order.append(node)

            for edge in self.graph.outgoing_edges(node):

                queue.append(edge.target_id)

        return order

    # ============================================================
    # Depth First Search
    # ============================================================

    def dfs(self, start_node_id):

        visited = set()

        order = []

        def visit(node):

            if node in visited:
                return

            visited.add(node)

            order.append(node)

            for edge in self.graph.outgoing_edges(node):

                visit(edge.target_id)

        visit(start_node_id)

        return order

    # ============================================================
    # Shortest Path
    # ============================================================

    def shortest_path(self, source_id, target_id):

        visited = set()

        queue = deque()

        queue.append((source_id, [source_id]))

        while queue:

            node_id, path = queue.popleft()

            if node_id == target_id:

                return path

            if node_id in visited:

                continue

            visited.add(node_id)

            for edge in self.graph.outgoing_edges(node_id):

                queue.append(

                    (

                        edge.target_id,

                        path + [edge.target_id]

                    )

                )

        return []

    # ============================================================
    # All Reachable Nodes
    # ============================================================

    def reachable(self, start_node_id):

        return set(

            self.bfs(start_node_id)

        )

    # ============================================================
    # Parents
    # ============================================================

    def parents(self, node_id):

        return [

            edge.source_id

            for edge in self.graph.incoming_edges(node_id)

        ]

    # ============================================================
    # Children
    # ============================================================

    def children(self, node_id):

        return [

            edge.target_id

            for edge in self.graph.outgoing_edges(node_id)

        ]

    # ============================================================
    # Connected Component
    # ============================================================

    def connected_component(self, start_node_id):

        component = set()

        queue = deque([start_node_id])

        while queue:

            node = queue.popleft()

            if node in component:
                continue

            component.add(node)

            for edge in self.graph.outgoing_edges(node):

                queue.append(edge.target_id)

            for edge in self.graph.incoming_edges(node):

                queue.append(edge.source_id)

        return component

    # ============================================================
    # Detect Cycle
    # ============================================================

    def has_cycle(self):

        visited = set()

        stack = set()

        def visit(node):

            if node in stack:

                return True

            if node in visited:

                return False

            visited.add(node)

            stack.add(node)

            for edge in self.graph.outgoing_edges(node):

                if visit(edge.target_id):

                    return True

            stack.remove(node)

            return False

        for node in self.graph.nodes.keys():

            if visit(node):

                return True

        return False