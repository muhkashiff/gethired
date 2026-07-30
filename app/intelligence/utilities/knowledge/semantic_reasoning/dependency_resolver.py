"""
Business Semantic Dependency Resolver

Builds semantic relationships between extracted entities.

This is NOT a grammatical dependency parser.

Instead it creates business relationships such as

Implemented ---> targets ---> ISO9001

Improved ---> affects ---> Production Yield

Managed ---> manages ---> Team

Reduced ---> optimizes ---> Customer Satisfaction
"""

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    DependencyEdge,
)


class DependencyResolver:

    def resolve(self, entities):

        dependencies = []

        actions = [
            e for e in entities
            if e.entity_type == "action"
        ]

        objects = [
            e for e in entities
            if e.entity_type == "object"
        ]

        metrics = [
            e for e in entities
            if e.entity_type in ("metric", "kpi")
        ]

        methodologies = [
            e for e in entities
            if e.entity_type == "methodology"
        ]

        domains = [
            e for e in entities
            if e.entity_type == "domain"
        ]

        skills = [
            e for e in entities
            if e.entity_type == "skill"
        ]

        standards = [
            e for e in entities
            if e.entity_type == "standard"
        ]

        # ----------------------------------------
        # Action -> Object
        # ----------------------------------------

        for action in actions:

            for obj in objects:

                relation = self._action_object_relation(action)

                if relation:

                    dependencies.append(

                        DependencyEdge(

                            source_entity=action.entity_id,

                            target_entity=obj.entity_id,

                            relation=relation,

                            confidence=0.98,

                        )

                    )

        # ----------------------------------------
        # Action -> KPI / Metric
        # ----------------------------------------

        for action in actions:

            for metric in metrics:

                relation = self._action_metric_relation(action)

                if relation:

                    dependencies.append(

                        DependencyEdge(

                            source_entity=action.entity_id,

                            target_entity=metric.entity_id,

                            relation=relation,

                            confidence=0.98,

                        )

                    )

        # ----------------------------------------
        # Action -> Methodology
        # ----------------------------------------

        for action in actions:

            for methodology in methodologies:

                dependencies.append(

                    DependencyEdge(

                        source_entity=action.entity_id,

                        target_entity=methodology.entity_id,

                        relation="achieved_using",

                        confidence=0.98,

                    )

                )

        # ----------------------------------------
        # Object -> Domain
        # ----------------------------------------

        for obj in objects:

            for domain in domains:

                dependencies.append(

                    DependencyEdge(

                        source_entity=obj.entity_id,

                        target_entity=domain.entity_id,

                        relation="belongs_to",

                        confidence=0.95,

                    )

                )

        # ----------------------------------------
        # Action -> Skill
        # ----------------------------------------

        for action in actions:

            for skill in skills:

                dependencies.append(

                    DependencyEdge(

                        source_entity=action.entity_id,

                        target_entity=skill.entity_id,

                        relation="requires",

                        confidence=0.95,

                    )

                )

        # ----------------------------------------
        # Action -> Standard
        # ----------------------------------------

        for action in actions:

            for standard in standards:

                dependencies.append(

                    DependencyEdge(

                        source_entity=action.entity_id,

                        target_entity=standard.entity_id,

                        relation="targets",

                        confidence=0.98,

                    )

                )

        return dependencies

    # ===================================================
    # Relationship Rules
    # ===================================================

    def _action_object_relation(self, action):

        verb = action.canonical.lower()

        mapping = {

            "implement": "targets",

            "develop": "creates",

            "lead": "manages",

            "manage": "manages",

            "improve": "optimizes",

            "optimize": "optimizes",

            "reduce": "optimizes",

            "increase": "improves",

            "certify": "certifies",

            "perform": "executes",

            "design": "creates",

            "build": "creates",

            "monitor": "monitors",

            "control": "controls",

            "maintain": "maintains",

        }

        return mapping.get(verb)

    def _action_metric_relation(self, action):

        verb = action.canonical.lower()

        mapping = {

            "improve": "affects",

            "reduce": "affects",

            "increase": "affects",

            "lead": "measured_by",

            "manage": "measured_by",

        }

        return mapping.get(verb)