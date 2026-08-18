"""
Leadership Profile Builder
Enterprise V14
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from .profile_models import LeadershipProfile


class LeadershipProfileBuilder:

    LEADERSHIP_ACTIONS = {
        "lead",
        "manage",
        "mentor",
        "coach",
        "train",
        "implement",
        "supervise",
        "direct",
        "coordinate",
        "develop",
        "build",
        "own",
        "oversee",
    }

    EXECUTIVE_ACTIONS = {
        "lead",
        "manage",
        "direct",
        "own",
        "oversee",
    }

    def build(
        self,
        graph: Any = None,
    ) -> LeadershipProfile:

        profile = LeadershipProfile()

        nodes = self._nodes(graph)

        actions = Counter()

        leadership_count = 0
        executive_count = 0

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

            if entity_type != "action":
                continue

            name = str(
                self._get(
                    node,
                    data,
                    "canonical",
                    "name",
                    "label",
                )
                or ""
            ).strip()

            normalized = name.lower()

            if normalized in self.LEADERSHIP_ACTIONS:

                leadership_count += 1

                actions[name] += 1

            if normalized in self.EXECUTIVE_ACTIONS:

                executive_count += 1

        profile.entity_count = leadership_count

        profile.executive_actions = (
            executive_count
        )

        profile.actions = dict(
            actions
        )

        profile.score = min(
            10.0,
            leadership_count * 1.0
            + executive_count * 0.5,
        )

        if executive_count >= 3:
            profile.level = "Executive"

        elif leadership_count >= 4:
            profile.level = "Strong Leadership"

        elif leadership_count >= 2:
            profile.level = "Leadership"

        elif leadership_count == 1:
            profile.level = "Emerging Leadership"

        else:
            profile.level = ""

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