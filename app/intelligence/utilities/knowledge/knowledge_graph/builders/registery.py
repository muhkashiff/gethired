"""
Enterprise Builder Registry

Automatically loads plugins.

Enterprise V7
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.loader import (
    PluginLoader,
)

import app.intelligence.utilities.knowledge.knowledge_graph.node_builders as node_pkg

import app.intelligence.utilities.knowledge.knowledge_graph.edge_builders as edge_pkg


class BuilderRegistry:

    def __init__(self):

        self.node_builders = PluginLoader.load(

            node_pkg

        )

        self.edge_builders = PluginLoader.load(

            edge_pkg
        )