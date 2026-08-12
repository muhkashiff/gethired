"""
Enterprise Dependency Resolver
Enterprise V12

Creates business-aware semantic dependencies between
SemanticEntity objects.

Pipeline

Semantic Entities
        ↓
DependencyResolver
        ↓
List[SemanticDependency]
        ↓
BusinessStatementBuilder
        ↓
BusinessStatement

Responsibilities
----------------
• Resolve meaningful semantic relationships
• Preserve entity IDs
• Preserve confidence
• Prevent duplicate dependencies
• Respect statement boundaries
• Support target/object backward compatibility
• Keep KPI and BKPI semantically distinct
• Avoid unsupported relationship invention
"""

from __future__ import annotations

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticDependency,
    SemanticEntity,
)


class DependencyResolver:
    """
    Resolves structural semantic dependencies between
    extracted SemanticEntity objects.

    This class does NOT create BusinessStatement objects.

    Responsibility:

        SemanticEntity[]
                ↓
        SemanticDependency[]

    BusinessStatementBuilder is responsible for converting
    these dependencies/entities into BusinessStatement objects.
    """

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def resolve(
        self,
        entities: list[SemanticEntity],
    ) -> list[SemanticDependency]:
        """
        Resolve semantic dependencies.

        KPI and BKPI are intentionally handled separately.

        KPI:
            Operational / measurable performance indicator.

        BKPI:
            Business-level KPI / broader business outcome.

        They are NOT merged into the same semantic category.
        """

        if not entities:
            return []

        # ------------------------------------------------------
        # Validate input
        # ------------------------------------------------------

        valid_entities = [
            entity
            for entity in entities
            if isinstance(entity, SemanticEntity)
            and entity.entity_id
        ]

        if not valid_entities:
            return []

        # ------------------------------------------------------
        # Entity groups
        # ------------------------------------------------------

        actions = self._entities_of_type(
            valid_entities,
            "action",
        )

        targets = self._entities_of_type(
            valid_entities,
            "target",
            "object",
        )

        standards = self._entities_of_type(
            valid_entities,
            "standard",
        )

        methodologies = self._entities_of_type(
            valid_entities,
            "methodology",
        )

        skills = self._entities_of_type(
            valid_entities,
            "skill",
        )

        domains = self._entities_of_type(
            valid_entities,
            "domain",
        )

        # IMPORTANT:
        # Keep generic metrics separate from KPI/BKPI.
        metrics = self._entities_of_type(
            valid_entities,
            "metric",
        )

        kpis = self._entities_of_type(
            valid_entities,
            "kpi",
        )

        business_kpis = self._entities_of_type(
            valid_entities,
            "bkpi",
            "business_kpi",
        )

        measurements = self._entities_of_type(
            valid_entities,
            "measurement",
        )

        dependencies: list[SemanticDependency] = []

        # ======================================================
        # ACTION → TARGET
        # ======================================================

        for action in actions:

            relation = self._target_relation(action)

            if not relation:
                continue

            for target in targets:

                if not self._same_statement(
                    action,
                    target,
                ):
                    continue

                self._append_dependency(
                    dependencies,
                    source=action,
                    target=target,
                    relation=relation,
                    confidence=0.98,
                )

        # ======================================================
        # ACTION → STANDARD
        # ======================================================

        for action in actions:

            relation = self._standard_relation(action)

            if not relation:
                continue

            for standard in standards:

                if not self._same_statement(
                    action,
                    standard,
                ):
                    continue

                self._append_dependency(
                    dependencies,
                    source=action,
                    target=standard,
                    relation=relation,
                    confidence=0.99,
                )

        # ======================================================
        # ACTION → METHODOLOGY
        # ======================================================

        for action in actions:

            for methodology in methodologies:

                if not self._same_statement(
                    action,
                    methodology,
                ):
                    continue

                self._append_dependency(
                    dependencies,
                    source=action,
                    target=methodology,
                    relation="performed_using",
                    confidence=0.98,
                )

        # ======================================================
        # ACTION → SKILL
        # ======================================================

        for action in actions:

            for skill in skills:

                if not self._same_statement(
                    action,
                    skill,
                ):
                    continue

                self._append_dependency(
                    dependencies,
                    source=action,
                    target=skill,
                    relation="requires",
                    confidence=0.95,
                )

        # ======================================================
        # ACTION → GENERIC METRIC
        # ======================================================

        for action in actions:

            relation = self._metric_relation(action)

            if not relation:
                continue

            for metric in metrics:

                if not self._same_statement(
                    action,
                    metric,
                ):
                    continue

                self._append_dependency(
                    dependencies,
                    source=action,
                    target=metric,
                    relation=relation,
                    confidence=0.98,
                )

        # ======================================================
        # ACTION → KPI
        # ======================================================

        for action in actions:

            relation = self._metric_relation(action)

            if not relation:
                continue

            for kpi in kpis:

                if not self._same_statement(
                    action,
                    kpi,
                ):
                    continue

                self._append_dependency(
                    dependencies,
                    source=action,
                    target=kpi,
                    relation=relation,
                    confidence=0.98,
                )

        # ======================================================
        # ACTION → BKPI
        #
        # BKPI intentionally uses a different relationship.
        #
        # We do NOT pretend BKPI is simply another metric.
        # ======================================================

        for action in actions:

            relation = self._business_kpi_relation(action)

            if not relation:
                continue

            for business_kpi in business_kpis:

                if not self._same_statement(
                    action,
                    business_kpi,
                ):
                    continue

                self._append_dependency(
                    dependencies,
                    source=action,
                    target=business_kpi,
                    relation=relation,
                    confidence=0.96,
                )

        # ======================================================
        # METRIC → MEASUREMENT
        # ======================================================

        for metric in metrics:

            for measurement in measurements:

                if not self._same_statement(
                    metric,
                    measurement,
                ):
                    continue

                self._append_dependency(
                    dependencies,
                    source=metric,
                    target=measurement,
                    relation="measured_by",
                    confidence=0.95,
                )

        # ======================================================
        # KPI → MEASUREMENT
        # ======================================================

        for kpi in kpis:

            for measurement in measurements:

                if not self._same_statement(
                    kpi,
                    measurement,
                ):
                    continue

                self._append_dependency(
                    dependencies,
                    source=kpi,
                    target=measurement,
                    relation="measured_by",
                    confidence=0.95,
                )

        # ======================================================
        # TARGET → DOMAIN
        # ======================================================

        for target in targets:

            for domain in domains:

                if not self._same_statement(
                    target,
                    domain,
                ):
                    continue

                self._append_dependency(
                    dependencies,
                    source=target,
                    target=domain,
                    relation="belongs_to",
                    confidence=0.95,
                )

        # ======================================================
        # ACTION → DOMAIN
        # ======================================================

        for action in actions:

            for domain in domains:

                if not self._same_statement(
                    action,
                    domain,
                ):
                    continue

                self._append_dependency(
                    dependencies,
                    source=action,
                    target=domain,
                    relation="belongs_to",
                    confidence=0.95,
                )

        # ======================================================
        # RETURN
        # ======================================================

        return dependencies

    # ==========================================================
    # ENTITY FILTER
    # ==========================================================

    @staticmethod
    def _entities_of_type(
        entities: list[SemanticEntity],
        *entity_types: str,
    ) -> list[SemanticEntity]:
        """
        Return entities matching one of the supplied types.

        Matching is case-insensitive.
        """

        allowed = {
            entity_type.lower()
            for entity_type in entity_types
        }

        return [
            entity
            for entity in entities
            if entity.entity_type
            and entity.entity_type.lower() in allowed
        ]

    # ==========================================================
    # STATEMENT BOUNDARY
    # ==========================================================

    @staticmethod
    def _same_statement(
        source: SemanticEntity,
        target: SemanticEntity,
    ) -> bool:
        """
        Prevent dependencies from crossing statement boundaries.

        Missing statement IDs are treated as STATEMENT_1.
        """

        source_statement = (
            getattr(
                source,
                "statement_id",
                "",
            )
            or "STATEMENT_1"
        )

        target_statement = (
            getattr(
                target,
                "statement_id",
                "",
            )
            or "STATEMENT_1"
        )

        return source_statement == target_statement

    # ==========================================================
    # DUPLICATE PROTECTION
    # ==========================================================

    @staticmethod
    def _append_dependency(
        dependencies: list[SemanticDependency],
        source: SemanticEntity,
        target: SemanticEntity,
        relation: str,
        confidence: float,
    ) -> None:
        """
        Add a dependency unless an identical dependency
        already exists.
        """

        if not source.entity_id:
            return

        if not target.entity_id:
            return

        for existing in dependencies:

            if (
                existing.source_entity
                == source.entity_id
                and existing.target_entity
                == target.entity_id
                and existing.relation
                == relation
            ):
                return

        effective_confidence = min(
            source.confidence,
            target.confidence,
            confidence,
        )

        dependencies.append(
            SemanticDependency(
                source_entity=source.entity_id,
                target_entity=target.entity_id,
                relation=relation,
                confidence=effective_confidence,
                metadata={
                    "source_type": source.entity_type,
                    "target_type": target.entity_type,
                    "statement_id": (
                        getattr(
                            source,
                            "statement_id",
                            "",
                        )
                        or "STATEMENT_1"
                    ),
                },
            )
        )

    # ==========================================================
    # ACTION → TARGET
    # ==========================================================

    @staticmethod
    def _target_relation(
        action: SemanticEntity,
    ) -> str | None:

        mapping = {
            "implement": "targets",
            "develop": "creates",
            "manage": "manages",
            "lead": "manages",
            "monitor": "monitors",
            "maintain": "maintains",
            "improve": "optimizes",
            "optimize": "optimizes",
            "reduce": "optimizes",
            "increase": "improves",
            "control": "controls",
            "perform": "executes",
            "certify": "certifies",
        }

        canonical = (
            action.canonical or ""
        ).strip().lower()

        return mapping.get(canonical)

    # ==========================================================
    # ACTION → STANDARD
    # ==========================================================

    @staticmethod
    def _standard_relation(
        action: SemanticEntity,
    ) -> str | None:

        mapping = {
            "implement": "complies_with",
            "develop": "complies_with",
            "certify": "certified_against",
            "audit": "audited_against",
        }

        canonical = (
            action.canonical or ""
        ).strip().lower()

        return mapping.get(canonical)

    # ==========================================================
    # ACTION → KPI / METRIC
    # ==========================================================

    @staticmethod
    def _metric_relation(
        action: SemanticEntity,
    ) -> str | None:

        mapping = {
            "improve": "improved",
            "reduce": "reduced",
            "increase": "increased",
            "optimize": "optimized",
            "monitor": "measures",
            "manage": "measured_by",
            "lead": "measured_by",
        }

        canonical = (
            action.canonical or ""
        ).strip().lower()

        return mapping.get(canonical)

    # ==========================================================
    # ACTION → BKPI
    # ==========================================================

    @staticmethod
    def _business_kpi_relation(
        action: SemanticEntity,
    ) -> str | None:
        """
        Determine how an action relates to a Business KPI.

        BKPI represents a broader business outcome, therefore
        it is intentionally not treated identically to KPI.
        """

        mapping = {
            "improve": "contributes_to",
            "reduce": "contributes_to",
            "increase": "contributes_to",
            "optimize": "contributes_to",
            "monitor": "supports",
            "manage": "supports",
            "lead": "supports",
        }

        canonical = (
            action.canonical or ""
        ).strip().lower()

        return mapping.get(canonical)