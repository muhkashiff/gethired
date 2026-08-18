"""
Domain Profile Builder
Enterprise V14
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import DomainProfile


class DomainProfileBuilder:

    def build(
        self,
        graph: Any = None,
    ) -> DomainProfile:

        profile = DomainProfile()

        nodes = self._nodes(graph)

        domains = Counter()
        areas = Counter()

        for node in nodes:

            data = self._data(node)

            domain = self._get(
                node,
                data,
                "domain",
                "primary_domain",
            )

            business_area = self._get(
                node,
                data,
                "business_area",
            )

            if domain:

                domains[
                    str(domain).strip().lower()
                ] += 1

            if business_area:

                areas[
                    str(business_area).strip().lower()
                ] += 1

        profile.domains = dict(
            domains
        )

        profile.business_areas = dict(
            areas
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

            if value:
                return value

        return ""