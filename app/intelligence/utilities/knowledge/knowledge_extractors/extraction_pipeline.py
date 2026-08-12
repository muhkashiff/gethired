"""
Enterprise Extraction Pipeline
Enterprise V5

Responsibility:

Sentence
    ↓
KnowledgeV5Pipeline
    ↓
Ontology-specific extraction
    ↓
Entity deduplication
    ↓
Unified ExtractionResult

This layer does NOT:
- tokenize
- normalize
- match
- calculate confidence
- resolve overlaps
- rank
- reason

Those responsibilities belong to other layers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import KnowledgeV5Pipeline


# =====================================================================
# CONFIGURATION
# =====================================================================

DEFAULT_ONTOLOGIES = (
    "skills",
    "actions",
    "targets",
    "domains",
    "metrics",
    "standards",
)


# =====================================================================
# EXTRACTED ENTITY
# =====================================================================

@dataclass(frozen=True)
class ExtractedEntity:

    entity_id: str

    canonical: str

    phrase: str

    confidence: float

    ontology: str


# =====================================================================
# EXTRACTION RESULT
# =====================================================================

@dataclass
class ExtractionResult:

    sentence: str

    skills: List[ExtractedEntity] = field(
        default_factory=list
    )

    actions: List[ExtractedEntity] = field(
        default_factory=list
    )

    targets: List[ExtractedEntity] = field(
        default_factory=list
    )

    domains: List[ExtractedEntity] = field(
        default_factory=list
    )

    metrics: List[ExtractedEntity] = field(
        default_factory=list
    )

    standards: List[ExtractedEntity] = field(
        default_factory=list
    )

    all_entities: List[ExtractedEntity] = field(
        default_factory=list
    )

    # =================================================================
    # COUNTS
    # =================================================================

    @property
    def counts(self) -> Dict[str, int]:

        return {

            "skills": len(self.skills),

            "actions": len(self.actions),

            "targets": len(self.targets),

            "domains": len(self.domains),

            "metrics": len(self.metrics),

            "standards": len(self.standards),

            "all_entities": len(
                self.all_entities
            ),
        }

    # =================================================================
    # ENTITY IDS
    # =================================================================

    @property
    def entity_ids(self) -> List[str]:

        return [
            entity.entity_id
            for entity in self.all_entities
        ]

    # =================================================================
    # CONTAINS
    # =================================================================

    def contains(
        self,
        entity_id: str,
    ) -> bool:

        return any(
            entity.entity_id == entity_id
            for entity in self.all_entities
        )


# =====================================================================
# EXTRACTION COORDINATOR
# =====================================================================

class ExtractionCoordinator:

    """
    Coordinates KnowledgeV5Pipeline across ontology collections.

    The V5 pipeline remains the single source of truth for:

        Tokenization
        Matching
        Confidence
        Overlap resolution
        Ranking
    """

    def __init__(
        self,
        knowledge_pipeline: Optional[
            KnowledgeV5Pipeline
        ] = None,

        ontologies=None,
    ) -> None:

        self.pipeline = (
            knowledge_pipeline
            or KnowledgeV5Pipeline()
        )

        self.ontologies = tuple(
            ontologies
            or DEFAULT_ONTOLOGIES
        )

    # =================================================================
    # RUN
    # =================================================================

    def run(
        self,
        sentence: str,
    ) -> ExtractionResult:

        if not isinstance(
            sentence,
            str,
        ):

            raise TypeError(
                "sentence must be a string."
            )

        sentence = sentence.strip()

        result = ExtractionResult(
            sentence=sentence
        )

        if not sentence:

            return result

        # =============================================================
        # RUN V5 PIPELINE FOR EACH ONTOLOGY
        # =============================================================

        for ontology in self.ontologies:

            matches = self.pipeline.run(
                ontology,
                sentence,
            )

            entities = self._convert_matches(
                matches,
                ontology,
            )

            self._store(
                result,
                ontology,
                entities,
            )

        # =============================================================
        # BUILD GLOBAL ENTITY LIST
        # =============================================================

        result.all_entities = (
            self._build_all_entities(
                result
            )
        )

        return result

    # =================================================================
    # CONVERT MATCH RESULTS
    # =================================================================

    @staticmethod
    def _convert_matches(
        matches,
        ontology: str,
    ) -> List[ExtractedEntity]:

        entities = []

        for match in matches:

            # ---------------------------------------------------------
            # Only use fields that actually exist in MatchResult
            # ---------------------------------------------------------

            entity_id = getattr(
                match,
                "entity_id",
                None,
            )

            canonical = getattr(
                match,
                "canonical",
                "",
            )

            phrase = getattr(
                match,
                "phrase",
                "",
            )

            confidence = getattr(
                match,
                "confidence",
                0.0,
            )

            # ---------------------------------------------------------
            # Defensive validation
            # ---------------------------------------------------------

            if not entity_id:

                continue

            entities.append(
                ExtractedEntity(

                    entity_id=str(
                        entity_id
                    ),

                    canonical=str(
                        canonical
                    ),

                    phrase=str(
                        phrase
                    ),

                    confidence=float(
                        confidence
                    ),

                    ontology=ontology,
                )
            )

        return entities

    # =================================================================
    # STORE BY ONTOLOGY
    # =================================================================

    @staticmethod
    def _store(
        result: ExtractionResult,
        ontology: str,
        entities: List[ExtractedEntity],
    ) -> None:

        if ontology == "skills":

            result.skills.extend(
                entities
            )

        elif ontology == "actions":

            result.actions.extend(
                entities
            )

        elif ontology == "targets":

            result.targets.extend(
                entities
            )

        elif ontology == "domains":

            result.domains.extend(
                entities
            )

        elif ontology == "metrics":

            result.metrics.extend(
                entities
            )

        elif ontology == "standards":

            result.standards.extend(
                entities
            )

    # =================================================================
    # BUILD GLOBAL ENTITY LIST
    # =================================================================

    @staticmethod
    def _build_all_entities(
        result: ExtractionResult,
    ) -> List[ExtractedEntity]:

        groups = (

            result.skills,

            result.actions,

            result.targets,

            result.domains,

            result.metrics,

            result.standards,
        )

        entity_map = {}

        for group in groups:

            for entity in group:

                existing = entity_map.get(
                    entity.entity_id
                )

                # -----------------------------------------------------
                # First occurrence
                # -----------------------------------------------------

                if existing is None:

                    entity_map[
                        entity.entity_id
                    ] = entity

                    continue

                # -----------------------------------------------------
                # Keep strongest confidence
                # -----------------------------------------------------

                if (
                    entity.confidence
                    >
                    existing.confidence
                ):

                    entity_map[
                        entity.entity_id
                    ] = entity

        # =============================================================
        # SORT BY CONFIDENCE
        # =============================================================

        return sorted(

            entity_map.values(),

            key=lambda entity: (
                -entity.confidence,
                entity.entity_id,
            ),
        )

    # =================================================================
    # BEST ENTITY
    # =================================================================

    def best(
        self,
        sentence: str,
    ) -> Optional[ExtractedEntity]:

        result = self.run(
            sentence
        )

        if not result.all_entities:

            return None

        return result.all_entities[0]