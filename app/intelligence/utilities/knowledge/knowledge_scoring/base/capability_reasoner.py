"""
Enterprise Capability Reasoner

Enterprise V12

Graph
    ↓
Ontology
    ↓
Capabilities
"""

from collections import defaultdict

from app.intelligence.utilities.knowledge.knowledge_scoring.ontology.ontology_registry import (
    registry,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.evidence.capability_evidence import (
    CapabilityEvidence,
)


class CapabilityReasoner:

    def __init__(self):

        pass

    # ---------------------------------------------------------

    def reason(self, graph):

        """
        Main reasoning entry.

        Returns

            dict[str, CapabilityEvidence]
        """

        capabilities = defaultdict(CapabilityEvidence)

        self._reason_nodes(

            graph,

            capabilities,

        )

        self._reason_edges(

            graph,

            capabilities,

        )

        return capabilities

    # ---------------------------------------------------------

    def _reason_nodes(

        self,

        graph,

        capabilities,

    ):

        """
        Every ontology item contributes capabilities.
        """

        for node in graph.get_nodes():

            ontology = registry.get(

                node.canonical

            )

            if ontology is None:

                continue

            for capability in ontology.capabilities:

                evidence = capabilities[

                    capability.capability

                ]

                evidence.capability = capability.capability

                evidence.score += capability.weight

                evidence.entities.append(

                    node.node_id

                )

    # ---------------------------------------------------------

    def _reason_edges(

        self,

        graph,

        capabilities,

    ):

        """
        Relations increase confidence.
        """

        relation_bonus = {

            "USES": 0.5,

            "COMPLIES_WITH": 0.75,

            "ACHIEVED": 1.25,

            "AFFECTS": 0.75,

            "MEASURED_BY": 0.5,

            "BELONGS_TO": 0.25,

            "REQUIRES": 0.50,

            "ACTS_ON": 0.50,

        }

        for edge in graph.get_edges():

            source = graph.get_node(

                edge.source_id

            )

            target = graph.get_node(

                edge.target_id

            )

            if source is None or target is None:

                continue

            ontology = registry.get(

                target.canonical

            )

            if ontology is None:

                continue

            bonus = relation_bonus.get(

                edge.relation,

                0.25,

            )

            for capability in ontology.capabilities:

                evidence = capabilities[

                    capability.capability

                ]

                evidence.score += bonus

                evidence.relations.append(

                    edge.edge_id

                )