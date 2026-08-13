"""
Enterprise Graph Statistics API

Enterprise Version

Provides read-only statistics access for KnowledgeGraph.

Responsibilities
----------------
• Expose graph statistics
• Provide node and edge counts
• Provide entity type counts
• Provide relation counts
• Keep statistics access modular
• Prevent callers from directly accessing graph internals

Architecture

KnowledgeGraph
      ↓
GraphStatisticsAPI
      ↓
GraphAPI.statistics()
"""


class GraphStatisticsAPI:

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, graph):

        self.graph = graph

    # ==========================================================
    # MAIN STATISTICS API
    # ==========================================================

    def statistics(self):
        """
        Return complete graph statistics.

        Delegates to KnowledgeGraph.statistics.

        Returns
        -------
        GraphStatistics
        """

        if self.graph is None:
            return None

        return self.graph.get_statistics()

    # ==========================================================
    # NODE COUNT
    # ==========================================================

    def node_count(self):
        """
        Return total number of graph nodes.
        """

        if self.graph is None:
            return 0

        statistics = self.graph.get_statistics()

        return statistics.node_count

    # ==========================================================
    # EDGE COUNT
    # ==========================================================

    def edge_count(self):
        """
        Return total number of graph edges.
        """

        if self.graph is None:
            return 0

        statistics = self.graph.get_statistics()

        return statistics.edge_count

    # ==========================================================
    # ENTITY COUNTS
    # ==========================================================

    def entity_counts(self):
        """
        Return entity counts by entity type.

        Example
        -------

        {
            "action": 2,
            "metric": 1,
            "kpi": 1,
            "bkpi": 1
        }
        """

        if self.graph is None:
            return {}

        statistics = self.graph.get_statistics()

        return dict(
            statistics.entity_counts
        )

    # ==========================================================
    # RELATION COUNTS
    # ==========================================================

    def relation_counts(self):
        """
        Return relation counts.

        Example
        -------

        {
            "affects": 2,
            "measured_by": 1
        }
        """

        if self.graph is None:
            return {}

        statistics = self.graph.get_statistics()

        return dict(
            statistics.relation_counts
        )

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(self):
        """
        Return a serializable statistics summary.
        """

        if self.graph is None:
            return {
                "nodes": 0,
                "edges": 0,
                "entities": {},
                "relations": {},
            }

        return self.graph.summary()