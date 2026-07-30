"""
Advanced Business Dependency Resolver V2

Creates business-aware semantic relationships between entities.
"""

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticDependency,
)


class DependencyResolver:

    def resolve(self, entities):

        dependencies = []

        actions = [e for e in entities if e.entity_type == "action"]
        objects = [e for e in entities if e.entity_type == "object"]
        standards = [e for e in entities if e.entity_type == "standard"]
        methodologies = [e for e in entities if e.entity_type == "methodology"]
        skills = [e for e in entities if e.entity_type == "skill"]
        domains = [e for e in entities if e.entity_type == "domain"]
        kpis = [
            e
            for e in entities
            if e.entity_type in ("kpi", "metric")
        ]
        measurements = [
            e
            for e in entities
            if e.entity_type == "measurement"
        ]

        # ==================================================
        # Action -> Object
        # ==================================================

        for action in actions:

            relation = self._object_relation(action)

            if relation:

                for obj in objects:

                    dependencies.append(
                        SemanticDependency(
                            source_entity=action.entity_id,
                            target_entity=obj.entity_id,
                            relation=relation,
                            confidence=0.98,
                        )
                    )

        # ==================================================
        # Action -> Standard
        # ==================================================

        for action in actions:

            relation = self._standard_relation(action)

            if relation:

                for standard in standards:

                    dependencies.append(
                        SemanticDependency(
                            source_entity=action.entity_id,
                            target_entity=standard.entity_id,
                            relation=relation,
                            confidence=0.99,
                        )
                    )

        # ==================================================
        # Action -> Methodology
        # ==================================================

        for action in actions:

            for methodology in methodologies:

                dependencies.append(
                    SemanticDependency(
                        source_entity=action.entity_id,
                        target_entity=methodology.entity_id,
                        relation="performed_using",
                        confidence=0.98,
                    )
                )

        # ==================================================
        # Action -> KPI
        # ==================================================

        for action in actions:

            relation = self._kpi_relation(action)

            if relation:

                for kpi in kpis:

                    dependencies.append(
                        SemanticDependency(
                            source_entity=action.entity_id,
                            target_entity=kpi.entity_id,
                            relation=relation,
                            confidence=0.98,
                        )
                    )

        # ==================================================
        # KPI -> Measurement
        # ==================================================

        for kpi in kpis:

            for measurement in measurements:

                dependencies.append(
                    SemanticDependency(
                        source_entity=kpi.entity_id,
                        target_entity=measurement.entity_id,
                        relation="measured_by",
                        confidence=0.95,
                    )
                )

        # ==================================================
        # Object -> Domain
        # ==================================================

        for obj in objects:

            for domain in domains:

                dependencies.append(
                    SemanticDependency(
                        source_entity=obj.entity_id,
                        target_entity=domain.entity_id,
                        relation="belongs_to",
                        confidence=0.95,
                    )
                )

        # ==================================================
        # Action -> Skill
        # ==================================================

        for action in actions:

            for skill in skills:

                dependencies.append(
                    SemanticDependency(
                        source_entity=action.entity_id,
                        target_entity=skill.entity_id,
                        relation="requires",
                        confidence=0.95,
                    )
                )

        # ==================================================
        # Remove duplicate edges
        # ==================================================

        unique = {}

        for edge in dependencies:

            key = (
                edge.source_entity,
                edge.target_entity,
                edge.relation,
            )

            if key not in unique:
                unique[key] = edge

        return list(unique.values())

    # ======================================================

    def _object_relation(self, action):

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

        return mapping.get(action.canonical.lower())

    # ======================================================

    def _standard_relation(self, action):

        mapping = {

            "implement": "complies_with",

            "develop": "complies_with",

            "certify": "certified_against",

            "audit": "audited_against",

        }

        return mapping.get(action.canonical.lower())

    # ======================================================

    def _kpi_relation(self, action):

        mapping = {

            "improve": "improved",

            "reduce": "reduced",

            "increase": "increased",

            "optimize": "optimized",

            "monitor": "measures",

            "manage": "measured_by",

            "lead": "measured_by",

        }

        return mapping.get(action.canonical.lower())