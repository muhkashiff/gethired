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
    metadata: dict = field(
        default_factory=dict
    )

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
                    ),

                    phrase=str(
                        getattr(
                            match,
                            "phrase",
                            "",
                        )
                    ),

                    ontology=ontology,

                    # -------------------------------------------------
                    # Confidence
                    # -------------------------------------------------

                    confidence=float(
                        getattr(
                            match,
                            "confidence",
                            0.0,
                        )
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
                    ),

                    category=str(
                        getattr(
                            match,
                            "category",
                            "",
                        )
                    ),

                    business_area=str(
                        getattr(
                            match,
                            "business_area",
                            "",
                        )
                    ),

                    domain=str(
                        getattr(
                            match,
                            "domain",
                            "",
                        )
                    ),

                    impact_weight=float(
                        getattr(
                            match,
                            "impact_weight",
                            1.0,
                        )
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
                    ),

                    token_count=int(
                        getattr(
                            match,
                            "token_count",
                            0,
                        )
                    ),

                    start_char=int(
                        getattr(
                            match,
                            "start_char",
                            0,
                        )
                    ),

                    end_char=int(
                        getattr(
                            match,
                            "end_char",
                            0,
                        )
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