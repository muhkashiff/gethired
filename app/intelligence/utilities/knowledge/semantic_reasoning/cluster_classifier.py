"""
Cluster Classifier V5

BusinessStatement is now the semantic source of truth.

This classifier simply validates and normalizes clusters.
"""

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticMetadata,
)


class ClusterClassifier:

    def classify(self, cluster):

        # -------------------------------------------------
        # Label
        # -------------------------------------------------

        if not cluster.label:

            cluster.label = cluster.cluster_id

        # -------------------------------------------------
        # Semantic Type
        # -------------------------------------------------

        if not cluster.semantic_type:

            cluster.semantic_type = "statement"

        # -------------------------------------------------
        # Metadata
        # -------------------------------------------------

        if cluster.metadata is None:

            cluster.metadata = SemanticMetadata()

        if not cluster.metadata.semantic_type:

            cluster.metadata.semantic_type = (

                cluster.semantic_type

            )

        # -------------------------------------------------
        # Confidence Clamp
        # -------------------------------------------------

        cluster.confidence = max(

            0.0,

            min(cluster.confidence, 0.99),

        )

        return cluster