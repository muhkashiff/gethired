"""
Action Collector

Collects action statistics from the Knowledge Graph.

This module DOES NOT calculate scores.

It only extracts structured information.

Future expansion:
- frequency
- executive actions
- strategic actions
- leadership actions
"""

from collections import Counter


class ActionCollector:

    def collect(self, graph):

        counter = Counter()

        actions = []

        for node in graph.nodes.values():

            if node.node_type != "Action":
                continue

            counter[node.category] += 1

            actions.append(
                {
                    "entity_id": node.entity_id,
                    "label": node.label,
                    "category": node.category,
                    "confidence": node.confidence,
                    "impact_weight": node.impact_weight,
                }
            )

        return {

            "count": len(actions),

            "categories": dict(counter),

            "actions": actions,

        }