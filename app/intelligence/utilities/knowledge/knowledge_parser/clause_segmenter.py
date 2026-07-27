"""
Clause Segmenter

The ClauseSegmenter is the orchestration layer for clause processing.

Pipeline

Sentence
    ↓
ClauseParser
    ↓
ClauseRebuilder
    ↓
ClauseNormalizer
    ↓
Extractors
    ↓
Reasoners
    ↓
Rich Clause objects
"""

from copy import deepcopy

from app.intelligence.utilities.knowledge.knowledge_parser.clause_parser import ClauseParser
from app.intelligence.utilities.knowledge.knowledge_parser.clause_rebuilder import ClauseRebuilder
from app.intelligence.utilities.knowledge.knowledge_parser.clause_normalizer import ClauseNormalizer

from app.intelligence.utilities.knowledge.knowledge_extractors.action_extractor import ActionExtractor
from app.intelligence.utilities.knowledge.knowledge_extractors.object_extractor import ObjectExtractor
from app.intelligence.utilities.knowledge.knowledge_extractors.metric_extractor import MetricExtractor
from app.intelligence.utilities.knowledge.knowledge_extractors.measurement_extractor import MeasurementExtractor
from app.intelligence.utilities.knowledge.knowledge_extractors.modifier_extractor import ModifierExtractor

from app.intelligence.utilities.knowledge.knowledge_reasoners.domain_reasoner import DomainReasoner
from app.intelligence.utilities.knowledge.knowledge_reasoners.measurement_reasoners.measurement_reasoner import MeasurementReasoner

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)

from app.intelligence.utilities.knowledge.knowledge_parser.parser_utils import (
    ParserUtils,
)


class ClauseSegmenter:

    def __init__(self):

        self.parser = ClauseParser()

        self.rebuilder = ClauseRebuilder()

        self.normalizer = ClauseNormalizer()

        self.action_extractor = ActionExtractor()

        self.object_extractor = ObjectExtractor()

        self.metric_extractor = MetricExtractor()

        self.measurement_extractor = MeasurementExtractor()

        self.modifier_extractor = ModifierExtractor()

        self.domain_reasoner = DomainReasoner()

        self.measurement_reasoner = MeasurementReasoner()

        self.utils = ParserUtils()

    # ----------------------------------------------------------

    def segment(self, sentence):

        # -------------------------
        # Parse
        # -------------------------

        clauses = self.parser.parse(sentence)

        # -------------------------
        # Rebuild
        # -------------------------

        clauses = self.rebuilder.rebuild(clauses)

        # -------------------------
        # Normalize
        # -------------------------

        actions = self.action_extractor.extract_all(sentence)

        clauses = self.normalizer.normalize(
            clauses,
            actions,
        )

        # -------------------------
        # Enrich every clause
        # -------------------------

        enriched = []

        for clause in clauses:

            new_clause = deepcopy(clause)

            action = self.action_extractor.extract(new_clause.text)

            obj = self.object_extractor.extract(new_clause.text)

            domain = self.domain_reasoner.reason(
                action,
                obj,
            )

            metric = self.metric_extractor.extract(
                new_clause.text,
            )

            measurement = self.measurement_extractor.extract(
                new_clause.text,
                metric,
            )

            measurement = self.measurement_reasoner.reason(
                action,
                measurement,
            )

            modifiers = self.modifier_extractor.extract(
                new_clause.text,
            )

            interpretation = KnowledgeInterpretation(

                action=action,

                object=obj,

                domain=domain,

                metric=metric,

                measurement=measurement,

                modifiers=modifiers,

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

                confidence=self.utils.calculate_confidence(
                    action,
                    obj,
                    domain,
                    metric,
                    measurement,
                    modifiers,
                ),
            )

            new_clause.action = action

            new_clause.object = obj

            new_clause.domain = domain

            new_clause.metric = metric

            new_clause.measurement = measurement

            new_clause.modifiers = modifiers

            new_clause.interpretation = interpretation

            new_clause.achievement = interpretation.achievement

            new_clause.quantified = interpretation.quantified

            new_clause.semantic_type = interpretation.semantic_type

            new_clause.business_area = interpretation.business_area

            new_clause.confidence = interpretation.confidence

            enriched.append(new_clause)

        return enriched