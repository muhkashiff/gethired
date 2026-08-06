"""
Enterprise Fuzzy Matcher

Enterprise V5
"""

from rapidfuzz import process
from rapidfuzz import fuzz


class FuzzyMatcher:

    ############################################################

    def __init__(

        self,

        repository,

        tokenizer,

        threshold=88,

    ):

        self.repository = repository

        self.tokenizer = tokenizer

        self.threshold = threshold

    ############################################################
    from typing import Optional

    def lookup(

        self,

        ontology,

        phrase,

    ):

        ontology = ontology.lower()

        alias_index = self.repository.cache.alias_indexes.get(

            ontology,

            {},

        )

        if not alias_index:

            return None

        result = process.extractOne(

            phrase.lower(),

            alias_index.keys(),

            scorer=fuzz.WRatio,

        )

        if result is None:

            return None

        matched = result[0]
        score = float(result[1])

        if score < self.threshold:

            return None

        return alias_index.get(matched)
   
    ############################################################

    def find_candidates(

        self,

        ontology,

        sentence,

    ):

        candidates = []

        seen = set()

        ########################################################

        for (

            phrase,

            token_index,

            token_count,

        ) in self.tokenizer.generate_ngrams(

            sentence

        ):

            entity = self.lookup(

                ontology,

                phrase,

            )

            if entity is None:

                continue

            ####################################################

            key = (

                entity.entity_id,

                token_index,

            )

            if key in seen:

                continue

            seen.add(

                key

            )

            ####################################################

            start,end = (

                self.tokenizer.get_char_position(

                    token_index,

                    token_count,

                )

            )

            ####################################################

            candidates.append(

                {

                    "entity": entity,

                    "phrase": phrase,

                    "matched_alias": True,

                    "confidence": 0.60,

                    "start_char": start,

                    "end_char": end,

                    "token_index": token_index,

                    "token_count": token_count,

                }

            )

        ########################################################

        return candidates