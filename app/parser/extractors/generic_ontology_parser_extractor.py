"""
Enterprise Generic Ontology Parser Extractor
Enterprise V5

Responsibility
--------------

Convert MatchResult objects into typed ontology knowledge objects.

Pipeline:

ExtractionRequest
        ↓
KnowledgeV5Pipeline
        ↓
MatchResult
        ↓
GenericOntologyParserExtractor
        ↓
KnowledgeEntity
        ↓
Ontology-specific Knowledge model
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, ClassVar, Generic, Mapping, TypeVar

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.match_result import (
    MatchResult,
)

from app.parser.extractors.base_parser_extractor import (
    BaseParserExtractor,
    KnowledgePipelineProtocol,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_request import ExtractionRequest


T = TypeVar("T")


class GenericOntologyParserExtractor(
    BaseParserExtractor[T],
    Generic[T],
):
    """
    Generic parser/extractor for ontology entities.

    Child classes normally configure only:

        ontology_name = "skills"
        knowledge_class = SkillKnowledge
        entity_type = "skill"

    Ontology-specific fields are populated through:

        extra_fields()
    """

    # ==============================================================
    # CONFIGURATION
    # ==============================================================

    ontology_name: ClassVar[str] = ""

    knowledge_class: ClassVar[type | None] = None

    entity_type: ClassVar[str | None] = None

    # ==============================================================
    # INITIALIZATION
    # ==============================================================

    def __init__(
        self,
        pipeline: KnowledgePipelineProtocol,
        ontology: str | None = None,
        entity_factory: Callable[[], T] | None = None,
        minimum_confidence: float = 0.0,
        allowed_categories: set[str] | None = None,
        allowed_entity_types: set[str] | None = None,
    ) -> None:

        resolved_ontology = (
            ontology
            or self.ontology_name
        )

        if not resolved_ontology:
            raise ValueError(
                "An ontology must be supplied or configured "
                "as ontology_name."
            )

        if not 0.0 <= minimum_confidence <= 1.0:
            raise ValueError(
                "minimum_confidence must be between 0.0 and 1.0."
            )

        resolved_factory = (
            entity_factory
            or self.knowledge_class
        )

        if resolved_factory is None:
            raise ValueError(
                "An entity_factory must be supplied or configured "
                "as knowledge_class."
            )

        super().__init__(
            ontology=resolved_ontology,
            pipeline=pipeline,
        )

        self._entity_factory = resolved_factory

        self._minimum_confidence = (
            minimum_confidence
        )

        self._allowed_categories = (
            frozenset(allowed_categories)
            if allowed_categories
            else None
        )

        self._allowed_entity_types = (
            frozenset(allowed_entity_types)
            if allowed_entity_types
            else None
        )

    # ==============================================================
    # FILTERING
    # ==============================================================

    def should_include(
        self,
        match: MatchResult,
        request: ExtractionRequest,
    ) -> bool:
        """
        Apply reusable filtering rules.
        """

        if (
            match.confidence
            < self._minimum_confidence
        ):
            return False

        if (
            self.entity_type is not None
            and match.entity_type
            != self.entity_type
        ):
            return False

        if (
            self._allowed_categories is not None
            and match.category
            not in self._allowed_categories
        ):
            return False

        if (
            self._allowed_entity_types is not None
            and match.entity_type
            not in self._allowed_entity_types
        ):
            return False

        return True

    # ==============================================================
    # BUILD ENTITY
    # ==============================================================

    def build_entity(
        self,
        match: MatchResult,
        request: ExtractionRequest,
    ) -> T:
        """
        Create one knowledge object.
        """

        model = self._entity_factory()

        return self.populate_entity(
            model=model,
            match=match,
            request=request,
        )

    # ==============================================================
    # POPULATE COMMON ENTITY
    # ==============================================================

    def populate_entity(
        self,
        model: T,
        match: MatchResult,
        request: ExtractionRequest,
    ) -> T:
        """
        Populate all fields common to ontology knowledge models.
        """

        repository_entity = match.entity

        metadata = deepcopy(
            repository_entity.metadata
            or {}
        )

        # ----------------------------------------------------------
        # COMMON KNOWLEDGE VALUES
        # ----------------------------------------------------------

        values = {

            # ======================================================
            # DETECTION
            # ======================================================

            "found": True,

            "confidence": (
                match.confidence
            ),

            # ======================================================
            # LINGUISTIC
            # ======================================================

            "original": (
                match.phrase
            ),

            "canonical": (
                repository_entity.canonical
            ),

            "normalized": (
                repository_entity.normalized
            ),

            "base": (
                repository_entity.base
            ),

            "past": (
                repository_entity.past
            ),

            "gerund": (
                repository_entity.gerund
            ),

            "plural": (
                repository_entity.plural
            ),

            "singular": (
                repository_entity.singular
            ),

            "abbreviation": (
                repository_entity.abbreviation
            ),

            "short_name": (
                repository_entity.short_name
            ),

            # ======================================================
            # CLASSIFICATION
            # ======================================================

            "category": (
                repository_entity.category
            ),

            "entity_id": (
                repository_entity.entity_id
            ),

            "entity_type": (
                repository_entity.entity_type
            ),

            "ontology_name": (
                repository_entity.ontology_name
                or self.ontology
            ),

            "business_area": (
                repository_entity.business_area
            ),

            "domain": (
                repository_entity.domain
            ),

            "description": (
                repository_entity.description
            ),

            # ======================================================
            # BUSINESS / SEMANTIC
            # ======================================================

            "related_metrics": list(
                repository_entity.related_metrics
                or []
            ),

            "impact_weight": (
                repository_entity.impact_weight
            ),

            "business_meaning": (
                repository_entity.business_meaning
            ),

            "preferred_direction": (
                repository_entity.preferred_direction
            ),

            "preferred_unit": (
                repository_entity.preferred_unit
            ),

            "higher_is_better": (
                repository_entity.higher_is_better
            ),

            # ======================================================
            # MATCH
            # ======================================================

            "matched_phrase": (
                match.phrase
            ),

            "matched_alias": (
                match.matched_alias
            ),

            # ======================================================
            # POSITION
            # ======================================================

            "start_char": (
                match.start_char
            ),

            "end_char": (
                match.end_char
            ),

            "token_index": (
                match.token_index
            ),

            "token_count": (
                match.token_count
            ),

            "sentence_index": (
                request.context.get(
                    "sentence_index",
                    0,
                )
            ),

            # ======================================================
            # REPOSITORY
            # ======================================================

            "source": (
                repository_entity.source
            ),

            "metadata": metadata,
        }

        # ----------------------------------------------------------
        # SET COMMON FIELDS
        # ----------------------------------------------------------

        for field_name, value in values.items():

            self._set_field(
                model=model,
                field_name=field_name,
                value=value,
            )

        # ----------------------------------------------------------
        # ONTOLOGY-SPECIFIC FIELDS
        # ----------------------------------------------------------

        extra_values = self.extra_fields(
            entity=repository_entity,
            metadata=metadata,
        )

        for field_name, value in extra_values.items():

            self._set_field(
                model=model,
                field_name=field_name,
                value=value,
            )

        return model

    # ==============================================================
    # EXTENSION HOOK
    # ==============================================================

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate ontology-specific fields.

        Child classes override this method.
        """

        return {}

    # ==============================================================
    # SAFE FIELD ASSIGNMENT
    # ==============================================================

    @staticmethod
    def _set_field(
        model: T,
        field_name: str,
        value: Any,
    ) -> None:

        try:

            setattr(
                model,
                field_name,
                value,
            )

        except (
            AttributeError,
            TypeError,
        ) as error:

            raise TypeError(
                "The knowledge output object must be "
                "mutable and support the "
                f"'{field_name}' field."
            ) from error