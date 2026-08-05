"""
Enterprise Skill Node Builder

Creates Skill Nodes from Business Statements.

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_node_builder import (
    BaseNodeBuilder,
)


class SkillNodeBuilder(BaseNodeBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        ################################################################
        # Business Statement may contain multiple Skills
        ################################################################

        skills = getattr(
            statement,
            "skills",
            [],
        )

        if not skills:
            return

        ################################################################
        # Create Skill Nodes
        ################################################################

        for skill in skills:

            if skill is None:
                continue

            if not getattr(
                skill,
                "found",
                False,
            ):
                continue

            node = self.create_node(

                entity=skill,

                entity_type="Skill",

            )

            self.register_node(

                context,

                node,

            )