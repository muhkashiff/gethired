

"""
Enterprise Resume Intelligence Pipeline
Enterprise V14

Architecture
============

Resume Text
    ↓
Section Detection
    ↓
KnowledgeDocument
    ↓
KnowledgeSentence
    ↓
KnowledgeFact
    ↓
ExtractionCoordinator
    ↓
KnowledgeV5Pipeline
    ↓
Ontology-specific extractors
    ├── skills
    ├── actions
    ├── targets
    ├── domains
    ├── metrics
    └── standards
    ↓
Tokenization
Normalization
Matching
Alias resolution
Confidence
Overlap resolution
Ranking
    ↓
ExtractedEntity
    ↓
KnowledgeInterpretation
    ↓
SemanticResolver
    ↓
BusinessStatementBuilder
    ↓
KnowledgeGraphBuilder
    ↓
KnowledgeProfileBuilder
    ↓
KnowledgeProfile


IMPORTANT
=========

KnowledgeV5Pipeline remains the authoritative extraction engine.

The enterprise pipeline does NOT replace:

    - tokenization
    - normalization
    - matching
    - confidence
    - overlap resolution
    - ranking

Those responsibilities remain inside KnowledgeV5Pipeline.

The EnterpriseResumePipeline is an orchestration layer.
"""
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional
import re
import traceback


# =====================================================================
# SECTION DETECTOR
# =====================================================================

try:
    from app.parser.section_detector import SectionDetector
except ImportError:
    SectionDetector = None


# =====================================================================
# KNOWLEDGE MODELS
# =====================================================================

from app.intelligence.utilities.knowledge.knowledge_models.knowledge_models import (
    KnowledgeDocument,
    KnowledgeSentence,
    KnowledgeFact,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)


# =====================================================================
# EXTRACTION COORDINATOR
# =====================================================================

try:
    from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_pipeline import (
        ExtractionCoordinator,
        ExtractedEntity,
    )
except ImportError:
    ExtractionCoordinator = None
    ExtractedEntity = None


# =====================================================================
# SEMANTIC RESOLVER
# =====================================================================

try:
    from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_resolver import (
        SemanticResolver,
    )
except ImportError:
    SemanticResolver = None


# =====================================================================
# BUSINESS STATEMENT BUILDER
# =====================================================================

try:

    from app.intelligence.utilities.knowledge.semantic_reasoning.business_statement_builder import (
        BusinessStatementBuilder,
    )

    print(
        "[PASS] BusinessStatementBuilder imported:"
    )

    print(
        "  Class:",
        BusinessStatementBuilder,
    )

    print(
        "  Module:",
        BusinessStatementBuilder.__module__,
    )

except Exception as exc:

    BusinessStatementBuilder = None

    print(
        "[FAIL] BusinessStatementBuilder import:"
    )

    print(
        "  Type:",
        type(exc).__name__,
    )

    print(
        "  Error:",
        repr(exc),
    )
# =====================================================================
# KNOWLEDGE GRAPH BUILDER
# =====================================================================

try:
    from app.intelligence.utilities.knowledge.knowledge_graph.knowledge_graph_builder import (
        KnowledgeGraphBuilder,
    )
except ImportError:
    KnowledgeGraphBuilder = None


# =====================================================================
# KNOWLEDGE PROFILE BUILDER
# =====================================================================

try:

    from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.knowledge_profile_builder import (
            KnowledgeProfileBuilder,
    )

    print(
        "[PASS] KnowledgeProfileBuilder imported:"
    )

    print(
        "  Class:",
        KnowledgeProfileBuilder,
    )

    print(
        "  Module:",
        KnowledgeProfileBuilder.__module__,
    )

except Exception as exc:

    KnowledgeProfileBuilder = None

    print(
        "[FAIL] KnowledgeProfileBuilder import:"
    )

    print(
        "  Type:",
        type(exc).__name__,
    )

    print(
        "  Error:",
        repr(exc),
    )

# =====================================================================
# DEFAULT ONTOLOGIES
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
# ENTERPRISE EXTRACTION ENTITY
# =====================================================================

@dataclass
class EnterpriseExtractedEntity:

    entity_id: str = ""

    canonical: str = ""

    phrase: str = ""

    confidence: float = 0.0

    ontology: str = ""

    entity_type: str = ""

    category: str = ""

    business_area: str = ""

    domain: str = ""

    impact_weight: float = 1.0

    matched_alias: str = ""

    is_alias: bool = False

    token_index: int = 0

    token_count: int = 0

    start_char: int = 0

    end_char: int = 0

    metadata: dict = field(
        default_factory=dict
    )

    # ---------------------------------------------------------------
    # SOURCE
    # ---------------------------------------------------------------

    source_fact: Optional[Any] = None

    source_sentence: Optional[Any] = None

    # ---------------------------------------------------------------
    # RAW V5 OBJECT
    # ---------------------------------------------------------------

    raw_match: Optional[Any] = None


# =====================================================================
# ENTERPRISE PIPELINE RESULT
# =====================================================================

