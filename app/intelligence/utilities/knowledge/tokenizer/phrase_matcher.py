"""
Enterprise Phrase Matcher

Enterprise V5
"""

from __future__ import annotations


class PhraseMatcher:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(

        self,

        repository,

        tokenizer,

    ):

        self.repository = repository
        self.tokenizer = tokenizer

    ####################################################################
    # FIND CANDIDATES
    ####################################################################

    def find_candidates(

        self,

        ontology,

        sentence,

    ):

        candidates = []

        seen = set()

        ############################################################

        ngrams = self.tokenizer.generate_ngrams(sentence)

        ############################################################

        for (

            phrase,

            token_index,

            token_count,

        ) in ngrams:

            entity = self.repository.find_entity(

                ontology,

                phrase,

            )

            if entity is None:

                continue

            ########################################################
            # prevent duplicates
            ########################################################

            if entity.entity_id in seen:

                continue

            seen.add(entity.entity_id)

            ########################################################

            start_char, end_char = (

                self.tokenizer.get_char_position(

                    token_index,

                    token_count,

                )

            )

            ########################################################
            # determine which alias matched
            ########################################################

            matched_alias = phrase

            if hasattr(entity, "aliases"):

                phrase_lower = phrase.lower()

                for alias in entity.aliases:

                    if alias.lower() == phrase_lower:

                        matched_alias = alias
                        break

            ########################################################

            candidates.append(

                {

                    "entity": entity,

                    # exact text from sentence
                    "phrase": phrase,

                    # ontology alias that matched
                    "matched_alias": matched_alias,

                    # exact match?
                    "is_alias": (
                        matched_alias.lower()
                        != entity.canonical.lower()
                    ),

                    "token_index": token_index,

                    "token_count": token_count,

                    "start_char": start_char,

                    "end_char": end_char,

                }

            )
            print(__file__)

        ############################################################

        return candidates
    