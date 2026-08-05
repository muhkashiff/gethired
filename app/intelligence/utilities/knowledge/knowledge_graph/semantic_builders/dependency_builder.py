"""
Enterprise Dependency Builder

Builds enterprise dependency relationships.

Purpose
-------
Creates semantic dependencies between entities contained
inside one BusinessStatement.

Runs AFTER

    RelationshipBuilder

    MeasurementBuilder

    AchievementBuilder

Runs BEFORE

    DependencyReasoner

Enterprise V11
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_semantic_builder import (
    BaseSemanticBuilder,
)


class DependencyBuilder(BaseSemanticBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        self._build_action_dependencies(
            context,
            statement,
        )

        self._build_metric_dependencies(
            context,
            statement,
        )

        self._build_skill_dependencies(
            context,
            statement,
        )

    ####################################################################
    # ACTION DEPENDENCIES
    ####################################################################

    def _build_action_dependencies(
        self,
        context,
        statement,
    ) -> None:

        """
        Action

            DEPENDS_ON

        Methodology

        Action

            DEPENDS_ON

        Standard

        Action

            DEPENDS_ON

        Skill
        """

        actions = statement.actions

        if not actions:
            return

        for action in actions:

            if action is None:
                continue

            if not getattr(action, "found", False):
                continue

            #
            # Standards
            #

            for standard in statement.standards:

                if standard is None:
                    continue

                if not getattr(standard, "found", False):
                    continue

                edge = self.create_edge(

                    source=action,

                    target=standard,

                    relation="DEPENDS_ON",

                    reasoning="Action depends on standard",

                    confidence=min(
                        action.confidence,
                        standard.confidence,
                    ),

                )

                self.register_edge(
                    context,
                    edge,
                )

            #
            # Skills
            #

            for skill in statement.skills:

                if skill is None:
                    continue

                if not getattr(skill, "found", False):
                    continue

                edge = self.create_edge(

                    source=action,

                    target=skill,

                    relation="DEPENDS_ON",

                    reasoning="Action depends on skill",

                    confidence=min(
                        action.confidence,
                        skill.confidence,
                    ),

                )

                self.register_edge(
                    context,
                    edge,
                )

            #
            # Methodologies
            #

            for methodology in statement.methods:

                if methodology is None:
                    continue

                if not getattr(methodology, "found", False):
                    continue

                edge = self.create_edge(

                    source=action,

                    target=methodology,

                    relation="DEPENDS_ON",

                    reasoning="Action depends on methodology",

                    confidence=min(
                        action.confidence,
                        methodology.confidence,
                    ),

                )

                self.register_edge(
                    context,
                    edge,
                )

    ####################################################################
    # METRIC DEPENDENCIES
    ####################################################################

    def _build_metric_dependencies(
        self,
        context,
        statement,
    ) -> None:

        """
        Metric

            DEPENDS_ON

        Measurement
        """

        metrics = statement.metrics

        measurements = statement.measurements

        if not metrics:
            return

        if not measurements:
            return

        for metric in metrics:

            if metric is None:
                continue

            if not getattr(metric, "found", False):
                continue

            for measurement in measurements:

                if measurement is None:
                    continue

                if not getattr(measurement, "found", False):
                    continue

                metadata = getattr(
                    measurement,
                    "metadata",
                    {},
                )

                metric_id = metadata.get(
                    "metric_id",
                )

                #
                # Only connect the correct measurement
                #

                if metric_id != metric.entity_id:
                    continue

                edge = self.create_edge(

                    source=metric,

                    target=measurement,

                    relation="DEPENDS_ON",

                    reasoning="Metric depends on measurement",

                    confidence=min(
                        metric.confidence,
                        measurement.confidence,
                    ),

                )

                self.register_edge(
                    context,
                    edge,
                )

    ####################################################################
    # SKILL DEPENDENCIES
    ####################################################################

    def _build_skill_dependencies(
        self,
        context,
        statement,
    ) -> None:

        """
        Skill

            DEPENDS_ON

        Domain

        Skill

            DEPENDS_ON

        Standard
        """

        skills = statement.skills

        if not skills:
            return

        #
        # Skill -> Domain
        #

        for skill in skills:

            if skill is None:
                continue

            if not getattr(skill, "found", False):
                continue

            for domain in statement.domains:

                if domain is None:
                    continue

                if not getattr(domain, "found", False):
                    continue

                if skill.domain.lower() != domain.domain.lower():
                    continue

                edge = self.create_edge(

                    source=skill,

                    target=domain,

                    relation="DEPENDS_ON",

                    reasoning="Skill belongs to domain",

                    confidence=min(
                        skill.confidence,
                        domain.confidence,
                    ),

                )

                self.register_edge(
                    context,
                    edge,
                )

        #
        # Skill -> Standard
        #

        for skill in skills:

            metadata = getattr(
                skill,
                "metadata",
                {},
            )

            linked = metadata.get(
                "standards",
                [],
            )

            for standard in statement.standards:

                if standard.canonical not in linked:
                    continue

                edge = self.create_edge(

                    source=skill,

                    target=standard,

                    relation="DEPENDS_ON",

                    reasoning="Skill supports standard",

                    confidence=min(
                        skill.confidence,
                        standard.confidence,
                    ),

                )

                self.register_edge(
                    context,
                    edge,
                )