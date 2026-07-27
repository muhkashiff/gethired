"""
Node Factory

Creates graph nodes while preventing duplicates.
"""

from .graph_models import GraphNode


class NodeFactory:

    def __init__(self):

        self.cache = {}

    # -----------------------------------------------------

    def create(
        self,
        node_type,
        label,
        attributes=None,
    ):

        attributes = attributes or {}

        key = (node_type.lower(), label.lower())

        if key in self.cache:

            return self.cache[key]

        node = GraphNode(

            id=f"{node_type}_{len(self.cache)+1}",

            label=label,

            node_type=node_type,

            attributes=attributes,

        )

        self.cache[key] = node

        return node

    # -----------------------------------------------------

    def all_nodes(self):

        return list(self.cache.values())