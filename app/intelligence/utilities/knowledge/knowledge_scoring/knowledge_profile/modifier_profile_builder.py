"""
Modifier Profile Builder
Enterprise V14 - DEBUG VERSION
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
        "president", "managing director", "principal", "head",
        "executive", "management", "lead", "manager"
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
        "quality": "quality",
        "safety": "safety",
        "food": "food_safety",
        "manufacturing": "manufacturing",
        "supply": "supply_chain",
        "chain": "supply_chain",
        "retail": "retail",
        "production": "production",
        "inventory": "inventory",
        "six_sigma": "six_sigma",
        "operations": "operations",
        "business": "business",
        "analytics": "analytics",
        "data": "data_analytics",
        "training": "training",
    }

    def build(
        self,
        entities: list = None,
        graph: Any = None,
        semantic_entities: list = None,
    ) -> ModifierProfile:

        profile = ModifierProfile()

        print("\n" + "="*60)
        print("MODIFIER PROFILE BUILDER - DEBUG")
        print("="*60)

        all_entities = []
        
        if semantic_entities:
            print(f"  semantic_entities: {len(semantic_entities)}")
            all_entities.extend(semantic_entities)
        
        if entities:
            print(f"  entities: {len(entities)}")
            all_entities.extend(entities)
        
        if graph:
            graph_nodes = self._nodes(graph)
            print(f"  graph_nodes: {len(graph_nodes)}")
            all_entities.extend(graph_nodes)

        print(f"  total_entities: {len(all_entities)}")
        print("="*60)

        if not all_entities:
            print("[DEBUG] No entities found for ModifierProfile")
            return profile

        categories = Counter()
        processed_entities = 0
        entity_samples = []

        # Sample first 10 entities to see their data
        for i, entity in enumerate(all_entities[:10]):
            data = self._data(entity)
            print(f"\n[ENTITY {i}] Data keys: {list(data.keys())}")
            
            # Show relevant fields
            canonical = data.get('canonical', data.get('name', data.get('label', 'N/A')))
            category = data.get('category', 'N/A')
            business_area = data.get('business_area', 'N/A')
            entity_type = data.get('entity_type', data.get('type', 'N/A'))
            
            print(f"  canonical: {canonical}")
            print(f"  category: {category}")
            print(f"  business_area: {business_area}")
            print(f"  entity_type: {entity_type}")
            
            # Check metadata
            metadata = data.get('metadata', {})
            if metadata:
                print(f"  metadata keys: {list(metadata.keys())}")
                # Show any modifier-related metadata
                for key in metadata:
                    if 'mod' in str(key).lower() or 'cat' in str(key).lower():
                        print(f"    {key}: {metadata[key]}")

        print("\n" + "-"*60)
        print("PROCESSING ENTITIES FOR MODIFIERS")
        print("-"*60)

        for entity_idx, entity in enumerate(all_entities):
            data = self._data(entity)
            
            # Get all possible text fields
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

            category_field = str(
                self._get(
                    entity,
                    data,
                    "category",
                )
                or ""
            ).strip().lower()

            business_area = str(
                self._get(
                    entity,
                    data,
                    "business_area",
                )
                or ""
            ).strip().lower()

            entity_type = str(
                self._get(
                    entity,
                    data,
                    "entity_type",
                    "type",
                )
                or ""
            ).strip().lower()

            # Check all text sources
            text_sources = [
                ("name", name),
                ("category", category_field),
                ("business_area", business_area),
                ("entity_type", entity_type),
            ]

            found_modifier = False
            matched_keyword = None
            matched_category = None

            # Check each text source for modifiers
            for source_name, text in text_sources:
                if not text:
                    continue

                # Check if text contains any modifier keywords
                for keyword, category in self.MODIFIER_KEYWORDS.items():
                    if keyword in text:
                        matched_keyword = keyword
                        matched_category = category
                        categories[category] += 1
                        profile.total_modifiers += 1
                        
                        if category in self.EXECUTIVE_MODIFIERS or keyword in self.EXECUTIVE_MODIFIERS:
                            profile.executive_modifiers += 1
                        
                        found_modifier = True
                        processed_entities += 1
                        
                        if entity_idx < 10:  # Print first 10 matches
                            print(f"[MATCH {entity_idx}] {source_name}='{text}' -> keyword='{keyword}' -> category='{category}'")
                        break

                if found_modifier:
                    break

            # If no modifier found yet, check if the entity itself is a modifier type
            if not found_modifier:
                if entity_type in self.MODIFIER_KEYWORDS:
                    category = self.MODIFIER_KEYWORDS[entity_type]
                    categories[category] += 1
                    profile.total_modifiers += 1
                    if category in self.EXECUTIVE_MODIFIERS:
                        profile.executive_modifiers += 1
                    processed_entities += 1
                    found_modifier = True
                    if entity_idx < 10:
                        print(f"[MATCH {entity_idx}] entity_type='{entity_type}' -> category='{category}'")

            # Check metadata for modifiers
            metadata = data.get("metadata", {})
            if isinstance(metadata, dict):
                # Check for modifiers list
                modifiers = metadata.get("modifiers", [])
                if isinstance(modifiers, list):
                    for mod in modifiers:
                        mod_str = str(mod).lower().strip()
                        if mod_str:
                            category = None
                            for keyword, cat in self.MODIFIER_KEYWORDS.items():
                                if keyword in mod_str:
                                    category = cat
                                    break
                            
                            if not category:
                                category = mod_str
                            
                            categories[category] += 1
                            profile.total_modifiers += 1
                            if category in self.EXECUTIVE_MODIFIERS or mod_str in self.EXECUTIVE_MODIFIERS:
                                profile.executive_modifiers += 1
                            processed_entities += 1
                            found_modifier = True
                            if entity_idx < 10:
                                print(f"[MATCH {entity_idx}] metadata.modifiers: '{mod_str}' -> category='{category}'")
                            break

                # Check for modifier flags in metadata
                if not found_modifier:
                    for key in ["modifier", "is_modifier", "modifier_type"]:
                        if key in metadata and metadata[key]:
                            mod_str = str(metadata[key]).lower().strip()
                            if mod_str:
                                categories[mod_str] += 1
                                profile.total_modifiers += 1
                                if mod_str in self.EXECUTIVE_MODIFIERS:
                                    profile.executive_modifiers += 1
                                processed_entities += 1
                                found_modifier = True
                                if entity_idx < 10:
                                    print(f"[MATCH {entity_idx}] metadata.{key}='{mod_str}'")
                                break

        print("-"*60)
        print("SUMMARY")
        print("-"*60)
        print(f"  Total entities processed: {len(all_entities)}")
        print(f"  Entities with modifiers: {processed_entities}")
        print(f"  total_modifiers: {profile.total_modifiers}")
        print(f"  executive_modifiers: {profile.executive_modifiers}")
        print(f"  categories: {dict(categories)}")
        print("="*60 + "\n")

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
        
        # If node has metadata attribute, ensure it's included
        if hasattr(node, 'metadata'):
            metadata = getattr(node, 'metadata')
            if metadata:
                result['metadata'] = metadata
        
        return result

    @staticmethod
    def _get(node, data, *names):
        for name in names:
            if name in data and data[name] is not None:
                return data[name]

            if node is not None:
                value = getattr(node, name, None)
                if value is not None:
                    return value

        return None