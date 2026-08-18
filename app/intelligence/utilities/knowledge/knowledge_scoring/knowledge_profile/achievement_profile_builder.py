"""
Achievement Profile Builder
Enterprise V14
"""

from __future__ import annotations

from typing import Any

from .profile_models import AchievementProfile


class AchievementProfileBuilder:

    def build(
        self,
        graph: Any = None,
        business_statements=None,
    ) -> AchievementProfile:

        profile = AchievementProfile()

        statements = (
            list(business_statements or [])
        )

        achievements = []

        for statement in statements:

            if not self._is_achievement(
                statement
            ):
                continue

            record = self._statement_record(
                statement
            )

            achievements.append(
                record
            )

        # ---------------------------------------------------------------
        # Fallback: inspect graph nodes if statements are unavailable.
        # ---------------------------------------------------------------

        if not achievements:

            achievements = (
                self._graph_achievements(
                    graph
                )
            )

        profile.achievement_count = len(
            achievements
        )

        profile.quantified_count = sum(
            1
            for item in achievements
            if item.get(
                "quantified",
                False,
            )
        )

        profile.top_achievements = sorted(
            achievements,
            key=lambda item: float(
                item.get(
                    "impact_weight",
                    0,
                )
                or 0
            ),
            reverse=True,
        )[:10]

        impact_values = [
            float(
                item.get(
                    "impact_weight",
                    0,
                )
                or 0
            )
            for item in achievements
        ]

        if impact_values:

            profile.impact_score = round(
                sum(impact_values),
                4,
            )

            profile.magnitude_score = round(
                max(impact_values),
                4,
            )

        profile.overall_score = round(
            (
                profile.achievement_count
                + profile.quantified_count
                + profile.impact_score
            ),
            4,
        )

        profile.details = {
            "source": (
                "business_statements"
                if statements
                else "knowledge_graph"
            ),
            "achievement_records": len(
                achievements
            ),
        }

        return profile

    @staticmethod
    def _is_achievement(
        statement,
    ):

        if isinstance(
            statement,
            dict,
        ):

            return bool(
                statement.get(
                    "achievement",
                    False,
                )
            )

        return bool(
            getattr(
                statement,
                "achievement",
                False,
            )
        )

    @staticmethod
    def _statement_record(
        statement,
    ):

        if isinstance(
            statement,
            dict,
        ):
            return dict(statement)

        result = dict(
            getattr(
                statement,
                "__dict__",
                {},
            )
        )

        result.setdefault(
            "text",
            getattr(
                statement,
                "text",
                "",
            ),
        )

        result.setdefault(
            "achievement",
            True,
        )

        result.setdefault(
            "quantified",
            getattr(
                statement,
                "quantified",
                False,
            ),
        )

        result.setdefault(
            "impact_weight",
            getattr(
                statement,
                "impact_weight",
                0.0,
            ),
        )

        return result

    def _graph_achievements(
        self,
        graph,
    ):

        if graph is None:
            return []

        nodes = getattr(
            graph,
            "nodes",
            [],
        )

        if isinstance(nodes, dict):
            nodes = nodes.values()

        result = []

        for node in nodes:

            data = (
                dict(node)
                if isinstance(node, dict)
                else dict(
                    getattr(
                        node,
                        "data",
                        getattr(
                            node,
                            "__dict__",
                            {},
                        ),
                    )
                )
            )

            if data.get(
                "achievement"
            ):

                result.append(
                    data
                )

        return result