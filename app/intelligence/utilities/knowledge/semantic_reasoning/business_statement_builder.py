"""
Business Statement Builder

Enterprise V13

Converts semantic entities and semantic dependencies
into BusinessStatement objects.

Preferred pipeline

SemanticEntity[]
        +
SemanticDependency[]
        ↓
BusinessStatementBuilder
        ↓
BusinessStatement[]
        ↓
KnowledgeGraphBuilder

Compatibility behavior

When semantic dependencies are absent, the builder performs
safe deterministic relation inference so older tests and
pipeline components remain functional.

The builder NEVER creates arbitrary entity-to-entity
relationships.
"""

from __future__ import annotations

from collections import defaultdict

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    BusinessStatement,
    SemanticDependency,
    SemanticEntity,
    StatementRelation,
)


class BusinessStatementBuilder:

    # ========================================================================
    # BUILD
    # ========================================================================

    def build(
        self,
        entities: list[SemanticEntity],
        dependencies: list[SemanticDependency],
    ) -> list[BusinessStatement]:

        if not entities:
            return []

        entities = list(entities or [])
        dependencies = list(dependencies or [])

        grouped_entities = self._group_entities(
            entities
        )

        grouped_dependencies = self._group_dependencies(
            dependencies,
            entities,
        )

        statements: list[BusinessStatement] = []

        for statement_id, statement_entities in grouped_entities.items():

            statement = BusinessStatement(
                statement_id=statement_id,
                entities=list(statement_entities),
            )

            self._populate_metadata(
                statement
            )

            statement_dependencies = grouped_dependencies.get(
                statement_id,
                [],
            )

            # ---------------------------------------------------------------
            # Preferred path:
            # semantic reasoner already resolved the relationship.
            # ---------------------------------------------------------------

            if statement_dependencies:

                self._add_dependency_relations(
                    statement,
                    statement_dependencies,
                )

            # ---------------------------------------------------------------
            # Compatibility path:
            # preserve deterministic inference when no dependency was
            # supplied for the relevant semantic relationship.
            # ---------------------------------------------------------------

            self._infer_missing_relations(
                statement
            )

            self._calculate_statement_confidence(
                statement
            )

            statements.append(
                statement
            )

        return statements

    # ========================================================================
    # GROUP ENTITIES
    # ========================================================================

    def _group_entities(
        self,
        entities: list[SemanticEntity],
    ) -> dict[str, list[SemanticEntity]]:

        grouped: dict[str, list[SemanticEntity]] = defaultdict(list)

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

    # ========================================================================
    # GROUP DEPENDENCIES
    # ========================================================================

    def _group_dependencies(
        self,
        dependencies: list[SemanticDependency],
        entities: list[SemanticEntity],
    ) -> dict[str, list[SemanticDependency]]:

        entity_lookup = {
            entity.entity_id: entity
            for entity in entities
        }

        grouped: dict[
            str,
            list[SemanticDependency],
        ] = defaultdict(list)

        for dependency in dependencies:

            source = entity_lookup.get(
                dependency.source_entity
            )

            target = entity_lookup.get(
                dependency.target_entity
            )

            if source is None:
                continue

            if target is None:
                continue

            source_statement = getattr(
                source,
                "statement_id",
                "",
            )

            target_statement = getattr(
                target,
                "statement_id",
                "",
            )

            # ---------------------------------------------------------------
            # Do not connect entities belonging to different statements.
            # ---------------------------------------------------------------

            if (
                source_statement
                and target_statement
                and source_statement != target_statement
            ):
                continue

            statement_id = (
                source_statement
                or target_statement
                or "STATEMENT_1"
            )

            grouped[statement_id].append(
                dependency
            )

        return grouped

    # ========================================================================
    # METADATA
    # ========================================================================

    def _populate_metadata(
        self,
        statement: BusinessStatement,
    ) -> None:

        actions = statement.actions
        targets = statement.targets
        metrics = statement.metrics
        measurements = statement.measurements
        domains = statement.domains
        standards = statement.standards
        methodologies = statement.methodologies
        skills = statement.skills

        # --------------------------------------------------------------------
        # LABEL
        # --------------------------------------------------------------------

        label_parts: list[str] = []

        if actions:
            label_parts.append(
                actions[0].canonical
            )

        if targets:
            label_parts.append(
                targets[0].canonical
            )

        if metrics and not targets:
            label_parts.append(
                metrics[0].canonical
            )

        statement.label = " ".join(
            part
            for part in label_parts
            if part
        ).strip()

        # --------------------------------------------------------------------
        # DOMAIN
        # --------------------------------------------------------------------

        if domains:

            statement.primary_domain = (
                domains[0].canonical
            )

        # --------------------------------------------------------------------
        # BUSINESS AREA
        # --------------------------------------------------------------------

        if domains:

            statement.business_area = (
                domains[0].business_area
            )

        elif actions:

            statement.business_area = (
                actions[0].business_area
            )

        # --------------------------------------------------------------------
        # SEMANTIC TYPE
        # --------------------------------------------------------------------

        if metrics:

            statement.semantic_type = (
                "Measured Action"
            )

        elif measurements:

            statement.semantic_type = (
                "Measured Action"
            )

        elif standards:

            statement.semantic_type = (
                "Compliance Action"
            )

        elif methodologies:

            statement.semantic_type = (
                "Method Action"
            )

        elif skills:

            statement.semantic_type = (
                "Skill Action"
            )

        elif actions:

            statement.semantic_type = (
                "Business Action"
            )

        else:

            statement.semantic_type = (
                "Business Statement"
            )

        # --------------------------------------------------------------------
        # ACHIEVEMENT
        # --------------------------------------------------------------------

        statement.achievement = bool(
            measurements
        )

        # --------------------------------------------------------------------
        # METADATA
        # --------------------------------------------------------------------

        statement.metadata.update(
            {
                "entity_count": statement.entity_count,
                "action_count": len(actions),
                "target_count": len(targets),
                "metric_count": len(metrics),
                "measurement_count": len(measurements),
                "skill_count": len(skills),
                "standard_count": len(standards),
                "methodology_count": len(methodologies),
                "domain_count": len(domains),
                "achievement": statement.achievement,
            }
        )

    # ========================================================================
    # DEPENDENCY → STATEMENT RELATION
    # ========================================================================

    def _add_dependency_relations(
        self,
        statement: BusinessStatement,
        dependencies: list[SemanticDependency],
    ) -> None:

        for dependency in dependencies:

            source = statement.entity(
                dependency.source_entity
            )

            target = statement.entity(
                dependency.target_entity
            )

            if source is None:
                continue

            if target is None:
                continue

            relation_type = self._normalize_dependency_relation(
                dependency.relation,
                source,
                target,
            )

            if not relation_type:
                continue

            self._create_relation(
                statement=statement,
                source=source,
                target=target,
                relation=relation_type,
                confidence=min(
                    source.confidence,
                    target.confidence,
                    dependency.confidence,
                ),
                reasoning=(
                    dependency.metadata.get(
                        "reasoning",
                        "",
                    )
                    if dependency.metadata
                    else ""
                ),
                metadata={
                    "dependency_relation": dependency.relation,
                    "dependency_confidence": dependency.confidence,
                    "source_type": source.entity_type,
                    "target_type": target.entity_type,
                },
            )

    # ========================================================================
    # DEPENDENCY RELATION NORMALIZATION
    # ========================================================================

    def _normalize_dependency_relation(
        self,
        relation: str,
        source: SemanticEntity,
        target: SemanticEntity,
    ) -> str:

        if not relation:
            return ""

        normalized = relation.strip().upper()

        # --------------------------------------------------------------------
        # Already canonical statement relation.
        # --------------------------------------------------------------------

        canonical = {
            "ACTS_ON",
            "AFFECTS",
            "MEASURED_BY",
            "REQUIRES",
            "COMPLIES_WITH",
            "USES",
            "BELONGS_TO",
            "ACHIEVED",
        }

        if normalized in canonical:
            return normalized

        # --------------------------------------------------------------------
        # Reasoner terminology → statement terminology.
        # --------------------------------------------------------------------

        mapping = {
            "TARGETS": "ACTS_ON",
            "CREATES": "ACTS_ON",
            "MANAGES": "ACTS_ON",
            "MONITORS": "ACTS_ON",
            "MAINTAINS": "ACTS_ON",
            "OPTIMIZES": "ACTS_ON",
            "IMPROVES": "ACTS_ON",
            "CONTROLS": "ACTS_ON",
            "EXECUTES": "ACTS_ON",
            "CERTIFIES": "COMPLIES_WITH",

            "IMPROVED": "AFFECTS",
            "REDUCED": "AFFECTS",
            "INCREASED": "AFFECTS",
            "OPTIMIZED": "AFFECTS",
            "MEASURES": "AFFECTS",
            "MEASURED_BY": "MEASURED_BY",

            "PERFORMED_USING": "USES",
            "REQUIRES": "REQUIRES",

            "BELONGS_TO": "BELONGS_TO",

            "COMPLIES_WITH": "COMPLIES_WITH",
            "CERTIFIED_AGAINST": "COMPLIES_WITH",
            "AUDITED_AGAINST": "COMPLIES_WITH",
        }

        mapped = mapping.get(
            normalized
        )

        if mapped:
            return mapped

        # --------------------------------------------------------------------
        # Unknown relations are retained only when they represent a
        # legitimate dependency. This prevents arbitrary invented edges.
        # --------------------------------------------------------------------

        if source.entity_type == "action":

            if target.entity_type == "skill":
                return "REQUIRES"

            if target.entity_type == "standard":
                return "COMPLIES_WITH"

            if target.entity_type == "methodology":
                return "USES"

            if target.entity_type == "domain":
                return "BELONGS_TO"

            if target.entity_type in {
                "target",
                "object",
            }:
                return "ACTS_ON"

            if target.entity_type in {
                "metric",
                "kpi",
            }:
                return "AFFECTS"

        if source.entity_type in {
            "metric",
            "kpi",
        } and target.entity_type == "measurement":

            return "MEASURED_BY"

        return ""

    # ========================================================================
    # FALLBACK INFERENCE
    # ========================================================================

    def _infer_missing_relations(
        self,
        statement: BusinessStatement,
    ) -> None:

        actions = statement.actions
        targets = statement.targets
        metrics = statement.metrics
        measurements = statement.measurements
        skills = statement.skills
        standards = statement.standards
        methodologies = statement.methodologies
        domains = statement.domains

        # --------------------------------------------------------------------
        # ACTION → TARGET
        # --------------------------------------------------------------------

        for action in actions:

            for target in targets:

                self._create_relation(
                    statement,
                    action,
                    target,
                    "ACTS_ON",
                )

        # --------------------------------------------------------------------
        # ACTION → METRIC
        # --------------------------------------------------------------------

        for action in actions:

            for metric in metrics:

                self._create_relation(
                    statement,
                    action,
                    metric,
                    "AFFECTS",
                )

        # --------------------------------------------------------------------
        # METRIC → MEASUREMENT
        # --------------------------------------------------------------------

        for metric in metrics:

            for measurement in measurements:

                self._create_relation(
                    statement,
                    metric,
                    measurement,
                    "MEASURED_BY",
                )

        # --------------------------------------------------------------------
        # ACTION → SKILL
        # --------------------------------------------------------------------

        for action in actions:

            for skill in skills:

                self._create_relation(
                    statement,
                    action,
                    skill,
                    "REQUIRES",
                )

        # --------------------------------------------------------------------
        # ACTION → STANDARD
        # --------------------------------------------------------------------

        for action in actions:

            for standard in standards:

                self._create_relation(
                    statement,
                    action,
                    standard,
                    "COMPLIES_WITH",
                )

        # --------------------------------------------------------------------
        # ACTION → METHODOLOGY
        # --------------------------------------------------------------------

        for action in actions:

            for methodology in methodologies:

                self._create_relation(
                    statement,
                    action,
                    methodology,
                    "USES",
                )

        # --------------------------------------------------------------------
        # ACTION → DOMAIN
        # --------------------------------------------------------------------

        for action in actions:

            for domain in domains:

                self._create_relation(
                    statement,
                    action,
                    domain,
                    "BELONGS_TO",
                )

        # --------------------------------------------------------------------
        # ACHIEVEMENT
        # --------------------------------------------------------------------

        if measurements:

            for action in actions:

                for metric in metrics:

                    self._create_relation(
                        statement,
                        action,
                        metric,
                        "ACHIEVED",
                    )

    # ========================================================================
    # CREATE RELATION
    # ========================================================================

    def _create_relation(
        self,
        statement: BusinessStatement,
        source: SemanticEntity,
        target: SemanticEntity,
        relation: str,
        confidence: float | None = None,
        reasoning: str = "",
        metadata: dict | None = None,
    ) -> None:

        if source is None:
            return

        if target is None:
            return

        if source.entity_id == target.entity_id:
            return

        # --------------------------------------------------------------------
        # HARD RULE:
        #
        # Never create object → object.
        # --------------------------------------------------------------------

        if (
            source.entity_type == "object"
            and target.entity_type == "object"
        ):
            return

        # --------------------------------------------------------------------
        # Duplicate protection
        # --------------------------------------------------------------------

        for existing in statement.relations:

            if (
                existing.source_id
                == source.entity_id
                and existing.target_id
                == target.entity_id
                and existing.relation_type
                == relation
            ):
                return

        # --------------------------------------------------------------------
        # Confidence
        # --------------------------------------------------------------------

        if confidence is None:

            confidence = min(
                source.confidence,
                target.confidence,
            )

        # --------------------------------------------------------------------
        # Reasoning
        # --------------------------------------------------------------------

        if not reasoning:

            reasoning = (
                f"{source.canonical} "
                f"{relation.replace('_', ' ').lower()} "
                f"{target.canonical}"
            )

        # --------------------------------------------------------------------
        # Relation
        # --------------------------------------------------------------------

        statement.relations.append(
            StatementRelation(
                source_id=source.entity_id,
                target_id=target.entity_id,
                relation_type=relation,
                confidence=confidence,
                reasoning=reasoning,
                metadata=metadata or {
                    "source_type": source.entity_type,
                    "target_type": target.entity_type,
                },
            )
        )

    # ========================================================================
    # STATEMENT CONFIDENCE
    # ========================================================================

    def _calculate_statement_confidence(
        self,
        statement: BusinessStatement,
    ) -> None:

        if not statement.entities:

            statement.confidence = 0.0

            return

        statement.confidence = min(
            entity.confidence
            for entity in statement.entities
        )

    # ========================================================================
    # DEBUG
    # ========================================================================

    def _debug_statement(
        self,
        statement: BusinessStatement,
    ) -> None:

        print()
        print("-" * 60)
        print(statement.label)
        print("-" * 60)

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
                relation.relation_type,
                relation.source_id,
                "->",
                relation.target_id,
                f"(confidence={relation.confidence:.2f})",
            )