"""
Semantic Graph Builder

Creates semantic graph nodes and edges
from KnowledgeInterpretation.
"""

from app.intelligence.utilities.knowledge.knowledge_dependency.dependency_models import (
    DependencyEdge,
)


class SemanticGraphBuilder:

    def build(self, interpretation):

        edges = []

        action = interpretation.action

        obj = interpretation.object

        practice = interpretation.practice

        metric = interpretation.metric

        # --------------------------------------------------

        if action.found and obj.found:

            edges.append(

                DependencyEdge(

                    source_entity=action.entity_id,

                    target_entity=obj.entity_id,

                    relation="targets",

                    confidence=0.95,

                )

            )

        # --------------------------------------------------

        if action.found and practice.found:

            edges.append(

                DependencyEdge(

                    source_entity=action.entity_id,

                    target_entity=practice.entity_id,

                    relation="achieved_using",

                    confidence=0.95,

                )

            )

        # --------------------------------------------------

        if obj.found and metric.found:

            edges.append(

                DependencyEdge(

                    source_entity=obj.entity_id,

                    target_entity=metric.entity_id,

                    relation="measured_by",

                    confidence=0.95,

                )

            )

        return edges