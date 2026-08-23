"""
Enterprise Extraction Pipeline
Enterprise V5

Responsibility
--------------

Sentence
    ↓
KnowledgeV5Pipeline
    ↓
Ontology-specific extraction
    ↓
Entity conversion
    ↓
Entity deduplication
    ↓
Unified ExtractionResult

This layer does NOT:

- tokenize
- normalize
- fuzzy match
- calculate confidence
- resolve overlaps
- rank
- reason

Those responsibilities belong to KnowledgeV5Pipeline
and later reasoning layers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)


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
    "technologies",
    "methodologies",
    "business_kpis",
    "certifications",
)


# =====================================================================
# EXTRACTED ENTITY
# =====================================================================

@dataclass(frozen=True)
class ExtractedEntity:

    entity_id: str = ""

    canonical: str = ""

    phrase: str = ""

    confidence: float = 0.0

    ontology: str = ""

    # Repository identity
    entity_type: str = ""

    category: str = ""

    business_area: str = ""

    domain: str = ""

    impact_weight: float = 1.0

    # Matching information
    matched_alias: str = ""

    is_alias: bool = False

    # Position information
    token_index: int = 0

    token_count: int = 0

    start_char: int = 0

    end_char: int = 0

    # Repository metadata
    metadata: dict = field(default_factory=dict)


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

    technologies: List[ExtractedEntity] = field(
        default_factory=list
    )

    methodologies: List[ExtractedEntity] = field(
        default_factory=list
    )

    business_kpis: List[ExtractedEntity] = field(
        default_factory=list
    )

    certifications: List[ExtractedEntity] = field(
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
            "technologies": len(self.technologies),
            "methodologies": len(self.methodologies),
            "business_kpis": len(self.business_kpis),
            "certifications": len(self.certifications),
            "all_entities": len(self.all_entities),
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
    Coordinates KnowledgeV5Pipeline across all ontology collections.

    KnowledgeV5Pipeline remains the single source of truth for:

        Tokenization
        Matching
        Confidence
        Overlap resolution
        Ranking

    This coordinator only:

        1. invokes the V5 pipeline
        2. converts MatchResult objects
        3. stores them under the requested ontology
        4. builds the unified entity list
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

        if not isinstance(sentence, str):

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
        # RUN V5 PIPELINE FOR EVERY ONTOLOGY
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

        entities: List[ExtractedEntity] = []

        for match in matches or []:

            entity_id = getattr(
                match,
                "entity_id",
                None,
            )

            if not entity_id:
                continue

            entity = getattr(
                match,
                "entity",
                None,
            )

            entities.append(
                ExtractedEntity(

                    # -------------------------------------------------
                    # Identity
                    # -------------------------------------------------

                    entity_id=str(
                        entity_id
                    ),

                    canonical=str(
                        getattr(
                            match,
                            "canonical",
                            "",
                        )
                        or ""
                    ),

                    phrase=str(
                        getattr(
                            match,
                            "phrase",
                            "",
                        )
                        or ""
                    ),

                    # IMPORTANT:
                    # The ontology passed to pipeline.run() is the
                    # authoritative ontology for this extraction pass.
                    ontology=str(
                        ontology
                    ),

                    # -------------------------------------------------
                    # Confidence
                    # -------------------------------------------------

                    confidence=float(
                        getattr(
                            match,
                            "confidence",
                            0.0,
                        )
                        or 0.0
                    ),

                    # -------------------------------------------------
                    # Repository information
                    # -------------------------------------------------

                    entity_type=str(
                        getattr(
                            match,
                            "entity_type",
                            "",
                        )
                        or ""
                    ),

                    category=str(
                        getattr(
                            match,
                            "category",
                            "",
                        )
                        or ""
                    ),

                    business_area=str(
                        getattr(
                            match,
                            "business_area",
                            "",
                        )
                        or ""
                    ),

                    domain=str(
                        getattr(
                            match,
                            "domain",
                            "",
                        )
                        or ""
                    ),

                    impact_weight=float(
                        getattr(
                            match,
                            "impact_weight",
                            1.0,
                        )
                        or 1.0
                    ),

                    # -------------------------------------------------
                    # Match information
                    # -------------------------------------------------

                    matched_alias=str(
                        getattr(
                            match,
                            "matched_alias",
                            "",
                        )
                        or ""
                    ),

                    is_alias=bool(
                        getattr(
                            match,
                            "is_alias",
                            False,
                        )
                    ),

                    # -------------------------------------------------
                    # Position
                    # -------------------------------------------------

                    token_index=int(
                        getattr(
                            match,
                            "token_index",
                            0,
                        )
                        or 0
                    ),

                    token_count=int(
                        getattr(
                            match,
                            "token_count",
                            0,
                        )
                        or 0
                    ),

                    start_char=int(
                        getattr(
                            match,
                            "start_char",
                            0,
                        )
                        or 0
                    ),

                    end_char=int(
                        getattr(
                            match,
                            "end_char",
                            0,
                        )
                        or 0
                    ),

                    # -------------------------------------------------
                    # Metadata
                    # -------------------------------------------------

                    metadata=dict(
                        getattr(
                            entity,
                            "metadata",
                            {},
                        )
                        or {}
                    ),
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

        # Normalize ontology name once.
        ontology = str(
            ontology
        ).strip().lower()

        # Explicit ontology → result field mapping.
        ontology_map = {
            "skills": result.skills,
            "actions": result.actions,
            "targets": result.targets,
            "domains": result.domains,
            "metrics": result.metrics,
            "standards": result.standards,
            "technologies": result.technologies,
            "methodologies": result.methodologies,
            "business_kpis": result.business_kpis,
            "certifications": result.certifications,
        }

        target = ontology_map.get(
            ontology
        )

        if target is None:
            return

        target.extend(
            entities
        )

    # =================================================================
    # BUILD GLOBAL ENTITY LIST
    # =================================================================

    @staticmethod
    def _build_all_entities(
        result: ExtractionResult,
    ) -> List[ExtractedEntity]:

        # IMPORTANT:
        # Include ALL ontology collections.
        #
        # The previous implementation only included:
        #   skills
        #   actions
        #   targets
        #   domains
        #   metrics
        #   standards
        #
        # That silently discarded:
        #   technologies
        #   methodologies
        #   business_kpis
        #   certifications

        groups = (
            result.skills,
            result.actions,
            result.targets,
            result.domains,
            result.metrics,
            result.standards,
            result.technologies,
            result.methodologies,
            result.business_kpis,
            result.certifications,
        )

        entity_map: Dict[
            str,
            ExtractedEntity
        ] = {}

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