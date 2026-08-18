"""
Metric Profile Builder
Enterprise V14
"""

from __future__ import annotations

from typing import Any

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import MetricProfile

class MetricProfileBuilder:

    def build(
        self,
        graph: Any = None,
    ) -> MetricProfile:

        profile = MetricProfile()

        nodes = self._nodes(graph)

        for node in nodes:

            data = self._data(node)

            entity_type = str(
                self._get(
                    node,
                    data,
                    "entity_type",
                    "type",
                )
                or ""
            ).lower()

            if entity_type not in {
                "metric",
                "kpi",
            }:
                continue

            record = dict(data)

            canonical = self._get(
                node,
                data,
                "canonical",
                "name",
                "label",
            )

            record.setdefault(
                "canonical",
                canonical,
            )

            profile.metrics.append(
                record
            )

            direction = str(
                self._get(
                    node,
                    data,
                    "direction",
                    "trend",
                    "change_direction",
                )
                or ""
            ).lower()

            higher_is_better = self._get(
                node,
                data,
                "higher_is_better",
            )

            if higher_is_better is True:
                profile.positive_metrics += 1

            elif higher_is_better is False:
                profile.negative_metrics += 1

            if direction in {
                "increase",
                "increased",
                "up",
                "positive",
                "improved",
            }:
                profile.increase_metrics += 1

            elif direction in {
                "decrease",
                "decreased",
                "down",
                "negative",
                "reduced",
            }:
                profile.decrease_metrics += 1

        profile.total_metrics = len(
            profile.metrics
        )

        return profile

    @staticmethod
    def _nodes(graph):

        if graph is None:
            return []

        nodes = getattr(
            graph,
            "nodes",
            []
        )

        if isinstance(nodes, dict):
            return list(nodes.values())

        return list(nodes)

    @staticmethod
    def _data(node):

        if isinstance(node, dict):
            return dict(node)

        data = getattr(
            node,
            "data",
            None,
        )

        if isinstance(data, dict):
            return dict(data)

        return dict(
            getattr(
                node,
                "__dict__",
                {},
            )
        )

    @staticmethod
    def _get(node, data, *names):

        for name in names:

            if name in data:
                return data[name]

            value = getattr(
                node,
                name,
                None,
            )

            if value is not None:
                return value

        return None