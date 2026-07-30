"""
Duplicate Merger

Removes duplicate semantic entities and duplicate dependency
relationships before graph construction.

This greatly reduces graph noise.
"""

from collections import OrderedDict


class DuplicateMerger:
    """
    Removes duplicate entities and dependency edges.
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def merge_entities(self, entities):
        """
        Keep only one entity for every entity_id.

        Highest confidence entity wins.
        """

        unique = OrderedDict()

        for entity in entities:

            if entity.entity_id not in unique:

                unique[entity.entity_id] = entity

                continue

            existing = unique[entity.entity_id]

            if entity.confidence > existing.confidence:

                unique[entity.entity_id] = entity

        return list(unique.values())

    # ---------------------------------------------------------

    def merge_dependencies(self, dependencies):
        """
        Remove duplicate dependency edges.

        Duplicate means

            source
            target
            relation

        are identical.
        """

        unique = OrderedDict()

        for edge in dependencies:

            key = (

                edge.source_entity,
                edge.target_entity,
                edge.relation,

            )

            if key not in unique:

                unique[key] = edge

                continue

            existing = unique[key]

            if edge.confidence > existing.confidence:

                unique[key] = edge

        return list(unique.values())

    # ---------------------------------------------------------

    def merge(self, resolution):
        """
        Clean a SemanticResolutionResult.
        """

        resolution.entities = self.merge_entities(
            resolution.entities
        )

        resolution.dependencies = self.merge_dependencies(
            resolution.dependencies
        )

        return resolution