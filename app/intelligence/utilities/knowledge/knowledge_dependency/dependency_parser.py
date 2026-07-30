"""
Dependency Parser

Builds semantic relationships between extracted entities.

SentenceParser extracts entities.
DependencyParser decides how they relate.
KnowledgeGraphBuilder only persists these relationships.
"""

from app.intelligence.utilities.knowledge.knowledge_models import (
    DependencyEdge,
)


class DependencyParser:

    def __init__(self):
        pass

    # ----------------------------------------------------------

    def build(self, entities, sentence):

        edges = []

        actions = self._filter(entities, "action")
        objects = self._filter(entities, "object")
        metrics = self._filter(entities, "metric")
        measurements = self._filter(entities, "measurement")
        domains = self._filter(entities, "domain")
        standards = self._filter(entities, "standard")
        technologies = self._filter(entities, "technology")
        practices = self._filter(entities, "practice")
        methodologies = self._filter(entities, "methodology")
        skills = self._filter(entities, "skill")
        numbers = self._filter(entities, "number")

        # --------------------------------------------------
        # Action -> Object
        # --------------------------------------------------

        for action in actions:
            for obj in objects:

                relation = self._action_object_relation(action)

                edges.append(

                    DependencyEdge(

                        source_entity=action.entity_id,
                        target_entity=obj.entity_id,

                        relation=relation,

                        confidence=0.95,

                    )

                )

        # --------------------------------------------------
        # Action -> Metric
        # --------------------------------------------------

        for action in actions:
            for metric in metrics:

                edges.append(

                    DependencyEdge(

                        source_entity=action.entity_id,
                        target_entity=metric.entity_id,

                        relation="affects",

                        confidence=0.98,

                    )

                )

        # --------------------------------------------------
        # Metric -> Measurement
        # --------------------------------------------------

        for metric in metrics:
            for measurement in measurements:

                edges.append(

                    DependencyEdge(

                        source_entity=metric.entity_id,
                        target_entity=measurement.entity_id,

                        relation="measured_by",

                        confidence=0.99,

                    )

                )

        # --------------------------------------------------
        # Object -> Domain
        # --------------------------------------------------

        for obj in objects:
            for domain in domains:

                if self._same_category(obj, domain):

                    edges.append(

                        DependencyEdge(

                            source_entity=obj.entity_id,
                            target_entity=domain.entity_id,

                            relation="belongs_to",

                            confidence=0.96,

                        )

                    )

        # --------------------------------------------------
        # Standard -> Domain
        # --------------------------------------------------

        for standard in standards:
            for domain in domains:

                if self._same_category(standard, domain):

                    edges.append(

                        DependencyEdge(

                            source_entity=standard.entity_id,
                            target_entity=domain.entity_id,

                            relation="belongs_to",

                            confidence=0.98,

                        )

                    )

        # --------------------------------------------------
        # Action -> Methodology
        # --------------------------------------------------

        for action in actions:
            for methodology in methodologies:

                edges.append(

                    DependencyEdge(

                        source_entity=action.entity_id,
                        target_entity=methodology.entity_id,

                        relation="achieved_using",

                        confidence=0.95,

                    )

                )

        # --------------------------------------------------
        # Action -> Practice
        # --------------------------------------------------

        for action in actions:
            for practice in practices:

                edges.append(

                    DependencyEdge(

                        source_entity=action.entity_id,
                        target_entity=practice.entity_id,

                        relation="achieved_using",

                        confidence=0.95,

                    )

                )

        # --------------------------------------------------
        # Action -> Technology
        # --------------------------------------------------

        for action in actions:
            for technology in technologies:

                edges.append(

                    DependencyEdge(

                        source_entity=action.entity_id,
                        target_entity=technology.entity_id,

                        relation="uses",

                        confidence=0.94,

                    )

                )

        # --------------------------------------------------
        # Action -> Skill
        # --------------------------------------------------

        for action in actions:
            for skill in skills:

                edges.append(

                    DependencyEdge(

                        source_entity=action.entity_id,
                        target_entity=skill.entity_id,

                        relation="requires",

                        confidence=0.93,

                    )

                )

        # --------------------------------------------------
        # Object -> Number
        # (Team -> 35)
        # --------------------------------------------------

        for obj in objects:
            for number in numbers:

                edges.append(

                    DependencyEdge(

                        source_entity=obj.entity_id,
                        target_entity=number.entity_id,

                        relation="counts",

                        confidence=0.97,

                    )

                )

        return edges

    # ======================================================

    def _filter(self, entities, entity_type):

        return [

            entity

            for entity in entities

            if entity.entity_type == entity_type

        ]

    # ======================================================

    def _same_category(self, entity, domain):

        return (

            entity.category != ""

            and entity.category.lower()

            == domain.category.lower()

        )

    # ======================================================

    def _action_object_relation(self, action):

        category = action.category.lower()

        mapping = {

            "leadership": "manages",

            "management": "manages",

            "implementation": "targets",

            "improvement": "improves",

            "optimization": "optimizes",

            "achievement": "achieves",

            "certification": "certifies",

            "development": "develops",

        }

        return mapping.get(category, "targets")