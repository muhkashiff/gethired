"""
Enterprise Graph Neighbor API

Provides graph navigation.

No engine should manually iterate over graph.edges.

Use this API instead.

Enterprise Version
"""


class GraphNeighbors:

    def __init__(self, graph):

        self.graph = graph

    # =====================================================
    # Incoming
    # =====================================================

    def parents(self, node_id):

        parents = []

        for edge in self.graph.edges:

            if edge.target_id == node_id:

                parent = self.graph.get_node(edge.source_id)

                if parent:

                    parents.append(parent)

        return parents

    # =====================================================
    # Outgoing
    # =====================================================

    def children(self, node_id):

        children = []

        for edge in self.graph.edges:

            if edge.source_id == node_id:

                child = self.graph.get_node(edge.target_id)

                if child:

                    children.append(child)

        return children

    # =====================================================
    # All Neighbors
    # =====================================================

    def neighbors(self, node_id):

        results = []

        results.extend(

            self.parents(node_id)

        )

        results.extend(

            self.children(node_id)

        )

        return results

    # =====================================================
    # Connected Nodes
    # =====================================================

    def connected(self, node_id):

        connected = set()

        for node in self.neighbors(node_id):

            connected.add(node.node_id)

        return [

            self.graph.get_node(i)

            for i in connected

        ]

    # =====================================================
    # Outgoing by Relation
    # =====================================================

    def children_by_relation(

        self,

        node_id,

        relation,

    ):

        relation = relation.lower()

        nodes = []

        for edge in self.graph.edges:

            if (

                edge.source_id == node_id

                and

                edge.relation.lower() == relation

            ):

                target = self.graph.get_node(

                    edge.target_id

                )

                if target:

                    nodes.append(target)

        return nodes

    # =====================================================
    # Incoming by Relation
    # =====================================================

    def parents_by_relation(

        self,

        node_id,

        relation,

    ):

        relation = relation.lower()

        nodes = []

        for edge in self.graph.edges:

            if (

                edge.target_id == node_id

                and

                edge.relation.lower() == relation

            ):

                source = self.graph.get_node(

                    edge.source_id

                )

                if source:

                    nodes.append(source)

        return nodes

    # =====================================================
    # Connected Edges
    # =====================================================

    def edges(self, node_id):

        return [

            edge

            for edge in self.graph.edges

            if (

                edge.source_id == node_id

                or

                edge.target_id == node_id

            )

        ]

    # =====================================================
    # Degree
    # =====================================================

    def degree(self, node_id):

        return len(

            self.edges(node_id)

        )

    # =====================================================
    # Isolated
    # =====================================================

    def isolated(self):

        return [

            node

            for node in self.graph.nodes.values()

            if self.degree(node.node_id) == 0

        ]