@dataclass
class EnterpriseResumePipelineResult:

    success: bool = False

    failed_stage: str = ""

    error: Optional[str] = None

    resume_text: str = ""

    sections: Any = None

    section_metadata: dict = field(
        default_factory=dict
    )

    knowledge_document: Optional[
        KnowledgeDocument
    ] = None

    # ---------------------------------------------------------------
    # EXTRACTION
    # ---------------------------------------------------------------

    extraction_results: list = field(
        default_factory=list
    )

    extracted_entities: list = field(
        default_factory=list
    )

    entities_by_ontology: dict = field(
        default_factory=dict
    )

    # ---------------------------------------------------------------
    # SEMANTIC
    # ---------------------------------------------------------------

    interpretations: list = field(
        default_factory=list
    )

    semantic_entities: list = field(
        default_factory=list
    )

    semantic_dependencies: list = field(
        default_factory=list
    )

    # ---------------------------------------------------------------
    # BUSINESS STATEMENTS
    # ---------------------------------------------------------------

    business_statements: list = field(
        default_factory=list
    )

    # ---------------------------------------------------------------
    # GRAPH
    # ---------------------------------------------------------------

    knowledge_graph: Any = None

    # ---------------------------------------------------------------
    # PROFILE
    # ---------------------------------------------------------------

    knowledge_profile: Any = None

    # ---------------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------------

    stages: dict = field(
        default_factory=dict
    )

    # ---------------------------------------------------------------
    # STATISTICS
    # ---------------------------------------------------------------

    statistics: dict = field(
        default_factory=dict
    )

    confidence: float = 0.0


# =====================================================================
# ENTERPRISE PIPELINE
# =====================================================================

