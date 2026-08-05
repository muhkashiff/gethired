"""
Enterprise Knowledge Graph

Enterprise V10

Central graph object.

Stores:

    Nodes
    Edges

Provides:

    Entity API
    Relation API
    Traversal API

BusinessStatement
        ↓
Node Builders
        ↓
Edge Builders
        ↓
Semantic Builders
        ↓
KnowledgeGraph
"""

from collections import defaultdict

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphNode,
    GraphEdge,
    GraphStatistics,
)


class KnowledgeGraph:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        ###############################################################
        # Graph Storage
        ###############################################################

        self.nodes: dict[str, GraphNode] = {}

        self.edges: list[GraphEdge] = []

        ###############################################################
        # Fast Lookup Indexes
        ###############################################################

        self.nodes_by_type = defaultdict(dict)

        self.edges_by_relation = defaultdict(list)

        ###############################################################
        # Statistics
        ###############################################################

        self.statistics = GraphStatistics()

    ####################################################################
    # ADD NODE
    ####################################################################

    def add_node(
        self,
        node: GraphNode,
    ) -> GraphNode:

        ###############################################################
        # Already Exists
        ###############################################################

        existing = self.nodes.get(
            node.node_id,
        )

        if existing is not None:
            return existing

        ###############################################################
        # Store
        ###############################################################

        self.nodes[node.node_id] = node

        ###############################################################
        # Type Index
        ###############################################################

        entity_type = node.entity_type.lower()

        self.nodes_by_type[
            entity_type
        ][
            node.node_id
        ] = node

        ###############################################################
        # Statistics
        ###############################################################

        self.statistics.node_count += 1

        self.statistics.entity_counts[
            node.entity_type
        ] = (

            self.statistics.entity_counts.get(
                node.entity_type,
                0,
            )

            + 1

        )

        return node

    ####################################################################
    # ADD EDGE
    ####################################################################

    def add_edge(
        self,
        edge: GraphEdge,
    ) -> GraphEdge:

        ###############################################################
        # Prevent Duplicate
        ###############################################################

        for existing in self.edges:

            if (

                existing.source_id == edge.source_id

                and

                existing.target_id == edge.target_id

                and

                existing.relation == edge.relation

            ):

                return existing

        ###############################################################
        # Store
        ###############################################################

        self.edges.append(edge)

        ###############################################################
        # Relation Index
        ###############################################################

        self.edges_by_relation[
            edge.relation.lower()
        ].append(edge)

        ###############################################################
        # Connect Nodes
        ###############################################################

        source = self.nodes.get(
            edge.source_id,
        )

        if source is not None:

            source.outgoing_edges.append(
                edge
            )

        target = self.nodes.get(
            edge.target_id,
        )

        if target is not None:

            target.incoming_edges.append(
                edge
            )

        ###############################################################
        # Statistics
        ###############################################################

        self.statistics.edge_count += 1

        self.statistics.relation_counts[
            edge.relation
        ] = (

            self.statistics.relation_counts.get(
                edge.relation,
                0,
            )

            + 1

        )

        return edge
        ####################################################################
    # BASIC API
    ####################################################################

    def get_node(
        self,
        node_id: str,
    ) -> GraphNode | None:

        return self.nodes.get(
            node_id,
        )

    ####################################################################

    def get_nodes(self) -> list[GraphNode]:

        return list(
            self.nodes.values()
        )

    ####################################################################

    def get_edges(self) -> list[GraphEdge]:

        return self.edges

    ####################################################################
    # ENTITY TYPE LOOKUP
    ####################################################################

    def find_by_type(
        self,
        entity_type: str,
    ) -> list[GraphNode]:

        return list(

            self.nodes_by_type[
                entity_type.lower()
            ].values()

        )

    ####################################################################
    # RELATION LOOKUP
    ####################################################################

    def find_by_relation(
        self,
        relation: str,
    ) -> list[GraphEdge]:

        return list(

            self.edges_by_relation[
                relation.lower()
            ]

        )

    ####################################################################
    # ENTITY COLLECTIONS
    ####################################################################

    def actions(self):

        return self.find_by_type(
            "Action"
        )

    ####################################################################

    def objects(self):

        return self.find_by_type(
            "Object"
        )

    ####################################################################

    def domains(self):

        return self.find_by_type(
            "Domain"
        )

    ####################################################################

    def skills(self):

        return self.find_by_type(
            "Skill"
        )

    ####################################################################

    def standards(self):

        return self.find_by_type(
            "Standard"
        )

    ####################################################################

    def methodologies(self):

        return self.find_by_type(
            "Methodology"
        )

    ####################################################################

    def metrics(self):

        return self.find_by_type(
            "Metric"
        )

    ####################################################################

    def measurements(self):

        return self.find_by_type(
            "Measurement"
        )

    ####################################################################

    def kpis(self):

        return self.find_by_type(
            "KPI"
        )

    ####################################################################

    def achievements(self):

        return self.find_by_type(
            "Achievement"
        )

    ####################################################################

    def leadership(self):

        return self.find_by_type(
            "Leadership"
        )

    ####################################################################
    # GENERIC FILTERS
    ####################################################################

    def category(
        self,
        category: str,
    ):

        category = category.lower()

        return [

            node

            for node in self.nodes.values()

            if getattr(
                node,
                "category",
                "",
            ).lower() == category

        ]

    ####################################################################

    def business_area(
        self,
        area: str,
    ):

        area = area.lower()

        return [

            node

            for node in self.nodes.values()

            if getattr(
                node,
                "business_area",
                "",
            ).lower() == area

        ]
    ####################################################################
    # BASIC API
    ####################################################################

    def get_node(
        self,
        node_id: str,
    ) -> GraphNode | None:

        return self.nodes.get(
            node_id,
        )

    ####################################################################

    def get_nodes(self) -> list[GraphNode]:

        return list(
            self.nodes.values()
        )

    ####################################################################

    def get_edges(self) -> list[GraphEdge]:

        return self.edges

    ####################################################################
    # ENTITY TYPE LOOKUP
    ####################################################################

    def find_by_type(
        self,
        entity_type: str,
    ) -> list[GraphNode]:

        return list(

            self.nodes_by_type[
                entity_type.lower()
            ].values()

        )

    ####################################################################
    # RELATION LOOKUP
    ####################################################################

    def find_by_relation(
        self,
        relation: str,
    ) -> list[GraphEdge]:

        return list(

            self.edges_by_relation[
                relation.lower()
            ]

        )

    ####################################################################
    # ENTITY COLLECTIONS
    ####################################################################

    def actions(self):

        return self.find_by_type(
            "Action"
        )

    ####################################################################

    def objects(self):

        return self.find_by_type(
            "Object"
        )

    ####################################################################

    def domains(self):

        return self.find_by_type(
            "Domain"
        )

    ####################################################################

    def skills(self):

        return self.find_by_type(
            "Skill"
        )

    ####################################################################

    def standards(self):

        return self.find_by_type(
            "Standard"
        )

    ####################################################################

    def methodologies(self):

        return self.find_by_type(
            "Methodology"
        )

    ####################################################################

    def metrics(self):

        return self.find_by_type(
            "Metric"
        )

    ####################################################################

    def measurements(self):

        return self.find_by_type(
            "Measurement"
        )

    ####################################################################

    def kpis(self):

        return self.find_by_type(
            "KPI"
        )

    ####################################################################

    def achievements(self):

        return self.find_by_type(
            "Achievement"
        )

    ####################################################################

    def leadership(self):

        return self.find_by_type(
            "Leadership"
        )

    ####################################################################
    # GENERIC FILTERS
    ####################################################################

    def category(
        self,
        category: str,
    ):

        category = category.lower()

        return [

            node

            for node in self.nodes.values()

            if getattr(
                node,
                "category",
                "",
            ).lower() == category

        ]

    ####################################################################

    def business_area(
        self,
        area: str,
    ):

        area = area.lower()

        return [

            node

            for node in self.nodes.values()

            if getattr(
                node,
                "business_area",
                "",
            ).lower() == area

        ]
    ####################################################################
    # COUNTS
    ####################################################################

    def count(
        self,
        entity_type: str,
    ):

        return len(

            self.find_by_type(
                entity_type,
            )

        )

    ####################################################################
    # GRAPH SUMMARY
    ####################################################################

    def summary(self):

        return {

            "nodes": self.statistics.node_count,

            "edges": self.statistics.edge_count,

            "entities": self.statistics.entity_counts,

            "relations": self.statistics.relation_counts,

        }

    ####################################################################

    def get_statistics(self):

        return self.statistics

    ####################################################################
    # EXPORT
    ####################################################################

    def to_dict(self):

        return {

            "nodes": [

                node.to_dict()

                if hasattr(node, "to_dict")

                else vars(node)

                for node in self.nodes.values()

            ],

            "edges": [

                edge.to_dict()

                if hasattr(edge, "to_dict")

                else vars(edge)

                for edge in self.edges

            ],

            "statistics": {

                "node_count": self.statistics.node_count,

                "edge_count": self.statistics.edge_count,

                "entity_counts": dict(

                    self.statistics.entity_counts

                ),

                "relation_counts": dict(

                    self.statistics.relation_counts

                ),

            },

        }

    ####################################################################
    # MAGIC METHODS
    ####################################################################

    def __len__(self):

        return len(

            self.nodes

        )

    ####################################################################

    def __repr__(self):

        return (

            f"<KnowledgeGraph "

            f"nodes={len(self.nodes)} "

            f"edges={len(self.edges)}>"

        )