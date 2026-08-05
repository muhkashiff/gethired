"""
Enterprise Dependency Reasoner

Enterprise V6

Purpose
-------
Analyzes graph relationships and produces dependency intelligence.

This reasoner is responsible for

• validating graph connectivity
• discovering dependency chains
• grouping relationships
• computing graph dependency statistics

Output

reasoning.dependencies
"""

from collections import defaultdict

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.dependency_models import (
    DependencyReasoningResult,
    DependencyChain,
)
from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.dependency_models import (
    DependencyStatistics,
)


class DependencyReasoner:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        pass

    ####################################################################
    # PUBLIC API
    ####################################################################

    def analyze(

        self,

        graph,

        reasoning,

    ):

        """
        Enterprise Dependency Analysis
        """

        result = DependencyReasoningResult()

        result.total_edges = len(graph.get_edges())

        ############################################################
        # Build Relation Index
        ############################################################

        result.relation_index = self._build_relation_index(graph)

        ############################################################
        # Build Incoming Index
        ############################################################

        result.incoming_index = self._build_incoming_index(graph)

        ############################################################
        # Build Outgoing Index
        ############################################################

        result.outgoing_index = self._build_outgoing_index(graph)

        ############################################################
        # Build Dependency Chains
        ############################################################

        result.chains = self._discover_dependency_chains(graph)

        ############################################################
        # Connectivity Statistics
        ############################################################

        result.statistics = self._calculate_statistics(graph)

        ############################################################
        # Save
        ############################################################

        reasoning.dependencies = result

        reasoning.reasoning_steps.append(

            "Dependency Reasoning"

        )

        return reasoning

    ####################################################################
    # RELATION INDEX
    ####################################################################

    def _build_relation_index(

        self,

        graph,

    ):

        index = defaultdict(list)

        for edge in graph.get_edges():

            index[edge.relation].append(edge)

        return dict(index)

    ####################################################################
    # OUTGOING INDEX
    ####################################################################

    def _build_outgoing_index(

        self,

        graph,

    ):

        outgoing = defaultdict(list)

        for edge in graph.get_edges():

            outgoing[edge.source_id].append(edge)

        return dict(outgoing)

    ####################################################################
    # INCOMING INDEX
    ####################################################################

    def _build_incoming_index(

        self,

        graph,

    ):

        incoming = defaultdict(list)

        for edge in graph.get_edges():

            incoming[edge.target_id].append(edge)

        return dict(incoming)

    ####################################################################
    # DISCOVER CHAINS
    ####################################################################

    def _discover_dependency_chains(

        self,

        graph,

    ):

        chains = []

        outgoing = self._build_outgoing_index(graph)

        for node in graph.get_nodes():

            if node.node_id not in outgoing:

                continue

            chain = DependencyChain(

                root=node.node_id,

            )

            self._walk_chain(

                node.node_id,

                outgoing,

                chain,

                visited=set(),

            )

            if len(chain.nodes) > 1:

                chains.append(chain)

        return chains

    ####################################################################
    # DFS WALK
    ####################################################################

    def _walk_chain(

        self,

        node_id,

        outgoing,

        chain,

        visited,

    ):

        if node_id in visited:

            return

        visited.add(node_id)

        chain.nodes.append(node_id)

        for edge in outgoing.get(node_id, []):

            chain.edges.append(edge)

            self._walk_chain(

                edge.target_id,

                outgoing,

                chain,

                visited,

            )

    ####################################################################
    # GRAPH STATISTICS
    ####################################################################

    def _calculate_statistics(self, graph):

        stats = DependencyStatistics()

        stats.nodes = len(graph.get_nodes())

        stats.edges = len(graph.get_edges())

        # populate relations, average_degree, etc.

        return stats
    ####################################################################
    # AVERAGE DEGREE
    ####################################################################

    def _average_degree(

        self,

        graph,

    ):

        if not graph.get_nodes():

            return 0

        degree = 0

        for node in graph.get_nodes():

            degree += len(node.incoming_edges)

            degree += len(node.outgoing_edges)

        return round(

            degree / len(graph.get_nodes()),

            2,

        )