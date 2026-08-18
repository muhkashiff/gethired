"""
Entity Profile Builder
Enterprise V14
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from .profile_models import EntityProfile


class EntityProfileBuilder:

    def build(
        self,
        graph: Any = None,
    ) -> EntityProfile:

        profile = EntityProfile()

        nodes = self._get_nodes(graph)

        for node in nodes:

            data = self._node_data(node)

            entity_type = self._get_entity_type(
                node,
                data,
            )

            entity_id = self._get(
                node,
                data,
                "entity_id",
                "id",
            )

            canonical = self._get(
                node,
                data,
                "canonical",
                "name",
                "label",
            )

            record = dict(data)

            record.setdefault(
                "entity_id",
                entity_id,
            )

            record.setdefault(
                "canonical",
                canonical,
            )

            record.setdefault(
                "entity_type",
                entity_type,
            )

            node_id = self._get(
                node,
                data,
                "node_id",
                "id",
            )

            if node_id:
                record.setdefault(
                    "node_id",
                    node_id,
                )

            profile.entities.append(record)

        profile.total_entities = len(
            profile.entities
        )

        profile.entity_counts = dict(
            Counter(
                item.get(
                    "entity_type",
                    ""
                )
                for item in profile.entities
                if item.get(
                    "entity_type"
                )
            )
        )

        return profile

    @staticmethod
    def _get_nodes(graph):

        if graph is None:
            return []

        nodes = getattr(
            graph,
            "nodes",
            None,
        )

        if nodes is None:
            return []

        if isinstance(nodes, dict):
            return list(nodes.values())

        return list(nodes)

    @staticmethod
    def _node_data(node):

        if isinstance(node, dict):
            return dict(node)

        data = getattr(
            node,
            "data",
            None,
        )

        if isinstance(data, dict):
            return dict(data)

        result = {}

        if hasattr(node, "__dict__"):
            result.update(
                node.__dict__
            )

        return result

    @classmethod
    def _get_entity_type(
        cls,
        node,
        data,
    ):

        value = cls._get(
            node,
            data,
            "entity_type",
            "type",
            "category",
        )

        return str(
            value or ""
        ).strip().lower()

    @staticmethod
    def _get(
        node,
        data,
        *names,
    ):

        for name in names:

            if name in data and data[name] is not None:
                return data[name]

            if node is not None:

                value = getattr(
                    node,
                    name,
                    None,
                )

                if value is not None:
                    return value

        return ""