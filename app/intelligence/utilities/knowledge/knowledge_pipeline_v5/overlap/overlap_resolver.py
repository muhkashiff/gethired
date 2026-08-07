"""
Enterprise Overlap Resolver

Stage 5

Responsibilities

• Remove overlapping entities

• Keep longest phrase

• Keep highest confidence

Input

list[MatchResult]

Output

list[MatchResult]
"""

class OverlapResolver:

    ############################################################

    def resolve(

        self,

        matches,

    ):

        if not matches:

            return []

        ########################################################

        matches = sorted(

            matches,

            key=lambda m:

            (

                -(m.token_count),

                -m.confidence,

            )

        )

        ########################################################

        accepted = []

        occupied = set()

        ########################################################

        for match in matches:

            overlap = False

            ####################################################

            for token in range(

                match.token_index,

                match.token_index +

                match.token_count,

            ):

                if token in occupied:

                    overlap = True

                    break

            ####################################################

            if overlap:

                continue

            ####################################################

            accepted.append(

                match

            )

            ####################################################

            for token in range(

                match.token_index,

                match.token_index +

                match.token_count,

            ):

                occupied.add(

                    token

                )

        ########################################################

        accepted.sort(

            key=lambda m:

            m.token_index

        )

        ########################################################

        return accepted