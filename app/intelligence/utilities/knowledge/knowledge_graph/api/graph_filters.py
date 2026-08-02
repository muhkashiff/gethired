"""
Enterprise Graph Filters

High-level filtering operations built on top of GraphQueryAPI.

Purpose
-------
Business filtering.

Examples

graph_api.filters.by_confidence(0.90)

graph_api.filters.by_business_area("quality")

graph_api.filters.by_category("food_safety")

graph_api.filters.executive_actions()

graph_api.filters.quantified_actions()

Enterprise Version
"""


class GraphFilters:

    def __init__(self, graph):

        self.graph = graph

    # =====================================================
    # BASIC FILTER
    # =====================================================

    def filter(self, predicate):

        return [

            node

            for node in self.graph.nodes.values()

            if predicate(node)

        ]

    # =====================================================
    # CONFIDENCE
    # =====================================================

    def by_confidence(self, minimum=0.90):

        return self.filter(

            lambda n: getattr(

                n,

                "confidence",

                0,

            ) >= minimum

        )

    # =====================================================
    # CATEGORY
    # =====================================================

    def by_category(self, category):

        category = category.lower()

        return self.filter(

            lambda n: getattr(

                n,

                "category",

                "",

            ).lower()

            == category

        )

    # =====================================================
    # ENTITY TYPE
    # =====================================================

    def by_type(self, entity_type):

        entity_type = entity_type.lower()

        return self.filter(

            lambda n: getattr(

                n,

                "entity_type",

                "",

            ).lower()

            == entity_type

        )

    # =====================================================
    # DOMAIN
    # =====================================================

    def by_domain(self, domain):

        domain = domain.lower()

        return self.filter(

            lambda n: getattr(

                n,

                "domain",

                "",

            ).lower()

            == domain

        )

    # =====================================================
    # BUSINESS AREA
    # =====================================================

    def by_business_area(self, business_area):

        business_area = business_area.lower()

        return self.filter(

            lambda n: getattr(

                n,

                "business_area",

                "",

            ).lower()

            == business_area

        )

    # =====================================================
    # IMPACT WEIGHT
    # =====================================================

    def by_impact_weight(self, minimum=0.80):

        return self.filter(

            lambda n: getattr(

                n,

                "impact_weight",

                0,

            ) >= minimum

        )

    # =====================================================
    # EXECUTIVE ACTIONS
    # =====================================================

    def executive_actions(self):

        return [

            node

            for node in self.graph.nodes.values()

            if (

                node.entity_type.lower() == "action"

                and

                node.category.lower()

                in (

                    "leadership",

                    "strategy",

                    "management",

                )

            )

        ]

    # =====================================================
    # QUANTIFIED METRICS
    # =====================================================

    def quantified_metrics(self):

        return [

            node

            for node in self.graph.nodes.values()

            if (

                node.entity_type.lower()

                == "measurement"

                and

                node.metadata.get(

                    "numeric_value"

                )

                is not None

            )

        ]

    # =====================================================
    # PERCENTAGE METRICS
    # =====================================================

    def percentage_metrics(self):

        return [

            node

            for node in self.graph.nodes.values()

            if (

                node.entity_type.lower()

                == "measurement"

                and

                node.metadata.get("unit")

                == "%"

            )

        ]

    # =====================================================
    # BUSINESS KPI
    # =====================================================

    def kpis(self):

        return [

            node

            for node in self.graph.nodes.values()

            if (

                node.entity_type.lower()

                == "metric"

            )

        ]

    # =====================================================
    # STANDARDS
    # =====================================================

    def standards(self):

        return [

            node

            for node in self.graph.nodes.values()

            if (

                node.entity_type.lower()

                == "standard"

            )

        ]

    # =====================================================
    # SKILLS
    # =====================================================

    def skills(self):

        return [

            node

            for node in self.graph.nodes.values()

            if (

                node.entity_type.lower()

                == "skill"

            )

        ]