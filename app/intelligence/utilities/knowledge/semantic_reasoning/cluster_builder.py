"""
Advanced Cluster Builder V3

Creates semantic business-event clusters instead of simply
grouping connected nodes.

Priority

Action
    ↓
Object
    ↓
Standard
    ↓
Methodology
    ↓
KPI / Metric
    ↓
Measurement
    ↓
Domain
    ↓
Skill
"""

from collections import defaultdict

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticCluster,
)


class ClusterBuilder:

    def build(self, entities, dependencies):

        if not entities:
            return []

        entity_lookup = {
            entity.entity_id: entity
            for entity in entities
        }

        # --------------------------------------------
        # Build adjacency map
        # --------------------------------------------

        adjacency = defaultdict(set)

        for edge in dependencies:

            adjacency[edge.source_entity].add(edge.target_entity)
            adjacency[edge.target_entity].add(edge.source_entity)

        # --------------------------------------------
        # Business event anchors
        # --------------------------------------------

        anchors = [
            entity
            for entity in entities
            if entity.entity_type == "action"
        ]

        visited = set()

        clusters = []

        cluster_number = 1

        # --------------------------------------------
        # Build clusters around every action
        # --------------------------------------------

        for action in anchors:

            if action.entity_id in visited:
                continue

            cluster_entities = {}

            queue = [action.entity_id]

            while queue:

                current = queue.pop(0)

                if current in visited:
                    continue

                visited.add(current)

                entity = entity_lookup.get(current)

                if entity:

                    cluster_entities[current] = entity

                for neighbour in adjacency[current]:

                    if neighbour not in visited:

                        queue.append(neighbour)

            cluster = SemanticCluster()

            cluster.cluster_id = f"CLUSTER_{cluster_number}"

            cluster.entities = list(cluster_entities.values())

            cluster.dependencies = [

                edge

                for edge in dependencies

                if edge.source_entity in cluster_entities
                and edge.target_entity in cluster_entities

            ]
            cluster.confidence = self._cluster_confidence(cluster)
            
            clusters.append(cluster)

            cluster_number += 1

        # --------------------------------------------
        # Remaining isolated entities
        # --------------------------------------------

        remaining = [

            entity

            for entity in entities

            if entity.entity_id not in visited

        ]

        priority = [

            "object",
            "standard",
            "methodology",
            "kpi",
            "metric",
            "measurement",
            "domain",
            "skill",
        ]

        for entity_type in priority:

            matching = [

                entity

                for entity in remaining

                if entity.entity_type == entity_type

            ]

            if not matching:
                continue

            cluster = SemanticCluster()

            cluster.cluster_id = f"CLUSTER_{cluster_number}"

            cluster.entities = matching

            cluster.dependencies = []

            clusters.append(cluster)

            cluster_number += 1

            for entity in matching:
                visited.add(entity.entity_id)

        return clusters
    # ==================================================

    def _cluster_confidence(self, cluster):

        if not cluster.entities:
            return 0.0

        entity_conf = sum(
            e.confidence
            for e in cluster.entities
        ) / len(cluster.entities)

        if cluster.dependencies:
            dep_conf = sum(
                d.confidence
                for d in cluster.dependencies
            ) / len(cluster.dependencies)

            return round(
                (entity_conf * 0.6) + (dep_conf * 0.4),
                2,
            )

        return round(entity_conf, 2)