"""
Enterprise Graph Validation API

Enterprise Version

Provides read-only validation of the KnowledgeGraph.

Responsibilities
----------------
• Validate graph node integrity
• Validate graph edge integrity
• Detect missing source/target nodes
• Detect duplicate node IDs
• Detect duplicate edges
• Detect invalid graph references
• Keep validation modular
• Prevent callers from directly accessing graph internals

Architecture

KnowledgeGraph
      ↓
GraphValidation
      ↓
GraphAPI
"""


class GraphValidation:

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, graph):

        self.graph = graph

    # ==========================================================
    # MAIN VALIDATION API
    # ==========================================================

    def validate(self):
        """
        Validate the complete KnowledgeGraph.

        Returns
        -------
        dict

        Example:

        {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        """

        if self.graph is None:

            return {
                "valid": True,
                "errors": [],
                "warnings": [],
            }

        errors = []

        warnings = []

        # ------------------------------------------------------
        # Validate nodes
        # ------------------------------------------------------

        self._validate_nodes(
            errors,
            warnings,
        )

        # ------------------------------------------------------
        # Validate edges
        # ------------------------------------------------------

        self._validate_edges(
            errors,
            warnings,
        )

        # ------------------------------------------------------
        # Validate indexes
        # ------------------------------------------------------

        self._validate_indexes(
            errors,
            warnings,
        )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    # ==========================================================
    # NODE VALIDATION
    # ==========================================================

    def _validate_nodes(
        self,
        errors,
        warnings,
    ):
        """
        Validate graph nodes.
        """

        if not hasattr(
            self.graph,
            "nodes",
        ):
            errors.append(
                "KnowledgeGraph has no nodes collection."
            )
            return

        seen_ids = set()

        for node_id, node in self.graph.nodes.items():

            # --------------------------------------------------
            # Node ID consistency
            # --------------------------------------------------

            if node_id in seen_ids:

                errors.append(
                    f"Duplicate node ID: {node_id}"
                )

            seen_ids.add(
                node_id
            )

            # --------------------------------------------------
            # Node object
            # --------------------------------------------------

            if node is None:

                errors.append(
                    f"Node '{node_id}' is None."
                )

                continue

            # --------------------------------------------------
            # Internal ID consistency
            # --------------------------------------------------

            actual_node_id = getattr(
                node,
                "node_id",
                None,
            )

            if actual_node_id != node_id:

                errors.append(
                    "Node dictionary key does not "
                    f"match node.node_id: {node_id}"
                )

            # --------------------------------------------------
            # Entity ID
            # --------------------------------------------------

            entity_id = getattr(
                node,
                "entity_id",
                None,
            )

            if not entity_id:

                warnings.append(
                    f"Node '{node_id}' has no entity_id."
                )

            # --------------------------------------------------
            # Entity type
            # --------------------------------------------------

            entity_type = getattr(
                node,
                "entity_type",
                "",
            )

            if not entity_type:

                warnings.append(
                    f"Node '{node_id}' has no entity_type."
                )

    # ==========================================================
    # EDGE VALIDATION
    # ==========================================================

    def _validate_edges(
        self,
        errors,
        warnings,
    ):
        """
        Validate graph edges.
        """

        if not hasattr(
            self.graph,
            "edges",
        ):
            errors.append(
                "KnowledgeGraph has no edges collection."
            )
            return

        seen_edges = set()

        for edge in self.graph.edges:

            if edge is None:

                errors.append(
                    "Graph contains a None edge."
                )

                continue

            source_id = getattr(
                edge,
                "source_id",
                None,
            )

            target_id = getattr(
                edge,
                "target_id",
                None,
            )

            relation = getattr(
                edge,
                "relation",
                None,
            )

            # --------------------------------------------------
            # Required edge information
            # --------------------------------------------------

            if not source_id:

                errors.append(
                    "Edge has no source_id."
                )

            if not target_id:

                errors.append(
                    "Edge has no target_id."
                )

            if not relation:

                errors.append(
                    "Edge has no relation."
                )

            # --------------------------------------------------
            # Source node must exist
            # --------------------------------------------------

            if (
                source_id
                and source_id not in self.graph.nodes
            ):

                errors.append(
                    "Edge source node does not exist: "
                    f"{source_id}"
                )

            # --------------------------------------------------
            # Target node must exist
            # --------------------------------------------------

            if (
                target_id
                and target_id not in self.graph.nodes
            ):

                errors.append(
                    "Edge target node does not exist: "
                    f"{target_id}"
                )

            # --------------------------------------------------
            # Duplicate edge detection
            # --------------------------------------------------

            edge_key = (
                source_id,
                target_id,
                relation,
            )

            if edge_key in seen_edges:

                errors.append(
                    "Duplicate edge detected: "
                    f"{source_id} -> "
                    f"{target_id} "
                    f"[{relation}]"
                )

            seen_edges.add(
                edge_key
            )

    # ==========================================================
    # INDEX VALIDATION
    # ==========================================================

    def _validate_indexes(
        self,
        errors,
        warnings,
    ):
        """
        Validate the graph's internal lookup indexes.
        """

        # ------------------------------------------------------
        # nodes_by_type
        # ------------------------------------------------------

        nodes_by_type = getattr(
            self.graph,
            "nodes_by_type",
            {},
        )

        for entity_type, indexed_nodes in (
            nodes_by_type.items()
        ):

            for node_id, node in indexed_nodes.items():

                if node_id not in self.graph.nodes:

                    errors.append(
                        "nodes_by_type contains "
                        f"unknown node: {node_id}"
                    )

                    continue

                actual_type = getattr(
                    node,
                    "entity_type",
                    "",
                ).lower()

                if actual_type != entity_type.lower():

                    errors.append(
                        "nodes_by_type index mismatch "
                        f"for node: {node_id}"
                    )

        # ------------------------------------------------------
        # edges_by_relation
        # ------------------------------------------------------

        edges_by_relation = getattr(
            self.graph,
            "edges_by_relation",
            {},
        )

        graph_edges = set(
            id(edge)
            for edge in self.graph.edges
        )

        for relation, indexed_edges in (
            edges_by_relation.items()
        ):

            for edge in indexed_edges:

                if id(edge) not in graph_edges:

                    errors.append(
                        "edges_by_relation contains "
                        "an edge not present in graph.edges."
                    )

                actual_relation = getattr(
                    edge,
                    "relation",
                    "",
                ).lower()

                if actual_relation != relation.lower():

                    errors.append(
                        "edges_by_relation index mismatch "
                        f"for relation: {relation}"
                    )

    # ==========================================================
    # CONVENIENCE CHECK
    # ==========================================================

    def is_valid(self):
        """
        Return True when the graph passes validation.
        """

        result = self.validate()

        return result["valid"]

    # ==========================================================
    # ERRORS ONLY
    # ==========================================================

    def errors(self):
        """
        Return validation errors only.
        """

        result = self.validate()

        return result["errors"]

    # ==========================================================
    # WARNINGS ONLY
    # ==========================================================

    def warnings(self):
        """
        Return validation warnings only.
        """

        result = self.validate()

        return result["warnings"]