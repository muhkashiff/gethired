"""
Enterprise Graph Validator

Validates graph integrity before reasoning.

Runs AFTER

    All Builders

Runs BEFORE

    Graph Optimizer

Enterprise V7
"""

from collections import Counter


class GraphValidator:

    ####################################################################
    # BUILD
    ####################################################################

    def build(

        self,

        graph,

    ):

        report = {

            "valid": True,

            "errors": [],

            "warnings": [],

        }

        # ---------------------------------------------------------
        # Validate Nodes
        # ---------------------------------------------------------

        self._validate_nodes(

            graph,

            report,

        )

        # ---------------------------------------------------------
        # Validate Edges
        # ---------------------------------------------------------

        self._validate_edges(

            graph,

            report,

        )

        # ---------------------------------------------------------
        # Validate Duplicate Edges
        # ---------------------------------------------------------

        self._validate_duplicate_edges(

            graph,

            report,

        )

        # ---------------------------------------------------------
        # Validate Orphan Nodes
        # ---------------------------------------------------------

        self._validate_orphans(

            graph,

            report,

        )

        report["valid"] = (

            len(report["errors"]) == 0

        )

        graph.statistics.validation_report = report

        return report

    ####################################################################
    # NODE VALIDATION
    ####################################################################

    def _validate_nodes(

        self,

        graph,

        report,

    ):

        for node in graph.get_nodes():

            if not node.node_id:

                report["errors"].append(

                    "Node missing node_id."

                )

            if not node.entity_type:

                report["errors"].append(

                    f"{node.node_id} missing entity_type."

                )

            if not node.label:

                report["warnings"].append(

                    f"{node.node_id} missing label."

                )

    ####################################################################
    # EDGE VALIDATION
    ####################################################################

    def _validate_edges(

        self,

        graph,

        report,

    ):

        for edge in graph.get_edges():

            if graph.get_node(edge.source_id) is None:

                report["errors"].append(

                    f"Missing source node: {edge.source_id}"

                )

            if graph.get_node(edge.target_id) is None:

                report["errors"].append(

                    f"Missing target node: {edge.target_id}"

                )

            if not edge.relation:

                report["errors"].append(

                    f"{edge.edge_id} missing relation."

                )

    ####################################################################
    # DUPLICATE EDGE VALIDATION
    ####################################################################

    def _validate_duplicate_edges(

        self,

        graph,

        report,

    ):

        edge_counter = Counter(

            edge.edge_id

            for edge in graph.get_edges()

        )

        duplicates = [

            edge_id

            for edge_id, count

            in edge_counter.items()

            if count > 1

        ]

        for edge_id in duplicates:

            report["warnings"].append(

                f"Duplicate edge detected: {edge_id}"

            )

    ####################################################################
    # ORPHAN NODE VALIDATION
    ####################################################################

    def _validate_orphans(

        self,

        graph,

        report,

    ):

        for node in graph.get_nodes():

            if (

                len(node.incoming_edges) == 0

                and

                len(node.outgoing_edges) == 0

            ):

                report["warnings"].append(

                    f"Orphan node: {node.node_id}"

                )