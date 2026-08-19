"""
ATS Profile Builder
Enterprise V14 - FIXED
"""

from __future__ import annotations

from typing import Any

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import ATSProfile


class ATSProfileBuilder:

    def build(
        self,
        semantic_entities: list = None,
        extracted_entities: list = None,
        graph: Any = None,
    ) -> ATSProfile:

        profile = ATSProfile()

        # Collect all entities from all sources
        all_entities = []
        
        if semantic_entities:
            all_entities.extend(semantic_entities)
        
        if extracted_entities:
            all_entities.extend(extracted_entities)
        
        if graph:
            graph_nodes = self._nodes(graph)
            all_entities.extend(graph_nodes)

        if not all_entities:
            return profile

        matched = []

        for entity in all_entities:
            data = self._data(entity)
            
            # Get ATS score from various possible locations
            ats_score = self._extract_ats_score(entity, data)
            
            if ats_score is None or ats_score <= 0:
                continue

            # Build matched entity record
            record = {
                "ats_score": ats_score,
                "entity_id": self._get(
                    entity,
                    data,
                    "entity_id",
                    "id",
                    "node_id",
                ),
                "canonical": self._get(
                    entity,
                    data,
                    "canonical",
                    "name",
                    "label",
                    "text",
                ),
                "entity_type": self._get(
                    entity,
                    data,
                    "entity_type",
                    "type",
                ),
                "confidence": self._get(
                    entity,
                    data,
                    "confidence",
                ),
            }
            
            # Add any additional metadata
            metadata = data.get("metadata", {})
            if isinstance(metadata, dict):
                for key, value in metadata.items():
                    if key not in record:
                        record[key] = value

            matched.append(record)

        profile.entity_count = len(matched)
        profile.matched_entities = sorted(
            matched,
            key=lambda item: float(item.get("ats_score", 0)),
            reverse=True,
        )[:20]  # Limit to top 20 for display

        if matched:
            # Calculate weighted score based on all matches
            total_score = sum(float(item.get("ats_score", 0)) for item in matched)
            profile.score = round(total_score / len(matched), 4)

        return profile

    def _extract_ats_score(self, entity, data):
        """Extract ATS score from various possible locations."""
        
        # Check direct attributes
        for key in (
            "ats_score",
            "ats_weight",
            "ats_match_score",
            "keyword_score",
            "score",
            "weight",
        ):
            value = self._get(entity, data, key)
            if value is not None:
                try:
                    score = float(value)
                    if 0 <= score <= 1:
                        return score
                    # Normalize if score is 0-100
                    if 0 <= score <= 100:
                        return score / 100
                    return score
                except (TypeError, ValueError):
                    pass

        # Check metadata
        metadata = data.get("metadata", {})
        if isinstance(metadata, dict):
            for key in (
                "ats_score",
                "ats_weight",
                "ats_match_score",
                "keyword_score",
                "score",
            ):
                value = metadata.get(key)
                if value is not None:
                    try:
                        score = float(value)
                        if 0 <= score <= 1:
                            return score
                        if 0 <= score <= 100:
                            return score / 100
                        return score
                    except (TypeError, ValueError):
                        pass

            # Check nested ats dict
            ats = metadata.get("ats", {})
            if isinstance(ats, dict):
                value = ats.get("score")
                if value is not None:
                    try:
                        score = float(value)
                        if 0 <= score <= 1:
                            return score
                        if 0 <= score <= 100:
                            return score / 100
                        return score
                    except (TypeError, ValueError):
                        pass

        # Check if entity has confidence as ATS proxy
        confidence = self._get(entity, data, "confidence")
        if confidence is not None:
            try:
                return float(confidence)
            except (TypeError, ValueError):
                pass

        return None

    @staticmethod
    def _nodes(graph):
        if graph is None:
            return []

        nodes = getattr(graph, "nodes", [])
        
        if callable(nodes):
            try:
                nodes = nodes()
            except Exception:
                return []

        if isinstance(nodes, dict):
            return list(nodes.values())

        return list(nodes)

    @staticmethod
    def _data(node):
        if isinstance(node, dict):
            return dict(node)

        data = getattr(node, "data", None)
        
        if isinstance(data, dict):
            return dict(data)

        # Try to get all attributes
        result = {}
        for key in dir(node):
            if not key.startswith("_"):
                try:
                    value = getattr(node, key)
                    if not callable(value):
                        result[key] = value
                except Exception:
                    pass
        
        return result

    @staticmethod
    def _get(node, data, *names):
        for name in names:
            if name in data:
                return data[name]

            value = getattr(node, name, None)
            if value is not None:
                return value

        return None