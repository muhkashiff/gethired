"""
Enterprise Entity Extractor

Enterprise V12

Pipeline

Resume Section
        ↓
Sentence Splitter
        ↓
Ontology Matcher
        ↓
Extraction Results
"""

from .sentence_splitter import SentenceSplitter
from .ontology_matcher import OntologyMatcher
from .extraction_models import ExtractionResult


class EntityExtractor:

    ####################################################################
    # INITIALIZE
    ####################################################################

    def __init__(

        self,

        ontology_repository,

    ):

        self.splitter = SentenceSplitter()

        self.matcher = OntologyMatcher(

            ontology_repository

        )

    ####################################################################
    # PUBLIC
    ####################################################################

    def extract(

        self,

        section_name,

        paragraphs,

    ):

        """
        Parameters
        ----------
        section_name : str

        paragraphs : list[str]

        Returns
        -------
        list[ExtractionResult]
        """

        results = []

        # ---------------------------------------------------------
        # Split section into business sentences
        # ---------------------------------------------------------

        sentences = self.splitter.split(

            section_name,

            paragraphs,

        )

        # ---------------------------------------------------------
        # Match ontology entities
        # ---------------------------------------------------------

        for sentence in sentences:

            entities = self.matcher.match(

                sentence

            )

            confidence = self._confidence(

                entities

            )

            results.append(

                ExtractionResult(

                    sentence=sentence,

                    entities=entities,

                    confidence=confidence,

                )

            )

        return results

    ####################################################################
    # PRIVATE
    ####################################################################

    def _confidence(

        self,

        entities,

    ):

        if not entities:

            return 0.0

        return round(

            sum(

                entity.confidence

                for entity in entities

            )

            / len(entities),

            2,

        )