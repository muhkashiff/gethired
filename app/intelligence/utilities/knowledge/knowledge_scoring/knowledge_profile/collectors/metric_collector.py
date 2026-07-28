"""
Metric Collector

Collects KPI / Metric nodes from the Knowledge Graph.

Examples

Production Yield
Revenue
Cost Savings
Efficiency
Customer Satisfaction

Future extensions

• KPI ranking
• KPI weighting
• Executive KPI detection
• Financial KPI detection
"""

from collections import Counter


class MetricCollector:

    # -----------------------------------------------------

    def collect(self, graph):

        metrics = []

        for node in graph.nodes.values():

            if node.node_type != "Metric":
                continue

            metrics.append(node)

        return metrics

    # -----------------------------------------------------

    def frequencies(self, graph):

        counts = Counter()

        for node in self.collect(graph):

            counts[node.canonical] += 1

        return dict(counts)

    # -----------------------------------------------------

    def unique(self, graph):

        unique_metrics = {}

        for node in self.collect(graph):

            unique_metrics[node.entity_id] = node

        return list(unique_metrics.values())

    # -----------------------------------------------------

    def categories(self, graph):

        counts = Counter()

        for node in self.collect(graph):

            counts[node.category] += 1

        return dict(counts)

    # -----------------------------------------------------

    def higher_is_better(self, graph):

        """
        Returns KPIs where improvement
        means increasing the value.
        """

        positive = []

        for node in self.collect(graph):

            if node.metadata.get("higher_is_better", False):

                positive.append(node)

        return positive

    # -----------------------------------------------------

    def units(self, graph):

        """
        Returns every KPI grouped by unit.

        Example

        %

        $

        hours

        count
        """

        units = {}

        for node in self.collect(graph):

            unit = node.metadata.get("unit", "")

            units.setdefault(unit, []).append(node)

        return units