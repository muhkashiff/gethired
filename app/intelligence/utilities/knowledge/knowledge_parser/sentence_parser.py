"""
Sentence Parser

Converts one resume sentence into a fully
interpreted KnowledgeSentence.

This is the core semantic parser used
throughout the GetHired Intelligence Engine.

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

from app.intelligence.utilities.knowledge.knowledge_reasoners.measurement_reasoner import (
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

    def parse(self, sentence: str):

        """
        Parse a single resume sentence.
        """

        # ------------------------------------------------------
        # Extraction
        # ------------------------------------------------------

        action = self.action_extractor.extract(sentence)

        obj = self.object_extractor.extract(sentence)

        domain = self.domain_reasoner.reason(
            action,
            obj
        )

        metric = self.metric_extractor.extract(sentence)

        measurement = self.measurement_extractor.extract(
            sentence,
            metric
        )

        measurement = self.measurement_reasoner.reason(
            action,
            measurement
        )

        modifiers = self.modifier_extractor.extract(sentence)

        # ------------------------------------------------------
        # Interpretation
        # ------------------------------------------------------

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

                modifiers

            )

        )

        # ------------------------------------------------------
        # Knowledge Fact
        # ------------------------------------------------------

        fact = KnowledgeFact(

            text=sentence,

            interpretation=interpretation,

            achievement=interpretation.achievement,

            quantified=interpretation.quantified,

            confidence=interpretation.confidence,

            source="resume"

        )

        # ------------------------------------------------------
        # Sentence
        # ------------------------------------------------------

        return KnowledgeSentence(

            original_text=sentence,

            facts=[fact],

            confidence=fact.confidence

        )

    