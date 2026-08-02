"""
Enterprise Relation Engine

Builds semantic relationships between extracted entities.

No business logic is hardcoded.

Everything comes from Relation Rules.

Enterprise V5
"""

from app.intelligence.utilities.knowledge.semantic_reasoning.relations.relation_models import (
    KnowledgeRelation,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.relations.relation_rules import (
    RELATION_RULES,
)


class RelationEngine:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.rules = RELATION_RULES
    ####################################################################
    # BUILD RELATIONS
    ####################################################################

    def build_relations(

        self,

        statement,

    ):

        """
        Builds all semantic relationships
        for a ParsedStatement.

        Returns
        -------
        list[KnowledgeRelation]
        """

        relations = []

        entities = self.collect_entities(

            statement

        )

        if len(entities) < 2:

            return relations

        # ------------------------------------------------------------
        # Compare every entity against every other entity
        # ------------------------------------------------------------

        for source in entities:

            for target in entities:

                if source is target:

                    continue

                relation = self.match_rule(

                    source,

                    target,

                    statement,

                )

                if relation:

                    relations.append(

                        relation

                    )

        return self.remove_duplicates(

            relations

        )
    ####################################################################
    # COLLECT ENTITIES
    ####################################################################

    def collect_entities(self, statement):

        """
        Collect every extracted entity into one list.

        This allows the Relation Engine to remain
        completely generic.

        Returns
        -------
        list[KnowledgeEntity]
        """

        entities = []

        # ----------------------------------------------------------
        # Single entities
        # ----------------------------------------------------------

        if getattr(statement, "action", None):

            if statement.action.found:

                entities.append(statement.action)

        if getattr(statement, "intent", None):

            if statement.intent.found:

                entities.append(statement.intent)

        # ----------------------------------------------------------
        # Lists
        # ----------------------------------------------------------

        collections = [

            "targets",

            "metrics",

            "measurements",

            "domains",

            "skills",

            "methods",

            "standards",

            "technologies",

            "certifications",

        ]

        for collection_name in collections:

            collection = getattr(

                statement,

                collection_name,

                []

            )

            if not collection:

                continue

            for entity in collection:

                if entity.found:

                    entities.append(entity)

        return entities
    ####################################################################
    # MATCH RELATION RULE
    ####################################################################

    def match_rule(

        self,

        source,

        target,

        statement,

    ):

        """
        Checks whether a relationship exists between
        two entities using Relation Rules.

        Returns
        -------
        KnowledgeRelation | None
        """

        for rule in self.rules:

            if source.entity_type != rule["source"]:

                continue

            if target.entity_type != rule["target"]:

                continue

            return self.create_relation(

                source,

                target,

                rule,

                statement,

            )

        return None
    ####################################################################
    # CREATE RELATION
    ####################################################################

    def create_relation(

        self,

        source,

        target,

        rule,

        statement,

    ):

        """
        Creates a KnowledgeRelation object.

        Parameters
        ----------
        source : KnowledgeEntity

        target : KnowledgeEntity

        rule : dict

        statement : ParsedStatement
        """

        relation_name = rule["relation"]

        confidence = min(

            source.confidence,

            target.confidence,

        )

        return KnowledgeRelation(

            ################################################################
            # Relation
            ################################################################

            relation=relation_name,

            confidence=confidence,

            ################################################################
            # Source
            ################################################################

            source_entity=source,

            source_id=source.entity_id,

            source_name=source.canonical,

            source_type=source.entity_type,

            ################################################################
            # Target
            ################################################################

            target_entity=target,

            target_id=target.entity_id,

            target_name=target.canonical,

            target_type=target.entity_type,

            ################################################################
            # Business
            ################################################################

            business_area=target.business_area
            or source.business_area,

            domain=target.domain
            or source.domain,

            ################################################################
            # Explainability
            ################################################################

            reasoning=(

                f"{source.canonical} "

                f"{relation_name} "

                f"{target.canonical}"

            ),

            ################################################################
            # Metadata
            ################################################################

            metadata={

                "rule": rule,

                "sentence_index": getattr(

                    source,

                    "sentence_index",

                    0,

                ),

            }

        )
    ####################################################################
    # REMOVE DUPLICATES
    ####################################################################

    def remove_duplicates(self, relations):

        """
        Removes duplicate semantic relations.

        Duplicate definition:
            source_id
            relation
            target_id

        Returns
        -------
        list[KnowledgeRelation]
        """

        unique = []

        seen = set()

        for relation in relations:

            key = (

                relation.source_id,

                relation.relation,

                relation.target_id,

            )

            if key in seen:

                continue

            seen.add(key)

            unique.append(relation)

        return unique