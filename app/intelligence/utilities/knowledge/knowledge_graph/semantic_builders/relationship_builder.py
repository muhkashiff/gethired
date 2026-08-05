"""
Enterprise Relationship Builder

Enriches the Knowledge Graph with higher-level semantic
relationships discovered from Business Statements.

Runs AFTER

Node Builders
Edge Builders

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_semantic_builder import (
    BaseSemanticBuilder,
)


class RelationshipBuilder(BaseSemanticBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        self._connect_skills_to_domains(
            context,
            statement,
        )

        self._connect_skills_to_standards(
            context,
            statement,
        )

        self._connect_actions_to_methodologies(
            context,
            statement,
        )

        self._connect_metrics_to_business_area(
            context,
            statement,
        )

    ####################################################################
    # Skill → Domain
    ####################################################################

    def _connect_skills_to_domains(
        self,
        context,
        statement,
    ):

        domains = {
            d.domain.lower(): d
            for d in statement.domains
            if getattr(d, "domain", "")
        }

        for skill in statement.skills:

            if skill is None:
                continue

            if not getattr(skill, "found", False):
                continue

            if not getattr(skill, "domain", ""):
                continue

            domain = domains.get(
                skill.domain.lower()
            )

            if domain is None:
                continue

            edge = self.create_edge(

                source=skill,

                target=domain,

                relation="BELONGS_TO",

                reasoning="Skill belongs to business domain",

                confidence=0.95,

            )

            self.register_edge(
                context,
                edge,
            )

    ####################################################################
    # Skill → Standard
    ####################################################################

    def _connect_skills_to_standards(
        self,
        context,
        statement,
    ):

        standards = {
            s.label.lower(): s
            for s in statement.standards
        }

        for skill in statement.skills:

            if skill is None:
                continue

            if not getattr(skill, "found", False):
                continue

            metadata = getattr(
                skill,
                "metadata",
                {},
            )

            linked = metadata.get(
                "standards",
                [],
            )

            for standard_name in linked:

                standard = standards.get(
                    standard_name.lower()
                )

                if standard is None:
                    continue

                edge = self.create_edge(

                    source=skill,

                    target=standard,

                    relation="SUPPORTS",

                    reasoning="Skill supports standard",

                    confidence=0.90,

                )

                self.register_edge(
                    context,
                    edge,
                )

    ####################################################################
    # Action → Methodology
    ####################################################################

    def _connect_actions_to_methodologies(
        self,
        context,
        statement,
    ):

        methodologies = {
            m.label.lower(): m
            for m in statement.methodologies
        }

        for action in statement.actions:

            if action is None:
                continue

            if not getattr(action, "found", False):
                continue

            metadata = getattr(
                action,
                "metadata",
                {},
            )

            linked = metadata.get(
                "methodologies",
                [],
            )

            for methodology_name in linked:

                methodology = methodologies.get(
                    methodology_name.lower()
                )

                if methodology is None:
                    continue

                edge = self.create_edge(

                    source=action,

                    target=methodology,

                    relation="USES",

                    reasoning="Action uses methodology",

                    confidence=0.90,

                )

                self.register_edge(
                    context,
                    edge,
                )

    ####################################################################
    # Metric → Business Area
    ####################################################################

    def _connect_metrics_to_business_area(
        self,
        context,
        statement,
    ):

        domains = {
            d.business_area.lower(): d
            for d in statement.domains
            if getattr(d, "business_area", "")
        }

        for metric in statement.metrics:

            if metric is None:
                continue

            if not getattr(metric, "found", False):
                continue

            if not getattr(metric, "business_area", ""):
                continue

            domain = domains.get(
                metric.business_area.lower()
            )

            if domain is None:
                continue

            edge = self.create_edge(

                source=metric,

                target=domain,

                relation="MEASURES",

                reasoning="Metric measures business area",

                confidence=0.85,

            )

            self.register_edge(
                context,
                edge,
            )