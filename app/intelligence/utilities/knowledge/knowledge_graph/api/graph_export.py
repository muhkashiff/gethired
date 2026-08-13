"""
Enterprise Graph Export

Enterprise Version

Provides serialization and export functionality
for KnowledgeGraph.

Responsibilities
----------------
• Export graph to dictionary
• Export graph to JSON
• Export nodes
• Export edges
• Export statistics
• Keep export logic outside KnowledgeGraph
"""


import json


class GraphExport:

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, graph):

        self.graph = graph

    # ==========================================================
    # DICTIONARY EXPORT
    # ==========================================================

    def to_dict(self):

        if self.graph is None:
            return {
                "nodes": [],
                "edges": [],
                "statistics": {},
            }

        return self.graph.to_dict()

    # ==========================================================
    # JSON EXPORT
    # ==========================================================

    def to_json(
        self,
        indent=2,
    ):
        """
        Serialize graph to JSON string.
        """

        return json.dumps(
            self.to_dict(),
            indent=indent,
            default=str,
        )

    # ==========================================================
    # NODE EXPORT
    # ==========================================================

    def nodes(self):

        if self.graph is None:
            return []

        result = []

        for node in self.graph.get_nodes():

            if hasattr(node, "to_dict"):

                result.append(
                    node.to_dict()
                )

            else:

                result.append(
                    vars(node).copy()
                )

        return result

    # ==========================================================
    # EDGE EXPORT
    # ==========================================================

    def edges(self):

        if self.graph is None:
            return []

        result = []

        for edge in self.graph.get_edges():

            if hasattr(edge, "to_dict"):

                result.append(
                    edge.to_dict()
                )

            else:

                result.append(
                    vars(edge).copy()
                )

        return result

    # ==========================================================
    # STATISTICS EXPORT
    # ==========================================================

    def statistics(self):

        if self.graph is None:
            return {}

        statistics = (
            self.graph.get_statistics()
        )

        return {
            "node_count": (
                statistics.node_count
            ),
            "edge_count": (
                statistics.edge_count
            ),
            "entity_counts": dict(
                statistics.entity_counts
            ),
            "relation_counts": dict(
                statistics.relation_counts
            ),
        }

    # ==========================================================
    # SAVE JSON
    # ==========================================================

    def save_json(
        self,
        path,
        indent=2,
    ):
        """
        Save graph as JSON file.
        """

        data = self.to_json(
            indent=indent
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(data)

        return path