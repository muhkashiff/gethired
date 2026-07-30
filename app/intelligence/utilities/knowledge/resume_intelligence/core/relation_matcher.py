from enum import Enum


class RelationType(Enum):

    TARGETS = "targets"

    AFFECTS = "affects"

    MEASURED_BY = "measured_by"

    CHANGED_TO = "changed_to"

    CHANGED_FROM = "changed_from"

    ACHIEVED_USING = "achieved_using"

    BELONGS_TO = "belongs_to"

    MANAGES = "manages"

    COUNTS = "counts"

    CERTIFIED_BY = "certified_by"

    APPLIED_TO = "applied_to"

    LOCATED_IN = "located_in"

    REPORTS_TO = "reports_to"

    SUPPORTS = "supports"

    PRODUCES = "produces"

from resume_intelligence.models.dependency_models import DependencyEdge
from resume_intelligence.core.relation_matcher import RelationType


class RelationMatcher:

    def build_edges(self, entities):

        edges = []

        action = entities.get("action")

        metric = entities.get("metric")

        measurement = entities.get("measurement")

        methodology = entities.get("methodology")

        standard = entities.get("standard")

        domain = entities.get("domain")

        team = entities.get("team")

        number = entities.get("number")

        if action and metric:

            edges.append(

                DependencyEdge(

                    action["entity_id"],

                    metric["entity_id"],

                    RelationType.AFFECTS.value,

                    0.98

                )

            )

        if metric and measurement:

            edges.append(

                DependencyEdge(

                    metric["entity_id"],

                    measurement["entity_id"],

                    RelationType.MEASURED_BY.value,

                    0.99

                )

            )

        if action and methodology:

            edges.append(

                DependencyEdge(

                    action["entity_id"],

                    methodology["entity_id"],

                    RelationType.ACHIEVED_USING.value,

                    0.95

                )

            )

        if action and standard:

            edges.append(

                DependencyEdge(

                    action["entity_id"],

                    standard["entity_id"],

                    RelationType.TARGETS.value,

                    0.97

                )

            )

        if standard and domain:

            edges.append(

                DependencyEdge(

                    standard["entity_id"],

                    domain["entity_id"],

                    RelationType.BELONGS_TO.value,

                    0.99

                )

            )

        if action and team:

            edges.append(

                DependencyEdge(

                    action["entity_id"],

                    team["entity_id"],

                    RelationType.MANAGES.value,

                    0.95

                )

            )

        if team and number:

            edges.append(

                DependencyEdge(

                    team["entity_id"],

                    number["entity_id"],

                    RelationType.COUNTS.value,

                    0.98

                )

            )

        return edges