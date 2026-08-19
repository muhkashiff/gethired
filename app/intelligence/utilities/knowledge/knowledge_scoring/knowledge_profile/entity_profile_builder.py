"""
Entity Profile Builder
Enterprise V14 - FIXED
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from .profile_models import EntityProfile


class EntityProfileBuilder:

    def build(
        self,
        graph: Any = None,
        semantic_entities: list = None,
        extracted_entities: list = None,
    ) -> EntityProfile:

        profile = EntityProfile()

        # Collect entities from all sources
        all_entities = []
        
        # 1. Semantic entities (primary source)
        if semantic_entities:
            all_entities.extend(semantic_entities)
        
        # 2. Extracted entities
        if extracted_entities:
            all_entities.extend(extracted_entities)
        
        # 3. Graph nodes (as fallback)
        if graph and not all_entities:
            graph_nodes = self._get_nodes(graph)
            all_entities.extend(graph_nodes)

        # If still no entities, try graph as primary
        if not all_entities and graph:
            graph_nodes = self._get_nodes(graph)
            all_entities.extend(graph_nodes)

        for entity in all_entities:
            data = self._node_data(entity)

            entity_type = self._get_entity_type(
                entity,
                data,
            )

            entity_id = self._get(
                entity,
                data,
                "entity_id",
                "id",
                "node_id",
            )

            canonical = self._get(
                entity,
                data,
                "canonical",
                "name",
                "label",
                "text",
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
                entity,
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
                    "unknown"
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

        if callable(nodes):
            try:
                nodes = nodes()
            except Exception:
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
            "kind",
        )

        return str(
            value or "unknown"
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