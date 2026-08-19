"""
Modifier Profile Builder
Enterprise V14 - FIXED
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import ModifierProfile


class ModifierProfileBuilder:

    EXECUTIVE_MODIFIERS = {
        "executive", "strategic", "enterprise", "organization-wide",
        "company-wide", "director", "senior", "leadership", "vp",
        "vice president", "chief", "cfo", "ceo", "cto", "coo",
        "president", "managing director", "principal", "head"
    }

    MODIFIER_KEYWORDS = {
        "senior": "seniority",
        "lead": "leadership",
        "executive": "executive",
        "strategic": "strategic",
        "advanced": "expertise",
        "expert": "expertise",
        "certified": "certification",
        "professional": "professional",
        "experienced": "experience",
        "specialized": "specialization",
        "cross-functional": "collaboration",
        "enterprise": "enterprise",
        "global": "global",
        "international": "global",
        "corporate": "corporate",
        "manager": "management",
        "director": "leadership",
        "principal": "leadership",
        "staff": "seniority",
        "leadership": "leadership",
        "management": "management",
        "strategic": "strategic",
        "tactical": "tactical",
        "operational": "operational",
        "technical": "technical",
        "functional": "functional",
    }

    def build(
        self,
        entities: list = None,
        graph: Any = None,
        semantic_entities: list = None,
    ) -> ModifierProfile:

        profile = ModifierProfile()

        all_entities = []
        
        if semantic_entities:
            all_entities.extend(semantic_entities)
        
        if entities:
            all_entities.extend(entities)
        
        if graph:
            graph_nodes = self._nodes(graph)
            all_entities.extend(graph_nodes)

        if not all_entities:
            return profile

        categories = Counter()

        for entity in all_entities:
            data = self._data(entity)
            
            name = str(
                self._get(
                    entity,
                    data,
                    "canonical",
                    "name",
                    "label",
                    "text",
                    "entity_id",
                )
                or ""
            ).strip().lower()

            if not name:
                continue

            # Check if entity contains modifier keywords
            for keyword, category in self.MODIFIER_KEYWORDS.items():
                if keyword in name:
                    categories[category] += 1
                    profile.total_modifiers += 1
                    
                    if category in self.EXECUTIVE_MODIFIERS or keyword in self.EXECUTIVE_MODIFIERS:
                        profile.executive_modifiers += 1
                    break

            # Check entity_type
            entity_type = str(
                self._get(
                    entity,
                    data,
                    "entity_type",
                    "type",
                )
                or ""
            ).lower()

            if entity_type in self.MODIFIER_KEYWORDS:
                category = self.MODIFIER_KEYWORDS[entity_type]
                categories[category] += 1
                profile.total_modifiers += 1
                if category in self.EXECUTIVE_MODIFIERS:
                    profile.executive_modifiers += 1

            # Check metadata
            metadata = data.get("metadata", {})
            if isinstance(metadata, dict):
                modifiers = metadata.get("modifiers", [])
                if isinstance(modifiers, list):
                    for mod in modifiers:
                        mod_str = str(mod).lower().strip()
                        if mod_str:
                            categories[mod_str] += 1
                            profile.total_modifiers += 1
                            if mod_str in self.EXECUTIVE_MODIFIERS:
                                profile.executive_modifiers += 1

        profile.categories = dict(categories)

        return profile

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