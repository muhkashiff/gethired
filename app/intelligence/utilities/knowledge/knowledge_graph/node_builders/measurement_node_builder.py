"""
Enterprise Measurement Node Builder

Creates Measurement Nodes from Business Statements.

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_node_builder import (
    BaseNodeBuilder,
)


class MeasurementNodeBuilder(BaseNodeBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        ################################################################
        # Business Statement may contain multiple Measurements
        ################################################################

        measurements = getattr(
            statement,
            "measurements",
            [],
        )

        if not measurements:
            return

        ################################################################
        # Create Measurement Nodes
        ################################################################

        for measurement in measurements:

            if measurement is None:
                continue

            if not getattr(
                measurement,
                "found",
                False,
            ):
                continue

            node = self.create_node(

                entity=measurement,

                entity_type="Measurement",

            )

            self.register_node(

                context,

                node,

            )