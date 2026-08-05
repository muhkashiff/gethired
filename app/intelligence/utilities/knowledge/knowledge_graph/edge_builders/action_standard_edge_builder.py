"""
Enterprise Action → Standard Edge Builder

Creates

Action --------complies_with--------> Standard

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_edge_builder import (
    BaseEdgeBuilder,
)


class ActionStandardEdgeBuilder(BaseEdgeBuilder):

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

        standards = getattr(
            statement,
            "standards",
            [],
        )

        if not actions:
            return

        if not standards:
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

            for standard in standards:

                if standard is None:
                    continue

                if not getattr(
                    standard,
                    "found",
                    False,
                ):
                    continue

                edge = self.create_edge(

                    source=action,

                    target=standard,

                    relation="complies_with",

                    reasoning="Action implements standard",

                    confidence=min(
                        action.confidence,
                        standard.confidence,
                    ),

                )

                self.register_edge(

                    context,

                    edge,

                )