"""
Enterprise Overlap Resolver

Enterprise V5
"""

from __future__ import annotations


class OverlapResolver:

    ####################################################################
    # RESOLVE
    ####################################################################

    def resolve(self, candidates):

        if not candidates:
            return []

        # safest sort
        candidates = sorted(
            candidates,
            key=lambda c: (
                c.get("start_char", 0),
                -c.get("token_count", 0),
                -c.get("confidence", 0.0),
            ),
        )

        kept = []
        occupied = []

        for candidate in candidates:

            start = candidate.get("start_char", 0)
            end = candidate.get("end_char", 0)

            overlap = False

            for existing_start, existing_end in occupied:

                if start < existing_end and end > existing_start:
                    overlap = True
                    break

            if overlap:
                continue

            kept.append(candidate)
            occupied.append((start, end))

        return kept

    ####################################################################
    # REMOVE DUPLICATES
    ####################################################################

    def remove_duplicates(self, candidates):

        results = []
        seen = set()

        for candidate in candidates:

            entity = candidate.get("entity")

            if entity is None:
                continue

            entity_id = entity.entity_id

            if entity_id in seen:
                continue

            seen.add(entity_id)
            results.append(candidate)

        return results

    ####################################################################
    # COMPLETE
    ####################################################################

    def clean(self, candidates):

        candidates = self.resolve(candidates)
        candidates = self.remove_duplicates(candidates)

        return candidates

    ####################################################################
    # DEBUG
    ####################################################################

    def debug(self, candidates):

        print()
        print("=" * 70)
        print("OVERLAP RESOLVER")
        print("=" * 70)

        cleaned = self.clean(candidates)

        for candidate in cleaned:

            entity = candidate["entity"]

            print(
                candidate["phrase"],
                "->",
                entity.canonical,
                candidate.get("confidence"),
            )

        return cleaned