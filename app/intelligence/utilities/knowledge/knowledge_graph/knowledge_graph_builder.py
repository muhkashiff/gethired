"""
Enterprise Knowledge Graph Builder

Enterprise V6
"""

from app.intelligence.utilities.knowledge.knowledge_graph.knowledge_graph import (
    KnowledgeGraph,
)

from app.intelligence.utilities.knowledge.knowledge_graph.builders.builder_registry import (
    BuilderRegistry,
)


class KnowledgeGraphBuilder:

    def __init__(self):

        self.registry = BuilderRegistry()

    # ---------------------------------------------------------

    def build(
        self,
        document,
        semantic_result=None,
    ):

        graph = KnowledgeGraph()

        # ---------------------------------------------
        # Build Nodes
        # ---------------------------------------------

        for fact in document.facts:

            for builder in self.registry.node_builders:

                builder.build(

                    graph,

                    fact,

                )

        # ---------------------------------------------
        # Build Edges
        # ---------------------------------------------

        for fact in document.facts:

            for builder in self.registry.edge_builders:

                builder.build(

                    graph,

                    fact,

                )

        return graph