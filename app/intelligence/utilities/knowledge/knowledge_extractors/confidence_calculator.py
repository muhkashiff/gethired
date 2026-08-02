"""
Enterprise Confidence Calculator

Calculates confidence for every extracted ontology entity.

Uses:

• confidence_rules.json
• ontology metadata
• repository
• alias matching
• context scoring

Version : Enterprise V3
"""

from __future__ import annotations

from app.intelligence.utilities.knowledge.repository.repository import Repository


class ConfidenceCalculator:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self, repository=None):

        self.repository = repository or Repository()

        self.rules = self.repository.get_confidence_rules()

        self.max_score = self.rules.get(
            "max_confidence",
            1.0
        )

    ####################################################################
    # PUBLIC
    ####################################################################

    def calculate(

        self,

        phrase,

        entity,

        sentence="",

        parser_context=None,

    ):

        score = 0.0

        score += self._ontology_score(
            phrase,
            entity
        )

        score += self._business_score(
            entity
        )

        score += self._context_score(
            sentence,
            entity
        )

        score += self._parser_score(
            parser_context
        )

        return round(

            min(score, self.max_score),

            3

        )

    ####################################################################
    # ONTOLOGY SCORE
    ####################################################################

    def _ontology_score(

        self,

        phrase,

        entity

    ):

        score = 0.0

        canonical = entity.canonical.lower()

        aliases = [

            a.lower()

            for a in entity.aliases

        ]

        if phrase.lower() == canonical:

            score += 0.45

        elif phrase.lower() in aliases:

            score += 0.35

        else:

            score += 0.20

        return score

    ####################################################################
    # BUSINESS IMPORTANCE
    ####################################################################

    def _business_score(

        self,

        entity

    ):

        score = 0.0

        score += (

            entity.impact_weight

            * 0.20

        )

        if entity.business_area:

            score += 0.05

        if entity.domain:

            score += 0.05

        return score
        ####################################################################
    # CONTEXT SCORE
    ####################################################################

    def _context_score(

        self,

        sentence,

        entity

    ):

        score = 0.0

        if not sentence:

            return score

        sentence = sentence.lower()

        # --------------------------------------------------------
        # Business Area Mention
        # --------------------------------------------------------

        if entity.business_area:

            business_area = entity.business_area.lower()

            if business_area in sentence:

                score += 0.05

        # --------------------------------------------------------
        # Domain Mention
        # --------------------------------------------------------

        if entity.domain:

            domain = entity.domain.lower()

            if domain in sentence:

                score += 0.05

        # --------------------------------------------------------
        # Metadata Keywords
        # --------------------------------------------------------

        keywords = entity.metadata.get(

            "keywords",

            []

        )

        for keyword in keywords:

            if keyword.lower() in sentence:

                score += 0.01

        return min(score, 0.15)

    ####################################################################
    # PARSER SCORE
    ####################################################################

    def _parser_score(

        self,

        parser_context

    ):

        score = 0.0

        if parser_context is None:

            return score

        if parser_context.get("verb_found"):

            score += self.rules.get(

                "verb_found",

                0.25

            )

        if parser_context.get("object_found"):

            score += self.rules.get(

                "object_found",

                0.20

            )

        if parser_context.get("domain_found"):

            score += self.rules.get(

                "domain_found",

                0.20

            )

        if parser_context.get("metric_found"):

            score += self.rules.get(

                "metric_found",

                0.15

            )

        if parser_context.get("numeric_value"):

            score += self.rules.get(

                "numeric_value",

                0.10

            )

        if parser_context.get("modifier_found"):

            score += self.rules.get(

                "modifier_found",

                0.10

            )

        return score * 0.20

    ####################################################################
    # EXECUTIVE BOOST
    ####################################################################

    def executive_bonus(

        self,

        entity

    ):

        """
        Used later by Profile Builder.
        """

        if entity.impact_weight >= 0.95:

            return 0.05

        if entity.impact_weight >= 0.90:

            return 0.03

        return 0.0

    ####################################################################
    # NORMALIZE
    ####################################################################

    def normalize(

        self,

        score

    ):

        return round(

            min(

                score,

                self.max_score

            ),

            3

        )