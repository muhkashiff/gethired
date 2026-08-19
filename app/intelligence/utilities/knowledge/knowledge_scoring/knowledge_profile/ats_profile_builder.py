"""
ATS Profile Builder
Enterprise V14 - FIXED (looks in metadata for ATS data)
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
            
            # Try to get ATS score - NOW LOOKS IN METADATA
            ats_score = self._extract_ats_score(entity, data)
            
            # If no ATS score found, use confidence as fallback
            if ats_score is None:
                confidence = self._get(entity, data, "confidence")
                if confidence is not None:
                    try:
                        ats_score = float(confidence)
                    except (TypeError, ValueError):
                        pass
            
            # If still no score, check if entity has any ATS metadata
            if ats_score is None:
                metadata = data.get("metadata", {})
                if isinstance(metadata, dict):
                    # Check for any ATS-related fields in metadata
                    for key in metadata:
                        if "ats" in key.lower() or "match" in key.lower():
                            value = metadata[key]
                            try:
                                score = float(value)
                                if 0 <= score <= 1:
                                    ats_score = score
                                    break
                                if 0 <= score <= 100:
                                    ats_score = score / 100
                                    break
                            except (TypeError, ValueError):
                                pass

            # If still no score, skip
            if ats_score is None or ats_score <= 0:
                continue

            # Build matched entity record
            canonical = self._get(
                entity,
                data,
                "canonical",
                "name",
                "label",
                "text",
            ) or "unknown"
            
            record = {
                "ats_score": ats_score,
                "entity_id": self._get(
                    entity,
                    data,
                    "entity_id",
                    "id",
                    "node_id",
                ) or "unknown",
                "canonical": canonical,
                "entity_type": self._get(
                    entity,
                    data,
                    "entity_type",
                    "type",
                ) or "unknown",
                "confidence": ats_score,
                "category": self._get(entity, data, "category") or "",
                "business_area": self._get(entity, data, "business_area") or "",
                "impact_weight": self._get(entity, data, "impact_weight", 1.0),
            }
            
            # Add any additional metadata
            metadata = data.get("metadata", {})
            if isinstance(metadata, dict):
                for key, value in metadata.items():
                    if key not in record:
                        record[key] = value

            matched.append(record)

        # Sort by score descending
        matched = sorted(
            matched,
            key=lambda item: float(item.get("ats_score", 0)),
            reverse=True,
        )

        profile.entity_count = len(matched)
        profile.matched_entities = matched[:20]  # Limit to top 20 for display

        if matched:
            total_score = sum(float(item.get("ats_score", 0)) for item in matched)
            profile.score = round(total_score / len(matched), 4)

        return profile

    def _extract_ats_score(self, entity, data):
        """
        Extract ATS score from various possible locations.
        PRIORITY: metadata first, then direct attributes.
        """
        
        # -----------------------------------------------------------------
        # 1. CHECK METADATA FIRST (most likely location)
        # -----------------------------------------------------------------
        metadata = data.get("metadata", {})
        if isinstance(metadata, dict):
            # Check for ATS score in metadata
            for key in (
                "ats_score",
                "ats_weight",
                "ats_match_score",
                "keyword_score",
                "match_score",
                "score",
                "weight",
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

            # Check nested ats dict in metadata
            ats = metadata.get("ats", {})
            if isinstance(ats, dict):
                for key in ("score", "weight", "match_score", "confidence"):
                    value = ats.get(key)
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

            # Check for any field containing 'ats' or 'match'
            for key, value in metadata.items():
                if "ats" in key.lower() or "match" in key.lower():
                    try:
                        score = float(value)
                        if 0 <= score <= 1:
                            return score
                        if 0 <= score <= 100:
                            return score / 100
                        return score
                    except (TypeError, ValueError):
                        pass

        # -----------------------------------------------------------------
        # 2. CHECK DIRECT ATTRIBUTES
        # -----------------------------------------------------------------
        for key in (
            "ats_score",
            "ats_weight",
            "ats_match_score",
            "keyword_score",
            "score",
            "weight",
            "confidence",
        ):
            value = self._get(entity, data, key)
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

        # -----------------------------------------------------------------
        # 3. CHECK ENTITY TYPE FOR DEFAULT SCORES
        # -----------------------------------------------------------------
        entity_type = self._get(entity, data, "entity_type", "type") or ""
        entity_type_lower = str(entity_type).lower()
        
        # Different entity types get different default scores
        default_scores = {
            "skill": 0.8,
            "certification": 0.9,
            "standard": 0.8,
            "target": 0.6,
            "action": 0.5,
            "domain": 0.5,
            "metric": 0.4,
        }
        
        for key, score in default_scores.items():
            if key in entity_type_lower:
                return score

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
        """Extract data from node, handling both objects and dicts."""
        if isinstance(node, dict):
            return dict(node)

        # If node has a metadata attribute, include it
        data = {}
        
        # Get all attributes
        for key in dir(node):
            if not key.startswith("_"):
                try:
                    value = getattr(node, key)
                    if not callable(value):
                        data[key] = value
                except Exception:
                    pass
        
        # If node has data attribute (common pattern)
        node_data = getattr(node, "data", None)
        if isinstance(node_data, dict):
            data.update(node_data)
        
        return data

    @staticmethod
    def _get(node, data, *names):
        """Get value from data dict or node attribute."""
        for name in names:
            if name in data and data[name] is not None:
                return data[name]

            if node is not None:
                value = getattr(node, name, None)
                if value is not None:
                    return value

        return None