"""
Sentence Parser

Converts a single semantic clause into a KnowledgeSentence.

NOTE:
This parser parses ONE semantic clause.

KnowledgePipeline is responsible for creating:
Document
    -> Sentence
        -> Clause

SentenceParser only returns a temporary KnowledgeSentence
containing the extracted KnowledgeFacts.
"""

from app.intelligence.utilities.knowledge.knowledge_parser.parser_utils import (
    ParserUtils,
)

from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeFact,
    KnowledgeSentence,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)

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

from app.intelligence.utilities.knowledge.knowledge_reasoners.domain_reasoner import (
    DomainReasoner,
)

from app.intelligence.utilities.knowledge.knowledge_reasoners.measurement_reasoners.measurement_reasoner import (
    MeasurementReasoner,
)


class SentenceParser:

    def __init__(self):

        self.action_extractor = ActionExtractor()

        self.object_extractor = ObjectExtractor()

        self.metric_extractor = MetricExtractor()

        self.measurement_extractor = MeasurementExtractor()

        self.modifier_extractor = ModifierExtractor()

        self.domain_reasoner = DomainReasoner()

        self.measurement_reasoner = MeasurementReasoner()

        self.utils = ParserUtils()

    # ----------------------------------------------------------

    def parse(self, text: str) -> KnowledgeSentence:
        """
        Parse ONE semantic clause.

        Returns a temporary KnowledgeSentence containing
        the extracted KnowledgeFact(s).

        KnowledgePipeline later inserts these facts
        into KnowledgeClause objects.
        """

        # --------------------------------------------------
        # Extraction
        # --------------------------------------------------

        action = self.action_extractor.extract(text)

        obj = self.object_extractor.extract(text)

        domain = self.domain_reasoner.reason(
            action,
            obj
        )

        metric = self.metric_extractor.extract(text)

        measurement = self.measurement_extractor.extract(
            text,
            metric
        )

        measurement = self.measurement_reasoner.reason(
            action,
            measurement
        )

        modifiers = self.modifier_extractor.extract(text)

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

            achievement=self.utils.is_achievement(
                action,
                measurement
            ),

            quantified=measurement.found,

            semantic_type=self.utils.semantic_type(
                domain
            ),

            business_area=self.utils.business_area(
                domain
            ),

            confidence=self.utils.calculate_confidence(

                action,

                obj,

                domain,

                metric,

                measurement,

                modifiers,

            ),

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
        # Temporary Sentence
        # --------------------------------------------------

        sentence = KnowledgeSentence(

            original_text=text,

            facts=[fact],

            confidence=fact.confidence,

        )

        return sentence