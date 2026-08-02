"""
Skill Node Builder
"""

from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.base_node_builder import (
    BaseNodeBuilder,
)


class SkillNodeBuilder(BaseNodeBuilder):

    def build(self, graph, fact):

        interpretation = getattr(fact, "interpretation", None)

        if interpretation is None:
            return

        for entity in interpretation.entities:

            if entity.entity_type.lower() != "skill":
                continue

            node = self.create_node(

                entity=entity,

                entity_type="Skill",

            )

            self.register_node(graph, node)