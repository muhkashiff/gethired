"""
Enterprise Domain Node Builder

Creates Domain Nodes from Business Statements.

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_node_builder import (
    BaseNodeBuilder,
)


class DomainNodeBuilder(BaseNodeBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        ################################################################
        # Business Statement may contain multiple Domains
        ################################################################

        domains = getattr(
            statement,
            "domains",
            [],
        )

        if not domains:
            return

        ################################################################
        # Create Domain Nodes
        ################################################################

        for domain in domains:

            if domain is None:
                continue

            if not getattr(
                domain,
                "found",
                False,
            ):
                continue

            node = self.create_node(

                entity=domain,

                entity_type="Domain",

            )

            self.register_node(

                context,

                node,

            )