"""
Sentence Parser

Universal Knowledge Parser

Parses ONE semantic clause and produces a fully interpreted
KnowledgeSentence.

Pipeline

Sentence
    ↓
Extractors
    ↓
Reasoners
    ↓
Practice Recognizer
    ↓
Entity Matcher
    ↓
Dependency Parser
    ↓
Knowledge Interpretation
    ↓
Knowledge Fact
    ↓
Knowledge Sentence
"""

from app.intelligence.utilities.knowledge.knowledge_parser.parser_utils import (
    ParserUtils,
)

# ------------------------------------------------------------
# Knowledge Models
# ------------------------------------------------------------

from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeFact,
    KnowledgeSentence,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)

# ------------------------------------------------------------
# Extractors
# ------------------------------------------------------------

from app.intelligence.utilities.knowledge.knowledge_extractors.action_extractor import (
    ActionExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.object_extractor import (
    ObjectExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.metric_extractor import (
    MetricExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.measurement_extractor import (
    MeasurementExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.modifier_extractor import (
    ModifierExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.practice_recognizer import (
    PracticeRecognizer,
)

# ------------------------------------------------------------
# Reasoners
# ------------------------------------------------------------

from app.intelligence.utilities.knowledge.knowledge_reasoners.domain_reasoner import (
    DomainReasoner,
)

from app.intelligence.utilities.knowledge.knowledge_reasoners.metric_reasoner.metric_reasoner import (
    MetricReasoner,
)

from app.intelligence.utilities.knowledge.knowledge_reasoners.measurement_reasoners.measurement_reasoner import (
    MeasurementReasoner,
)

# ------------------------------------------------------------
# Entity Matching
# ------------------------------------------------------------

from app.intelligence.utilities.knowledge.entity_matching.entity_matcher import (
    EntityMatcher,
)

# ------------------------------------------------------------
# Dependency Parser
# ------------------------------------------------------------

from app.intelligence.utilities.knowledge.knowledge_dependency.dependency_parser import (
    DependencyParser,
)

# ------------------------------------------------------------
# Parser
# ------------------------------------------------------------


class SentenceParser:

    """
    Universal Knowledge Sentence Parser

    Parses ONE semantic clause.

    KnowledgePipeline is responsible for splitting

        Document
            ↓
        Sentence
            ↓
        Clause

    SentenceParser parses ONE clause.
    """

    def __init__(self):

        # ----------------------------------------------------
        # Extractors
        # ----------------------------------------------------

        self.action_extractor = ActionExtractor()

        self.object_extractor = ObjectExtractor()

        self.metric_extractor = MetricExtractor()

        self.measurement_extractor = MeasurementExtractor()

        self.modifier_extractor = ModifierExtractor()

        self.practice_recognizer = PracticeRecognizer()

        # ----------------------------------------------------
        # Reasoners
        # ----------------------------------------------------

        self.domain_reasoner = DomainReasoner()

        self.metric_reasoner = MetricReasoner()

        self.measurement_reasoner = MeasurementReasoner()

        # ----------------------------------------------------
        # Ontology Components
        # ----------------------------------------------------

        self.entity_matcher = EntityMatcher()

        self.dependency_parser = DependencyParser()

        # ----------------------------------------------------
        # Utilities
        # ----------------------------------------------------

        self.utils = ParserUtils()

    # ========================================================
    # Helper Methods
    # ========================================================

    def _extract_action(self, text):

        return self.action_extractor.extract(text)

    # --------------------------------------------------------

    def _extract_object(self, text):

        return self.object_extractor.extract(text)

    # --------------------------------------------------------

    def _extract_metric(self, text):

        return self.metric_extractor.extract(text)

    # --------------------------------------------------------

    def _extract_measurement(
        self,
        text,
        metric,
    ):

        return self.measurement_extractor.extract(
            text,
            metric,
        )

    # --------------------------------------------------------

    def _extract_modifiers(self, text):

        return self.modifier_extractor.extract(text)

    # --------------------------------------------------------

    def _extract_practice(self, text):

        return self.practice_recognizer.recognize(text)

    # --------------------------------------------------------

    def _match_entities(self, text):

        """
        Central ontology lookup.

        Returns

            list[KnowledgeEntity]
        """

        return self.entity_matcher.match(text)

    # --------------------------------------------------------

    def _build_dependencies(
        self,
        entities,
        sentence,
    ):

        """
        Build dependency graph.

        Returns

            list[DependencyEdge]
        """

        return self.dependency_parser.build(

            entities,

            sentence,

        )
        # ========================================================
    # Main Parser
    # ========================================================

    def parse(self, text: str) -> KnowledgeSentence:

        """
        Parse ONE semantic clause.

        Returns

            KnowledgeSentence
        """

        # --------------------------------------------------
        # Extraction
        # --------------------------------------------------

        action = self._extract_action(text)

        obj = self._extract_object(text)

        domain = self.domain_reasoner.reason(
            action,
            obj,
        )

        metric = self._extract_metric(text)

        metric = self.metric_reasoner.reason(

            text,

            metric,

            action,

            obj,

        )

        measurement = self._extract_measurement(

            text,

            metric,

        )

        measurement = self.measurement_reasoner.reason(

            action,

            measurement,

        )

        modifiers = self._extract_modifiers(text)

        practice = self._extract_practice(text)

        # --------------------------------------------------
        # Ontology Entity Matching
        # --------------------------------------------------

        entities = self._match_entities(text)

        # --------------------------------------------------
        # Dependency Graph
        # --------------------------------------------------

        dependencies = self._build_dependencies(

            entities,

            text,

        )

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        confidence = self.utils.calculate_confidence(

            action,

            obj,

            domain,

            metric,

            measurement,

            modifiers,

        )

        # --------------------------------------------------
        # Interpretation
        # --------------------------------------------------

        interpretation = KnowledgeInterpretation(

            action=action,

            object=obj,

            domain=domain,

            metric=metric,

            measurement=measurement,

            modifiers=modifiers,

            practice=practice,

            entities=entities,

            dependencies=dependencies,

            achievement=self.utils.is_achievement(

                action,

                measurement,

            ),

            quantified=measurement.found,

            semantic_type=self.utils.semantic_type(

                domain,

            ),

            business_area=self.utils.business_area(

                domain,

            ),

            confidence=confidence,

        )

        # --------------------------------------------------
        # Overall Impact Weight
        # --------------------------------------------------

        impact = 0.0

        count = 0

        for entity in entities:

            metadata = entity.metadata or {}

            if "impact_weight" in metadata:

                try:

                    impact += float(

                        metadata["impact_weight"]

                    )

                    count += 1

                except Exception:

                    pass

        if count > 0:

            interpretation.overall_impact_weight = (

                impact / count

            )

        else:

            interpretation.overall_impact_weight = 1.0

        # --------------------------------------------------
        # Explanation
        # --------------------------------------------------

        explanation_parts = []

        if action.found:

            explanation_parts.append(

                f"Action={action.base}"

            )

        if obj.found:

            explanation_parts.append(

                f"Object={obj.canonical}"

            )

        if domain.found:

            explanation_parts.append(

                f"Domain={domain.domain}"

            )

        if metric.found:

            explanation_parts.append(

                f"Metric={metric.canonical}"

            )

        if measurement.found:

            explanation_parts.append(

                f"Measurement={measurement.value}"

            )

        if practice.found:

            explanation_parts.append(

                f"Practice={practice.canonical}"

            )

        interpretation.explanation = " | ".join(

            explanation_parts

        )
                # --------------------------------------------------
        # Knowledge Fact
        # --------------------------------------------------

        fact = KnowledgeFact(

            text=text,

            interpretation=interpretation,

            achievement=interpretation.achievement,

            quantified=interpretation.quantified,

            confidence=interpretation.confidence,

            source="resume",

        )

        # --------------------------------------------------
        # Sentence
        # --------------------------------------------------

        sentence = KnowledgeSentence(

            original_text=text,

            facts=[fact],

            confidence=fact.confidence,

        )

        return sentence