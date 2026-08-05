"""
Business Statement Builder

Enterprise V12

Converts semantic entities + semantic dependencies into
BusinessStatement objects.

Pipeline

Semantic Entities
        ↓
Group by Statement
        ↓
BusinessStatement
        ↓
Infer Semantic Relations
        ↓
Knowledge Graph
"""

from collections import defaultdict

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    BusinessStatement,
    SemanticEntity,
    SemanticDependency,
    StatementRelation,
)


class BusinessStatementBuilder:

    def __init__(self):

        pass

    # ==========================================================
    # BUILD
    # ==========================================================

    def build(

        self,

        entities: list[SemanticEntity],

        dependencies: list[SemanticDependency],

    ) -> list[BusinessStatement]:

        """
        Main Builder

        1. Group entities by statement
        2. Group dependencies by statement
        3. Build BusinessStatement
        4. Infer semantic relations
        """

        grouped_entities = self._group_entities(

            entities

        )

        grouped_dependencies = self._group_dependencies(

            dependencies,

            entities,

        )

        statements = []

        for statement_id in grouped_entities:

            statement = BusinessStatement()

            statement.statement_id = statement_id

            statement.entities.extend(

                grouped_entities[statement_id]

            )

            self._populate_metadata(

                statement

            )

            self._infer_relations(

                statement,

                grouped_dependencies.get(

                    statement_id,

                    [],

                ),

            )

            statements.append(

                statement

            )

        return statements
        # ==========================================================
    # GROUP ENTITIES
    # ==========================================================

    def _group_entities(

        self,

        entities: list[SemanticEntity],

    ) -> dict[str, list[SemanticEntity]]:

        """
        Groups entities by statement_id.

        If statement_id is missing,
        place everything into DEFAULT.
        """

        grouped = defaultdict(list)

        for entity in entities:

            statement_id = getattr(

                entity,

                "statement_id",

                "",

            )

            if not statement_id:

                statement_id = "STATEMENT_1"

            grouped[statement_id].append(

                entity

            )

        return grouped


    # ==========================================================
    # GROUP DEPENDENCIES
    # ==========================================================

    def _group_dependencies(

        self,

        dependencies: list[SemanticDependency],

        entities: list[SemanticEntity],

    ) -> dict[str, list[SemanticDependency]]:

        """
        Groups dependency edges by statement.

        Dependency belongs to the statement
        containing its source entity.
        """

        entity_lookup = {

            entity.entity_id: entity

            for entity in entities

        }

        grouped = defaultdict(list)

        for dependency in dependencies:

            source = entity_lookup.get(

                dependency.source_entity

            )

            if source is None:

                continue

            statement_id = getattr(

                source,

                "statement_id",

                "",

            )

            if not statement_id:

                statement_id = "STATEMENT_1"

            grouped[statement_id].append(

                dependency

            )

        return grouped


    # ==========================================================
    # POPULATE METADATA
    # ==========================================================

    def _populate_metadata(

        self,

        statement: BusinessStatement,

    ):

        """
        Determines

        • label
        • semantic_type
        • primary_domain
        • business_area
        • achievement
        """

        actions = statement.actions

        targets = statement.targets

        metrics = statement.metrics

        measurements = statement.measurements

        domains = statement.domains

        standards = statement.standards

        methodologies = statement.methodologies

        skills = statement.skills


        # ---------------------------------------------
        # Label
        # ---------------------------------------------

        label_parts = []

        if actions:

            label_parts.append(

                actions[0].canonical

            )

        if targets:

            label_parts.append(

                targets[0].canonical

            )

        statement.label = " ".join(

            label_parts

        ).strip()


        # ---------------------------------------------
        # Domain
        # ---------------------------------------------

        if domains:

            statement.primary_domain = (

                domains[0].canonical

            )


        # ---------------------------------------------
        # Business Area
        # ---------------------------------------------

        if domains:

            statement.business_area = (

                domains[0].business_area

            )


        # ---------------------------------------------
        # Semantic Type
        # ---------------------------------------------

        if metrics:

            statement.semantic_type = "Measured Action"

        elif standards:

            statement.semantic_type = "Compliance Action"

        elif methodologies:

            statement.semantic_type = "Method Action"

        elif skills:

            statement.semantic_type = "Skill Action"

        else:

            statement.semantic_type = "Business Action"


        # ---------------------------------------------
        # Achievement
        # ---------------------------------------------

        statement.achievement = (

            len(measurements) > 0

        )
        # ==========================================================
    # RELATION INFERENCE
    # ==========================================================

    def _infer_relations(

        self,

        statement: BusinessStatement,

        dependencies: list[SemanticDependency],

    ):

        """
        Infer semantic relationships.

        Enterprise Rule Engine

        Action
            ↓
        Target

        Action
            ↓
        Metric
            ↓
        Measurement

        Action
            ↓
        Skill

        Action
            ↓
        Methodology

        Action
            ↓
        Standard

        Action
            ↓
        Domain

        Action
            ↓
        Achievement (Metric)
        """

        actions = statement.actions

        targets = statement.targets

        metrics = statement.metrics

        measurements = statement.measurements

        skills = statement.skills

        methodologies = statement.methodologies

        standards = statement.standards

        domains = statement.domains


        # -------------------------------------------------
        # ACTION → TARGET
        # -------------------------------------------------

        for action in actions:

            for target in targets:

                self._create_relation(

                    statement,

                    action,

                    target,

                    "ACTS_ON",

                )


        # -------------------------------------------------
        # ACTION → METRIC
        # -------------------------------------------------

        for action in actions:

            for metric in metrics:

                self._create_relation(

                    statement,

                    action,

                    metric,

                    "AFFECTS",

                )


        # -------------------------------------------------
        # METRIC → MEASUREMENT
        # -------------------------------------------------

        for metric in metrics:

            for measurement in measurements:

                self._create_relation(

                    statement,

                    metric,

                    measurement,

                    "MEASURED_BY",

                )


        # -------------------------------------------------
        # ACTION → SKILL
        # -------------------------------------------------

        for action in actions:

            for skill in skills:

                self._create_relation(

                    statement,

                    action,

                    skill,

                    "REQUIRES",

                )


        # -------------------------------------------------
        # ACTION → STANDARD
        # -------------------------------------------------

        for action in actions:

            for standard in standards:

                self._create_relation(

                    statement,

                    action,

                    standard,

                    "COMPLIES_WITH",

                )


        # -------------------------------------------------
        # ACTION → METHODOLOGY
        # -------------------------------------------------

        for action in actions:

            for methodology in methodologies:

                self._create_relation(

                    statement,

                    action,

                    methodology,

                    "USES",

                )


        # -------------------------------------------------
        # ACTION → DOMAIN
        # -------------------------------------------------

        for action in actions:

            for domain in domains:

                self._create_relation(

                    statement,

                    action,

                    domain,

                    "BELONGS_TO",

                )


        # -------------------------------------------------
        # ACTION → ACHIEVEMENT
        # (Action achieving a metric)
        # -------------------------------------------------

        if measurements:

            for action in actions:

                for metric in metrics:

                    self._create_relation(

                        statement,

                        action,

                        metric,

                        "ACHIEVED",

                    )
        # ==========================================================
    # CREATE RELATION
    # ==========================================================

    def _create_relation(

        self,

        statement: BusinessStatement,

        source: SemanticEntity,

        target: SemanticEntity,

        relation: str,

    ):

        """
        Creates one semantic relation.

        Duplicate relations are ignored.
        """

        if source is None:

            return

        if target is None:

            return

        # ------------------------------------------
        # Duplicate Protection
        # ------------------------------------------

        for existing in statement.relations:

            if (
                existing.source_id == source.entity_id
                and existing.target_id == target.entity_id
                and existing.relation_type == relation
            ):
                return

        # ------------------------------------------
        # Confidence
        # ------------------------------------------

        confidence = min(

            source.confidence,

            target.confidence,

        )

        # ------------------------------------------
        # Reasoning
        # ------------------------------------------

        reasoning = (

            f"{source.canonical} "

            f"{relation.replace('_',' ').lower()} "

            f"{target.canonical}"

        )

        # ------------------------------------------
        # Create Relation
        # ------------------------------------------

        statement.relations.append(

            StatementRelation(
                source_id=source.entity_id,
                target_id=target.entity_id,
                relation_type=relation,
                confidence=confidence,
                reasoning=reasoning,
                metadata={
                    "source_type": source.entity_type,
                    "target_type": target.entity_type,
                },
            )

        )

    # ==========================================================
    # DEBUG
    # ==========================================================

    def _debug_statement(

        self,

        statement: BusinessStatement,

    ):

        print("\n----------------------------------------")

        print(statement.label)

        print("----------------------------------------")

        print("Entities")

        for entity in statement.entities:

            print(

                entity.entity_type,

                entity.canonical,

            )

        print()

        print("Relations")

        for relation in statement.relations:

            print(

                relation.relation,

                relation.source_id,

                "->",

                relation.target_id,

            )