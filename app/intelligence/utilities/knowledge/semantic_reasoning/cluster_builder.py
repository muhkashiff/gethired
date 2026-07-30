"""
Advanced Semantic Cluster Builder V2

Builds business clusters using dependency relationships.

Pipeline

Entities
     +
Dependencies
        ↓
Business Clusters

Example

Implemented ISO9001 using Lean Manufacturing

becomes one cluster

Action
Object
Standard
Methodology
Domain
Measurement
"""

from collections import defaultdict

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticCluster,
)


class ClusterBuilder:

    def build(self, entities, dependencies):

        entity_lookup = {

            entity.entity_id: entity

            for entity in entities

        }

        # ---------------------------------------------
        # Build adjacency graph
        # ---------------------------------------------

        adjacency = defaultdict(set)

        for dep in dependencies:

            adjacency[dep.source_entity].add(dep.target_entity)

            adjacency[dep.target_entity].add(dep.source_entity)

        visited = set()

        clusters = []

        cluster_number = 1

        # ---------------------------------------------
        # Connected Components
        # ---------------------------------------------

        for entity in entities:

            if entity.entity_id in visited:

                continue

            component = []

            queue = [entity.entity_id]

            while queue:

                current = queue.pop(0)

                if current in visited:

                    continue

                visited.add(current)

                if current in entity_lookup:

                    component.append(entity_lookup[current])

                for neighbour in adjacency[current]:

                    if neighbour not in visited:

                        queue.append(neighbour)

            # -----------------------------------------
            # Collect dependencies
            # -----------------------------------------

            component_ids = {

                e.entity_id

                for e in component

            }

            component_dependencies = [

                dep

                for dep in dependencies

                if dep.source_entity in component_ids
                and dep.target_entity in component_ids

            ]

            cluster = SemanticCluster(

                cluster_id=f"CLUSTER_{cluster_number}",

                entities=component,

                dependencies=component_dependencies,

                confidence=self._cluster_confidence(component),

            )

            clusters.append(cluster)

            cluster_number += 1

        # ---------------------------------------------
        # Handle isolated entities
        # ---------------------------------------------

        if not clusters:

            clusters = [

                SemanticCluster(

                    cluster_id="CLUSTER_1",

                    entities=entities,

                    dependencies=[],

                    confidence=self._cluster_confidence(entities),

                )

            ]

        return clusters

    # ==================================================

    def _cluster_confidence(self, entities):

        if not entities:

            return 0.0

        scores = [

            e.confidence

            for e in entities

        ]

        return round(

            sum(scores) / len(scores),

            2,

        )