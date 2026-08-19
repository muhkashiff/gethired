"""
Achievement Profile Builder
Enterprise V14 - FIXED
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from .profile_models import AchievementProfile


class AchievementProfileBuilder:

    def build(
        self,
        graph: Any = None,
        business_statements=None,
        semantic_entities: list = None,
        extracted_entities: list = None,
    ) -> AchievementProfile:

        profile = AchievementProfile()

        statements = list(business_statements or [])
        achievements = []

        # ---------------------------------------------------------------
        # 1. Extract achievements from business statements
        # ---------------------------------------------------------------

        for statement in statements:
            if not self._is_achievement(statement):
                continue

            record = self._statement_record(statement)
            achievements.append(record)

        # ---------------------------------------------------------------
        # 2. Fallback: inspect graph nodes
        # ---------------------------------------------------------------

        if not achievements:
            achievements = self._graph_achievements(graph)

        # ---------------------------------------------------------------
        # 3. Also extract from semantic entities
        # ---------------------------------------------------------------

        if semantic_entities:
            for entity in semantic_entities:
                data = self._entity_data(entity)
                if data.get("achievement", False):
                    record = dict(data)
                    record.setdefault("quantified", data.get("quantified", False))
                    record.setdefault("impact_weight", data.get("impact_weight", 0.0))
                    achievements.append(record)

        # ---------------------------------------------------------------
        # 4. Extract metrics from achievements
        # ---------------------------------------------------------------

        metrics = []
        for achievement in achievements:
            text = achievement.get("text", "")
            # Look for metric patterns
            metric = self._extract_metric(text)
            if metric:
                metrics.append(metric)

        # ---------------------------------------------------------------
        # 5. Calculate distributions
        # ---------------------------------------------------------------

        impact_values = []
        magnitude_values = []
        impact_distribution = Counter()
        magnitude_distribution = Counter()

        for item in achievements:
            impact = float(item.get("impact_weight", 0) or 0)
            if impact > 0:
                impact_values.append(impact)
                # Bin impacts
                if impact < 0.25:
                    impact_distribution["low"] += 1
                elif impact < 0.5:
                    impact_distribution["medium"] += 1
                elif impact < 0.75:
                    impact_distribution["high"] += 1
                else:
                    impact_distribution["very_high"] += 1

            # Check for quantified achievements
            if item.get("quantified", False):
                magnitude = self._extract_magnitude(item)
                if magnitude is not None:
                    magnitude_values.append(magnitude)
                    if magnitude < 10:
                        magnitude_distribution["small"] += 1
                    elif magnitude < 50:
                        magnitude_distribution["medium"] += 1
                    elif magnitude < 100:
                        magnitude_distribution["large"] += 1
                    else:
                        magnitude_distribution["very_large"] += 1

        # ---------------------------------------------------------------
        # 6. Populate profile
        # ---------------------------------------------------------------

        profile.achievement_count = len(achievements)
        profile.quantified_count = sum(
            1 for item in achievements
            if item.get("quantified", False)
        )

        # Top achievements by impact
        profile.top_achievements = sorted(
            achievements,
            key=lambda item: float(item.get("impact_weight", 0) or 0),
            reverse=True,
        )[:10]

        # Top metrics
        profile.top_metrics = sorted(
            metrics,
            key=lambda m: m.get("value", 0),
            reverse=True,
        )[:10]

        # Impact distribution
        profile.impact_distribution = dict(impact_distribution)

        # Magnitude distribution
        profile.magnitude_distribution = dict(magnitude_distribution)

        # Impact score
        if impact_values:
            profile.impact_score = round(sum(impact_values), 4)

        # Magnitude score
        if magnitude_values:
            profile.magnitude_score = round(max(magnitude_values), 4)
        else:
            profile.magnitude_score = 1.0

        # Overall score
        profile.overall_score = round(
            (profile.achievement_count * 2) +
            (profile.quantified_count * 3) +
            profile.impact_score,
            4,
        )

        profile.details = {
            "source": (
                "business_statements"
                if statements
                else "knowledge_graph"
            ),
            "achievement_records": len(achievements),
            "has_metrics": len(metrics) > 0,
        }

        return profile

    def _extract_metric(self, text: str):
        """Extract metric from text."""
        if not text:
            return None

        import re

        # Look for patterns like "improved X by Y%" or "reduced X by Y%"
        patterns = [
            r"(improved|increased|enhanced|boosted|raised)\s+([a-z\s]+?)\s+by\s+(\d+)%",
            r"(reduced|decreased|lowered|cuts?)\s+([a-z\s]+?)\s+by\s+(\d+)%",
            r"(increased|decreased)\s+([a-z\s]+?)\s+from\s+(\d+)%\s+to\s+(\d+)%",
            r"(\d+)%\s+(improvement|reduction|increase|decrease)\s+in\s+([a-z\s]+)",
            r"([a-z\s]+?)\s+(improved|increased|decreased)\s+by\s+(\d+)%",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) >= 3:
                    # Try to extract metric name and value
                    metric_name = " ".join(g for g in groups[1:-1] if g)
                    value = float(groups[-1])
                    return {
                        "name": metric_name.strip(),
                        "value": value,
                        "unit": "%",
                        "type": "percentage",
                    }

        return None

    def _extract_magnitude(self, item: dict):
        """Extract magnitude from achievement."""
        # Look for numbers in text
        import re
        
        text = item.get("text", "")
        if not text:
            return None

        # Look for percentages
        percent_match = re.search(r"(\d+)%", text)
        if percent_match:
            return float(percent_match.group(1))

        # Look for numbers with units
        number_match = re.search(r"(\d+)\s*(?:x|times|fold)", text)
        if number_match:
            return float(number_match.group(1))

        # Look for plain numbers (like "15+ years")
        number_match = re.search(r"(\d+)\+?\s*(?:years|months|weeks|days)", text)
        if number_match:
            return float(number_match.group(1))

        return None

    @staticmethod
    def _is_achievement(statement):
        if isinstance(statement, dict):
            return bool(statement.get("achievement", False))

        return bool(getattr(statement, "achievement", False))

    @staticmethod
    def _statement_record(statement):
        if isinstance(statement, dict):
            return dict(statement)

        result = dict(getattr(statement, "__dict__", {}))

        result.setdefault("text", getattr(statement, "text", ""))
        result.setdefault("achievement", True)
        result.setdefault("quantified", getattr(statement, "quantified", False))
        result.setdefault("impact_weight", getattr(statement, "impact_weight", 0.0))

        return result

    def _graph_achievements(self, graph):
        if graph is None:
            return []

        nodes = getattr(graph, "nodes", [])
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
                        getattr(node, "__dict__", {}),
                    )
                )
            )

            if data.get("achievement") or data.get("entity_type") == "achievement":
                result.append(data)

        return result

    @staticmethod
    def _entity_data(entity):
        if isinstance(entity, dict):
            return dict(entity)

        data = getattr(entity, "data", None)
        if isinstance(data, dict):
            return dict(data)

        return dict(getattr(entity, "__dict__", {}))