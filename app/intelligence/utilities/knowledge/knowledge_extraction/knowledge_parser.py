"""
Enterprise Knowledge Parser

Enterprise V12

Pipeline

Resume Sections
        ↓
Sentence Splitter
        ↓
Entity Extractor
        ↓
Interpretation Builder
        ↓
Fact Builder
        ↓
Knowledge Document

Author : Enterprise V12
"""

from collections import defaultdict

from app.intelligence.utilities.knowledge.knowledge_models.knowledge_models import (
    KnowledgeDocument,
)

from app.intelligence.utilities.knowledge.knowledge_extraction.entity_extractor import (
    EntityExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extraction.interpretation_builder import (
    InterpretationBuilder,
)

from app.intelligence.utilities.knowledge.knowledge_extraction.fact_builder import (
    FactBuilder,
)


class KnowledgeParser:

    ####################################################################
    # INITIALIZE
    ####################################################################

    def __init__(

        self,

        ontology_repository,

    ):

        self.entity_extractor = EntityExtractor(

            ontology_repository

        )

        self.interpretation_builder = InterpretationBuilder()

        self.fact_builder = FactBuilder()

    ####################################################################
    # PUBLIC
    ####################################################################

    def parse(

        self,

        resume_sections,

    ):

        """
        Parameters
        ----------
        resume_sections

            Output of ResumeParser

            Expected format

            {
                "Experience":[...],
                "Education":[...],
                ...
            }

        Returns
        -------
        KnowledgeDocument
        """

        document = KnowledgeDocument()

        document.facts = []

        extraction_results = []

        # ---------------------------------------------------------
        # Process every resume section
        # ---------------------------------------------------------

        for section_name, paragraphs in resume_sections.items():

            if not paragraphs:
                continue

            section_results = self.entity_extractor.extract(

                section_name,

                paragraphs,

            )

            extraction_results.extend(

                section_results

            )

        # ---------------------------------------------------------
        # Build Interpretations
        # ---------------------------------------------------------

        interpretations = []

        for extraction in extraction_results:

            interpretations.append(

                self.interpretation_builder.build(

                    extraction

                )

            )

        # ---------------------------------------------------------
        # Build Facts
        # ---------------------------------------------------------

        facts = self.fact_builder.build_many(

            interpretations

        )

        document.facts = facts

        # ---------------------------------------------------------
        # Statistics
        # ---------------------------------------------------------

        document.statistics = self._build_statistics(

            facts

        )

        # ---------------------------------------------------------
        # Confidence
        # ---------------------------------------------------------

        document.confidence = self._calculate_confidence(

            facts

        )

        return document

    ####################################################################
    # PRIVATE
    ####################################################################

    def _build_statistics(

        self,

        facts,

    ):
        """
        Build enterprise statistics for downstream analytics.
        """

        stats = {}

        stats["total_facts"] = len(facts)

        stats["achievements"] = sum(

            1

            for fact in facts

            if fact.achievement

        )

        stats["quantified"] = sum(

            1

            for fact in facts

            if fact.quantified

        )

        # ---------------------------------------------------------
        # Entity Statistics
        # ---------------------------------------------------------

        entity_counter = defaultdict(int)

        category_counter = defaultdict(int)

        business_area_counter = defaultdict(int)

        for fact in facts:

            interpretation = fact.interpretation

            for entity in interpretation.entities:

                entity_counter[

                    entity.entity_type

                ] += 1

                if entity.category:

                    category_counter[

                        entity.category

                    ] += 1

                if entity.business_area:

                    business_area_counter[

                        entity.business_area

                    ] += 1

        stats["entity_types"] = dict(entity_counter)

        stats["categories"] = dict(category_counter)

        stats["business_areas"] = dict(business_area_counter)

        # ---------------------------------------------------------
        # Standards
        # ---------------------------------------------------------

        standards = []

        methodologies = []

        metrics = []

        actions = []

        technologies = []

        for fact in facts:

            for entity in fact.interpretation.entities:

                etype = entity.entity_type.lower()

                if etype == "standard":

                    standards.append(entity.canonical)

                elif etype == "methodology":

                    methodologies.append(entity.canonical)

                elif etype == "metric":

                    metrics.append(entity.canonical)

                elif etype == "action":

                    actions.append(entity.canonical)

                elif etype == "technology":

                    technologies.append(entity.canonical)

        stats["standards"] = sorted(set(standards))

        stats["methodologies"] = sorted(set(methodologies))

        stats["metrics"] = sorted(set(metrics))

        stats["actions"] = sorted(set(actions))

        stats["technologies"] = sorted(set(technologies))

        return stats

    ####################################################################
    # CONFIDENCE
    ####################################################################

    def _calculate_confidence(

        self,

        facts,

    ):
        """
        Aggregate confidence from all extracted facts.
        """

        if not facts:

            return 0.0

        scores = [

            fact.confidence

            for fact in facts

        ]

        return round(

            sum(scores)

            / len(scores),

            2,

        )

    ####################################################################
    # DEBUG
    ####################################################################

    def summary(

        self,

        document,

    ):
        """
        Simple debug helper.
        """

        print("=" * 70)
        print("KNOWLEDGE DOCUMENT")
        print("=" * 70)

        print(f"Facts        : {len(document.facts)}")
        print(f"Confidence   : {document.confidence}")

        print("\nStatistics")

        for key, value in document.statistics.items():

            print(f"{key:20} : {value}")

        print("\nFacts")

        for index, fact in enumerate(

            document.facts,

            start=1,

        ):

            print("-" * 60)

            print(f"Fact {index}")

            print(f"Text : {fact.text}")

            print(f"Confidence : {fact.confidence}")

            print("Entities")

            for entity in fact.interpretation.entities:

                print(
                    f"   {entity.entity_type:15}"
                    f"{entity.canonical}"
                )

        print("=" * 70)