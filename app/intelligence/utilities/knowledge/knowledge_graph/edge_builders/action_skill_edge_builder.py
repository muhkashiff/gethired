"""
Enterprise Action → Skill Edge Builder

Creates

Action --------requires--------> Skill

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_edge_builder import (
    BaseEdgeBuilder,
)


class ActionSkillEdgeBuilder(BaseEdgeBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        ################################################################
        # Read Business Statement Collections
        ################################################################

        actions = getattr(
            statement,
            "actions",
            [],
        )

        skills = getattr(
            statement,
            "skills",
            [],
        )

        if not actions:
            return

        if not skills:
            return

        ################################################################
        # Create Edges
        ################################################################

        for action in actions:

            if action is None:
                continue

            if not getattr(
                action,
                "found",
                False,
            ):
                continue

            for skill in skills:

                if skill is None:
                    continue

                if not getattr(
                    skill,
                    "found",
                    False,
                ):
                    continue

                edge = self.create_edge(

                    source=action,

                    target=skill,

                    relation="requires",

                    reasoning="Action requires skill",

                    confidence=min(
                        action.confidence,
                        skill.confidence,
                    ),

                )

                self.register_edge(

                    context,

                    edge,

                )