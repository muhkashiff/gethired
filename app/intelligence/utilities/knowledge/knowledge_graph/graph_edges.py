"""
Edge Factory

Creates graph relationships.
"""

from .graph_models import GraphEdge


class EdgeFactory:

    def __init__(self):

        self.edges = []

    # --------------------------------------------------

    def connect(

        self,

        source,

        relation,

        target,

        confidence=1.0,

    ):

        edge = GraphEdge(

            source=source.id,

            target=target.id,

            relation=relation,

            confidence=confidence,

        )

        self.edges.append(edge)

        return edge