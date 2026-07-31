"""
Advanced Cluster Builder V4

Builds semantic clusters directly from Business Statements.

Business Statement
        ↓
Semantic Cluster
"""

import uuid

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticCluster,
    SemanticMetadata,
)


class ClusterBuilder:

    def build(self, business_statements):

        clusters = []

        for statement in business_statements:

            cluster = SemanticCluster()

            # -----------------------------------
            # Identity
            # -----------------------------------

            cluster.cluster_id = statement.statement_id.replace(
                "STATEMENT",
                "CLUSTER",
            )
            cluster.label = statement.label

            cluster.semantic_type = statement.semantic_type

            cluster.confidence = statement.confidence

            # -----------------------------------
            # Entities
            # -----------------------------------

            cluster.entities = list(statement.entities)

            # -----------------------------------
            # Dependencies
            # -----------------------------------

            cluster.dependencies = list(

                statement.dependencies

            )

            # -----------------------------------
            # Metadata
            # -----------------------------------

            cluster.metadata = SemanticMetadata(

                primary_domain=statement.primary_domain,

                primary_business_area=statement.primary_business_area,

                semantic_type=statement.semantic_type,

                achievement=statement.achievement,

            )

            clusters.append(cluster)

        return clusters