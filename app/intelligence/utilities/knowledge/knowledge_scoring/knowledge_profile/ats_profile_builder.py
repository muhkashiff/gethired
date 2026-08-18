"""
ATS Profile Builder
Enterprise V14
"""

from __future__ import annotations

from typing import Any

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import ATSProfile


class ATSProfileBuilder:

    def build(
        self,
        graph: Any = None,
    ) -> ATSProfile:

        profile = ATSProfile()

        nodes = self._nodes(graph)

        matched = []

        for node in nodes:

            data = self._data(node)

            ats_score = self._ats_score(
                node,
                data,
            )

            if ats_score is None:
                continue

            if ats_score <= 0:
                continue

            record = dict(data)

            record.setdefault(
                "ats_score",
                ats_score,
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

            matched.append(
                record
            )

        profile.entity_count = len(
            matched
        )

        profile.matched_entities = sorted(
            matched,
            key=lambda item: float(
                item.get(
                    "ats_score",
                    0,
                )
            ),
            reverse=True,
        )

        if matched:

            profile.score = round(
                sum(
                    float(
                        item.get(
                            "ats_score",
                            0,
                        )
                    )
                    for item in matched
                )
                / len(matched),
                4,
            )

        return profile

    @classmethod
    def _ats_score(
        cls,
        node,
        data,
    ):

        for key in (
            "ats_score",
            "ats_weight",
            "ats_match_score",
            "keyword_score",
        ):

            value = cls._get(
                node,
                data,
                key,
            )

            if value is not None:

                try:
                    return float(value)

                except (
                    TypeError,
                    ValueError,
                ):
                    pass

        metadata = data.get(
            "metadata"
        )

        if isinstance(
            metadata,
            dict,
        ):

            for key in (
                "ats_score",
                "ats_weight",
                "ats_match_score",
                "keyword_score",
            ):

                value = metadata.get(
                    key
                )

                if value is not None:

                    try:
                        return float(
                            value
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):
                        pass

            ats = metadata.get(
                "ats"
            )

            if isinstance(
                ats,
                dict,
            ):

                value = ats.get(
                    "score"
                )

                if value is not None:

                    try:
                        return float(
                            value
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):
                        pass

        return None

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