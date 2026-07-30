"""
Knowledge Graph Builder

Builds a semantic knowledge graph from a parsed
KnowledgeDocument.

NEW VERSION

Uses the semantic interpretation produced by the
SentenceParser.

Pipeline

KnowledgeDocument
        ↓
KnowledgeFact
        ↓
KnowledgeInterpretation
        ↓
Entities
Dependencies
Measurement
        ↓
KnowledgeGraph
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

    """
    Converts semantic knowledge into a graph.

    Every ontology entity becomes one GraphNode.

    Relationships are generated from

        • semantic interpretation
        • dependency parser
    """

    # ------------------------------------------------------------

    def __init__(self):

        self.node_counter = 1
        self.edge_counter = 1

    # ============================================================
    # PUBLIC
    # ============================================================

    def build(self, knowledge_document):

        """
        Build one complete graph document.
        """

        graph = KnowledgeGraph()

        # ---------------------------------------------
        # Every parsed fact becomes graph knowledge
        # ---------------------------------------------

        for sentence in knowledge_document.sentences:

            for fact in sentence.facts:

                self._build_fact(

                    graph=graph,

                    fact=fact,

                )

        graph.confidence = knowledge_document.confidence

        return KnowledgeGraphDocument(

            knowledge_document=knowledge_document,

            graph=graph,

            confidence=graph.confidence,

            statistics=knowledge_document.statistics,

        )

    # ============================================================
    # FACT BUILDER
    # ============================================================

    def _build_fact(

        self,

        graph,

        fact,

    ):

        """
        Builds one graph fragment.

        Order

            1. ontology entities
            2. measurement node
            3. semantic edges
            4. dependency edges
        """

        interpretation = fact.interpretation

        # -----------------------------------------
        # Build ontology entities
        # -----------------------------------------

        for entity in interpretation.entities:

            self._add_node_from_entity(

                graph,

                entity,

            )

        # -----------------------------------------
        # Measurement is NOT an ontology entity
        # -----------------------------------------

        measurement_node = None

        if interpretation.measurement.found:

            measurement_node = self._add_measurement_node(

                graph,

                interpretation.measurement,

            )

        # -----------------------------------------
        # Semantic relationships
        # -----------------------------------------

        self._build_semantic_edges(

            graph,

            interpretation,

            measurement_node,

        )

        # -----------------------------------------
        # Dependency parser relationships
        # -----------------------------------------

        self._build_dependency_edges(

            graph,

            interpretation.dependencies,

        )
            # ============================================================
    # GENERIC ENTITY NODE
    # ============================================================

    def _add_node_from_entity(

        self,

        graph,

        entity,

    ):

        """
        Creates one ontology node.

        Works for

            Action
            Object
            Domain
            Standard
            Technology
            Methodology
            Skill
            KPI
        """

        existing = graph.get_node_by_entity(

            entity.entity_id

        )

        if existing:

            existing.frequency += 1

            return existing

        node = GraphNode(

            node_id=f"N{self.node_counter:05}",

            entity_id=entity.entity_id,

            node_type=entity.entity_type.title(),

            label=entity.canonical,

            canonical=entity.canonical,

            category=entity.category,

            business_area=entity.business_area,

            confidence=entity.confidence,

            impact_weight=entity.metadata.get(

                "impact_weight",

                1.0,

            ),

            metadata=entity.metadata,

        )

        graph.add_node(node)

        self.node_counter += 1

        return node

    # ============================================================
    # MEASUREMENT NODE
    # ============================================================

    def _add_measurement_node(

        self,

        graph,

        measurement,

    ):

        """
        Measurements are generated dynamically.

        They are NOT ontology entities.
        """

        entity_id = (

            f"MEASUREMENT_"

            f"{measurement.metric.upper().replace(' ','_')}_"

            f"{measurement.numeric_value}"

        )

        existing = graph.get_node_by_entity(

            entity_id

        )

        if existing:

            existing.frequency += 1

            return existing

        node = GraphNode(

            node_id=f"N{self.node_counter:05}",

            entity_id=entity_id,

            node_type="Measurement",

            label=measurement.value,

            canonical=measurement.metric,

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

                "from_value": measurement.from_value,

                "to_value": measurement.to_value,

                "change_value": measurement.change_value,

                "percent_change": measurement.percent_change,

                "comparison_operator": measurement.comparison_operator,

                "direction": measurement.direction,

                "effect": measurement.effect,

                "business_meaning": measurement.business_meaning,

            },

        )

        # ---------------------------------------------
        # Promote important values into properties
        # ---------------------------------------------

        node.properties["value"] = measurement.value

        node.properties["numeric_value"] = measurement.numeric_value

        node.properties["normalized_value"] = measurement.normalized_value

        node.properties["unit"] = measurement.unit

        node.properties["measurement_type"] = measurement.measurement_type

        node.properties["from_value"] = measurement.from_value

        node.properties["to_value"] = measurement.to_value

        node.properties["change_value"] = measurement.change_value

        node.properties["percent_change"] = measurement.percent_change

        node.properties["comparison_operator"] = measurement.comparison_operator

        node.properties["direction"] = measurement.direction

        node.properties["effect"] = measurement.effect

        node.properties["business_meaning"] = measurement.business_meaning

        graph.add_node(node)

        self.node_counter += 1

        return node

    # ============================================================
    # GENERIC EDGE
    # ============================================================

    def _add_edge(

        self,

        graph,

        source,

        target,

        relationship,

        confidence=1.0,

        source_name="knowledge_pipeline",

    ):

        """
        Creates one graph edge.
        """

        if source is None:

            return

        if target is None:

            return

        edge = GraphEdge(

            edge_id=f"E{self.edge_counter:05}",

            source_node=source.entity_id,

            target_node=target.entity_id,

            relationship=relationship,

            relationship_label=relationship,

            confidence=confidence,

            weight=1.0,

            source=source_name,

        )

        graph.add_edge(edge)

        source.add_edge(edge)

        target.add_edge(edge)

        self.edge_counter += 1

            # ============================================================
    # SEMANTIC EDGES
    # ============================================================

    def _build_semantic_edges(

        self,

        graph,

        interpretation,

        measurement_node,

    ):

        """
        Builds semantic relationships.

        Action
            ├── targets
            ├── belongs_to
            ├── measured_by
            ├── achieved_using
            └── has_value
        """

        action = graph.get_node_by_entity(

            interpretation.action.entity_id

        )

        obj = graph.get_node_by_entity(

            interpretation.object.entity_id

        )

        domain = graph.get_node_by_entity(

            interpretation.domain.entity_id

        )

        metric = graph.get_node_by_entity(

            interpretation.metric.entity_id

        )

        practice = None

        if hasattr(interpretation, "practice"):

            if interpretation.practice.found:

                practice = graph.get_node_by_entity(

                    interpretation.practice.entity_id

                )

        # ------------------------------------------------
        # Action → Object
        # ------------------------------------------------

        if action and obj:

            self._add_edge(

                graph,

                action,

                obj,

                "targets",

            )

        # ------------------------------------------------
        # Object → Domain
        # ------------------------------------------------

        if obj and domain:

            self._add_edge(

                graph,

                obj,

                domain,

                "belongs_to",

            )

        # ------------------------------------------------
        # Domain → KPI
        # ------------------------------------------------

        if domain and metric:

            self._add_edge(

                graph,

                domain,

                metric,

                "contains_metric",

            )

        # ------------------------------------------------
        # Action → KPI
        # ------------------------------------------------

        if action and metric:

            self._add_edge(

                graph,

                action,

                metric,

                "measured_by",

            )

        # ------------------------------------------------
        # KPI → Measurement
        # ------------------------------------------------

        if metric and measurement_node:

            self._add_edge(

                graph,

                metric,

                measurement_node,

                "has_value",

            )

        # ------------------------------------------------
        # Action → Practice
        # ------------------------------------------------

        if action and practice:

            self._add_edge(

                graph,

                action,

                practice,

                "achieved_using",

            )

    # ============================================================
    # DEPENDENCY EDGES
    # ============================================================

    def _build_dependency_edges(

        self,

        graph,

        dependencies,

    ):

        """
        Dependency parser relationships.

        Example

            implement

                achieved_using

                    Lean

            improve

                modifies

                    Yield
        """

        if not dependencies:

            return

        for dep in dependencies:

            source = graph.get_node_by_entity(

                dep.source_entity

            )

            target = graph.get_node_by_entity(

                dep.target_entity

            )

            if source is None:

                continue

            if target is None:

                continue

            self._add_edge(

                graph,

                source,

                target,

                dep.relation,

                confidence=dep.confidence,

                source_name="dependency_parser",

            )