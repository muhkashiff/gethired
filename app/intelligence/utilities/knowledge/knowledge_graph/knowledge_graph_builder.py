"""
Knowledge Graph Builder

Builds a semantic knowledge graph from a parsed
KnowledgeDocument.
"""

from app.intelligence.utilities.knowledge.knowledge_graph.graph_document import (
    KnowledgeGraphDocument,
)

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    KnowledgeGraph,
)

from app.intelligence.utilities.knowledge.knowledge_graph.node_models import (
    GraphNode,
)

from app.intelligence.utilities.knowledge.knowledge_graph.edge_models import (
    GraphEdge,
)


class KnowledgeGraphBuilder:

    def __init__(self):

        self.node_counter = 1
        self.edge_counter = 1

    # -------------------------------------------------

    def build(self, knowledge_document):

        graph = KnowledgeGraph()

        for sentence in knowledge_document.sentences:

            for fact in sentence.facts:

                self._build_fact(graph, fact)

            if hasattr(sentence, "dependency_result"):

                self._build_dependency_edges(

                    graph,

                    sentence.dependency_result

                )

        graph.confidence = knowledge_document.confidence

        return KnowledgeGraphDocument(

            knowledge_document=knowledge_document,

            graph=graph,

            confidence=graph.confidence,

            statistics=knowledge_document.statistics,

        )

    # -------------------------------------------------

    def _build_fact(self, graph, fact):

        interpretation = fact.interpretation

        action = interpretation.action
        obj = interpretation.object
        domain = interpretation.domain
        metric = interpretation.metric
        measurement = interpretation.measurement

        # ---------------------------------------------
        # Action
        # ---------------------------------------------

        action_node = None

        if action.found:

            action_node = self._add_node(

                graph=graph,

                entity_id=action.entity_id,

                node_type="Action",

                label=action.base,

                category=action.category,

                business_area=action.business_area,

                confidence=action.confidence,

                impact_weight=action.impact_weight,

                metadata=action.metadata,

            )

        # ---------------------------------------------
        # Object
        # ---------------------------------------------

        object_node = None

        if obj.found:

            object_node = self._add_node(

                graph=graph,

                entity_id=obj.entity_id,

                node_type="Object",

                label=obj.canonical,

                category=obj.category,

                business_area=obj.business_area,

                confidence=obj.confidence,

                impact_weight=obj.impact_weight,

                metadata=obj.metadata,

            )

        # ---------------------------------------------
        # Domain
        # ---------------------------------------------

        domain_node = None

        if domain.found:

            domain_node = self._add_node(

                graph=graph,

                entity_id=domain.entity_id,

                node_type="Domain",

                label=domain.domain,

                category="domain",

                business_area=domain.business_area,

                confidence=domain.confidence,

                impact_weight=domain.impact_weight,

                metadata=domain.metadata,

            )

        # ---------------------------------------------
        # Metric
        # ---------------------------------------------

        metric_node = None

        if metric.found:

            metric_node = self._add_node(

                graph=graph,

                entity_id=metric.entity_id,

                node_type="Metric",

                label=metric.canonical,

                category=metric.category,

                business_area=metric.business_area,

                confidence=metric.confidence,

                impact_weight=metric.impact_weight,

                metadata=metric.metadata,

            )

        # ---------------------------------------------
        # Measurement
        # ---------------------------------------------

        measurement_node = None

        if measurement.found:

            measurement_node = self._add_node(

                graph=graph,

                entity_id=(
                    f"MEASUREMENT_"
                    f"{measurement.metric.upper().replace(' ', '_')}_"
                    f"{measurement.numeric_value}"
                ),

                node_type="Measurement",

                label=measurement.value,

                category="measurement",

                business_area=measurement.business_area,

                confidence=measurement.confidence,

                impact_weight=measurement.impact_weight,

                metadata={

                    "value": measurement.value,
                    "numeric_value": measurement.numeric_value,
                    "normalized_value": measurement.normalized_value,
                    "unit": measurement.unit,

                    "measurement_type": measurement.measurement_type,

                    "start_value": measurement.from_value,
                    "end_value": measurement.to_value,
                    "change_value": measurement.change_value,
                    "percent_change": measurement.percent_change,

                    "comparison_operator": measurement.comparison_operator,

                    "direction": measurement.direction,
                    "effect": measurement.effect,
                    "business_meaning": measurement.business_meaning,

                },

            )

            # --------------------------------------------------
            # Promote important measurement fields
            # into node.properties for fast access
            # --------------------------------------------------

            measurement_node.properties["value"] = measurement.value
            measurement_node.properties["numeric_value"] = measurement.numeric_value
            measurement_node.properties["normalized_value"] = measurement.normalized_value

            measurement_node.properties["unit"] = measurement.unit

            measurement_node.properties["measurement_type"] = measurement.measurement_type

            measurement_node.properties["from_value"] = measurement.from_value
            measurement_node.properties["to_value"] = measurement.to_value

            measurement_node.properties["change_value"] = measurement.change_value
            measurement_node.properties["percent_change"] = measurement.percent_change

            measurement_node.properties["comparison_operator"] = measurement.comparison_operator

            measurement_node.properties["direction"] = measurement.direction
            measurement_node.properties["effect"] = measurement.effect
            measurement_node.properties["business_meaning"] = measurement.business_meaning

        
    # -------------------------------------------------

    def _add_node(

        self,

        graph,

        entity_id,

        node_type,

        label,

        category,

        business_area,

        confidence,

        metadata,

        impact_weight=1.0,

    ):

        existing = graph.get_node_by_entity(entity_id)

        if existing:

            existing.frequency += 1
            return existing

        node = GraphNode(

            node_id=f"N{self.node_counter:05}",

            entity_id=entity_id,

            node_type=node_type,

            label=label,

            canonical=label,

            category=category,

            business_area=business_area,

            confidence=confidence,

            impact_weight=impact_weight,

            metadata=metadata,

        )

        graph.add_node(node)

        self.node_counter += 1

        return node

    # -------------------------------------------------

    def _add_edge(

        self,

        graph,

        source,

        target,

        relationship,

    ):

        edge = GraphEdge(

            edge_id=f"E{self.edge_counter:05}",

            source_node=source.entity_id,

            target_node=target.entity_id,

            relationship=relationship,

            relationship_label=relationship,

            confidence=1.0,

            weight=1.0,

            source="knowledge_pipeline",

        )

        graph.add_edge(edge)

        source.add_edge(edge)
        target.add_edge(edge)

        self.edge_counter += 1

    #--------------------------------------------
    # Dependency parser
    #--------------------------------------------

    def _build_dependency_edges(self, graph, dependency_result):

        for dep in dependency_result.edges:

            source = graph.get_node_by_entity(dep.source_entity)
            target = graph.get_node_by_entity(dep.target_entity)

            if source is None or target is None:
                continue

            edge = GraphEdge(

                edge_id=f"E{self.edge_counter:05}",

                source_node=source.entity_id,

                target_node=target.entity_id,

                relationship=dep.relation,

                relationship_label=dep.relation,

                confidence=dep.confidence,

                weight=1.0,

                source="dependency_parser",

            )

            graph.add_edge(edge)

            source.add_edge(edge)
            target.add_edge(edge)

            self.edge_counter += 1