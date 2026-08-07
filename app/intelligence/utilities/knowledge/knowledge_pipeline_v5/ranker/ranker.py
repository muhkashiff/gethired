"""
Enterprise Ranker

Stage 6

Input
    list[MatchResult]

Output
    list[MatchResult]
"""

class Ranker:

    ############################################################

    def rank(

        self,

        matches,

    ):

        if not matches:

            return []

        ########################################################

        ranked = sorted(

            matches,

            key=lambda m:

            (

                -m.confidence,

                -m.token_count,

                m.token_index,

            )

        )

        ########################################################

        return ranked

    ############################################################

    def best(

        self,

        matches,

    ):

        ranked = self.rank(matches)

        if ranked:

            return ranked[0]

        return None