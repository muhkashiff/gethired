"""
Modifier Profile Builder
Enterprise V14
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import ModifierProfile


class ModifierProfileBuilder:

    EXECUTIVE_MODIFIERS = {
        "executive",
        "strategic",
        "enterprise",
        "organization-wide",
        "company-wide",
        "director",
        "senior",
        "leadership",
    }

    def build(
        self,
        graph: Any = None,
    ) -> ModifierProfile:

        profile = ModifierProfile()

        nodes = self._nodes(graph)

        categories = Counter()

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

            if entity_type != "modifier":
                continue

            name = str(
                self._get(
                    node,
                    data,
                    "canonical",
                    "name",
                    "label",
                    "modifier",
                )
                or ""
            ).strip()

            if not name:
                continue

            categories[name] += 1

            profile.total_modifiers += 1

            if name.lower() in self.EXECUTIVE_MODIFIERS:
                profile.executive_modifiers += 1

        profile.categories = dict(
            categories
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

        return ""