"""
Graph-Native Knowledge Profile Builder

Enterprise V14

KnowledgeGraph
        ↓
KnowledgeProfileBuilder
        ↓
KnowledgeProfile

The graph is the source of truth.

This builder does NOT depend on:

    CapabilityReasoner
    GenericEvidenceBuilder
    DomainEvidence
    TechnicalEvidence
    LeadershipEvidence
    ontology capability definitions

Entity-level metadata such as:

    impact_weight
    impact_score
    ats_score
    domain
    business_area
    entity_type
    canonical
    description

is consumed directly from KnowledgeGraph nodes.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from .profile_models import (
    KnowledgeProfile,
    SummaryProfile,
    AchievementProfile,
    LeadershipProfile,
    SeniorityProfile,
    MetricProfile,
    DomainProfile,
    EntityProfile,
    ImpactProfile,
    ATSProfile,
    BusinessStatementProfile,
)


class KnowledgeProfileBuilder:

    # ============================================================
    # PUBLIC
    # ============================================================

    def build(
        self,
        graph,
        semantic_resolution=None,
    ) -> KnowledgeProfile:
        """
        Build KnowledgeProfile directly from KnowledgeGraph.
        """

        if graph is None:

            return KnowledgeProfile(
                confidence=0.0
            )

        nodes = self._get_nodes(graph)

        edges = self._get_edges(graph)

        statements = self._get_business_statements(
            semantic_resolution
        )

        entity_profile = self._build_entities(
            nodes
        )

        impact_profile = self._build_impact(
            nodes
        )

        ats_profile = self._build_ats(
            nodes
        )

        domain_profile = self._build_domains(
            nodes
        )

        metric_profile = self._build_metrics(
            nodes
        )

        achievement_profile = self._build_achievements(
            nodes,
            statements,
        )

        leadership_profile = self._build_leadership(
            nodes
        )

        seniority_profile = self._build_seniority(
            nodes
        )

        business_statement_profile = (
            self._build_business_statements(
                statements
            )
        )

        summary = self._build_summary(
            impact=impact_profile,
            ats=ats_profile,
            achievements=achievement_profile,
            leadership=leadership_profile,
            seniority=seniority_profile,
        )

        confidence = self._calculate_confidence(
            nodes,
            statements,
        )

        return KnowledgeProfile(

            summary=summary,

            entities=entity_profile,

            achievements=achievement_profile,

            leadership=leadership_profile,

            seniority=seniority_profile,

            metrics=metric_profile,

            domains=domain_profile,

            impact=impact_profile,

            ats=ats_profile,

            business_statements=(
                business_statement_profile
            ),

            confidence=confidence,
        )

    # ============================================================
    # GRAPH ACCESS
    # ============================================================

    @staticmethod
    def _get_nodes(graph) -> list[Any]:

        getter = getattr(
            graph,
            "get_nodes",
            None,
        )

        if callable(getter):

            return list(
                getter() or []
            )

        nodes = getattr(
            graph,
            "nodes",
            [],
        )

        if isinstance(
            nodes,
            dict,
        ):

            return list(
                nodes.values()
            )

        return list(
            nodes or []
        )

    @staticmethod
    def _get_edges(graph) -> list[Any]:

        getter = getattr(
            graph,
            "get_edges",
            None,
        )

        if callable(getter):

            return list(
                getter() or []
            )

        edges = getattr(
            graph,
            "edges",
            [],
        )

        if isinstance(
            edges,
            dict,
        ):

            return list(
                edges.values()
            )

        return list(
            edges or []
        )

    # ============================================================
    # ENTITY PROFILE
    # ============================================================

    def _build_entities(
        self,
        nodes,
    ) -> EntityProfile:

        counts = Counter()

        entities = []

        for node in nodes:

            entity_type = self._entity_type(
                node
            )

            counts[entity_type] += 1

            entities.append(
                self._entity_dict(node)
            )

        return EntityProfile(

            total_entities=len(nodes),

            entity_counts=dict(
                counts
            ),

            entities=entities,
        )

    # ============================================================
    # IMPACT
    # ============================================================

    def _build_impact(
        self,
        nodes,
    ) -> ImpactProfile:

        values = []

        weighted_entities = []

        for node in nodes:

            impact = self._impact_value(
                node
            )

            if impact <= 0:

                continue

            values.append(
                impact
            )

            weighted_entities.append({

                "entity_id": getattr(
                    node,
                    "entity_id",
                    getattr(
                        node,
                        "node_id",
                        "",
                    ),
                ),

                "canonical": getattr(
                    node,
                    "canonical",
                    "",
                ),

                "entity_type": self._entity_type(
                    node
                ),

                "impact_weight": impact,

            })

        if not values:

            return ImpactProfile()

        return ImpactProfile(

            total_impact=round(
                sum(values),
                2,
            ),

            average_impact=round(
                sum(values) / len(values),
                2,
            ),

            maximum_impact=round(
                max(values),
                2,
            ),

            entity_count=len(values),

            weighted_entities=(
                weighted_entities
            ),
        )

    # ============================================================
    # ATS
    # ============================================================

    def _build_ats(
        self,
        nodes,
    ) -> ATSProfile:

        total = 0.0

        count = 0

        matched = []

        for node in nodes:

            score = self._ats_value(
                node
            )

            if score <= 0:

                continue

            total += score

            count += 1

            matched.append({

                "entity_id": getattr(
                    node,
                    "entity_id",
                    getattr(
                        node,
                        "node_id",
                        "",
                    ),
                ),

                "canonical": getattr(
                    node,
                    "canonical",
                    "",
                ),

                "entity_type": self._entity_type(
                    node
                ),

                "ats_score": score,

            })

        return ATSProfile(

            score=round(
                total,
                2,
            ),

            entity_count=count,

            matched_entities=matched,
        )

    # ============================================================
    # DOMAINS
    # ============================================================

    def _build_domains(
        self,
        nodes,
    ) -> DomainProfile:

        domains = Counter()

        business_areas = Counter()

        for node in nodes:

            domain = str(
                getattr(
                    node,
                    "domain",
                    "",
                )
                or ""
            ).strip()

            business_area = str(
                getattr(
                    node,
                    "business_area",
                    "",
                )
                or ""
            ).strip()

            if domain:

                domains[domain] += 1

            if business_area:

                business_areas[
                    business_area
                ] += 1

        return DomainProfile(

            domains=dict(
                domains
            ),

            business_areas=dict(
                business_areas
            ),
        )

    # ============================================================
    # METRICS
    # ============================================================

    def _build_metrics(
        self,
        nodes,
    ) -> MetricProfile:

        profile = MetricProfile()

        metric_types = {
            "metric",
            "kpi",
            "bkpi",
            "business_kpi",
            "measurement",
        }

        for node in nodes:

            entity_type = (
                self._entity_type(node)
                .casefold()
            )

            if entity_type not in metric_types:

                continue

            profile.total_metrics += 1

            metadata = getattr(
                node,
                "metadata",
                {},
            )

            if not isinstance(
                metadata,
                dict,
            ):

                metadata = {}

            direction = str(
                getattr(
                    node,
                    "preferred_direction",
                    "",
                )
                or metadata.get(
                    "direction",
                    "",
                )
                or ""
            ).casefold()

            if direction in {
                "increase",
                "increased",
                "positive",
                "improved",
            }:

                profile.positive_metrics += 1

                profile.increase_metrics += 1

            elif direction in {
                "decrease",
                "decreased",
                "negative",
                "reduced",
            }:

                profile.negative_metrics += 1

                profile.decrease_metrics += 1

            profile.metrics.append(
                self._entity_dict(node)
            )

        return profile

    # ============================================================
    # ACHIEVEMENTS
    # ============================================================

    def _build_achievements(
        self,
        nodes,
        statements,
    ) -> AchievementProfile:

        achievement_nodes = []

        for node in nodes:

            entity_type = (
                self._entity_type(node)
                .casefold()
            )

            if entity_type in {
                "achievement",
                "result",
                "business_value",
                "businessvalue",
                "impact",
            }:

                achievement_nodes.append(
                    node
                )

        quantified = 0

        top = []

        for node in achievement_nodes:

            metadata = getattr(
                node,
                "metadata",
                {},
            )

            if not isinstance(
                metadata,
                dict,
            ):

                metadata = {}

            if (
                metadata.get(
                    "quantified",
                    False,
                )
                or metadata.get(
                    "has_metric",
                    False,
                )
            ):

                quantified += 1

            top.append(
                self._entity_dict(node)
            )

        impact_score = round(
            sum(
                self._impact_value(node)
                for node in achievement_nodes
            ),
            2,
        )

        return AchievementProfile(

            achievement_count=len(
                achievement_nodes
            ),

            quantified_count=quantified,

            impact_score=impact_score,

            top_achievements=top[:10],
        )

    # ============================================================
    # LEADERSHIP
    # ============================================================

    def _build_leadership(
        self,
        nodes,
    ) -> LeadershipProfile:

        actions = Counter()

        count = 0

        for node in nodes:

            entity_type = (
                self._entity_type(node)
                .casefold()
            )

            canonical = str(
                getattr(
                    node,
                    "canonical",
                    "",
                )
                or ""
            )

            if entity_type == "action":

                if any(
                    keyword in canonical.casefold()
                    for keyword in (
                        "lead",
                        "manage",
                        "direct",
                        "supervise",
                        "mentor",
                        "train",
                        "develop",
                        "coordinate",
                        "implement",
                    )
                ):

                    count += 1

                    actions[
                        canonical
                    ] += 1

        return LeadershipProfile(

            score=float(
                count
            ),

            entity_count=count,

            actions=dict(
                actions
            ),
        )

    # ============================================================
    # SENIORITY
    # ============================================================

    def _build_seniority(
        self,
        nodes,
    ) -> SeniorityProfile:

        indicators = []

        seniority_keywords = {

            "lead",
            "manager",
            "director",
            "head",
            "chief",
            "executive",
            "senior",
            "supervisor",
            "managing director",
        }

        score = 0.0

        for node in nodes:

            text = " ".join(
                str(
                    getattr(
                        node,
                        attribute,
                        "",
                    )
                    or ""
                )
                for attribute in (
                    "canonical",
                    "description",
                    "business_meaning",
                )
            ).casefold()

            for keyword in seniority_keywords:

                if keyword in text:

                    score += 1.0

                    indicators.append(
                        keyword
                    )

                    break

        level = ""

        if score >= 8:

            level = "Executive"

        elif score >= 5:

            level = "Senior"

        elif score >= 3:

            level = "Mid-Senior"

        elif score >= 1:

            level = "Professional"

        return SeniorityProfile(

            score=round(
                score,
                2,
            ),

            level=level,

            indicators=sorted(
                set(indicators)
            ),
        )

    # ============================================================
    # BUSINESS STATEMENTS
    # ============================================================

    @staticmethod
    def _get_business_statements(
        semantic_resolution,
    ) -> list[Any]:

        if semantic_resolution is None:

            return []

        statements = getattr(
            semantic_resolution,
            "business_statements",
            [],
        )

        return list(
            statements or []
        )

    def _build_business_statements(
        self,
        statements,
    ) -> BusinessStatementProfile:

        output = []

        for statement in statements:

            if isinstance(
                statement,
                dict,
            ):

                output.append(
                    dict(statement)
                )

            else:

                data = {}

                for name in getattr(
                    statement,
                    "__dataclass_fields__",
                    {},
                ):

                    data[name] = getattr(
                        statement,
                        name,
                        None,
                    )

                output.append(
                    data
                )

        return BusinessStatementProfile(

            total_statements=len(
                output
            ),

            statements=output,
        )

    # ============================================================
    # SUMMARY
    # ============================================================

    @staticmethod
    def _build_summary(
        impact,
        ats,
        achievements,
        leadership,
        seniority,
    ) -> SummaryProfile:

        scores = [

            impact.average_impact,

            ats.score,

            achievements.impact_score,

            leadership.score,

            seniority.score,

        ]

        valid = [
            value
            for value in scores
            if value > 0
        ]

        overall = (
            sum(valid) / len(valid)
            if valid
            else 0.0
        )

        return SummaryProfile(

            overall_score=round(
                overall,
                2,
            ),

            impact_score=round(
                impact.total_impact,
                2,
            ),

            ats_score=round(
                ats.score,
                2,
            ),

            achievement_score=round(
                achievements.impact_score,
                2,
            ),

            leadership_score=round(
                leadership.score,
                2,
            ),

            seniority_score=round(
                seniority.score,
                2,
            ),

            career_level=seniority.level,
        )

    # ============================================================
    # CONFIDENCE
    # ============================================================

    @staticmethod
    def _calculate_confidence(
        nodes,
        statements,
    ) -> float:

        if not nodes:

            return 0.0

        confidences = []

        for node in nodes:

            value = getattr(
                node,
                "confidence",
                None,
            )

            if value is None:

                continue

            try:

                value = float(
                    value
                )

            except (
                TypeError,
                ValueError,
            ):

                continue

            if 0 <= value <= 1:

                confidences.append(
                    value
                )

        if not confidences:

            return 1.0

        return round(
            sum(confidences)
            / len(confidences),
            2,
        )

    # ============================================================
    # ENTITY UTILITIES
    # ============================================================

    @staticmethod
    def _entity_type(
        node,
    ) -> str:

        return str(
            getattr(
                node,
                "entity_type",
                getattr(
                    node,
                    "type",
                    "",
                ),
            )
            or ""
        ).strip()

    @staticmethod
    def _impact_value(
        node,
    ) -> float:

        for attribute in (
            "impact_score",
            "impact_weight",
        ):

            value = getattr(
                node,
                attribute,
                None,
            )

            if value is not None:

                try:

                    return float(
                        value
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

        return 0.0

    @staticmethod
    def _ats_value(
        node,
    ) -> float:

        for attribute in (
            "ats_score",
            "ats_weight",
            "ats",
        ):

            value = getattr(
                node,
                attribute,
                None,
            )

            if value is not None:

                try:

                    return float(
                        value
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

        metadata = getattr(
            node,
            "metadata",
            {},
        )

        if isinstance(
            metadata,
            dict,
        ):

            for key in (
                "ats_score",
                "ats_weight",
                "ats",
            ):

                value = metadata.get(
                    key
                )

                if value is not None:

                    try:

                        return float(
                            value
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        pass

        return 0.0

    @classmethod
    def _entity_dict(
        cls,
        node,
    ) -> dict[str, Any]:

        return {

            "node_id": getattr(
                node,
                "node_id",
                "",
            ),

            "entity_id": getattr(
                node,
                "entity_id",
                "",
            ),

            "canonical": getattr(
                node,
                "canonical",
                "",
            ),

            "entity_type": cls._entity_type(
                node
            ),

            "domain": getattr(
                node,
                "domain",
                "",
            ),

            "business_area": getattr(
                node,
                "business_area",
                "",
            ),

            "description": getattr(
                node,
                "description",
                "",
            ),

            "confidence": getattr(
                node,
                "confidence",
                0.0,
            ),

            "impact_weight": cls._impact_value(
                node
            ),

            "ats_score": cls._ats_value(
                node
            ),
        }