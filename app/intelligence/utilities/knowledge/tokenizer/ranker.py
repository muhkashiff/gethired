"""
Enterprise Candidate Ranker

Enterprise V5
"""

from operator import itemgetter


class CandidateRanker:

    ############################################################

    def rank(

        self,

        candidates,

    ):

        if not candidates:

            return []

        ########################################################

        candidates.sort(

            key=lambda c: (

                c["confidence"],

                c["token_count"],

                len(c["phrase"]),

            ),

            reverse=True,

        )

        return candidates

    ############################################################

    def best(

        self,

        candidates,

    ):

        ranked = self.rank(

            candidates

        )

        if ranked:

            return ranked[0]

        return None