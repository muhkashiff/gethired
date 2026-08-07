"""
Enterprise Confidence Calculator
Enterprise V5

Stage 4

Responsibilities
----------------
• Calculate confidence only
• Never perform matching
• Never perform overlap removal
• Never modify entity

Input
-----
MatchResult

Output
------
MatchResult
"""

from __future__ import annotations


class ConfidenceCalculator:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(

        self,

        repository,

        ):

        self.repository = repository 

    ####################################################################
    # SCORE SINGLE MATCH
    ####################################################################

    def score(

        self,

        match,

    ):

        score = 0.0

        entity = match.entity

        phrase = match.phrase.lower()

        canonical = entity.canonical.lower()

        aliases = [

            a.lower()

            for a in entity.aliases

        ]

        ############################################################
        # Canonical
        ############################################################

        if phrase == canonical:

            score += 0.45

        ############################################################
        # Alias
        ############################################################

        elif phrase in aliases:

            score += 0.35

        ############################################################
        # Fallback
        ############################################################

        else:

            score += 0.20

        ############################################################
        # Business weight
        ############################################################

        score += (

            entity.impact_weight

            * 0.20

        )

        ############################################################
        # Business Area
        ############################################################

        if entity.business_area:

            score += 0.05

        ############################################################
        # Domain
        ############################################################

        if entity.domain:

            score += 0.05

        ############################################################

        match.confidence = round(

            min(score,1.0),

            3,

        )

        return match

    ####################################################################
    # SCORE LIST
    ####################################################################

    def score_all(

        self,

        matches,

    ):

        return [

            self.score(m)

            for m in matches

        ]