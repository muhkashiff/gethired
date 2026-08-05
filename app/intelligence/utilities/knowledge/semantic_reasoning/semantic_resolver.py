"""
Enterprise Semantic Resolver

Master semantic reasoning pipeline.

Enterprise V11

Pipeline

Knowledge Entities
        ↓
Semantic Entities
        ↓
Dependency Resolver
        ↓
Business Statement Builder
            • creates StatementRelation
            • groups entities
        ↓
Cluster Builder
        ↓
Cluster Classifier
        ↓
Metadata Builder
        ↓
Semantic Resolution
"""

from app.intelligence.utilities.knowledge.semantic_reasoning.dependency_resolver import (
    DependencyResolver,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.business_statement_builder import (
    BusinessStatementBuilder,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.cluster_builder import (
    ClusterBuilder,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.cluster_classifier import (
    ClusterClassifier,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.metadata_builder import (
    MetadataBuilder,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticResolution,
    SemanticEntity,
)


class SemanticResolver:

    ####################################################################
    # INITIALIZE
    ####################################################################

    def __init__(self):

        self.dependency_resolver = DependencyResolver()

        self.statement_builder = BusinessStatementBuilder()

        self.cluster_builder = ClusterBuilder()

        self.cluster_classifier = ClusterClassifier()

        self.metadata_builder = MetadataBuilder()

    ####################################################################
    # RESOLVE
    ####################################################################

    def resolve(

        self,

        facts,

    ):

        result = SemanticResolution()

        ###############################################################
        # Collect Parser Entities
        ###############################################################

        entities = []

        for fact in facts:

            interpretation = fact.interpretation

            entities.extend(

                interpretation.entities

            )

        ###############################################################
        # Convert → SemanticEntity
        ###############################################################

        entities = self._convert_entities(

            entities

        )

        result.entities = entities

        ###############################################################
        # Build Semantic Dependencies
        ###############################################################

        dependencies = self.dependency_resolver.resolve(

            entities

        )

        result.dependencies = dependencies

        ###############################################################
        # Build Business Statements
        #
        # IMPORTANT
        #
        # This stage creates:
        #
        #   • entities
        #   • relations (StatementRelation)
        #
        ###############################################################

        business_statements = self.statement_builder.build(

            entities=entities,

            dependencies=dependencies,

        )

        result.business_statements = business_statements

        ###############################################################
        # Cluster Statements
        ###############################################################

        clusters = self.cluster_builder.build(

            business_statements

        )

        ###############################################################
        # Classify Clusters
        ###############################################################

        classified_clusters = []

        for cluster in clusters:

            classified_clusters.append(

                self.cluster_classifier.classify(

                    cluster

                )

            )

        result.clusters = classified_clusters

        ###############################################################
        # Metadata
        ###############################################################

        result.metadata = self.metadata_builder.build(

            result

        )

        ###############################################################
        # Overall Confidence
        ###############################################################

        result.confidence = self._calculate_confidence(

            result

        )

        return result

    ####################################################################
    # CONFIDENCE
    ####################################################################

    def _calculate_confidence(

        self,

        result,

    ):

        if not result.clusters:

            return 0.0

        scores = [

            cluster.confidence

            for cluster in result.clusters

        ]

        return round(

            sum(scores) / len(scores),

            2,

        )

    ####################################################################
    # Convert Parser Entity → SemanticEntity
    ####################################################################

    def _convert_entities(

        self,

        entities,

    ):

        converted = []

        for entity in entities:

            converted.append(

                SemanticEntity(

                    entity_id=entity.entity_id,

                    entity_type=entity.entity_type,

                    canonical=entity.canonical,

                    original=entity.matched_text,

                    matched_text=entity.matched_text,

                    category=entity.category,

                    business_area=entity.business_area,

                    confidence=entity.confidence,

                    metadata=entity.metadata,

                )

            )

        return converted