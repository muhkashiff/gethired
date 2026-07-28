"""
Measurement Collector

Collects Measurement nodes from the Knowledge Graph.

Examples

99%

35%

$2M

150

12 Hours

Future versions

• ROI calculation

• Business impact scoring

• Resume strength scoring

• Executive KPI analysis

• Benchmark comparison
"""

from collections import Counter


class MeasurementCollector:

    # -----------------------------------------------------

    def collect(self, graph):

        measurements = []

        for node in graph.nodes.values():

            if node.node_type != "Measurement":
                continue

            measurements.append(node)

        return measurements

    # -----------------------------------------------------

    def frequencies(self, graph):

        counts = Counter()

        for node in self.collect(graph):

            counts[node.canonical] += 1

        return dict(counts)

    # -----------------------------------------------------

    def unique(self, graph):

        unique_measurements = {}

        for node in self.collect(graph):

            unique_measurements[node.entity_id] = node

        return list(unique_measurements.values())

    # -----------------------------------------------------

    def positive(self, graph):

        """
        Positive business outcomes.
        """

        results = []

        for node in self.collect(graph):

            if node.metadata.get("effect") == "positive":

                results.append(node)

        return results

    # -----------------------------------------------------

    def negative(self, graph):

        """
        Negative business outcomes.
        """

        results = []

        for node in self.collect(graph):

            if node.metadata.get("effect") == "negative":

                results.append(node)

        return results

    # -----------------------------------------------------

    def increases(self, graph):

        """
        Measurements produced by increase/improvement.
        """

        results = []

        for node in self.collect(graph):

            if node.metadata.get("direction") == "increase":

                results.append(node)

        return results

    # -----------------------------------------------------

    def decreases(self, graph):

        """
        Measurements produced by reduction.
        """

        results = []

        for node in self.collect(graph):

            if node.metadata.get("direction") == "decrease":

                results.append(node)

        return results

    # -----------------------------------------------------

    def by_unit(self, graph):

        """
        Groups measurements by unit.

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

    # -----------------------------------------------------

    def summary(self, graph):

        """
        High-level statistics used later by
        scoring engines.
        """

        measurements = self.collect(graph)

        return {

            "count": len(measurements),

            "positive": len(self.positive(graph)),

            "negative": len(self.negative(graph)),

            "increase": len(self.increases(graph)),

            "decrease": len(self.decreases(graph))

        }