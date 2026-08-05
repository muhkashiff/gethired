"""
Enterprise Ontology Reasoner

Enterprise V6

Purpose
-------
Creates semantic understanding of the graph.

Responsible for

• Standards
• Methodologies
• Skills
• Metrics
• Measurements
• Actions
• Domains
• Business Areas
• Semantic Groups

Output

reasoning.ontology
"""

from collections import defaultdict

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.ontology_models import (

    OntologyReasoningResult,
    OntologyStatistics,
    SemanticGroup,

)


class OntologyReasoner:

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

        result = OntologyReasoningResult()

        ############################################################
        # Entity Extraction
        ############################################################

        result.standards = self._extract(

            graph,

            "standard",

        )

        result.methodologies = self._extract(

            graph,

            "methodology",

        )

        result.skills = self._extract(

            graph,

            "skill",

        )

        result.actions = self._extract(

            graph,

            "action",

        )

        result.metrics = self._extract(

            graph,

            "metric",

        )

        result.measurements = self._extract(

            graph,

            "measurement",

        )

        result.modifiers = self._extract(

            graph,

            "modifier",

        )

        ############################################################
        # Domains
        ############################################################

        result.domains = self._group_domains(graph)

        ############################################################
        # Business Areas
        ############################################################

        result.business_areas = self._group_business_areas(graph)

        ############################################################
        # Semantic Groups
        ############################################################

        result.semantic_groups = (

            self._build_semantic_groups(

                result,

            )

        )

        ############################################################
        # Statistics
        ############################################################

        result.statistics = (

            self._statistics(

                result,

            )

        )

        ############################################################

        reasoning.ontology = result

        reasoning.reasoning_steps.append(

            "Ontology Reasoning"

        )

        return reasoning

    ####################################################################
    # ENTITY EXTRACTION
    ####################################################################

    def _extract(

        self,

        graph,

        entity_type,

    ):

        return [

            node

            for node in graph.get_nodes()

            if node.entity_type == entity_type

        ]

    ####################################################################
    # DOMAIN GROUPING
    ####################################################################

    def _group_domains(

        self,

        graph,

    ):

        grouped = defaultdict(list)

        for node in graph.get_nodes():

            if getattr(

                node,

                "domain",

                "",

            ):

                grouped[node.domain].append(node)

        return dict(grouped)

    ####################################################################
    # BUSINESS AREA GROUPING
    ####################################################################

    def _group_business_areas(

        self,

        graph,

    ):

        grouped = defaultdict(list)

        for node in graph.get_nodes():

            if getattr(

                node,

                "business_area",

                "",

            ):

                grouped[node.business_area].append(node)

        return dict(grouped)

    ####################################################################
    # SEMANTIC GROUPS
    ####################################################################

    def _build_semantic_groups(

        self,

        ontology,

    ):

        groups = []

        for area, entities in ontology.business_areas.items():

            group = SemanticGroup(

                name=area,

                category="Business Area",

                business_area=area,

                entities=entities,

            )

            groups.append(group)

        return groups

    ####################################################################
    # STATISTICS
    ####################################################################

    def _statistics(

        self,

        ontology,

    ):

        stats = OntologyStatistics()

        stats.standards = len(

            ontology.standards

        )

        stats.methodologies = len(

            ontology.methodologies

        )

        stats.skills = len(

            ontology.skills

        )

        stats.actions = len(

            ontology.actions

        )

        stats.metrics = len(

            ontology.metrics

        )

        stats.measurements = len(

            ontology.measurements

        )

        stats.modifiers = len(

            ontology.modifiers

        )

        stats.domains = len(

            ontology.domains

        )

        stats.business_areas = len(

            ontology.business_areas

        )

        stats.semantic_groups = len(

            ontology.semantic_groups

        )

        return stats