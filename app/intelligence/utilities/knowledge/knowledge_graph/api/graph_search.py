"""
Enterprise Graph Search

Enterprise Version

Provides text-based and identity-based search over
KnowledgeGraph nodes.

Responsibilities
----------------
• Search nodes by text
• Search by entity ID
• Search by canonical value
• Search by label
• Search by entity type
• Search by category
• Search by business area
• Preserve KPI / BKPI / Metric distinctions
• Return GraphNode objects
"""


class GraphSearch:

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, graph):

        self.graph = graph

    # ==========================================================
    # GENERAL SEARCH
    # ==========================================================

    def search(self, text):
        """
        Search graph nodes using text.

        Searches:

        • entity_id
        • label
        • canonical
        • category
        • business_area

        Matching is case-insensitive.

        Returns
        -------
        list[GraphNode]
        """

        if self.graph is None:
            return []

        if text is None:
            return []

        query = str(text).strip().casefold()

        if not query:
            return []

        results = []

        for node in self.graph.get_nodes():

            searchable_values = [
                getattr(node, "entity_id", ""),
                getattr(node, "node_id", ""),
                getattr(node, "label", ""),
                getattr(node, "canonical", ""),
                getattr(node, "category", ""),
                getattr(node, "business_area", ""),
            ]

            if any(
                query in str(value).casefold()
                for value in searchable_values
                if value is not None
            ):
                results.append(node)

        return results

    # ==========================================================
    # EXACT ENTITY ID
    # ==========================================================

    def by_entity_id(self, entity_id):

        if self.graph is None:
            return None

        if not entity_id:
            return None

        for node in self.graph.get_nodes():

            if (
                getattr(node, "entity_id", "")
                == entity_id
            ):
                return node

        return None

    # ==========================================================
    # EXACT NODE ID
    # ==========================================================

    def by_node_id(self, node_id):

        if self.graph is None:
            return None

        if not node_id:
            return None

        return self.graph.get_node(node_id)

    # ==========================================================
    # TYPE SEARCH
    # ==========================================================

    def by_type(self, entity_type):

        if self.graph is None:
            return []

        if not entity_type:
            return []

        return self.graph.find_by_type(
            entity_type
        )

    # ==========================================================
    # CATEGORY SEARCH
    # ==========================================================

    def by_category(self, category):

        if self.graph is None:
            return []

        if not category:
            return []

        return [
            node
            for node in self.graph.get_nodes()
            if getattr(
                node,
                "category",
                "",
            ).casefold()
            == str(category).casefold()
        ]

    # ==========================================================
    # BUSINESS AREA SEARCH
    # ==========================================================

    def by_business_area(self, business_area):

        if self.graph is None:
            return []

        if not business_area:
            return []

        return [
            node
            for node in self.graph.get_nodes()
            if getattr(
                node,
                "business_area",
                "",
            ).casefold()
            == str(business_area).casefold()
        ]

    # ==========================================================
    # KPI
    # ==========================================================

    def kpis(self):

        return self.by_type("KPI")

    # ==========================================================
    # BUSINESS KPI
    # ==========================================================

    def business_kpis(self):

        return self.by_type("BKPI")

    # ==========================================================
    # METRIC
    # ==========================================================

    def metrics(self):

        return self.by_type("Metric")

    # ==========================================================
    # EXACT TYPE + TEXT
    # ==========================================================

    def search_type(
        self,
        text,
        entity_type,
    ):
        """
        Search within a specific entity type.

        This is important because:

            KPI
            BKPI
            Metric

        must remain separate.
        """

        candidates = self.by_type(
            entity_type
        )

        if not text:
            return candidates

        query = str(text).casefold()

        results = []

        for node in candidates:

            values = [
                getattr(node, "entity_id", ""),
                getattr(node, "label", ""),
                getattr(node, "canonical", ""),
            ]

            if any(
                query in str(value).casefold()
                for value in values
            ):
                results.append(node)

        return results