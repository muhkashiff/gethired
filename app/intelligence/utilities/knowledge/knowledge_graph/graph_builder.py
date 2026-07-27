"""
Knowledge Graph Builder

Converts KnowledgeDocument
into a semantic graph.
"""

from .graph_models import KnowledgeGraph
from .graph_nodes import NodeFactory
from .graph_edges import EdgeFactory


class GraphBuilder:

    def __init__(self):

        self.nodes = NodeFactory()

        self.edges = EdgeFactory()

    # -------------------------------------------------

    def build(self, document):

        graph = KnowledgeGraph()

        for fact in document.facts:

            interp = fact.interpretation

            if interp.action.found:

                action = self.nodes.create(

                    "Action",

                    interp.action.base,

                )

            else:

                continue

            # ------------------------------------------

            if interp.object.found:

                obj = self.nodes.create(

                    "Object",

                    interp.object.canonical,

                )

                self.edges.connect(

                    action,

                    "acts_on",

                    obj,

                )

            # ------------------------------------------

            if interp.metric.found:

                metric = self.nodes.create(

                    "Metric",

                    interp.metric.canonical,

                )

                self.edges.connect(

                    action,

                    "changes",

                    metric,

                )

            # ------------------------------------------

            if interp.measurement.found:

                value = self.nodes.create(

                    "Measurement",

                    interp.measurement.value,

                    {

                        "unit": interp.measurement.unit,

                        "direction": interp.measurement.direction,

                        "effect": interp.measurement.effect,

                    },

                )

                self.edges.connect(

                    metric,

                    "measured_as",

                    value,

                )

            # ------------------------------------------

            if interp.domain.found:

                domain = self.nodes.create(

                    "Domain",

                    interp.domain.domain,

                )

                self.edges.connect(

                    action,

                    "belongs_to",

                    domain,

                )

        graph.nodes = self.nodes.all_nodes()

        graph.edges = self.edges.edges

        return graph