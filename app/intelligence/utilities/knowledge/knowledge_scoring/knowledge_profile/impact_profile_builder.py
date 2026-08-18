"""
Impact Profile Builder
Enterprise V14
"""

from __future__ import annotations

from typing import Any

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import ImpactProfile


class ImpactProfileBuilder:

    def build(
        self,
        graph: Any = None,
    ) -> ImpactProfile:

        profile = ImpactProfile()

        nodes = self._nodes(graph)

        weighted = []

        for node in nodes:

            data = self._data(node)

            value = self._impact_weight(
                node,
                data,
            )

            if value <= 0:
                continue

            record = dict(data)

            record.setdefault(
                "impact_weight",
                value,
            )

            record.setdefault(
                "entity_id",
                self._get(
                    node,
                    data,
                    "entity_id",
                    "id",
                ),
            )

            record.setdefault(
                "canonical",
                self._get(
                    node,
                    data,
                    "canonical",
                    "name",
                    "label",
                ),
            )

            weighted.append(
                record
            )

        if not weighted:
            return profile

        values = [
            float(
                item["impact_weight"]
            )
            for item in weighted
        ]

        profile.entity_count = len(
            weighted
        )

        profile.total_impact = round(
            sum(values),
            4,
        )

        profile.average_impact = round(
            sum(values) / len(values),
            4,
        )

        profile.maximum_impact = round(
            max(values),
            4,
        )

        profile.weighted_entities = sorted(
            weighted,
            key=lambda item: float(
                item.get(
                    "impact_weight",
                    0,
                )
            ),
            reverse=True,
        )

        return profile

    @staticmethod
    def _impact_weight(node, data):

        for name in (
            "impact_weight",
            "impact",
            "business_impact",
        ):

            value = (
                data.get(name)
                if name in data
                else getattr(
                    node,
                    name,
                    None,
                )
            )

            try:

                if value is not None:
                    return float(value)

            except (
                TypeError,
                ValueError,
            ):
                continue

        return 0.0

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

        return ""