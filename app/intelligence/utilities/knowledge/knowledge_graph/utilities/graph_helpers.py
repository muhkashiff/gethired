"""
Enterprise Graph Helpers

Reusable helper functions for Knowledge Graph.

These helpers keep every builder extremely small.

Enterprise V5
"""

from typing import List

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphNode,
)


class GraphHelpers:
    """
    Collection of helper methods used throughout
    the Knowledge Graph.
    """

    # ---------------------------------------------------------
    # Safe Metadata Access
    # ---------------------------------------------------------

    @staticmethod
    def get(node: GraphNode, key: str, default=None):
        """
        Safe metadata getter.

        Example

        GraphHelpers.get(node,"numeric_value")
        """

        if node.metadata is None:
            return default

        return node.metadata.get(key, default)

    # ---------------------------------------------------------
    # Numeric Value
    # ---------------------------------------------------------

    @staticmethod
    def numeric(node: GraphNode):

        value = GraphHelpers.get(node, "numeric_value")

        if value is None:
            return 0

        return value

    # ---------------------------------------------------------
    # Percentage Change
    # ---------------------------------------------------------

    @staticmethod
    def percent_change(node: GraphNode):

        value = GraphHelpers.get(node, "percent_change")

        if value is None:
            return 0

        return value

    # ---------------------------------------------------------
    # Unit
    # ---------------------------------------------------------

    @staticmethod
    def unit(node: GraphNode):

        return GraphHelpers.get(node, "unit", "")

    # ---------------------------------------------------------
    # Business Area
    # ---------------------------------------------------------

    @staticmethod
    def business_area(node: GraphNode):

        if node.business_area:
            return node.business_area

        return GraphHelpers.get(node, "business_area", "")

    # ---------------------------------------------------------
    # Category
    # ---------------------------------------------------------

    @staticmethod
    def category(node: GraphNode):

        if node.category:
            return node.category

        return GraphHelpers.get(node, "category", "")

    # ---------------------------------------------------------
    # Domain
    # ---------------------------------------------------------

    @staticmethod
    def domain(node: GraphNode):

        if node.domain:
            return node.domain

        return GraphHelpers.get(node, "domain", "")

    # ---------------------------------------------------------
    # Node Filtering
    # ---------------------------------------------------------

    @staticmethod
    def filter_type(nodes: List[GraphNode], entity_type: str):

        entity_type = entity_type.lower()

        return [

            node

            for node in nodes

            if node.entity_type.lower() == entity_type

        ]

    # ---------------------------------------------------------
    # Category Filtering
    # ---------------------------------------------------------

    @staticmethod
    def filter_category(nodes, category):

        category = category.lower()

        return [

            node

            for node in nodes

            if GraphHelpers.category(node).lower() == category

        ]

    # ---------------------------------------------------------
    # Business Area Filtering
    # ---------------------------------------------------------

    @staticmethod
    def filter_business_area(nodes, area):

        area = area.lower()

        return [

            node

            for node in nodes

            if GraphHelpers.business_area(node).lower() == area

        ]

    # ---------------------------------------------------------
    # Has Measurement
    # ---------------------------------------------------------

    @staticmethod
    def has_measurement(node):

        return GraphHelpers.numeric(node) != 0

    # ---------------------------------------------------------
    # Label
    # ---------------------------------------------------------

    @staticmethod
    def label(node):

        return node.label or node.canonical

    # ---------------------------------------------------------
    # Pretty Print
    # ---------------------------------------------------------

    @staticmethod
    def describe(node):

        return {

            "entity_id": node.entity_id,

            "entity_type": node.entity_type,

            "label": node.label,

            "category": GraphHelpers.category(node),

            "business_area": GraphHelpers.business_area(node),

        }