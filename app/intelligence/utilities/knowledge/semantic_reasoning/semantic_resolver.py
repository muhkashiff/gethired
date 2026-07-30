"""
Semantic Resolver

Master semantic reasoning engine.

Pipeline

Entities
      ↓
Dependency Resolver
      ↓
Cluster Builder
      ↓
Cluster Classifier
      ↓
Business Metadata
      ↓
Semantic Result
"""

from app.intelligence.utilities.knowledge.semantic_reasoning.dependency_resolver import (
    DependencyResolver,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.cluster_builder import (
    ClusterBuilder,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.cluster_classifier import (
    ClusterClassifier,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticResolution,
    SemanticMetadata,
    SemanticStatistics,
)


class SemanticResolver:

    def __init__(self):

        self.dependency_resolver = DependencyResolver()

        self.cluster_builder = ClusterBuilder()

        self.cluster_classifier = ClusterClassifier()

    # ---------------------------------------------------------

    def resolve(self, facts):

        result = SemanticResolution()

        entities = []

        for fact in facts:

            interpretation = fact.interpretation

            entities.extend(interpretation.entities)

        result.entities = entities

        # -----------------------------------------------------
        # Dependencies
        # -----------------------------------------------------

        dependencies = self.dependency_resolver.resolve(entities)

        result.dependencies = dependencies

        # -----------------------------------------------------
        # Clusters
        # -----------------------------------------------------

        clusters = self.cluster_builder.build(
            entities,
            dependencies,
        )

        classified = []

        for cluster in clusters:

            classified.append(

                self.cluster_classifier.classify(
                    cluster
                )

            )

        result.clusters = classified

        # -----------------------------------------------------
        # Metadata
        # -----------------------------------------------------

        result.metadata = self._build_metadata(
            result
        )

        # -----------------------------------------------------
        # Confidence
        # -----------------------------------------------------

        result.confidence = self._calculate_confidence(
            result
        )

        return result

    # ---------------------------------------------------------

    # ---------------------------------------------------------

    def _build_metadata(self, result):

        metadata = SemanticMetadata()

        # ---------------------------------------
        # Primary Domain
        # ---------------------------------------

        domains = [

            e

            for e in result.entities

            if e.entity_type == "domain"

        ]

        if domains:

            metadata.primary_domain = domains[0].entity_id

            metadata.primary_business_area = domains[0].business_area

        # ---------------------------------------
        # Highest Semantic Type
        # ---------------------------------------

        if result.clusters:

            metadata.semantic_type = result.clusters[0].semantic_type

        # ---------------------------------------
        # Achievement
        # ---------------------------------------

        metadata.achievement = any(

            c.semantic_type in (

                "achievement",

                "certification",

                "continuous_improvement",

            )

            for c in result.clusters

        )

        # ---------------------------------------
        # Statistics
        # ---------------------------------------

        metadata.statistics = SemanticStatistics(

            entities=len(result.entities),

            dependencies=len(result.dependencies),

            clusters=len(result.clusters),

            actions=sum(

                1

                for e in result.entities

                if e.entity_type == "action"

            ),

            objects=sum(

                1

                for e in result.entities

                if e.entity_type == "object"

            ),

            domains=sum(

                1

                for e in result.entities

                if e.entity_type == "domain"

            ),

            metrics=sum(

                1

                for e in result.entities

                if e.entity_type == "metric"

            ),

            measurements=sum(

                1

                for e in result.entities

                if e.entity_type == "measurement"

            ),

            methodologies=sum(

                1

                for e in result.entities

                if e.entity_type == "methodology"

            ),

            standards=sum(

                1

                for e in result.entities

                if e.entity_type == "standard"

            ),

        )

        return metadata

    # ---------------------------------------------------------

    def _calculate_confidence(self, result):

        if not result.entities:

            return 0.0

        scores = [

            e.confidence

            for e in result.entities

        ]

        return round(

            sum(scores) / len(scores),

            2,

        )