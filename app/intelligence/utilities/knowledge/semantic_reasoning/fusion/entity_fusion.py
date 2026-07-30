"""
Entity Fusion Engine

Responsible for grouping extracted ontology entities into
logical semantic clusters.

Example

Implemented ISO9001 using Lean Manufacturing.

↓

SemanticCluster

    Action
    Standard
    Methodology

instead of three disconnected entities.
"""

from collections import defaultdict

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticCluster,
)


class EntityFusion:

    """
    Creates semantic clusters from extracted entities.
    """

    def __init__(self):

        pass

    # ---------------------------------------------------------

    def fuse(self, entities, dependencies):

        """
        Build semantic clusters.

        Current version groups entities around actions.

        Future versions will also cluster

            • noun phrases

            • coordinated entities

            • dependency trees

            • semantic similarity

        """

        clusters = []

        action_entities = [

            entity

            for entity in entities

            if entity.entity_type.lower() == "action"

        ]

        # -----------------------------------------------------
        # No action found
        # -----------------------------------------------------

        if not action_entities:

            cluster = SemanticCluster(

                cluster_id="CLUSTER_1",

                label="General",

                semantic_type="general",

                confidence=1.0,

                entities=entities,

                dependencies=dependencies,

            )

            clusters.append(cluster)

            return clusters

        # -----------------------------------------------------
        # Cluster around every action
        # -----------------------------------------------------

        for index, action in enumerate(action_entities, start=1):

            cluster_entities = [action]

            cluster_dependencies = []

            connected = set()

            connected.add(action.entity_id)

            # ---------------------------------------------

            for dep in dependencies:

                if dep.source_entity == action.entity_id:

                    connected.add(dep.target_entity)

                    cluster_dependencies.append(dep)

                elif dep.target_entity == action.entity_id:

                    connected.add(dep.source_entity)

                    cluster_dependencies.append(dep)

            # ---------------------------------------------

            for entity in entities:

                if entity.entity_id in connected:

                    if entity not in cluster_entities:

                        cluster_entities.append(entity)

            cluster = SemanticCluster(

                cluster_id=f"CLUSTER_{index}",

                label=action.canonical,

                semantic_type="business_statement",

                confidence=action.confidence,

                entities=cluster_entities,

                dependencies=cluster_dependencies,

            )

            clusters.append(cluster)

        return clusters