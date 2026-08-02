"""
Enterprise Graph ID Generator

Generates deterministic IDs for Graph Nodes and Graph Edges.

Enterprise V5

Examples

ACT_IMPLEMENT
    ↓
NODE_ACT_IMPLEMENT

EDGE_NODE_ACT_IMPLEMENT_NODE_STD_FSSC22000

"""

import hashlib


class GraphIDGenerator:
    """
    Centralized ID generator.

    Every node and edge inside the Knowledge Graph
    should be created through this class.
    """

    # ---------------------------------------------------------

    @staticmethod
    def node_id(entity_type: str, entity_id: str) -> str:
        """
        Create deterministic node id.

        Example

        Action + ACT_IMPLEMENT

        →

        NODE_ACTION_ACT_IMPLEMENT
        """

        entity_type = (entity_type or "UNKNOWN").upper()
        entity_id = (entity_id or "UNKNOWN").upper()

        return f"NODE_{entity_type}_{entity_id}"

    # ---------------------------------------------------------

    @staticmethod
    def edge_id(source_id: str,
                relation: str,
                target_id: str) -> str:
        """
        Create deterministic edge id.

        Example

        NODE_ACTION_ACT_IMPLEMENT
                +
            COMPLIES_WITH
                +
        NODE_STANDARD_STD_FSSC22000

        →
        EDGE_91A37D83B6
        """

        raw = f"{source_id}|{relation}|{target_id}"

        digest = hashlib.sha1(
            raw.encode("utf-8")
        ).hexdigest()[:10].upper()

        return f"EDGE_{digest}"