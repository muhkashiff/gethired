"""
Enterprise Graph Ontology API

Enterprise Version

Provides ontology-level information for the KnowledgeGraph.

Responsibilities
----------------
• Identify entity types
• Identify supported entity categories
• Identify relationship categories
• Preserve KPI / BKPI / Metric distinction
• Provide ontology metadata
• Never modify the graph
"""


class GraphOntology:

    # ==========================================================
    # ENTITY TYPES
    # ==========================================================

    ENTITY_TYPES = {

        "action",

        "target",

        "object",

        "metric",

        "kpi",

        "bkpi",

        "business_kpi",

        "measurement",

        "skill",

        "standard",

        "methodology",

        "domain",

        "achievement",

        "leadership",

        "technology",

        "certification",

    }

    # ==========================================================
    # RELATION TYPES
    # ==========================================================

    RELATION_TYPES = {

        "acts_on",

        "targets",

        "creates",

        "manages",

        "monitors",

        "maintains",

        "optimizes",

        "improves",

        "controls",

        "executes",

        "certifies",

        "complies_with",

        "certified_against",

        "audited_against",

        "performed_using",

        "requires",

        "measured_by",

        "measures",

        "reduced",

        "increased",

        "optimized",

        "improved",

        "belongs_to",

        "belongs_to_domain",

        "governs",

        "supports",

        "enables",

        "implements",

        "requires_skill",

        "supports_methodology",

        "used_for",

        "validates",

        "validated_by",

        "semantic_similarity",

        "cross_domain",

        "career_progression",

        "experience_implies_skill",

        "experience_implies_domain",

        "supports_job_matching",

        "supports_resume_scoring",

    }

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, graph=None):

        self.graph = graph

    # ==========================================================
    # ENTITY TYPE VALIDATION
    # ==========================================================

    @classmethod
    def is_entity_type(
        cls,
        entity_type,
    ):

        if not entity_type:
            return False

        return (
            str(entity_type)
            .casefold()
            in cls.ENTITY_TYPES
        )

    # ==========================================================
    # RELATION TYPE VALIDATION
    # ==========================================================

    @classmethod
    def is_relation_type(
        cls,
        relation_type,
    ):

        if not relation_type:
            return False

        return (
            str(relation_type)
            .casefold()
            in cls.RELATION_TYPES
        )

    # ==========================================================
    # KPI
    # ==========================================================

    @classmethod
    def is_kpi(
        cls,
        entity_type,
    ):

        return (
            str(entity_type)
            .casefold()
            == "kpi"
        )

    # ==========================================================
    # BUSINESS KPI
    # ==========================================================

    @classmethod
    def is_business_kpi(
        cls,
        entity_type,
    ):

        return (
            str(entity_type)
            .casefold()
            in {
                "bkpi",
                "business_kpi",
            }
        )

    # ==========================================================
    # METRIC
    # ==========================================================

    @classmethod
    def is_metric(
        cls,
        entity_type,
    ):

        return (
            str(entity_type)
            .casefold()
            == "metric"
        )

    # ==========================================================
    # KPI FAMILY
    # ==========================================================

    @classmethod
    def kpi_family(
        cls,
        entity_type,
    ):

        normalized = (
            str(entity_type)
            .casefold()
        )

        if normalized == "kpi":

            return "KPI"

        if normalized in {
            "bkpi",
            "business_kpi",
        }:

            return "BKPI"

        if normalized == "metric":

            return "Metric"

        return None

    # ==========================================================
    # GRAPH ENTITY TYPES
    # ==========================================================

    def entity_types(self):

        return sorted(
            self.ENTITY_TYPES
        )

    # ==========================================================
    # GRAPH RELATION TYPES
    # ==========================================================

    def relation_types(self):

        return sorted(
            self.RELATION_TYPES
        )

    # ==========================================================
    # NODE TYPE COUNTS
    # ==========================================================

    def type_counts(self):

        if self.graph is None:
            return {}

        counts = {}

        for node in self.graph.get_nodes():

            entity_type = getattr(
                node,
                "entity_type",
                "",
            )

            if not entity_type:
                continue

            counts[entity_type] = (
                counts.get(
                    entity_type,
                    0,
                )
                + 1
            )

        return counts

    # ==========================================================
    # ONTOLOGY DESCRIPTION
    # ==========================================================

    def describe(self):

        return {

            "entity_types": self.entity_types(),

            "relation_types": self.relation_types(),

            "kpi_types": [
                "KPI",
                "BKPI",
                "Metric",
            ],

        }