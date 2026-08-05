"""
Enterprise Graph Helpers

Reusable helper functions used across

• Builders
• Validators
• Optimizer
• Reasoners
• Query Engine

Enterprise V7
"""

from collections import defaultdict


class GraphHelpers:

    ####################################################################
    # NODE LOOKUPS
    ####################################################################

    @staticmethod
    def node_by_entity_id(

        graph,

        entity_id,

    ):

        for node in graph.get_nodes():

            if node.entity_id == entity_id:

                return node

        return None

    ####################################################################
    # TYPE LOOKUP
    ####################################################################

    @staticmethod
    def nodes_by_type(

        graph,

        entity_type,

    ):

        entity_type = entity_type.lower()

        return [

            node

            for node in graph.get_nodes()

            if node.entity_type.lower() == entity_type

        ]

    ####################################################################
    # DOMAIN LOOKUP
    ####################################################################

    @staticmethod
    def nodes_by_domain(

        graph,

        domain,

    ):

        domain = domain.lower()

        return [

            node

            for node in graph.get_nodes()

            if node.domain.lower() == domain

        ]

    ####################################################################
    # BUSINESS AREA LOOKUP
    ####################################################################

    @staticmethod
    def nodes_by_business_area(

        graph,

        area,

    ):

        area = area.lower()

        return [

            node

            for node in graph.get_nodes()

            if node.business_area.lower() == area

        ]

    ####################################################################
    # EDGE LOOKUPS
    ####################################################################

    @staticmethod
    def outgoing(

        graph,

        node_id,

        relation=None,

    ):

        edges = [

            edge

            for edge in graph.get_edges()

            if edge.source_id == node_id

        ]

        if relation:

            relation = relation.upper()

            edges = [

                edge

                for edge in edges

                if edge.relation.upper() == relation

            ]

        return edges

    ####################################################################

    @staticmethod
    def incoming(

        graph,

        node_id,

        relation=None,

    ):

        edges = [

            edge

            for edge in graph.get_edges()

            if edge.target_id == node_id

        ]

        if relation:

            relation = relation.upper()

            edges = [

                edge

                for edge in edges

                if edge.relation.upper() == relation

            ]

        return edges

    ####################################################################
    # NEIGHBORS
    ####################################################################

    @staticmethod
    def neighbors(

        graph,

        node_id,

    ):

        output = []

        for edge in graph.get_edges():

            if edge.source_id == node_id:

                node = graph.get_node(

                    edge.target_id

                )

                if node:

                    output.append(node)

            elif edge.target_id == node_id:

                node = graph.get_node(

                    edge.source_id

                )

                if node:

                    output.append(node)

        return output

    ####################################################################
    # GROUP BY TYPE
    ####################################################################

    @staticmethod
    def group_nodes_by_type(

        graph,

    ):

        groups = defaultdict(list)

        for node in graph.get_nodes():

            groups[node.entity_type].append(node)

        return dict(groups)

    ####################################################################
    # GROUP BY DOMAIN
    ####################################################################

    @staticmethod
    def group_nodes_by_domain(

        graph,

    ):

        groups = defaultdict(list)

        for node in graph.get_nodes():

            groups[node.domain].append(node)

        return dict(groups)

    ####################################################################
    # GROUP BY BUSINESS AREA
    ####################################################################

    @staticmethod
    def group_nodes_by_business_area(

        graph,

    ):

        groups = defaultdict(list)

        for node in graph.get_nodes():

            groups[node.business_area].append(node)

        return dict(groups)

    ####################################################################
    # GRAPH SUMMARY
    ####################################################################

    @staticmethod
    def summary(

        graph,

    ):

        return {

            "nodes": len(graph.nodes),

            "edges": len(graph.edges),

            "entity_types": len(

                GraphHelpers.group_nodes_by_type(

                    graph

                )

            ),

            "domains": len(

                GraphHelpers.group_nodes_by_domain(

                    graph

                )

            ),

            "business_areas": len(

                GraphHelpers.group_nodes_by_business_area(

                    graph

                )

            ),

        }