"""
Enterprise Action → Target Edge Builder

Parser Layer
------------
Object

Business Layer
--------------
Target

Creates

Action --------acts_on--------> Target

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_edge_builder import (
    BaseEdgeBuilder,
)


class ActionObjectEdgeBuilder(BaseEdgeBuilder):

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
        #
        # NOTE:
        # Parser extracts "Object".
        #
        # BusinessStatement exposes these Objects as
        # business Targets.
        ################################################################

        actions = getattr(
            statement,
            "actions",
            [],
        )

        targets = getattr(
            statement,
            "targets",
            [],
        )

        if not actions:
            return

        if not targets:
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

            for target in targets:

                if target is None:
                    continue

                if not getattr(
                    target,
                    "found",
                    False,
                ):
                    continue

                edge = self.create_edge(

                    source=action,

                    target=target,

                    relation="acts_on",

                    reasoning="Action acts on business target",

                    confidence=min(
                        action.confidence,
                        target.confidence,
                    ),

                )

                self.register_edge(

                    context,

                    edge,

                )