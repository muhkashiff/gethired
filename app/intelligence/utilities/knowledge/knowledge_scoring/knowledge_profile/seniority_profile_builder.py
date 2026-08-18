"""
Seniority Profile Builder
Enterprise V14
"""

from __future__ import annotations

from typing import Any

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import SeniorityProfile


class SeniorityProfileBuilder:

    ACTION_LEVELS = {
        "lead": 3,
        "manage": 3,
        "direct": 3,
        "own": 3,
        "oversee": 3,
        "supervise": 2,
        "coordinate": 2,
        "implement": 2,
        "develop": 2,
        "train": 2,
        "mentor": 2,
        "improve": 1,
    }

    def build(
        self,
        graph: Any = None,
    ) -> SeniorityProfile:

        profile = SeniorityProfile()

        nodes = self._nodes(graph)

        score = 0.0

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

            if entity_type == "action":

                action = str(
                    self._get(
                        node,
                        data,
                        "canonical",
                        "name",
                        "label",
                    )
                    or ""
                ).strip()

                level = self.ACTION_LEVELS.get(
                    action.lower()
                )

                if level:

                    profile.actions[action] = (
                        profile.actions.get(
                            action,
                            0,
                        )
                        + 1
                    )

                    score += level

                    if action.lower() == "lead":
                        profile.indicators.append(
                            "lead"
                        )

            domain = self._get(
                node,
                data,
                "domain",
            )

            if domain:

                domain_name = str(
                    domain
                ).strip().lower()

                profile.domains[
                    domain_name
                ] = (
                    profile.domains.get(
                        domain_name,
                        0.0,
                    )
                    + 1.0
                )

        profile.indicators = list(
            dict.fromkeys(
                profile.indicators
            )
        )

        profile.score = min(
            10.0,
            score / 3.0,
        )

        if profile.score >= 8:
            profile.level = "Executive"

        elif profile.score >= 6:
            profile.level = "Senior"

        elif profile.score >= 3:
            profile.level = "Professional"

        elif profile.score > 0:
            profile.level = "Developing"

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