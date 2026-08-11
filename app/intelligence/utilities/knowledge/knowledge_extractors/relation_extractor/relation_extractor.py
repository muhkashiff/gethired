"""
Enterprise Relation Extractor

Enterprise V5

Responsibilities

• Resolve repository relations
• Connect extracted source entities
• Connect extracted target entities
• Produce RelationKnowledge objects
• Never load relations.json directly
"""

from __future__ import annotations

from typing import Optional

from app.intelligence.utilities.knowledge.knowledge_extractor_models.relation_models import (
    RelationKnowledge,
)

from app.intelligence.utilities.knowledge.repository_v5.repository import (
    Repository,
)


class RelationExtractor:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(
        self,
        repository: Repository,
    ) -> None:

        self.repository = repository

    ####################################################################
    # EXTRACT
    ####################################################################

    def extract(
        self,
        source_entity,
        target_entity,
        sentence_index: int = 0,
    ) -> Optional[RelationKnowledge]:
        """
        Resolve the relationship between two already-extracted
        knowledge entities.

        This method does NOT extract entities from raw text.

        It receives:

            source_entity
            target_entity

        and resolves whether a repository relationship exists.
        """

        if source_entity is None:

            return None

        if target_entity is None:

            return None

        ################################################################
        # SOURCE ID
        ################################################################

        source_id = getattr(
            source_entity,
            "entity_id",
            "",
        )

        if not source_id:

            return None

        ################################################################
        # TARGET ID
        ################################################################

        target_id = getattr(
            target_entity,
            "entity_id",
            "",
        )

        if not target_id:

            return None

        ################################################################
        # FIND RELATIONS
        ################################################################

        relations = (
            self.repository.find_relations_by_source(
                source_id
            )
        )

        ################################################################
        # FIND MATCHING TARGET
        ################################################################

        matched_relation = None

        for relation in relations:

            if not relation.active:
                continue

            if not relation.searchable:
                continue

            if (
                relation.target.casefold()
                ==
                target_id.casefold()
            ):

                matched_relation = relation

                break

        ################################################################
        # NO RELATION
        ################################################################

        if matched_relation is None:

            return RelationKnowledge(

                found=False,

                confidence=0.0,

                sentence_index=sentence_index,

                source_entity_id=source_id,

                target_entity_id=target_id,

                source_entity_type=getattr(
                    source_entity,
                    "entity_type",
                    "",
                ),

                target_entity_type=getattr(
                    target_entity,
                    "entity_type",
                    "",
                ),

                source_canonical=getattr(
                    source_entity,
                    "canonical",
                    "",
                ),

                target_canonical=getattr(
                    target_entity,
                    "canonical",
                    "",
                ),

                source_phrase=getattr(
                    source_entity,
                    "canonical",
                    "",
                ),

                target_phrase=getattr(
                    target_entity,
                    "canonical",
                    "",
                ),

                source="relation_extractor",
            )

        ################################################################
        # CONFIDENCE
        ################################################################

        confidence = min(
            max(
                float(
                    matched_relation.weight
                ),
                0.0,
            ),
            1.0,
        )

        ################################################################
        # BUILD KNOWLEDGE OBJECT
        ################################################################

        return RelationKnowledge(

            found=True,

            confidence=confidence,

            ################################################################
            # RELATION IDENTITY
            ################################################################

            relation_id=(
                matched_relation.relation_id
            ),

            relation_type=(
                matched_relation.relation_type
            ),

            relation_family=(
                self._relation_family(
                    matched_relation.relation_type
                )
            ),

            ################################################################
            # SOURCE
            ################################################################

            source_entity_id=source_id,

            source_entity_type=getattr(
                source_entity,
                "entity_type",
                "",
            ),

            source_canonical=getattr(
                source_entity,
                "canonical",
                "",
            ),

            source_phrase=getattr(
                source_entity,
                "canonical",
                "",
            ),

            ################################################################
            # TARGET
            ################################################################

            target_entity_id=target_id,

            target_entity_type=getattr(
                target_entity,
                "entity_type",
                "",
            ),

            target_canonical=getattr(
                target_entity,
                "canonical",
                "",
            ),

            target_phrase=getattr(
                target_entity,
                "canonical",
                "",
            ),

            ################################################################
            # POSITION
            ################################################################

            sentence_index=sentence_index,

            ################################################################
            # SEMANTICS
            ################################################################

            description=(
                matched_relation.description
            ),

            impact_weight=(
                matched_relation.weight
            ),

            ################################################################
            # GRAPH
            ################################################################

            graph_edge=True,

            ################################################################
            # SOURCE
            ################################################################

            source="relation_extractor",

            ################################################################
            # METADATA
            ################################################################

            metadata={
                "repository_relation": (
                    matched_relation.relation_id
                ),
                "repository_relation_type": (
                    matched_relation.relation_type
                ),
            },
        )

    ####################################################################
    # RELATION FAMILY
    ####################################################################

    @staticmethod
    def _relation_family(
        relation_type: str,
    ) -> str:

        relation_type = (
            relation_type.casefold().strip()
        )

        ################################################################
        # OPERATIONAL
        ################################################################

        if relation_type in {
            "acts_on",
            "supports",
            "improves",
        }:

            return "operational"

        ################################################################
        # GOVERNANCE
        ################################################################

        if relation_type in {
            "governs",
        }:

            return "governance"

        ################################################################
        # CLASSIFICATION
        ################################################################

        if relation_type in {
            "belongs_to_domain",
        }:

            return "classification"

        ################################################################
        # GENERAL
        ################################################################

        return "general"