class EnterpriseResumePipeline:

    def __init__(
        self,
        section_detector=None,
        extraction_coordinator=None,
        semantic_resolver=None,
        business_statement_builder=None,
        knowledge_graph_builder=None,
        knowledge_profile_builder=None,
        ontologies=None,
        debug=False,
    ):

        self.debug = debug

        self.ontologies = tuple(
            ontologies
            or DEFAULT_ONTOLOGIES
        )

        self.section_detector = (
            section_detector
            if section_detector is not None
            else self._create_section_detector()
        )

        self.extraction_coordinator = (
            extraction_coordinator
            if extraction_coordinator is not None
            else self._create_extraction_coordinator()
        )

        self.semantic_resolver = (
            semantic_resolver
            if semantic_resolver is not None
            else self._create_semantic_resolver()
        )

        self.business_statement_builder = (
            business_statement_builder
            if business_statement_builder is not None
            else self._create_business_statement_builder()
        )

        self.knowledge_graph_builder = (
            knowledge_graph_builder
            if knowledge_graph_builder is not None
            else self._create_knowledge_graph_builder()
        )

        self.knowledge_profile_builder = (
            knowledge_profile_builder
            if knowledge_profile_builder is not None
            else self._create_knowledge_profile_builder()
        )

    # =================================================================
    # FACTORIES
    # =================================================================

    @staticmethod
    def _create_section_detector():

        if SectionDetector is None:
            return None

        return SectionDetector()

    # -----------------------------------------------------------------

    def _create_extraction_coordinator(self):

        if ExtractionCoordinator is None:
            return None

        return ExtractionCoordinator(
            ontologies=self.ontologies
        )

    # -----------------------------------------------------------------

    @staticmethod
    def _create_semantic_resolver():

        if SemanticResolver is None:
            return None

        return SemanticResolver()

    # -----------------------------------------------------------------

    @staticmethod
    def _create_business_statement_builder():

        print()
        print("=" * 80)
        print("BUSINESS STATEMENT BUILDER DIAGNOSTIC")
        print("=" * 80)

        print(
            "BusinessStatementBuilder symbol:",
            BusinessStatementBuilder,
        )

        print(
            "BusinessStatementBuilder type:",
            type(BusinessStatementBuilder),
        )

        if BusinessStatementBuilder is None:

            print(
                "[FAIL] BusinessStatementBuilder is None"
            )

            raise ImportError(
                "BusinessStatementBuilder import resolved to None."
            )

        try:

            builder = BusinessStatementBuilder()

            print(
                "[PASS] BusinessStatementBuilder instantiated."
            )

            print(
                "Builder class:",
                type(builder).__name__,
            )

            print(
                "Builder module:",
                type(builder).__module__,
            )

            print(
                "Builder methods:",
                [
                    name
                    for name in dir(builder)
                    if not name.startswith("_")
                ],
            )

            return builder

        except Exception as exc:

            print(
                "[FAIL] BusinessStatementBuilder "
                "instantiation failed."
            )

            print(
                "Exception type:",
                type(exc).__name__,
            )

            print(
                "Exception:",
                repr(exc),
            )

            raise
    # -----------------------------------------------------------------

    @staticmethod
    def _create_knowledge_graph_builder():

        if KnowledgeGraphBuilder is None:
            return None

        return KnowledgeGraphBuilder()

    # -----------------------------------------------------------------

    @staticmethod
    def _create_knowledge_profile_builder():

        if KnowledgeProfileBuilder is None:
            return None

        return KnowledgeProfileBuilder()

    # =================================================================
    # DEBUG
    # =================================================================

    def _debug(self, *args):

        if self.debug:
            print(*args)

    # =================================================================
    # PUBLIC RUN
    # =================================================================

    def run(
        self,
        resume_text: str,
    ) -> EnterpriseResumePipelineResult:

        result = EnterpriseResumePipelineResult(
            resume_text=resume_text or ""
        )

        # =============================================================
        # INPUT
        # =============================================================

        if not isinstance(
            resume_text,
            str,
        ):

            return self._fail(
                result,
                "input_validation",
                TypeError(
                    "resume_text must be a string."
                ),
            )

        resume_text = resume_text.strip()

        if not resume_text:

            return self._fail(
                result,
                "input_validation",
                ValueError(
                    "resume_text cannot be empty."
                ),
            )

        result.resume_text = resume_text

        try:

            # =========================================================
            # STAGE 1
            # =========================================================

            self._debug(
                "\n[STAGE 1] Section detection"
            )

            self._stage_section_detection(
                result
            )

            # =========================================================
            # STAGE 2
            # =========================================================

            self._debug(
                "\n[STAGE 2] Knowledge document"
            )

            self._stage_knowledge_document(
                result
            )

            # =========================================================
            # STAGE 3
            # =========================================================

            self._debug(
                "\n[STAGE 3] Knowledge V5 extraction"
            )

            self._stage_semantic_extraction(
                result
            )

            # =========================================================
            # STAGE 4
            # =========================================================

            self._debug(
                "\n[STAGE 4] Semantic resolution"
            )

            self._stage_semantic_resolution(
                result
            )

            # =========================================================
            # STAGE 5
            # =========================================================

            self._debug(
                "\n[STAGE 5] Business statements"
            )

            self._stage_business_statements(
                result
            )

            # =========================================================
            # STAGE 6
            # =========================================================

            self._debug(
                "\n[STAGE 6] Knowledge graph"
            )

            self._stage_knowledge_graph(
                result
            )

            # =========================================================
            # STAGE 7
            # =========================================================

            self._debug(
                "\n[STAGE 7] Graph profile"
            )

            self._stage_knowledge_profile(
                result
            )

            # =========================================================
            # COMPLETE
            # =========================================================

            result.confidence = (
                self._calculate_confidence(
                    result
                )
            )

            result.success = True

            result.failed_stage = ""

            result.error = None

            return result

        except Exception as exc:

            stage = (
                self._infer_failed_stage(
                    result
                )
            )

            return self._fail(
                result,
                stage,
                exc,
            )

    # =================================================================
    # STAGE 1
    # =================================================================

    def _stage_section_detection(
        self,
        result,
    ):

        detector = self.section_detector

        if detector is None:

            result.sections = {}

            result.section_metadata = {}

            result.stages[
                "section_detection"
            ] = True

            return

        if hasattr(
            detector,
            "detect",
        ):

            output = detector.detect(
                result.resume_text
            )

        elif callable(
            detector
        ):

            output = detector(
                result.resume_text
            )

        else:

            raise TypeError(
                "SectionDetector must expose "
                "detect() or be callable."
            )

        result.sections = output

        result.section_metadata = (
            self._extract_section_metadata(
                output
            )
        )

        result.stages[
            "section_detection"
        ] = True

    # =================================================================
    # STAGE 2
    # =================================================================

    def _stage_knowledge_document(
        self,
        result,
    ):

        document = KnowledgeDocument()

        texts = self._split_resume_text(
            result.resume_text
        )

        for text in texts:

            sentence = KnowledgeSentence(
                original_text=text,
                facts=[],
                confidence=1.0,
            )

            fact = KnowledgeFact(
                text=text,
                achievement=False,
                quantified=False,
                source="resume",
                confidence=1.0,
            )

            fact.interpretation = (
                KnowledgeInterpretation()
            )

            sentence.facts.append(
                fact
            )

            document.sentences.append(
                sentence
            )

            document.facts.append(
                fact
            )

        document.statistics = {
            "sentence_count": len(
                document.sentences
            ),
            "fact_count": len(
                document.facts
            ),
            "raw_text": bool(
                result.resume_text
            ),
        }

        document.confidence = (
            1.0
            if document.facts
            else 0.0
        )

        result.knowledge_document = (
            document
        )

        result.stages[
            "knowledge_document"
        ] = True

        result.statistics[
            "knowledge_facts"
        ] = len(
            document.facts
        )

    # =================================================================
    # STAGE 3
    # KNOWLEDGE V5 EXTRACTION
    # =================================================================

    def _stage_semantic_extraction(
        self,
        result,
    ):

        document = (
            result.knowledge_document
        )

        if document is None:
            raise ValueError(
                "KnowledgeDocument is missing."
            )

        coordinator = (
            self.extraction_coordinator
        )

        if coordinator is None:
            raise ImportError(
                "ExtractionCoordinator could not "
                "be created."
            )

        result.extraction_results = []

        result.extracted_entities = []

        result.entities_by_ontology = {
            ontology: []
            for ontology in self.ontologies
        }

        # -------------------------------------------------------------
        # Process every KnowledgeSentence / KnowledgeFact
        # -------------------------------------------------------------

        for sentence_index, sentence in enumerate(
            document.sentences
        ):

            for fact_index, fact in enumerate(
                sentence.facts
            ):

                text = (
                    getattr(
                        fact,
                        "text",
                        "",
                    )
                    or ""
                ).strip()

                if not text:
                    continue

                self._debug(
                    f"\n  FACT {sentence_index}:{fact_index}"
                )

                self._debug(
                    f"  TEXT: {text}"
                )

                # -----------------------------------------------------
                # CRITICAL CALL
                #
                # THIS IS WHERE THE WORKING V5 PIPELINE IS CALLED.
                # -----------------------------------------------------

                extraction = coordinator.run(
                    text
                )

                result.extraction_results.append(
                    extraction
                )

                # -----------------------------------------------------
                # Convert V5 entities into enterprise entities.
                # -----------------------------------------------------

                entities = (
                    self._convert_extraction_result(
                        extraction,
                        fact,
                        sentence,
                    )
                )

                self._debug(
                    f"  ENTITIES: {len(entities)}"
                )

                # -----------------------------------------------------
                # Attach entities to fact interpretation.
                # -----------------------------------------------------

                self._attach_entities_to_fact(
                    fact,
                    entities,
                )

                # -----------------------------------------------------
                # Store globally.
                # -----------------------------------------------------

                for entity in entities:

                    result.extracted_entities.append(
                        entity
                    )

                    result.entities_by_ontology.setdefault(
                        entity.ontology,
                        []
                    ).append(
                        entity
                    )

                # -----------------------------------------------------
                # Existing lightweight fact analysis.
                # -----------------------------------------------------

                self._populate_fact_metadata(
                    fact
                )

        # -------------------------------------------------------------
        # GLOBAL DEDUPLICATION
        # -------------------------------------------------------------

        result.extracted_entities = (
            self._unique_objects(
                result.extracted_entities
            )
        )

        for ontology in (
            result.entities_by_ontology
        ):

            result.entities_by_ontology[
                ontology
            ] = self._unique_objects(
                result.entities_by_ontology[
                    ontology
                ]
            )

        # -------------------------------------------------------------
        # Statistics
        # -------------------------------------------------------------

        result.statistics[
            "extracted_entities"
        ] = len(
            result.extracted_entities
        )

        result.statistics[
            "extraction_calls"
        ] = len(
            result.extraction_results
        )

        result.statistics[
            "entities_by_ontology"
        ] = {
            key: len(value)
            for key, value
            in result.entities_by_ontology.items()
        }

        # -------------------------------------------------------------
        # IMPORTANT
        #
        # Do NOT fail here merely because one resume has no entities.
        #
        # The V5 extractor is allowed to produce zero matches for
        # individual facts.
        # -------------------------------------------------------------

        result.stages[
            "extraction"
        ] = True

    # =================================================================
    # CONVERT EXTRACTION RESULT
    # =================================================================

    @staticmethod
    def _convert_extraction_result(
        extraction,
        fact,
        sentence,
    ):

        entities = []

        raw_entities = getattr(
            extraction,
            "all_entities",
            None,
        )

        if raw_entities is None:

            raw_entities = []

            for ontology in DEFAULT_ONTOLOGIES:

                raw_entities.extend(
                    getattr(
                        extraction,
                        ontology,
                        [],
                    )
                    or []
                )

        for raw in raw_entities:

            entity = EnterpriseExtractedEntity(

                entity_id=str(
                    getattr(
                        raw,
                        "entity_id",
                        "",
                    )
                    or ""
                ),

                canonical=str(
                    getattr(
                        raw,
                        "canonical",
                        "",
                    )
                    or ""
                ),

                phrase=str(
                    getattr(
                        raw,
                        "phrase",
                        "",
                    )
                    or ""
                ),

                confidence=float(
                    getattr(
                        raw,
                        "confidence",
                        0.0,
                    )
                    or 0.0
                ),

                ontology=str(
                    getattr(
                        raw,
                        "ontology",
                        "",
                    )
                    or ""
                ),

                entity_type=str(
                    getattr(
                        raw,
                        "entity_type",
                        "",
                    )
                    or ""
                ),

                category=str(
                    getattr(
                        raw,
                        "category",
                        "",
                    )
                    or ""
                ),

                business_area=str(
                    getattr(
                        raw,
                        "business_area",
                        "",
                    )
                    or ""
                ),

                domain=str(
                    getattr(
                        raw,
                        "domain",
                        "",
                    )
                    or ""
                ),

                impact_weight=float(
                    getattr(
                        raw,
                        "impact_weight",
                        1.0,
                    )
                    or 1.0
                ),

                matched_alias=str(
                    getattr(
                        raw,
                        "matched_alias",
                        "",
                    )
                    or ""
                ),

                is_alias=bool(
                    getattr(
                        raw,
                        "is_alias",
                        False,
                    )
                ),

                token_index=int(
                    getattr(
                        raw,
                        "token_index",
                        0,
                    )
                    or 0
                ),

                token_count=int(
                    getattr(
                        raw,
                        "token_count",
                        0,
                    )
                    or 0
                ),

                start_char=int(
                    getattr(
                        raw,
                        "start_char",
                        0,
                    )
                    or 0
                ),

                end_char=int(
                    getattr(
                        raw,
                        "end_char",
                        0,
                    )
                    or 0
                ),

                metadata=dict(
                    getattr(
                        raw,
                        "metadata",
                        {},
                    )
                    or {}
                ),

                source_fact=fact,

                source_sentence=sentence,

                raw_match=raw,
            )

            if entity.entity_id:

                entities.append(
                    entity
                )

        return entities

    # =================================================================
    # ATTACH ENTITIES
    # =================================================================

    @staticmethod
    def _attach_entities_to_fact(
        fact,
        entities,
    ):

        interpretation = getattr(
            fact,
            "interpretation",
            None,
        )

        if interpretation is None:

            interpretation = (
                KnowledgeInterpretation()
            )

            fact.interpretation = (
                interpretation
            )

        # -------------------------------------------------------------
        # Explicit entity collection
        # -------------------------------------------------------------

        try:

            existing = getattr(
                interpretation,
                "entities",
                None,
            )

            if existing is None:

                interpretation.entities = []

            interpretation.entities.extend(
                entities
            )

        except Exception:

            # Some versions of KnowledgeInterpretation
            # may use slots or immutable fields.
            pass

        # -------------------------------------------------------------
        # Also expose entities through typed fields.
        # -------------------------------------------------------------

        field_mapping = {
            "actions": "action",
            "targets": "target",
            "domains": "domain",
            "metrics": "metric",
            "skills": "skill",
            "standards": "standard",
        }

        grouped = {}

        for entity in entities:

            grouped.setdefault(
                entity.ontology,
                []
            ).append(
                entity
            )

        for ontology, attribute in (
            field_mapping.items()
        ):

            values = grouped.get(
                ontology,
                []
            )

            if not values:
                continue

            # If the model supports the field,
            # expose the strongest entity.
            strongest = max(
                values,
                key=lambda x: x.confidence,
            )

            try:

                setattr(
                    interpretation,
                    attribute,
                    strongest,
                )

            except Exception:

                pass

    # =================================================================
    # FACT METADATA
    # =================================================================

    @staticmethod
    def _populate_fact_metadata(
        fact,
    ):

        text = (
            getattr(
                fact,
                "text",
                "",
            )
            or ""
        ).casefold()

        achievement_terms = (
            "increased",
            "improved",
            "reduced",
            "decreased",
            "achieved",
            "delivered",
            "saved",
            "grew",
            "generated",
            "implemented",
            "certified",
            "certification",
            "successfully",
            "reached",
            "raised",
            "lowered",
            "spearheaded",
            "led",
            "oversaw",
            "strengthened",
            "enhanced",
            "drove",
        )

        achievement = any(
            term in text
            for term in achievement_terms
        )

        fact.achievement = achievement

        interpretation = getattr(
            fact,
            "interpretation",
            None,
        )

        if interpretation is not None:

            try:
                interpretation.achievement = (
                    achievement
                )
            except Exception:
                pass

        quantified = bool(
            re.search(
                r"\d+(?:\.\d+)?%?"
                r"|\$\s*\d+"
                r"|\d+\s*(?:million|billion|k|m|kg|g|l|ml)",
                getattr(
                    fact,
                    "text",
                    "",
                )
                or "",
                re.IGNORECASE,
            )
        )

        fact.quantified = quantified

        if interpretation is not None:

            try:
                interpretation.quantified = (
                    quantified
                )
            except Exception:
                pass

    # =================================================================
    # STAGE 4
    # SEMANTIC RESOLUTION
    # =================================================================

    def _stage_semantic_resolution(
        self,
        result,
    ):

        resolver = (
            self.semantic_resolver
        )

        if resolver is None:

            raise ImportError(
                "SemanticResolver could not be created."
            )

        document = (
            result.knowledge_document
        )

        output = None

        if hasattr(
            resolver,
            "resolve",
        ):

            try:

                output = resolver.resolve(
                    document
                )

            except TypeError:

                output = resolver.resolve(
                    document.facts
                )

        elif hasattr(
            resolver,
            "process",
        ):

            output = resolver.process(
                document
            )

        else:

            raise TypeError(
                "SemanticResolver must expose "
                "resolve() or process()."
            )

        interpretations = []

        entities = []

        dependencies = []

        if output is None:

            output = []

        if isinstance(
            output,
            dict,
        ):

            interpretations = (
                output.get(
                    "interpretations",
                    output.get(
                        "results",
                        [],
                    ),
                )
                or []
            )

            entities = (
                output.get(
                    "entities",
                    [],
                )
                or []
            )

            dependencies = (
                output.get(
                    "dependencies",
                    [],
                )
                or []
            )

        elif isinstance(
            output,
            (list, tuple),
        ):

            interpretations = list(
                output
            )

        else:

            interpretations = [
                output
            ]

        self._attach_interpretations(
            document,
            interpretations,
        )

        # -------------------------------------------------------------
        # The extractor has already populated the facts.
        #
        # Now collect them together with anything returned by the
        # SemanticResolver.
        # -------------------------------------------------------------

        embedded = (
            self._collect_fact_entities(
                document
            )
        )

        entities.extend(
            embedded
        )

        # Add V5 entities explicitly too.
        entities.extend(
            result.extracted_entities
        )

        result.interpretations = (
            self._unique_objects(
                interpretations
            )
        )

        result.semantic_entities = (
            self._unique_objects(
                entities
            )
        )

        result.semantic_dependencies = (
            self._unique_objects(
                dependencies
            )
        )

        result.statistics[
            "semantic_entities"
        ] = len(
            result.semantic_entities
        )

        result.statistics[
            "interpretations"
        ] = len(
            result.interpretations
        )

        result.statistics[
            "semantic_dependencies"
        ] = len(
            result.semantic_dependencies
        )

        result.stages[
            "semantic_resolution"
        ] = True

    # =================================================================
    # ATTACH INTERPRETATIONS
    # =================================================================

    @staticmethod
    def _attach_interpretations(
        document,
        interpretations,
    ):

        if not document.facts:
            return

        if not interpretations:
            return

        for index, item in enumerate(
            interpretations
        ):

            interpretation = None

            if isinstance(
                item,
                KnowledgeInterpretation,
            ):

                interpretation = item

            elif isinstance(
                item,
                dict,
            ):

                interpretation = (
                    item.get(
                        "interpretation"
                    )
                )

            else:

                interpretation = getattr(
                    item,
                    "interpretation",
                    None,
                )

            if interpretation is None:
                continue

            fact_index = None

            if isinstance(
                item,
                dict,
            ):

                fact_index = item.get(
                    "fact_index"
                )

            else:

                fact_index = getattr(
                    item,
                    "fact_index",
                    None,
                )

            if fact_index is not None:

                try:

                    fact = document.facts[
                        int(fact_index)
                    ]

                except (
                    ValueError,
                    IndexError,
                    TypeError,
                ):

                    continue

            else:

                if index >= len(
                    document.facts
                ):
                    continue

                fact = document.facts[
                    index
                ]

            fact.interpretation = (
                interpretation
            )

    # =================================================================
    # COLLECT FACT ENTITIES
    # =================================================================

    @staticmethod
    def _collect_fact_entities(
        document,
    ):

        entities = []

        for fact in document.facts:

            interpretation = getattr(
                fact,
                "interpretation",
                None,
            )

            if interpretation is None:
                continue

            embedded = getattr(
                interpretation,
                "entities",
                None,
            )

            if isinstance(
                embedded,
                (list, tuple),
            ):

                entities.extend(
                    embedded
                )

            for attribute in (
                "skill",
                "action",
                "target",
                "domain",
                "metric",
                "measurement",
                "practice",
                "standard",
            ):

                value = getattr(
                    interpretation,
                    attribute,
                    None,
                )

                if value is not None:

                    found = getattr(
                        value,
                        "found",
                        True,
                    )

                    if found:
                        entities.append(
                            value
                        )

            modifiers = getattr(
                interpretation,
                "modifiers",
                []
            )

            if isinstance(
                modifiers,
                (list, tuple),
            ):

                entities.extend(
                    modifiers
                )

        return entities

    # =================================================================
    # STAGE 5
    # =================================================================

    def _stage_business_statements(
        self,
        result,
    ):

        builder = (
            self.business_statement_builder
        )

        if builder is None:
            raise ImportError(
                "BusinessStatementBuilder could not "
                "be created."
            )

        interpretations = (
            result.interpretations
        )

        if hasattr(
            builder,
            "build",
        ):

            try:

                output = builder.build(
                    interpretations
                )

            except TypeError:

                output = builder.build(
                    result.knowledge_document
                )

        elif hasattr(
            builder,
            "build_all",
        ):

            output = builder.build_all(
                interpretations
            )

        else:

            raise TypeError(
                "BusinessStatementBuilder must "
                "expose build() or build_all()."
            )

        if output is None:
            output = []

        if isinstance(
            output,
            dict,
        ):

            output = list(
                output.values()
            )

        elif not isinstance(
            output,
            (list, tuple),
        ):

            output = [output]

        result.business_statements = list(
            output
        )

        result.statistics[
            "business_statements"
        ] = len(
            result.business_statements
        )

        result.stages[
            "business_statement_builder"
        ] = True

    # =================================================================
    # STAGE 6
    # =================================================================

    def _stage_knowledge_graph(
        self,
        result,
    ):

        builder = (
            self.knowledge_graph_builder
        )

        if builder is None:
            raise ImportError(
                "KnowledgeGraphBuilder could not "
                "be created."
            )

        statements = (
            result.business_statements
        )

        if hasattr(
            builder,
            "build",
        ):

            try:

                output = builder.build(
                    statements
                )

            except TypeError:

                output = builder.build(
                    statements=statements
                )

        elif hasattr(
            builder,
            "build_graph",
        ):

            output = builder.build_graph(
                statements
            )

        else:

            raise TypeError(
                "KnowledgeGraphBuilder must expose "
                "build() or build_graph()."
            )

        if output is None:
            raise ValueError(
                "KnowledgeGraphBuilder returned None."
            )

        result.knowledge_graph = output

        nodes = self._graph_nodes(
            output
        )

        edges = self._graph_edges(
            output
        )

        result.statistics[
            "graph_nodes"
        ] = len(nodes)

        result.statistics[
            "graph_edges"
        ] = len(edges)

        result.stages[
            "knowledge_graph"
        ] = True

    # =================================================================
    # STAGE 7
    # =================================================================

    def _stage_knowledge_profile(
        self,
        result,
    ):

        builder = (
            self.knowledge_profile_builder
        )

        if builder is None:
            raise ImportError(
                "KnowledgeProfileBuilder could not "
                "be created."
            )

        graph = (
            result.knowledge_graph
        )

        if graph is None:
            raise ValueError(
                "KnowledgeGraph is missing."
            )

        if hasattr(
            builder,
            "build",
        ):

            output = builder.build(
                graph
            )

        elif callable(
            builder
        ):

            output = builder(
                graph
            )

        else:

            raise TypeError(
                "KnowledgeProfileBuilder must expose "
                "build() or be callable."
            )

        if output is None:
            raise ValueError(
                "KnowledgeProfileBuilder returned None."
            )

        result.knowledge_profile = output

        result.stages[
            "knowledge_profile"
        ] = True

    # =================================================================
    # GRAPH ACCESS
    # =================================================================

    @staticmethod
    def _graph_nodes(
        graph,
    ):

        if graph is None:
            return []

        getter = getattr(
            graph,
            "get_nodes",
            None,
        )

        if callable(
            getter
        ):

            try:
                nodes = getter()
            except Exception:
                nodes = []

        else:

            nodes = getattr(
                graph,
                "nodes",
                []
            )

        if nodes is None:
            return []

        if isinstance(
            nodes,
            dict,
        ):

            return list(
                nodes.values()
            )

        try:
            return list(nodes)
        except TypeError:
            return []

    # -----------------------------------------------------------------

    @staticmethod
    def _graph_edges(
        graph,
    ):

        if graph is None:
            return []

        getter = getattr(
            graph,
            "get_edges",
            None,
        )

        if callable(
            getter
        ):

            try:
                edges = getter()
            except Exception:
                edges = []

        else:

            edges = getattr(
                graph,
                "edges",
                []
            )

        if edges is None:
            return []

        if isinstance(
            edges,
            dict,
        ):

            return list(
                edges.values()
            )

        try:
            return list(edges)
        except TypeError:
            return []

    # =================================================================
    # TEXT SPLITTING
    # =================================================================

    @staticmethod
    def _split_resume_text(
        text,
    ):

        if not text:
            return []

        output = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            while line.startswith(
                (
                    "- ",
                    "* ",
                    "• ",
                    "▪ ",
                    "● ",
                )
            ):

                line = line[2:].strip()

            if not line:
                continue

            parts = (
                EnterpriseResumePipeline
                ._split_sentences(
                    line
                )
            )

            if parts:
                output.extend(
                    parts
                )
            else:
                output.append(
                    line
                )

        return output

    # -----------------------------------------------------------------

    @staticmethod
    def _split_sentences(
        text,
    ):

        if not text:
            return []

        text = " ".join(
            str(text).split()
        )

        if not text:
            return []

        parts = re.split(
            r"(?<=[.!?])\s+",
            text,
        )

        return [
            part.strip()
            for part in parts
            if part.strip()
        ]

    # =================================================================
    # SECTION METADATA
    # =================================================================

    @staticmethod
    def _extract_section_metadata(
        sections,
    ):

        if sections is None:
            return {}

        metadata = getattr(
            sections,
            "metadata",
            None,
        )

        if isinstance(
            metadata,
            dict,
        ):
            return metadata

        if isinstance(
            sections,
            dict,
        ):

            metadata = sections.get(
                "metadata"
            )

            if isinstance(
                metadata,
                dict,
            ):
                return metadata

        return {}

    # =================================================================
    # DEDUPLICATION
    # =================================================================

    @staticmethod
    def _unique_objects(
        objects,
    ):

        if not objects:
            return []

        result = []

        seen = set()

        for obj in objects:

            if obj is None:
                continue

            key = (
                EnterpriseResumePipeline
                ._unique_object_key(
                    obj
                )
            )

            if key in seen:
                continue

            seen.add(key)

            result.append(obj)

        return result

    # -----------------------------------------------------------------

    @staticmethod
    def _unique_object_key(
        obj,
    ):

        if isinstance(
            obj,
            (
                str,
                int,
                float,
                bool,
            ),
        ):

            return (
                type(obj).__name__,
                str(obj)
                .strip()
                .casefold(),
            )

        entity_id = getattr(
            obj,
            "entity_id",
            None,
        )

        if entity_id:

            return (
                "entity",
                str(
                    getattr(
                        obj,
                        "ontology",
                        "",
                    )
                )
                .casefold(),
                str(entity_id)
                .casefold(),
            )

        relation_id = getattr(
            obj,
            "relation_id",
            None,
        )

        if relation_id:

            return (
                "relation",
                str(relation_id)
                .casefold(),
            )

        dependency_id = getattr(
            obj,
            "dependency_id",
            None,
        )

        if dependency_id:

            return (
                "dependency",
                str(dependency_id)
                .casefold(),
            )

        canonical = getattr(
            obj,
            "canonical",
            None,
        )

        if canonical:

            return (
                "canonical",
                type(obj).__name__,
                str(canonical)
                .strip()
                .casefold(),
            )

        try:

            return (
                "object",
                type(obj).__name__,
                repr(obj),
            )

        except Exception:

            return (
                "object",
                type(obj).__name__,
                id(obj),
            )

    # =================================================================
    # CONFIDENCE
    # =================================================================

    @staticmethod
    def _calculate_confidence(
        result,
    ):

        values = []

        document = (
            result.knowledge_document
        )

        if document is not None:

            value = getattr(
                document,
                "confidence",
                None,
            )

            if value is not None:

                try:
                    values.append(
                        float(value)
                    )
                except (
                    TypeError,
                    ValueError,
                ):
                    pass

        for entity in (
            result.extracted_entities
            or []
        ):

            try:

                values.append(
                    float(
                        getattr(
                            entity,
                            "confidence",
                            0.0,
                        )
                    )
                )

            except (
                TypeError,
                ValueError,
            ):

                pass

        for entity in (
            result.semantic_entities
            or []
        ):

            try:

                values.append(
                    float(
                        getattr(
                            entity,
                            "confidence",
                            1.0,
                        )
                    )
                )

            except (
                TypeError,
                ValueError,
            ):

                pass

        for statement in (
            result.business_statements
            or []
        ):

            try:

                values.append(
                    float(
                        getattr(
                            statement,
                            "confidence",
                            1.0,
                        )
                    )
                )

            except (
                TypeError,
                ValueError,
            ):

                pass

        profile = (
            result.knowledge_profile
        )

        if profile is not None:

            try:

                values.append(
                    float(
                        getattr(
                            profile,
                            "confidence",
                            1.0,
                        )
                    )
                )

            except (
                TypeError,
                ValueError,
            ):

                pass

        if not values:
            return 0.0

        values = [
            max(
                0.0,
                min(
                    1.0,
                    value,
                )
            )
            for value in values
        ]

        return round(
            sum(values) / len(values),
            2,
        )

    # =================================================================
    # FAILURE
    # =================================================================

    @staticmethod
    def _fail(
        result,
        stage,
        exc,
    ):

        result.success = False

        result.failed_stage = stage

        result.error = (
            repr(exc)
        )

        result.stages[
            stage
        ] = False

        return result

    # -----------------------------------------------------------------

    @staticmethod
    def _infer_failed_stage(
        result,
    ):

        stages = (
            "section_detection",
            "knowledge_document",
            "extraction",
            "semantic_resolution",
            "business_statement_builder",
            "knowledge_graph",
            "knowledge_profile",
        )

        for stage in stages:

            if not result.stages.get(
                stage,
                False,
            ):

                return stage

        return "unknown"


