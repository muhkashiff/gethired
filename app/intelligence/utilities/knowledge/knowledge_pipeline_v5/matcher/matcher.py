"""
Enterprise Matcher

Stage 3

Pipeline

Sentence
    ↓
Tokenizer
    ↓
NGram
    ↓
Repository
    ↓
MatchResult

Responsibilities
----------------
• Match NGrams against Repository
• Build MatchResult objects
• No confidence
• No overlap
• No ranking
"""

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.match_result import MatchResult


class Matcher:

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
    # MATCH SENTENCE
    ####################################################################

    def match(
        self,
        ontology,
        sentence,
    ):

        results = []

        ############################################################
        # Generate NGrams
        ############################################################

        ngrams = self.tokenizer.generate_ngrams(sentence)

        ############################################################

        seen = set()

        ############################################################

        for ngram in ngrams:

            ########################################################
            # Repository lookup
            ########################################################

            entity = self.repository.find_entity(
                ontology,
                ngram.phrase,
            )

            if entity is None:
                continue

            ########################################################
            # Prevent duplicate entity + location
            ########################################################

            key = (
                entity.entity_id,
                ngram.token_index,
            )

            if key in seen:
                continue

            seen.add(key)

            ########################################################
            # Determine matched alias
            ########################################################

            matched_alias = entity.canonical

            for alias in entity.aliases:

                if alias.lower() == ngram.phrase.lower():

                    matched_alias = alias
                    break

            ########################################################

            is_alias = (
                matched_alias.lower()
                != entity.canonical.lower()
            )

            ########################################################
            # Build MatchResult
            ########################################################

            result = MatchResult(
                entity=entity,
                phrase=ngram.phrase,
                matched_alias=matched_alias,
                is_alias=is_alias,
                token_index=ngram.token_index,
                token_count=ngram.token_count,
                start_char=ngram.start_char,
                end_char=ngram.end_char,
            )

            results.append(result)

        ############################################################

        return results

    ####################################################################
    # MATCH BEST
    ####################################################################

    def best(
        self,
        ontology,
        sentence,
    ):

        matches = self.match(
            ontology,
            sentence,
        )

        if matches:
            return matches[0]

        return None