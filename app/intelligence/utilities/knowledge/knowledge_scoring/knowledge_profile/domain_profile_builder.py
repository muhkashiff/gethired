"""
Domain Profile Builder
Enterprise V14 - FIXED
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import DomainProfile


class DomainProfileBuilder:

    # Map entity types to domains
    ENTITY_TO_DOMAIN = {
        "skill": "skills",
        "target": "business",
        "domain": "domain",
        "action": "operations",
        "metric": "metrics",
        "standard": "compliance",
        "quality": "quality_management",
        "food_safety": "food_safety",
        "manufacturing": "manufacturing",
        "supply_chain": "supply_chain",
        "retail": "retail",
        "leadership": "leadership",
        "production": "production",
        "inventory": "inventory",
        "six_sigma": "process_improvement",
        "operations": "operations",
        "business": "business",
        "business_analytics": "analytics",
        "data_analytics": "analytics",
        "training": "training",
        "management": "management",
    }

    def build(
        self,
        graph: Any = None,
        semantic_entities: list = None,
        extracted_entities: list = None,
    ) -> DomainProfile:

        profile = DomainProfile()

        # Collect entities from all sources
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

        domains = Counter()
        areas = Counter()

        for entity in all_entities:
            data = self._data(entity)

            # Try to get domain from various sources
            domain = self._extract_domain(entity, data)
            business_area = self._extract_business_area(entity, data)

            if domain:
                domains[domain] += 1

            if business_area:
                areas[business_area] += 1

        profile.domains = dict(domains)
        profile.business_areas = dict(areas)

        return profile

    def _extract_domain(self, entity, data):
        """Extract domain from entity data."""
        
        # Direct domain field
        domain = self._get(
            entity,
            data,
            "domain",
            "primary_domain",
            "category",
        )
        
        if domain:
            return str(domain).strip().lower()

        # Derive from entity_type
        entity_type = str(
            self._get(
                entity,
                data,
                "entity_type",
                "type",
                "category",
            )
            or ""
        ).strip().lower()

        # Try to map entity_type to domain
        if entity_type in self.ENTITY_TO_DOMAIN:
            return self.ENTITY_TO_DOMAIN[entity_type]

        # Try to derive from canonical name
        canonical = str(
            self._get(
                entity,
                data,
                "canonical",
                "name",
                "label",
                "text",
            )
            or ""
        ).strip().lower()

        for key, domain_name in self.ENTITY_TO_DOMAIN.items():
            if key in canonical:
                return domain_name

        # Try metadata
        metadata = data.get("metadata", {})
        if isinstance(metadata, dict):
            domain = metadata.get("domain")
            if domain:
                return str(domain).strip().lower()

        return None

    def _extract_business_area(self, entity, data):
        """Extract business area from entity data."""
        
        # Direct business_area field
        business_area = self._get(
            entity,
            data,
            "business_area",
            "area",
            "sector",
            "industry",
        )
        
        if business_area:
            return str(business_area).strip().lower()

        # Derive from entity_type
        entity_type = str(
            self._get(
                entity,
                data,
                "entity_type",
                "type",
            )
            or ""
        ).strip().lower()

        if entity_type:
            return entity_type

        # Derive from canonical name
        canonical = str(
            self._get(
                entity,
                data,
                "canonical",
                "name",
                "label",
                "text",
            )
            or ""
        ).strip().lower()

        # Look for business area keywords
        business_keywords = {
            "quality": "quality",
            "food": "food_safety",
            "safety": "food_safety",
            "manufacturing": "manufacturing",
            "production": "production",
            "supply": "supply_chain",
            "chain": "supply_chain",
            "retail": "retail",
            "inventory": "inventory",
            "six sigma": "six_sigma",
            "lean": "lean_management",
            "operations": "operations",
            "business": "business",
            "analytics": "analytics",
            "data": "data_analytics",
            "training": "training",
            "management": "management",
            "leadership": "leadership",
            "compliance": "compliance",
            "audit": "compliance",
        }

        for keyword, area in business_keywords.items():
            if keyword in canonical:
                return area

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
            if name in data and data[name]:
                return data[name]

            if node is not None:
                value = getattr(node, name, None)
                if value:
                    return value

        return None