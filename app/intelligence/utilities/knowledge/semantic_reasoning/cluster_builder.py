"""
Enterprise Cluster Builder

BusinessStatement
        ↓
SemanticCluster

Enterprise V10
"""

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticCluster,
    SemanticMetadata,
)


class ClusterBuilder:

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        business_statements,
    ):

        clusters = []

        for statement in business_statements:

            cluster = SemanticCluster(

                cluster_id=statement.statement_id.replace(
                    "STATEMENT",
                    "CLUSTER",
                ),

                label=statement.label,

                semantic_type=statement.semantic_type,

                primary_domain=statement.primary_domain,

                business_area=statement.business_area,

                confidence=statement.confidence,

                entities=list(statement.entities),

                #dependencies=list(statement.dependencies),

                metadata=SemanticMetadata(

                    primary_domain=statement.primary_domain,

                    primary_business_area=statement.business_area,

                    semantic_type=statement.semantic_type,

                    achievement=statement.achievement,

                ),

            )

            clusters.append(cluster)

        return clusters