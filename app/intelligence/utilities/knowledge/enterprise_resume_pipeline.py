"""
Enterprise Resume Intelligence Pipeline - FIXED V16
Enterprise V16

FIXES:
1. Business Statement Builder now receives SemanticResolution with clusters
2. Relations and Dependencies are properly extracted and stored
3. Clusters are properly extracted and stored
4. All semantic data flow is preserved through the pipeline
5. FIXED: KnowledgeProfileBuilder receives business_statements and semantic_entities
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict
import re
import traceback
import logging

# Set up logging
logger = logging.getLogger(__name__)

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
# SEMANTIC MODELS
# =====================================================================

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticResolution,
    SemanticEntity,
    StatementRelation,
    SemanticDependency,
    SemanticCluster,
    BusinessStatement,
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
    print("[PASS] BusinessStatementBuilder imported successfully")
except Exception as exc:
    BusinessStatementBuilder = None
    print(f"[FAIL] BusinessStatementBuilder import: {exc}")

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
    print("[PASS] KnowledgeProfileBuilder imported successfully")
except Exception as exc:
    KnowledgeProfileBuilder = None
    print(f"[FAIL] KnowledgeProfileBuilder import: {exc}")

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
    metadata: dict = field(default_factory=dict)
    source_fact: Optional[Any] = None
    source_sentence: Optional[Any] = None
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
    section_metadata: dict = field(default_factory=dict)
    knowledge_document: Optional[KnowledgeDocument] = None
    extraction_results: list = field(default_factory=list)
    extracted_entities: list = field(default_factory=list)
    entities_by_ontology: dict = field(default_factory=dict)
    interpretations: list = field(default_factory=list)
    semantic_entities: list = field(default_factory=list)
    semantic_relations: list = field(default_factory=list)  # NEW: Store relations
    semantic_dependencies: list = field(default_factory=list)
    semantic_clusters: list = field(default_factory=list)  # NEW: Store clusters
    semantic_resolution: Optional[SemanticResolution] = None
    business_statements: list = field(default_factory=list)
    knowledge_graph: Any = None
    knowledge_profile: Any = None
    stages: dict = field(default_factory=dict)
    statistics: dict = field(default_factory=dict)
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
        self.ontologies = tuple(ontologies or DEFAULT_ONTOLOGIES)

        self.section_detector = section_detector or self._create_section_detector()
        self.extraction_coordinator = extraction_coordinator or self._create_extraction_coordinator()
        self.semantic_resolver = semantic_resolver or self._create_semantic_resolver()
        self.business_statement_builder = business_statement_builder or self._create_business_statement_builder()
        self.knowledge_graph_builder = knowledge_graph_builder or self._create_knowledge_graph_builder()
        self.knowledge_profile_builder = knowledge_profile_builder or self._create_knowledge_profile_builder()

    # =================================================================
    # FACTORIES
    # =================================================================

    @staticmethod
    def _create_section_detector():
        return SectionDetector() if SectionDetector else None

    def _create_extraction_coordinator(self):
        return ExtractionCoordinator(ontologies=self.ontologies) if ExtractionCoordinator else None

    @staticmethod
    def _create_semantic_resolver():
        return SemanticResolver() if SemanticResolver else None

    @staticmethod
    def _create_business_statement_builder():
        if BusinessStatementBuilder is None:
            raise ImportError("BusinessStatementBuilder could not be imported")
        return BusinessStatementBuilder()

    @staticmethod
    def _create_knowledge_graph_builder():
        return KnowledgeGraphBuilder() if KnowledgeGraphBuilder else None

    @staticmethod
    def _create_knowledge_profile_builder():
        return KnowledgeProfileBuilder() if KnowledgeProfileBuilder else None

    def _debug(self, *args):
        if self.debug:
            print(*args)

    # =================================================================
    # PUBLIC RUN
    # =================================================================

    def run(self, resume_text: str) -> EnterpriseResumePipelineResult:
        result = EnterpriseResumePipelineResult(resume_text=resume_text or "")

        if not isinstance(resume_text, str):
            return self._fail(result, "input_validation", TypeError("resume_text must be a string."))

        resume_text = resume_text.strip()
        if not resume_text:
            return self._fail(result, "input_validation", ValueError("resume_text cannot be empty."))

        result.resume_text = resume_text

        try:
            self._debug("\n[STAGE 1] Section detection")
            self._stage_section_detection(result)

            self._debug("\n[STAGE 2] Knowledge document")
            self._stage_knowledge_document(result)

            self._debug("\n[STAGE 3] Knowledge V5 extraction")
            self._stage_semantic_extraction(result)

            self._debug("\n[STAGE 4] Semantic resolution")
            self._stage_semantic_resolution(result)  # FIXED: Properly extracts relations/dependencies

            self._debug("\n[STAGE 5] Business statements")
            self._stage_business_statements(result)

            self._debug("\n[STAGE 6] Knowledge graph")
            self._stage_knowledge_graph(result)

            self._debug("\n[STAGE 7] Graph profile")
            self._stage_knowledge_profile(result)  # FIXED: Passes all data to profile builder

            result.confidence = self._calculate_confidence(result)
            result.success = True
            result.failed_stage = ""
            result.error = None

            return result

        except Exception as exc:
            stage = self._infer_failed_stage(result)
            return self._fail(result, stage, exc)

    # =================================================================
    # STAGE 1: SECTION DETECTION
    # =================================================================

    def _stage_section_detection(self, result):
        detector = self.section_detector
        if detector is None:
            result.sections = {}
            result.section_metadata = {}
            result.stages["section_detection"] = True
            return

        if hasattr(detector, "detect"):
            output = detector.detect(result.resume_text)
        elif callable(detector):
            output = detector(result.resume_text)
        else:
            raise TypeError("SectionDetector must expose detect() or be callable.")

        result.sections = output
        result.section_metadata = self._extract_section_metadata(output)
        result.stages["section_detection"] = True

    # =================================================================
    # STAGE 2: KNOWLEDGE DOCUMENT
    # =================================================================

    def _stage_knowledge_document(self, result):
        document = KnowledgeDocument()
        texts = self._split_resume_text(result.resume_text)

        for text in texts:
            sentence = KnowledgeSentence(original_text=text, facts=[], confidence=1.0)
            fact = KnowledgeFact(
                text=text,
                achievement=False,
                quantified=False,
                source="resume",
                confidence=1.0,
            )
            fact.interpretation = KnowledgeInterpretation()
            sentence.facts.append(fact)
            document.sentences.append(sentence)
            document.facts.append(fact)

        document.statistics = {
            "sentence_count": len(document.sentences),
            "fact_count": len(document.facts),
            "raw_text": bool(result.resume_text),
        }
        document.confidence = 1.0 if document.facts else 0.0

        result.knowledge_document = document
        result.stages["knowledge_document"] = True
        result.statistics["knowledge_facts"] = len(document.facts)

    # =================================================================
    # STAGE 3: KNOWLEDGE V5 EXTRACTION
    # =================================================================

    def _stage_semantic_extraction(self, result):
        document = result.knowledge_document
        if document is None:
            raise ValueError("KnowledgeDocument is missing.")

        coordinator = self.extraction_coordinator
        if coordinator is None:
            raise ImportError("ExtractionCoordinator could not be created.")

        result.extraction_results = []
        result.extracted_entities = []
        result.entities_by_ontology = {ontology: [] for ontology in self.ontologies}

        for sentence_index, sentence in enumerate(document.sentences):
            for fact_index, fact in enumerate(sentence.facts):
                text = (getattr(fact, "text", "") or "").strip()
                if not text:
                    continue

                self._debug(f"\n  FACT {sentence_index}:{fact_index}")
                self._debug(f"  TEXT: {text}")

                extraction = coordinator.run(text)
                result.extraction_results.append(extraction)

                entities = self._convert_extraction_result(extraction, fact, sentence)
                self._debug(f"  ENTITIES: {len(entities)}")

                self._attach_entities_to_fact(fact, entities)

                for entity in entities:
                    result.extracted_entities.append(entity)
                    result.entities_by_ontology.setdefault(entity.ontology, []).append(entity)

                self._populate_fact_metadata(fact)

        result.extracted_entities = self._unique_objects(result.extracted_entities)
        for ontology in result.entities_by_ontology:
            result.entities_by_ontology[ontology] = self._unique_objects(result.entities_by_ontology[ontology])

        result.statistics["extracted_entities"] = len(result.extracted_entities)
        result.statistics["extraction_calls"] = len(result.extraction_results)
        result.statistics["entities_by_ontology"] = {
            key: len(value) for key, value in result.entities_by_ontology.items()
        }

        result.stages["extraction"] = True

    # =================================================================
    # STAGE 4: SEMANTIC RESOLUTION
    # =================================================================

    def _stage_semantic_resolution(self, result):
        """Semantic resolution with proper relation/dependency extraction."""
        
        resolver = self.semantic_resolver
        if resolver is None:
            raise ImportError("SemanticResolver could not be created.")

        document = result.knowledge_document

        # Call resolver
        if hasattr(resolver, "resolve"):
            try:
                resolution = resolver.resolve(document)
            except TypeError:
                resolution = resolver.resolve(document.facts)
        elif hasattr(resolver, "process"):
            resolution = resolver.process(document)
        else:
            raise TypeError("SemanticResolver must expose resolve() or process().")

        # Store the full SemanticResolution
        result.semantic_resolution = resolution

        # Extract ALL data from resolution
        entities = []
        relations = []
        dependencies = []
        clusters = []
        interpretations = []

        if resolution is None:
            resolution = SemanticResolution()

        # Handle SemanticResolution object
        if isinstance(resolution, SemanticResolution):
            entities = list(resolution.entities) if resolution.entities else []
            self._debug(f"  Entities from resolution: {len(entities)}")
            
            relations = list(resolution.relations) if resolution.relations else []
            self._debug(f"  Relations from resolution: {len(relations)}")
            
            dependencies = list(resolution.dependencies) if resolution.dependencies else []
            self._debug(f"  Dependencies from resolution: {len(dependencies)}")
            
            clusters = list(resolution.clusters) if resolution.clusters else []
            self._debug(f"  Clusters from resolution: {len(clusters)}")
            
            for fact in document.facts:
                interp = getattr(fact, "interpretation", None)
                if interp:
                    interpretations.append(interp)
        
        # Handle dict response
        elif isinstance(resolution, dict):
            entities = resolution.get("entities", [])
            relations = resolution.get("relations", [])
            dependencies = resolution.get("dependencies", [])
            clusters = resolution.get("clusters", [])
            interpretations = resolution.get("interpretations", resolution.get("results", []))
            
            self._debug(f"  Entities from dict: {len(entities)}")
            self._debug(f"  Relations from dict: {len(relations)}")
            self._debug(f"  Dependencies from dict: {len(dependencies)}")
            self._debug(f"  Clusters from dict: {len(clusters)}")
        
        # Handle list/tuple response
        elif isinstance(resolution, (list, tuple)):
            interpretations = list(resolution)
        
        # Handle single object
        else:
            interpretations = [resolution]

        # Attach interpretations to facts
        self._attach_interpretations(document, interpretations)

        # Collect embedded entities from facts
        embedded = self._collect_fact_entities(document)
        entities.extend(embedded)
        entities.extend(result.extracted_entities)

        # Store ALL extracted data in result
        result.interpretations = self._unique_objects(interpretations)
        result.semantic_entities = self._unique_objects(entities)
        result.semantic_relations = self._unique_objects(relations)
        result.semantic_dependencies = self._unique_objects(dependencies)
        result.semantic_clusters = self._unique_objects(clusters)

        # Update statistics
        result.statistics["semantic_entities"] = len(result.semantic_entities)
        result.statistics["semantic_relations"] = len(result.semantic_relations)
        result.statistics["semantic_dependencies"] = len(result.semantic_dependencies)
        result.statistics["semantic_clusters"] = len(result.semantic_clusters)
        result.statistics["interpretations"] = len(result.interpretations)

        self._debug(f"  Final - Entities: {len(result.semantic_entities)}")
        self._debug(f"  Final - Relations: {len(result.semantic_relations)}")
        self._debug(f"  Final - Dependencies: {len(result.semantic_dependencies)}")
        self._debug(f"  Final - Clusters: {len(result.semantic_clusters)}")

        result.stages["semantic_resolution"] = True

    # =================================================================
    # STAGE 5: BUSINESS STATEMENTS
    # =================================================================

    def _stage_business_statements(self, result):
        """Build business statements using SemanticResolution with clusters."""
        
        builder = self.business_statement_builder
        if builder is None:
            raise ImportError("BusinessStatementBuilder could not be created.")

        resolution = result.semantic_resolution
        
        if resolution is None:
            self._debug("WARNING: No SemanticResolution found - trying fallback")
            output = self._build_statements_from_interpretations(result.interpretations)
        else:
            self._debug(f"Using SemanticResolution with: {len(resolution.entities)} entities, {len(resolution.clusters)} clusters")
            
            if hasattr(builder, "build"):
                try:
                    output = builder.build(resolution)
                except TypeError as e:
                    self._debug(f"build() failed with resolution: {e}")
                    output = builder.build(
                        semantic_resolution=resolution,
                        entities=resolution.entities,
                        dependencies=resolution.dependencies,
                        clusters=resolution.clusters,
                    )
            else:
                raise TypeError("BusinessStatementBuilder must expose build().")

        if output is None:
            output = []

        if isinstance(output, dict):
            output = list(output.values())
        elif not isinstance(output, (list, tuple)):
            output = [output]

        result.business_statements = list(output)
        result.statistics["business_statements"] = len(result.business_statements)

        self._debug(f"Generated {len(result.business_statements)} business statements")
        
        for i, stmt in enumerate(result.business_statements[:5], 1):
            text = getattr(stmt, "text", None) or getattr(stmt, "canonical", str(stmt))
            self._debug(f"  {i}. {text[:100]}")

        result.stages["business_statement_builder"] = True

    def _build_statements_from_interpretations(self, interpretations):
        """Fallback: Build statements from interpretations."""
        statements = []
        for interp in interpretations:
            if interp is None:
                continue
            
            action = getattr(interp, "action", None)
            target = getattr(interp, "target", None)
            
            if action and target:
                action_name = getattr(action, "canonical", str(action))
                target_name = getattr(target, "canonical", str(target))
                text = f"{action_name} {target_name}"
                
                statement = BusinessStatement(
                    statement_id=f"BS-{hash(text)}",
                    canonical=text,
                    text=text,
                    normalized=text.lower(),
                    fact_id="",
                    sentence_index=-1,
                    source_text=text,
                    source="resume",
                    action=action,
                    target=target,
                    domain=getattr(interp, "domain", None),
                    metric=getattr(interp, "metric", None),
                    entities=[action, target],
                    relations=[],
                    dependencies=[],
                    achievement=True,
                    quantified=False,
                    impact="",
                    business_value="",
                    category="achievement",
                    business_area="",
                    confidence=0.5,
                    impact_weight=1.0,
                    metadata={}
                )
                statements.append(statement)
        
        return statements

    # =================================================================
    # STAGE 6: KNOWLEDGE GRAPH
    # =================================================================

    def _stage_knowledge_graph(self, result):
        builder = self.knowledge_graph_builder
        if builder is None:
            raise ImportError("KnowledgeGraphBuilder could not be created.")

        statements = result.business_statements
        resolution = result.semantic_resolution

        if hasattr(builder, "build"):
            try:
                output = builder.build(statements, resolution=resolution)
            except TypeError:
                try:
                    output = builder.build(statements)
                except TypeError:
                    output = builder.build(statements=statements, resolution=resolution)
        elif hasattr(builder, "build_graph"):
            output = builder.build_graph(statements)
        else:
            raise TypeError("KnowledgeGraphBuilder must expose build() or build_graph().")

        if output is None:
            raise ValueError("KnowledgeGraphBuilder returned None.")

        result.knowledge_graph = output
        nodes = self._graph_nodes(output)
        edges = self._graph_edges(output)

        result.statistics["graph_nodes"] = len(nodes)
        result.statistics["graph_edges"] = len(edges)
        result.stages["knowledge_graph"] = True

    # =================================================================
    # STAGE 7: KNOWLEDGE PROFILE - FIXED
    # =================================================================

    def _stage_knowledge_profile(self, result):
        builder = self.knowledge_profile_builder
        if builder is None:
            raise ImportError("KnowledgeProfileBuilder could not be created.")

        graph = result.knowledge_graph
        if graph is None:
            raise ValueError("KnowledgeGraph is missing.")

        # Get business statements and semantic entities for the profile
        business_statements = result.business_statements
        semantic_entities = result.semantic_entities
        semantic_relations = result.semantic_relations
        semantic_dependencies = result.semantic_dependencies
        semantic_clusters = result.semantic_clusters
        
        # Get the full resolution as well
        resolution = result.semantic_resolution

        self._debug(f"Building KnowledgeProfile with:")
        self._debug(f"  graph: {graph is not None}")
        self._debug(f"  business_statements: {len(business_statements) if business_statements else 0}")
        self._debug(f"  semantic_entities: {len(semantic_entities) if semantic_entities else 0}")
        self._debug(f"  semantic_relations: {len(semantic_relations) if semantic_relations else 0}")
        self._debug(f"  semantic_dependencies: {len(semantic_dependencies) if semantic_dependencies else 0}")
        self._debug(f"  semantic_clusters: {len(semantic_clusters) if semantic_clusters else 0}")

        # Build profile with all data
        if hasattr(builder, "build"):
            try:
                # Try passing graph with all data
                output = builder.build(
                    knowledge_graph=graph,
                    business_statements=business_statements,
                    semantic_entities=semantic_entities,
                    extracted_entities=result.extracted_entities,
                    result=result,
                )
            except TypeError as e:
                self._debug(f"build() failed with extended params: {e}")
                # Fallback: try original signature
                try:
                    output = builder.build(graph, resolution=resolution)
                except TypeError:
                    output = builder.build(graph)
        elif callable(builder):
            output = builder(graph)
        else:
            raise TypeError("KnowledgeProfileBuilder must expose build() or be callable.")

        if output is None:
            raise ValueError("KnowledgeProfileBuilder returned None.")

        result.knowledge_profile = output
        result.stages["knowledge_profile"] = True
        self._debug(f"KnowledgeProfile built successfully with confidence: {getattr(output, 'confidence', 0)}")

    # =================================================================
    # HELPER METHODS
    # =================================================================

    @staticmethod
    def _convert_extraction_result(extraction, fact, sentence):
        entities = []
        raw_entities = getattr(extraction, "all_entities", None)
        if raw_entities is None:
            raw_entities = []
            for ontology in DEFAULT_ONTOLOGIES:
                raw_entities.extend(getattr(extraction, ontology, []) or [])

        for raw in raw_entities:
            entity = EnterpriseExtractedEntity(
                entity_id=str(getattr(raw, "entity_id", "") or ""),
                canonical=str(getattr(raw, "canonical", "") or ""),
                phrase=str(getattr(raw, "phrase", "") or ""),
                confidence=float(getattr(raw, "confidence", 0.0) or 0.0),
                ontology=str(getattr(raw, "ontology", "") or ""),
                entity_type=str(getattr(raw, "entity_type", "") or ""),
                category=str(getattr(raw, "category", "") or ""),
                business_area=str(getattr(raw, "business_area", "") or ""),
                domain=str(getattr(raw, "domain", "") or ""),
                impact_weight=float(getattr(raw, "impact_weight", 1.0) or 1.0),
                matched_alias=str(getattr(raw, "matched_alias", "") or ""),
                is_alias=bool(getattr(raw, "is_alias", False)),
                token_index=int(getattr(raw, "token_index", 0) or 0),
                token_count=int(getattr(raw, "token_count", 0) or 0),
                start_char=int(getattr(raw, "start_char", 0) or 0),
                end_char=int(getattr(raw, "end_char", 0) or 0),
                metadata=dict(getattr(raw, "metadata", {}) or {}),
                source_fact=fact,
                source_sentence=sentence,
                raw_match=raw,
            )
            if entity.entity_id:
                entities.append(entity)
        return entities

    @staticmethod
    def _attach_entities_to_fact(fact, entities):
        interpretation = getattr(fact, "interpretation", None)
        if interpretation is None:
            interpretation = KnowledgeInterpretation()
            fact.interpretation = interpretation

        try:
            existing = getattr(interpretation, "entities", None)
            if existing is None:
                interpretation.entities = []
            interpretation.entities.extend(entities)
        except Exception:
            pass

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
            grouped.setdefault(entity.ontology, []).append(entity)

        for ontology, attribute in field_mapping.items():
            values = grouped.get(ontology, [])
            if not values:
                continue
            strongest = max(values, key=lambda x: x.confidence)
            try:
                setattr(interpretation, attribute, strongest)
            except Exception:
                pass

    @staticmethod
    def _populate_fact_metadata(fact):
        text = (getattr(fact, "text", "") or "").casefold()
        achievement_terms = (
            "increased", "improved", "reduced", "decreased", "achieved",
            "delivered", "saved", "grew", "generated", "implemented",
            "certified", "certification", "successfully", "reached",
            "raised", "lowered", "spearheaded", "led", "oversaw",
            "strengthened", "enhanced", "drove"
        )
        achievement = any(term in text for term in achievement_terms)
        fact.achievement = achievement

        interpretation = getattr(fact, "interpretation", None)
        if interpretation is not None:
            try:
                interpretation.achievement = achievement
            except Exception:
                pass

        quantified = bool(re.search(
            r"\d+(?:\.\d+)?%?|\$\s*\d+|\d+\s*(?:million|billion|k|m|kg|g|l|ml)",
            getattr(fact, "text", "") or "",
            re.IGNORECASE,
        ))
        fact.quantified = quantified

        if interpretation is not None:
            try:
                interpretation.quantified = quantified
            except Exception:
                pass

    @staticmethod
    def _attach_interpretations(document, interpretations):
        if not document.facts or not interpretations:
            return

        for index, item in enumerate(interpretations):
            interpretation = None
            if isinstance(item, KnowledgeInterpretation):
                interpretation = item
            elif isinstance(item, dict):
                interpretation = item.get("interpretation")
            else:
                interpretation = getattr(item, "interpretation", None)

            if interpretation is None:
                continue

            fact_index = None
            if isinstance(item, dict):
                fact_index = item.get("fact_index")
            else:
                fact_index = getattr(item, "fact_index", None)

            if fact_index is not None:
                try:
                    fact = document.facts[int(fact_index)]
                except (ValueError, IndexError, TypeError):
                    continue
            else:
                if index >= len(document.facts):
                    continue
                fact = document.facts[index]

            fact.interpretation = interpretation

    @staticmethod
    def _collect_fact_entities(document):
        entities = []
        for fact in document.facts:
            interpretation = getattr(fact, "interpretation", None)
            if interpretation is None:
                continue

            embedded = getattr(interpretation, "entities", None)
            if isinstance(embedded, (list, tuple)):
                entities.extend(embedded)

            for attribute in ("skill", "action", "target", "domain", "metric", "measurement", "practice", "standard"):
                value = getattr(interpretation, attribute, None)
                if value is not None:
                    found = getattr(value, "found", True)
                    if found:
                        entities.append(value)

            modifiers = getattr(interpretation, "modifiers", [])
            if isinstance(modifiers, (list, tuple)):
                entities.extend(modifiers)

        return entities

    @staticmethod
    def _split_resume_text(text):
        if not text:
            return []

        output = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            while line.startswith(("- ", "* ", "• ", "▪ ", "● ")):
                line = line[2:].strip()
            if not line:
                continue

            parts = EnterpriseResumePipeline._split_sentences(line)
            if parts:
                output.extend(parts)
            else:
                output.append(line)

        return output

    @staticmethod
    def _split_sentences(text):
        if not text:
            return []
        text = " ".join(str(text).split())
        if not text:
            return []
        parts = re.split(r"(?<=[.!?])\s+", text)
        return [part.strip() for part in parts if part.strip()]

    @staticmethod
    def _extract_section_metadata(sections):
        if sections is None:
            return {}
        metadata = getattr(sections, "metadata", None)
        if isinstance(metadata, dict):
            return metadata
        if isinstance(sections, dict):
            metadata = sections.get("metadata")
            if isinstance(metadata, dict):
                return metadata
        return {}

    @staticmethod
    def _unique_objects(objects):
        if not objects:
            return []
        result = []
        seen = set()
        for obj in objects:
            if obj is None:
                continue
            key = EnterpriseResumePipeline._unique_object_key(obj)
            if key in seen:
                continue
            seen.add(key)
            result.append(obj)
        return result

    @staticmethod
    def _unique_object_key(obj):
        if isinstance(obj, (str, int, float, bool)):
            return (type(obj).__name__, str(obj).strip().casefold())

        entity_id = getattr(obj, "entity_id", None)
        if entity_id:
            return ("entity", str(getattr(obj, "ontology", "")).casefold(), str(entity_id).casefold())

        relation_id = getattr(obj, "relation_id", None)
        if relation_id:
            return ("relation", str(relation_id).casefold())

        dependency_id = getattr(obj, "dependency_id", None)
        if dependency_id:
            return ("dependency", str(dependency_id).casefold())

        cluster_id = getattr(obj, "cluster_id", None)
        if cluster_id:
            return ("cluster", str(cluster_id).casefold())

        canonical = getattr(obj, "canonical", None)
        if canonical:
            return ("canonical", type(obj).__name__, str(canonical).strip().casefold())

        try:
            return ("object", type(obj).__name__, repr(obj))
        except Exception:
            return ("object", type(obj).__name__, id(obj))

    @staticmethod
    def _graph_nodes(graph):
        if graph is None:
            return []
        getter = getattr(graph, "get_nodes", None)
        if callable(getter):
            try:
                nodes = getter()
            except Exception:
                nodes = []
        else:
            nodes = getattr(graph, "nodes", [])
        if nodes is None:
            return []
        if isinstance(nodes, dict):
            return list(nodes.values())
        try:
            return list(nodes)
        except TypeError:
            return []

    @staticmethod
    def _graph_edges(graph):
        if graph is None:
            return []
        getter = getattr(graph, "get_edges", None)
        if callable(getter):
            try:
                edges = getter()
            except Exception:
                edges = []
        else:
            edges = getattr(graph, "edges", [])
        if edges is None:
            return []
        if isinstance(edges, dict):
            return list(edges.values())
        try:
            return list(edges)
        except TypeError:
            return []

    @staticmethod
    def _calculate_confidence(result):
        values = []

        document = result.knowledge_document
        if document is not None:
            value = getattr(document, "confidence", None)
            if value is not None:
                try:
                    values.append(float(value))
                except (TypeError, ValueError):
                    pass

        for entity in result.extracted_entities or []:
            try:
                values.append(float(getattr(entity, "confidence", 0.0)))
            except (TypeError, ValueError):
                pass

        for entity in result.semantic_entities or []:
            try:
                values.append(float(getattr(entity, "confidence", 1.0)))
            except (TypeError, ValueError):
                pass

        for statement in result.business_statements or []:
            try:
                values.append(float(getattr(statement, "confidence", 1.0)))
            except (TypeError, ValueError):
                pass

        profile = result.knowledge_profile
        if profile is not None:
            try:
                values.append(float(getattr(profile, "confidence", 1.0)))
            except (TypeError, ValueError):
                pass

        if not values:
            return 0.0

        values = [max(0.0, min(1.0, value)) for value in values]
        return round(sum(values) / len(values), 2)

    @staticmethod
    def _fail(result, stage, exc):
        result.success = False
        result.failed_stage = stage
        result.error = f"{type(exc).__name__}: {str(exc)}"
        result.stages[stage] = False
        return result

    @staticmethod
    def _infer_failed_stage(result):
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
            if not result.stages.get(stage, False):
                return stage
        return "unknown"


# =====================================================================
# CONVENIENCE API
# =====================================================================

def run_enterprise_resume_pipeline(resume_text, **kwargs):
    pipeline = EnterpriseResumePipeline(**kwargs)
    return pipeline.run(resume_text)


# =====================================================================
# EXPORTS
# =====================================================================

__all__ = [
    "EnterpriseResumePipeline",
    "EnterpriseResumePipelineResult",
    "EnterpriseExtractedEntity",
    "run_enterprise_resume_pipeline",
]