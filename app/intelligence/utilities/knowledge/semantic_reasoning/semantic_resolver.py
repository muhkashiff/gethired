"""
Enterprise Semantic Resolver

Enterprise V12

Master semantic reasoning pipeline.

Pipeline

KnowledgeV5 MatchResult
        ↓
SemanticEntity
        ↓
DependencyResolver
        ↓
BusinessStatementBuilder
        ↓
BusinessStatement
        ↓
ClusterBuilder
        ↓
ClusterClassifier
        ↓
MetadataBuilder
        ↓
SemanticResolution

Responsibilities
----------------
• Consume KnowledgeV5 MatchResult objects
• Convert MatchResult → SemanticEntity
• Preserve repository entity identity
• Preserve KPI / BKPI / Metric distinctions
• Resolve semantic dependencies
• Build Business Statements
• Build clusters
• Build semantic metadata
• Calculate overall confidence

This class does NOT:
• build the Knowledge Graph
• access graph storage
• load ontology files directly
• perform repository matching
"""

from __future__ import annotations

from collections.abc import Iterable

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.match_result import (
    MatchResult,
)

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

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self) -> None:

        self.dependency_resolver = (
            DependencyResolver()
        )

        self.statement_builder = (
            BusinessStatementBuilder()
        )

        self.cluster_builder = (
            ClusterBuilder()
        )

        self.cluster_classifier = (
            ClusterClassifier()
        )

        self.metadata_builder = (
            MetadataBuilder()
        )

    # ==========================================================
    # PUBLIC RESOLVE API
    # ==========================================================

    def resolve(
        self,
        matches,
    ) -> SemanticResolution:
        """
        Resolve KnowledgeV5 MatchResult objects.

        Expected input
        ---------------

        list[MatchResult]

        Example:

            matches = [
                MatchResult(...),
                MatchResult(...),
                MatchResult(...),
            ]

        Pipeline:

            MatchResult
                ↓
            SemanticEntity
                ↓
            DependencyResolver
                ↓
            BusinessStatementBuilder
                ↓
            SemanticResolution
        """

        result = SemanticResolution()

        # ------------------------------------------------------
        # Normalize input
        # ------------------------------------------------------

        match_results = self._normalize_matches(
            matches
        )

        if not match_results:

            result.entities = []
            result.dependencies = []
            result.business_statements = []
            result.clusters = []
            result.metadata = {}
            result.confidence = 0.0

            return result

        # ------------------------------------------------------
        # Convert MatchResult → SemanticEntity
        # ------------------------------------------------------

        entities = self._convert_matches(
            match_results
        )

        result.entities = entities

        # ------------------------------------------------------
        # Resolve Dependencies
        # ------------------------------------------------------

        dependencies = (
            self.dependency_resolver.resolve(
                entities
            )
        )

        result.dependencies = dependencies

        # ------------------------------------------------------
        # Build Business Statements
        # ------------------------------------------------------

        business_statements = (
            self.statement_builder.build(
                entities=entities,
                dependencies=dependencies,
            )
        )

        result.business_statements = (
            business_statements
        )

        # ------------------------------------------------------
        # Build Clusters
        # ------------------------------------------------------

        clusters = (
            self.cluster_builder.build(
                business_statements
            )
        )

        # ------------------------------------------------------
        # Classify Clusters
        # ------------------------------------------------------

        classified_clusters = []

        for cluster in clusters:

            classified_cluster = (
                self.cluster_classifier.classify(
                    cluster
                )
            )

            classified_clusters.append(
                classified_cluster
            )

        result.clusters = (
            classified_clusters
        )

        # ------------------------------------------------------
        # Metadata
        # ------------------------------------------------------

        result.metadata = (
            self.metadata_builder.build(
                result
            )
        )

        # ------------------------------------------------------
        # Overall Confidence
        # ------------------------------------------------------

        result.confidence = (
            self._calculate_confidence(
                result
            )
        )

        return result

    # ==========================================================
    # NORMALIZE MATCH INPUT
    # ==========================================================

    def _normalize_matches(
        self,
        matches,
    ) -> list[MatchResult]:
        """
        Normalize V5 match input.

        Primary supported input:

            list[MatchResult]

        For backward compatibility this method also accepts
        iterable containers containing MatchResult objects.

        Invalid objects are ignored.
        """

        if matches is None:

            return []

        if isinstance(
            matches,
            MatchResult,
        ):

            return [matches]

        if isinstance(
            matches,
            (str, bytes),
        ):

            return []

        try:

            iterable = list(matches)

        except TypeError:

            return []

        normalized = []

        for item in iterable:

            if isinstance(
                item,
                MatchResult,
            ):

                normalized.append(
                    item
                )

        return normalized

    # ==========================================================
    # MATCH RESULT → SEMANTIC ENTITY
    # ==========================================================

    def _convert_matches(
        self,
        matches: list[MatchResult],
    ) -> list[SemanticEntity]:
        """
        Convert KnowledgeV5 MatchResult objects into
        SemanticEntity objects.

        Repository identity is preserved exactly.
        """

        entities = []

        seen_ids = set()

        for match in matches:

            if not isinstance(
                match,
                MatchResult,
            ):

                continue

            entity_id = (
                match.entity_id
                or ""
            ).strip()

            if not entity_id:

                continue

            # --------------------------------------------------
            # Duplicate entity protection
            #
            # Same entity can appear more than once in a
            # sentence. Do not destroy positional information,
            # therefore only skip exact duplicate matches.
            # --------------------------------------------------

            duplicate_key = (
                entity_id,
                match.start_char,
                match.end_char,
                match.statement_id,
            )

            if duplicate_key in seen_ids:

                continue

            seen_ids.add(
                duplicate_key
            )

            # --------------------------------------------------
            # Preserve repository metadata
            # --------------------------------------------------

            metadata = {}

            if match.metadata:

                metadata.update(
                    match.metadata
                )

            # --------------------------------------------------
            # Explicit semantic identity
            # --------------------------------------------------

            metadata.update(
                {
                    "repository_entity_id":
                        match.entity_id,

                    "repository_entity_type":
                        match.entity_type,

                    "repository_canonical":
                        match.canonical,

                    "matched_phrase":
                        match.phrase,

                    "matched_alias":
                        match.matched_alias,

                    "is_alias":
                        match.is_alias,

                    "statement_id":
                        match.statement_id,

                    "sentence_index":
                        match.sentence_index,

                    "start_char":
                        match.start_char,

                    "end_char":
                        match.end_char,

                    "token_index":
                        match.token_index,

                    "token_count":
                        match.token_count,
                }
            )

            # --------------------------------------------------
            # Create SemanticEntity
            # --------------------------------------------------

            semantic_entity = SemanticEntity(

                entity_id=match.entity_id,

                entity_type=match.entity_type,

                canonical=match.canonical,

                original=match.phrase,

                matched_text=match.phrase,

                category=match.category,

                business_area=match.business_area,

                confidence=self._safe_confidence(
                    match.confidence
                ),

                metadata=metadata,

            )

            # --------------------------------------------------
            # Preserve statement information if the
            # SemanticEntity model supports it.
            #
            # setattr is intentionally used so this remains
            # compatible with older SemanticEntity versions.
            # --------------------------------------------------

            self._set_optional_attribute(
                semantic_entity,
                "statement_id",
                match.statement_id,
            )

            self._set_optional_attribute(
                semantic_entity,
                "sentence_index",
                match.sentence_index,
            )

            self._set_optional_attribute(
                semantic_entity,
                "start_char",
                match.start_char,
            )

            self._set_optional_attribute(
                semantic_entity,
                "end_char",
                match.end_char,
            )

            self._set_optional_attribute(
                semantic_entity,
                "token_index",
                match.token_index,
            )

            self._set_optional_attribute(
                semantic_entity,
                "token_count",
                match.token_count,
            )

            # --------------------------------------------------
            # Preserve KPI / BKPI / Metric identity explicitly.
            #
            # DO NOT normalize these into one type.
            # --------------------------------------------------

            self._preserve_entity_type_metadata(
                semantic_entity
            )

            entities.append(
                semantic_entity
            )

        return entities

    # ==========================================================
    # ENTITY TYPE PRESERVATION
    # ==========================================================

    @staticmethod
    def _preserve_entity_type_metadata(
        entity: SemanticEntity,
    ) -> None:
        """
        Preserve exact repository semantic type.

        Important distinction:

            metric
            KPI
            BKPI
            business_kpi

        are NOT collapsed here.

        The repository remains the authority for entity type.
        """

        entity_type = (
            getattr(
                entity,
                "entity_type",
                "",
            )
            or ""
        )

        metadata = getattr(
            entity,
            "metadata",
            None,
        )

        if metadata is None:

            metadata = {}

            try:

                entity.metadata = metadata

            except Exception:

                return

        metadata[
            "semantic_entity_type"
        ] = entity_type

        # Explicit flags make downstream debugging
        # and graph validation easier.

        normalized = (
            entity_type
            .strip()
            .casefold()
        )

        metadata[
            "is_metric"
        ] = normalized == "metric"

        metadata[
            "is_kpi"
        ] = normalized == "kpi"

        metadata[
            "is_bkpi"
        ] = normalized in {
            "bkpi",
            "business_kpi",
        }

    # ==========================================================
    # CONFIDENCE
    # ==========================================================

    @staticmethod
    def _safe_confidence(
        value,
    ) -> float:
        """
        Normalize confidence into [0, 1].
        """

        try:

            value = float(value)

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

        return min(
            max(value, 0.0),
            1.0,
        )

    # ==========================================================
    # OPTIONAL ATTRIBUTE
    # ==========================================================

    @staticmethod
    def _set_optional_attribute(
        entity,
        attribute,
        value,
    ) -> None:
        """
        Set optional SemanticEntity attributes without
        breaking older model versions.
        """

        try:

            setattr(
                entity,
                attribute,
                value,
            )

        except (
            AttributeError,
            TypeError,
        ):

            pass

    # ==========================================================
    # OVERALL CONFIDENCE
    # ==========================================================

    def _calculate_confidence(
        self,
        result: SemanticResolution,
    ) -> float:
        """
        Calculate overall semantic resolution confidence.

        Cluster confidence is used when available.
        """

        if not result.clusters:

            # If clusters are unavailable but entities exist,
            # use entity confidence as a fallback.

            if result.entities:

                scores = [

                    self._safe_confidence(
                        entity.confidence
                    )

                    for entity in result.entities

                ]

                if scores:

                    return round(
                        sum(scores)
                        / len(scores),
                        2,
                    )

            return 0.0

        scores = [

            self._safe_confidence(
                cluster.confidence
            )

            for cluster in result.clusters

        ]

        if not scores:

            return 0.0

        return round(
            sum(scores)
            / len(scores),
            2,
        )