# =====================================================================
# CONVENIENCE API
# =====================================================================

def run_enterprise_resume_pipeline(
    resume_text,
    **kwargs,
):

    pipeline = EnterpriseResumePipeline(
        **kwargs
    )

    return pipeline.run(
        resume_text
    )


# =====================================================================
# EXPORTS
# =====================================================================

__all__ = [
    "EnterpriseResumePipeline",
    "EnterpriseResumePipelineResult",
    "EnterpriseExtractedEntity",
    "run_enterprise_resume_pipeline",
]


# =====================================================================
# DIRECT TEST
# =====================================================================

def main():

    print("=" * 80)
    print("ENTERPRISE V14 PIPELINE TEST")
    print("=" * 80)

    test_sentence = (
        "Spearheaded the site-wide implementation, execution, "
        "and regulatory compliance of the integrated Quality "
        "and Food Safety Management System (QMS)."
    )

    print("\nINPUT:")
    print(test_sentence)

    print("\n" + "-" * 80)
    print("CREATING PIPELINE")
    print("-" * 80)

    pipeline = EnterpriseResumePipeline(
        debug=True
    )

    print(
        "Extraction coordinator:",
        type(
            pipeline.extraction_coordinator
        ).__name__
        if pipeline.extraction_coordinator
        else None
    )

    print(
        "Knowledge V5 pipeline:",
        type(
            pipeline.extraction_coordinator.pipeline
        ).__name__
        if (
            pipeline.extraction_coordinator
            and hasattr(
                pipeline.extraction_coordinator,
                "pipeline",
            )
        )
        else None
    )

    print(
        "Ontologies:",
        pipeline.ontologies
    )

    print("\n" + "-" * 80)
    print("RUNNING ENTERPRISE PIPELINE")
    print("-" * 80)

    result = pipeline.run(
        test_sentence
    )

    print("\n" + "=" * 80)
    print("FINAL RESULT")
    print("=" * 80)

    print(
        "Success:",
        result.success
    )

    print(
        "Failed stage:",
        result.failed_stage
    )

    print(
        "Error:",
        result.error
    )

    print(
        "Confidence:",
        result.confidence
    )

    print("\nSTAGES:")

    for stage, status in (
        result.stages.items()
    ):

        print(
            f"  {stage:<35} "
            f"{'PASS' if status else 'FAIL'}"
        )

    print("\nSTATISTICS:")

    for key, value in (
        result.statistics.items()
    ):

        print(
            f"  {key:<35}: {value}"
        )

    print("\nENTITIES BY ONTOLOGY:")

    for ontology in (
        pipeline.ontologies
    ):

        entities = (
            result.entities_by_ontology.get(
                ontology,
                []
            )
        )

        print(
            f"\n[{ontology.upper()}] "
            f"{len(entities)}"
        )

        for entity in entities:

            print(
                f"  - "
                f"{entity.entity_id} | "
                f"{entity.canonical} | "
                f"{entity.confidence:.2f}"
            )

    print("\nALL EXTRACTED ENTITIES:")

    for index, entity in enumerate(
        result.extracted_entities,
        start=1,
    ):

        print(
            f"\nENTITY {index}"
        )

        print(
            f"  ID          : "
            f"{entity.entity_id}"
        )

        print(
            f"  Canonical   : "
            f"{entity.canonical}"
        )

        print(
            f"  Phrase      : "
            f"{entity.phrase}"
        )

        print(
            f"  Ontology    : "
            f"{entity.ontology}"
        )

        print(
            f"  Confidence  : "
            f"{entity.confidence}"
        )

        print(
            f"  Position    : "
            f"{entity.start_char}-"
            f"{entity.end_char}"
        )

    print("\n" + "=" * 80)

    if result.success:

        print(
            "FINAL STATUS: PASS"
        )

    else:

        print(
            "FINAL STATUS: FAIL"
        )

        print(
            "\nTRACEBACK:"
        )

        if result.error:
            print(
                result.error
            )

    print("=" * 80)


if __name__ == "__main__":
    main()

    """