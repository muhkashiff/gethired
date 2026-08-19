"""
Knowledge Profile Builder
Enterprise V14

Purpose
-------

Build KnowledgeProfile from an already populated KnowledgeGraph.

Architecture
------------

KnowledgeGraph
        |
        v
KnowledgeProfileBuilder
        |
        +--> SummaryProfile
        +--> EntityProfile
        +--> AchievementProfile
        +--> LeadershipProfile
        +--> SeniorityProfile
        +--> MetricProfile
        +--> DomainProfile
        +--> ModifierProfile
        +--> ImpactProfile
        +--> ATSProfile
        +--> BusinessStatementProfile
        |
        v
KnowledgeProfile


IMPORTANT
---------

This builder DOES NOT:

    - rebuild the KnowledgeGraph
    - create graph nodes
    - create graph edges
    - modify existing graph nodes
    - modify existing graph edges
    - perform ontology matching
    - perform semantic extraction

The KnowledgeGraph is treated as the source of truth.

The builder is intentionally tolerant of small differences between
KnowledgeGraph / graph-node implementations.

It supports:

    graph.nodes
    graph.nodes.values()
    graph.nodes as iterable
    graph.edges
    graph.edges.values()
    graph.edges as iterable

It also supports nodes represented as:

    objects
    dictionaries

No graph information is discarded.
"""


from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Iterable, Optional


# ============================================================================
# MODEL IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import (
    KnowledgeProfile,
    SummaryProfile,
    EntityProfile,
    AchievementProfile,
    LeadershipProfile,
    SeniorityProfile,
    MetricProfile,
    DomainProfile,
    ModifierProfile,
    ImpactProfile,
    ATSProfile,
    BusinessStatementProfile,
)


# ============================================================================
# BUILDER
# ============================================================================


class KnowledgeProfileBuilder:
    """
    Build a KnowledgeProfile from an existing KnowledgeGraph.

    The graph is NEVER rebuilt here.

    The builder reads:

        graph.nodes
        graph.edges

    and derives the profile components from them.
    """

    # ------------------------------------------------------------------------
    # KNOWN ENTITY TYPES
    # ------------------------------------------------------------------------

    ENTITY_TYPES = {
        "skill",
        "target",
        "domain",
        "action",
        "metric",
        "standard",
        "certification",
        "technology",
        "methodology",
        "modifier",
        "kpi",
    }

    # ------------------------------------------------------------------------
    # LEADERSHIP ACTIONS
    # ------------------------------------------------------------------------

    LEADERSHIP_ACTIONS = {
        "lead",
        "manage",
        "train",
        "implement",
        "direct",
        "supervise",
        "mentor",
        "coach",
        "coordinate",
        "develop",
        "establish",
        "oversee",
        "own",
        "drive",
        "head",
    }

    EXECUTIVE_ACTIONS = {
        "lead",
        "manage",
        "direct",
        "supervise",
        "oversee",
        "own",
        "head",
        "establish",
    }

    # ------------------------------------------------------------------------
    # SENIORITY INDICATORS
    # ------------------------------------------------------------------------

    SENIORITY_INDICATORS = {
        "lead": 4.0,
        "manage": 4.0,
        "direct": 5.0,
        "supervise": 4.0,
        "oversee": 4.0,
        "head": 5.0,
        "own": 5.0,
        "establish": 4.0,
        "drive": 4.0,
        "mentor": 3.0,
        "coach": 3.0,
        "coordinate": 2.5,
        "implement": 2.0,
        "improve": 2.0,
        "reduce": 2.0,
        "increase": 2.0,
        "develop": 3.0,
        "train": 3.0,
    }

    # ------------------------------------------------------------------------
    # MODIFIER TYPES
    # ------------------------------------------------------------------------

    MODIFIER_TYPES = {
        "modifier",
        "executive_modifier",
        "strategic_modifier",
        "ownership_modifier",
        "scale_modifier",
        "scope_modifier",
    }

    # ------------------------------------------------------------------------
    # INITIALIZATION
    # ------------------------------------------------------------------------

    def __init__(
        self,
        top_n: int = 10,
    ) -> None:

        self.top_n = max(
            int(top_n),
            1,
        )

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def build(
        self,
        knowledge_graph: Any = None,
        graph: Any = None,
        business_statements: Optional[Iterable[Any]] = None,
    ) -> KnowledgeProfile:
        """
        Build KnowledgeProfile.

        Preferred:

            builder.build(
                knowledge_graph
            )

        Compatibility:

            builder.build(
                graph=knowledge_graph
            )

        business_statements may optionally be supplied when the graph
        implementation does not expose statements directly.
        """

        if knowledge_graph is None:

            knowledge_graph = graph

        if knowledge_graph is None:

            return KnowledgeProfile()

        # ---------------------------------------------------------------------
        # IMPORTANT:
        #
        # We read the existing graph.
        #
        # We NEVER rebuild nodes or edges.
        # ---------------------------------------------------------------------

        nodes = self._extract_nodes(
            knowledge_graph
        )

        edges = self._extract_edges(
            knowledge_graph
        )

        statements = self._extract_business_statements(
            knowledge_graph=knowledge_graph,
            explicit_statements=business_statements,
        )

        # ---------------------------------------------------------------------
        # PROFILE COMPONENTS
        # ---------------------------------------------------------------------

        entity_profile = self._build_entity_profile(
            nodes
        )

        achievement_profile = self._build_achievement_profile(
            nodes
        )

        leadership_profile = self._build_leadership_profile(
            nodes
        )

        seniority_profile = self._build_seniority_profile(
            nodes
        )

        metric_profile = self._build_metric_profile(
            nodes
        )

        domain_profile = self._build_domain_profile(
            nodes
        )

        modifier_profile = self._build_modifier_profile(
            nodes
        )

        impact_profile = self._build_impact_profile(
            nodes
        )

        ats_profile = self._build_ats_profile(
            nodes
        )

        statement_profile = self._build_business_statement_profile(
            statements
        )

        # ---------------------------------------------------------------------
        # SUMMARY
        # ---------------------------------------------------------------------

        summary = self._build_summary_profile(
            achievement_profile=achievement_profile,
            leadership_profile=leadership_profile,
            seniority_profile=seniority_profile,
            impact_profile=impact_profile,
            ats_profile=ats_profile,
        )

        # ---------------------------------------------------------------------
        # CONFIDENCE
        # ---------------------------------------------------------------------

        confidence = self._profile_confidence(
            nodes=nodes,
            edges=edges,
            achievements=achievement_profile,
            ats=ats_profile,
            statements=statement_profile,
        )

        # ---------------------------------------------------------------------
        # MASTER PROFILE
        # ---------------------------------------------------------------------

        return KnowledgeProfile(

            summary=summary,

            entities=entity_profile,

            achievements=achievement_profile,

            leadership=leadership_profile,

            seniority=seniority_profile,

            metrics=metric_profile,

            domains=domain_profile,

            modifiers=modifier_profile,

            impact=impact_profile,

            ats=ats_profile,

            business_statements=statement_profile,

            confidence=confidence,
        )

    # =========================================================================
    # GRAPH EXTRACTION
    # =========================================================================

    @classmethod
    def _extract_nodes(
        cls,
        graph: Any,
    ) -> list[Any]:
        """
        Extract ALL graph nodes.

        No node filtering occurs here.
        """

        candidates = getattr(
            graph,
            "nodes",
            None,
        )

        if candidates is None:

            return []

        if isinstance(
            candidates,
            dict,
        ):

            return list(
                candidates.values()
            )

        try:

            return list(
                candidates
            )

        except TypeError:

            return []

    # -------------------------------------------------------------------------

    @classmethod
    def _extract_edges(
        cls,
        graph: Any,
    ) -> list[Any]:
        """
        Extract ALL graph edges.

        Edges are not scored or rebuilt here.
        """

        candidates = getattr(
            graph,
            "edges",
            None,
        )

        if candidates is None:

            return []

        if isinstance(
            candidates,
            dict,
        ):

            return list(
                candidates.values()
            )

        try:

            return list(
                candidates
            )

        except TypeError:

            return []

    # =========================================================================
    # GENERIC VALUE HELPERS
    # =========================================================================

    @staticmethod
    def _value(
        obj: Any,
        *names: str,
        default: Any = None,
    ) -> Any:
        """
        Read the first available attribute/dictionary key.
        """

        if obj is None:

            return default

        for name in names:

            if isinstance(
                obj,
                dict,
            ):

                value = obj.get(
                    name
                )

            else:

                value = getattr(
                    obj,
                    name,
                    None,
                )

            if value is not None:

                return value

        return default

    # -------------------------------------------------------------------------

    @classmethod
    def _text(
        cls,
        obj: Any,
        *names: str,
        default: str = "",
    ) -> str:

        value = cls._value(
            obj,
            *names,
            default=default,
        )

        if value is None:

            return default

        return str(
            value
        ).strip()

    # -------------------------------------------------------------------------

    @classmethod
    def _float(
        cls,
        obj: Any,
        *names: str,
        default: float = 0.0,
    ) -> float:

        value = cls._value(
            obj,
            *names,
            default=None,
        )

        if value is None:

            return default

        try:

            return float(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return default

    # -------------------------------------------------------------------------

    @classmethod
    def _bool(
        cls,
        obj: Any,
        *names: str,
        default: bool = False,
    ) -> bool:

        value = cls._value(
            obj,
            *names,
            default=None,
        )

        if value is None:

            return default

        if isinstance(
            value,
            bool,
        ):

            return value

        if isinstance(
            value,
            str,
        ):

            return value.strip().casefold() in {
                "true",
                "yes",
                "1",
                "positive",
                "increase",
                "increased",
            }

        return bool(
            value
        )

    # -------------------------------------------------------------------------

    @classmethod
    def _metadata(
        cls,
        obj: Any,
    ) -> dict[str, Any]:

        metadata = cls._value(
            obj,
            "metadata",
            default={},
        )

        if isinstance(
            metadata,
            dict,
        ):

            return metadata

        return {}

    # =========================================================================
    # ENTITY IDENTITY
    # =========================================================================

    @classmethod
    def _entity_id(
        cls,
        entity: Any,
    ) -> str:

        return cls._text(
            entity,
            "entity_id",
            "node_id",
            "id",
        )

    # -------------------------------------------------------------------------

    @classmethod
    def _node_id(
        cls,
        entity: Any,
    ) -> str:

        return cls._text(
            entity,
            "node_id",
            "entity_id",
            "id",
        )

    # -------------------------------------------------------------------------

    @classmethod
    def _label(
        cls,
        entity: Any,
    ) -> str:

        return cls._text(
            entity,
            "label",
            "canonical",
            "name",
            "normalized",
            "original",
        )

    # -------------------------------------------------------------------------

    @classmethod
    def _entity_type(
        cls,
        entity: Any,
    ) -> str:

        return cls._text(
            entity,
            "entity_type",
            "type",
            "node_type",
            default="",
        ).casefold()

    # -------------------------------------------------------------------------

    @classmethod
    def _category(
        cls,
        entity: Any,
    ) -> str:

        return cls._text(
            entity,
            "category",
            default="",
        )

    # -------------------------------------------------------------------------

    @classmethod
    def _business_area(
        cls,
        entity: Any,
    ) -> str:

        return cls._text(
            entity,
            "business_area",
            default="",
        )

    # -------------------------------------------------------------------------

    @classmethod
    def _domain(
        cls,
        entity: Any,
    ) -> str:

        return cls._text(
            entity,
            "domain",
            "primary_domain",
            default="",
        )

    # =========================================================================
    # ENTITY PROFILE
    # =========================================================================

    def _build_entity_profile(
        self,
        nodes: list[Any],
    ) -> EntityProfile:

        counts = Counter()

        entities = []

        for node in nodes:

            entity_type = self._entity_type(
                node
            )

            if not entity_type:

                continue

            counts[
                entity_type
            ] += 1

            # Preserve ALL node information.
            entities.append(
                self._serialize_entity(
                    node
                )
            )

        return EntityProfile(

            total_entities=len(
                nodes
            ),

            entity_counts=dict(
                counts
            ),

            entities=entities,
        )

    # =========================================================================
    # ENTITY SERIALIZATION
    # =========================================================================

    @classmethod
    def _serialize_entity(
        cls,
        entity: Any,
    ) -> dict[str, Any]:
        """
        Convert graph node into a profile dictionary.

        Important:
        This preserves the important semantic information instead of
        reducing the node to only its name.
        """

        metadata = cls._metadata(
            entity
        )

        result = {

            "node_id": cls._node_id(
                entity
            ),

            "entity_id": cls._entity_id(
                entity
            ),

            "label": cls._label(
                entity
            ),

            "canonical": cls._text(
                entity,
                "canonical",
            ),

            "normalized": cls._text(
                entity,
                "normalized",
            ),

            "entity_type": cls._entity_type(
                entity
            ),

            "category": cls._category(
                entity
            ),

            "domain": cls._domain(
                entity
            ),

            "business_area": cls._business_area(
                entity
            ),

            "description": cls._text(
                entity,
                "description",
            ),

            "confidence": cls._float(
                entity,
                "confidence",
                default=0.0,
            ),

            "impact_weight": cls._impact_weight(
                entity
            ),

            "achievement": cls._bool(
                entity,
                "achievement",
            ),

            "quantified": cls._bool(
                entity,
                "quantified",
            ),
        }

        # Preserve ATS fields when available.

        ats = cls._extract_ats(
            entity
        )

        if ats:

            result[
                "ats"
            ] = ats

        # Preserve useful metadata.

        if metadata:

            result[
                "metadata"
            ] = dict(
                metadata
            )

        return result

    # =========================================================================
    # IMPACT
    # =========================================================================

    @classmethod
    def _impact_weight(
        cls,
        entity: Any,
    ) -> float:

        value = cls._value(
            entity,
            "impact_weight",
            default=None,
        )

        if value is None:

            metadata = cls._metadata(
                entity
            )

            value = metadata.get(
                "impact_weight",
                0.0,
            )

        try:

            return float(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    # =========================================================================
    # ATS
    # =========================================================================

    @classmethod
    def _extract_ats(
        cls,
        entity: Any,
    ) -> dict[str, Any]:
        """
        Extract ATS information from every possible known location.
        """

        metadata = cls._metadata(
            entity
        )

        ats_metadata = metadata.get(
            "ats"
        )

        result = {}

        # Direct attributes.

        for key in (
            "ats_score",
            "ats_weight",
            "ats_match",
            "ats_matched",
            "matched",
            "keyword_match",
            "keyword_score",
        ):

            value = cls._value(
                entity,
                key,
                default=None,
            )

            if value is not None:

                result[
                    key
                ] = value

        # Direct metadata.

        for key in (
            "ats_score",
            "ats_weight",
            "ats_match",
            "ats_matched",
            "matched",
            "keyword_match",
            "keyword_score",
        ):

            if key in metadata:

                result[
                    key
                ] = metadata[
                    key
                ]

        # Nested ATS metadata.

        if isinstance(
            ats_metadata,
            dict,
        ):

            result[
                "ats"
            ] = dict(
                ats_metadata
            )

        return result

    # =========================================================================
    # ATS PROFILE
    # =========================================================================

    def _build_ats_profile(
        self,
        nodes: list[Any],
    ) -> ATSProfile:
        """
        Build ATS profile.

        The previous implementation returned:

            score = 0
            entity_count = 0

        because it relied on one exact ATS field.

        This implementation checks:

            direct ATS fields
            metadata ATS fields
            nested ATS objects
            matched flags
            keyword scores

        It does NOT require every node to have ATS data.
        """

        matched = []

        scores = []

        for node in nodes:

            ats = self._extract_ats(
                node
            )

            if not ats:

                continue

            score = self._ats_score_from_data(
                ats
            )

            is_matched = self._ats_is_matched(
                ats
            )

            if score is not None:

                scores.append(
                    score
                )

            if (
                is_matched
                or score is not None
            ):

                record = self._serialize_entity(
                    node
                )

                record[
                    "ats_score"
                ] = (
                    score
                    if score is not None
                    else 0.0
                )

                record[
                    "ats_matched"
                ] = is_matched

                matched.append(
                    record
                )

        if not scores:

            score = 0.0

        else:

            score = round(
                sum(scores)
                / len(scores),
                4,
            )

        return ATSProfile(

            score=score,

            entity_count=len(
                matched
            ),

            matched_entities=matched,
        )

    # -------------------------------------------------------------------------

    @classmethod
    def _ats_score_from_data(
        cls,
        ats: dict[str, Any],
    ) -> Optional[float]:

        candidate_values = []

        for key in (
            "ats_score",
            "ats_weight",
            "keyword_score",
            "keyword_match",
        ):

            if key in ats:

                value = ats[
                    key
                ]

                if isinstance(
                    value,
                    bool,
                ):

                    continue

                try:

                    candidate_values.append(
                        float(value)
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

        nested = ats.get(
            "ats"
        )

        if isinstance(
            nested,
            dict,
        ):

            for key in (
                "score",
                "weight",
                "match_score",
                "keyword_score",
            ):

                if key in nested:

                    try:

                        candidate_values.append(
                            float(
                                nested[
                                    key
                                ]
                            )
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        pass

        if not candidate_values:

            return None

        # If scores are percentages, normalize to 0-1.

        value = max(
            candidate_values
        )

        if value > 1.0:

            if value <= 100.0:

                value /= 100.0

        return round(
            max(
                0.0,
                min(
                    value,
                    1.0,
                ),
            ),
            4,
        )

    # -------------------------------------------------------------------------

    @classmethod
    def _ats_is_matched(
        cls,
        ats: dict[str, Any],
    ) -> bool:

        for key in (
            "ats_match",
            "ats_matched",
            "matched",
            "keyword_match",
        ):

            if key not in ats:

                continue

            value = ats[
                key
            ]

            if isinstance(
                value,
                bool,
            ):

                if value:

                    return True

            elif isinstance(
                value,
                (int, float),
            ):

                if value > 0:

                    return True

            elif isinstance(
                value,
                str,
            ):

                if value.strip().casefold() in {
                    "true",
                    "yes",
                    "matched",
                    "match",
                    "1",
                }:

                    return True

        return False

    # =========================================================================
    # ACHIEVEMENTS
    # =========================================================================

    def _is_achievement(
        self,
        node: Any,
    ) -> bool:

        if self._bool(
            node,
            "achievement",
            "is_achievement",
            default=False,
        ):

            return True

        metadata = self._metadata(
            node
        )

        if metadata.get(
            "achievement"
        ):

            return True

        category = self._category(
            node
        ).casefold()

        return category in {
            "achievement",
            "impact",
            "result",
        }

    # -------------------------------------------------------------------------

    def _build_achievement_profile(
        self,
        nodes: list[Any],
    ) -> AchievementProfile:

        achievement_nodes = [
            node
            for node in nodes
            if self._is_achievement(
                node
            )
        ]

        quantified = [
            node
            for node in achievement_nodes
            if self._bool(
                node,
                "quantified",
                "is_quantified",
                default=False,
            )
            or self._has_numeric_evidence(
                node
            )
        ]

        impact_values = [
            self._impact_weight(
                node
            )
            for node in achievement_nodes
        ]

        impact_values = [
            value
            for value in impact_values
            if value > 0
        ]

        impact_score = round(
            sum(
                impact_values
            ),
            4,
        )

        magnitude_values = [
            self._magnitude_score(
                node
            )
            for node in quantified
        ]

        magnitude_values = [
            value
            for value in magnitude_values
            if value > 0
        ]

        magnitude_score = round(
            sum(
                magnitude_values
            ),
            4,
        )

        top_achievements = sorted(
            (
                self._serialize_entity(
                    node
                )
                for node in achievement_nodes
            ),
            key=lambda item: (
                float(
                    item.get(
                        "impact_weight",
                        0.0,
                    )
                    or 0.0
                )
            ),
            reverse=True,
        )[: self.top_n]

        metrics = [
            node
            for node in nodes
            if self._entity_type(
                node
            ) in {
                "metric",
                "kpi",
            }
        ]

        top_metrics = sorted(
            (
                self._serialize_entity(
                    node
                )
                for node in metrics
            ),
            key=lambda item: (
                float(
                    item.get(
                        "impact_weight",
                        0.0,
                    )
                    or 0.0
                )
            ),
            reverse=True,
        )[: self.top_n]

        impact_distribution = self._distribution(
            impact_values
        )

        magnitude_distribution = self._distribution(
            magnitude_values
        )

        # Preserve useful diagnostic details.

        details = {
            "source": "knowledge_graph",
            "achievement_records": len(
                achievement_nodes
            ),
            "quantified_records": len(
                quantified
            ),
            "graph_entity_count": len(
                nodes
            ),
        }

        overall_score = round(
            impact_score
            + magnitude_score,
            4,
        )

        return AchievementProfile(

            overall_score=overall_score,

            achievement_count=len(
                achievement_nodes
            ),

            quantified_count=len(
                quantified
            ),

            impact_score=impact_score,

            magnitude_score=magnitude_score,

            top_achievements=top_achievements,

            top_metrics=top_metrics,

            impact_distribution=impact_distribution,

            magnitude_distribution=magnitude_distribution,

            details=details,
        )

    # =========================================================================
    # NUMERIC EVIDENCE
    # =========================================================================

    @classmethod
    def _has_numeric_evidence(
        cls,
        node: Any,
    ) -> bool:

        for key in (
            "value",
            "metric_value",
            "numeric_value",
            "percentage",
            "percent",
            "magnitude",
            "amount",
            "delta",
        ):

            value = cls._value(
                node,
                key,
                default=None,
            )

            if value is None:

                continue

            try:

                float(
                    value
                )

                return True

            except (
                TypeError,
                ValueError,
            ):

                pass

        metadata = cls._metadata(
            node
        )

        for key in (
            "value",
            "metric_value",
            "numeric_value",
            "percentage",
            "percent",
            "magnitude",
            "amount",
            "delta",
        ):

            if key in metadata:

                try:

                    float(
                        metadata[
                            key
                        ]
                    )

                    return True

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

        return False

    # -------------------------------------------------------------------------

    @classmethod
    def _magnitude_score(
        cls,
        node: Any,
    ) -> float:

        candidates = []

        for key in (
            "magnitude_score",
            "magnitude",
            "percentage",
            "percent",
            "value",
            "metric_value",
            "numeric_value",
        ):

            value = cls._value(
                node,
                key,
                default=None,
            )

            if value is None:

                continue

            try:

                candidates.append(
                    abs(
                        float(value)
                    )
                )

            except (
                TypeError,
                ValueError,
            ):

                pass

        metadata = cls._metadata(
            node
        )

        for key in (
            "magnitude_score",
            "magnitude",
            "percentage",
            "percent",
            "value",
            "metric_value",
            "numeric_value",
        ):

            if key in metadata:

                try:

                    candidates.append(
                        abs(
                            float(
                                metadata[
                                    key
                                ]
                            )
                        )
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

        if not candidates:

            return 0.0

        value = max(
            candidates
        )

        # Percentage-like magnitude.

        if value > 1:

            value = min(
                value / 100.0,
                1.0,
            )

        return round(
            value,
            4,
        )

    # -------------------------------------------------------------------------

    @staticmethod
    def _distribution(
        values: list[float],
    ) -> dict[str, float]:

        if not values:

            return {}

        buckets = {
            "low": 0,
            "medium": 0,
            "high": 0,
        }

        for value in values:

            if value < 0.34:

                buckets[
                    "low"
                ] += 1

            elif value < 0.67:

                buckets[
                    "medium"
                ] += 1

            else:

                buckets[
                    "high"
                ] += 1

        total = len(
            values
        )

        return {
            key: round(
                count / total,
                4,
            )
            for key, count
            in buckets.items()
            if count
        }

    # =========================================================================
    # LEADERSHIP
    # =========================================================================

    def _build_leadership_profile(
        self,
        nodes: list[Any],
    ) -> LeadershipProfile:

        actions = {}

        leadership_nodes = []

        executive_actions = 0

        for node in nodes:

            if self._entity_type(
                node
            ) != "action":

                continue

            name = self._label(
                node
            )

            normalized = name.casefold()

            if normalized not in self.LEADERSHIP_ACTIONS:

                continue

            leadership_nodes.append(
                node
            )

            actions[
                name
            ] = (
                actions.get(
                    name,
                    0,
                )
                + 1
            )

            if normalized in self.EXECUTIVE_ACTIONS:

                executive_actions += 1

        count = len(
            leadership_nodes
        )

        # Keep scoring compatible with the working profile output.

        if executive_actions >= 2:

            score = 5.0

            level = "Strong Leadership"

        elif count >= 3:

            score = 4.0

            level = "Leadership"

        elif count >= 1:

            score = 2.0

            level = "Emerging Leadership"

        else:

            score = 0.0

            level = ""

        return LeadershipProfile(

            score=score,

            level=level,

            entity_count=count,

            actions=actions,

            executive_actions=executive_actions,
        )

    # =========================================================================
    # SENIORITY
    # =========================================================================

    def _build_seniority_profile(
        self,
        nodes: list[Any],
    ) -> SeniorityProfile:

        actions = {}

        indicators = []

        score_values = []

        for node in nodes:

            if self._entity_type(
                node
            ) != "action":

                continue

            label = self._label(
                node
            )

            normalized = label.casefold()

            if normalized not in self.SENIORITY_INDICATORS:

                continue

            actions[
                label
            ] = (
                actions.get(
                    label,
                    0,
                )
                + 1
            )

            score_values.append(
                self.SENIORITY_INDICATORS[
                    normalized
                ]
            )

            if normalized in {
                "lead",
                "manage",
                "direct",
                "head",
                "own",
                "oversee",
            }:

                if normalized not in indicators:

                    indicators.append(
                        normalized
                    )

        if not score_values:

            return SeniorityProfile()

        score = round(
            sum(
                score_values
            )
            / len(
                score_values
            ),
            4,
        )

        if score >= 4.5:

            level = "Executive"

        elif score >= 3.0:

            level = "Professional"

        elif score >= 2.0:

            level = "Intermediate"

        else:

            level = "Entry"

        return SeniorityProfile(

            score=score,

            level=level,

            actions=actions,

            domains={},

            indicators=indicators,
        )

    # =========================================================================
    # METRIC PROFILE
    # =========================================================================

    def _build_metric_profile(
        self,
        nodes: list[Any],
    ) -> MetricProfile:

        metric_nodes = [
            node
            for node in nodes
            if self._entity_type(
                node
            ) in {
                "metric",
                "kpi",
            }
        ]

        positive = 0
        negative = 0
        increase = 0
        decrease = 0

        serialized = []

        for node in metric_nodes:

            direction = self._metric_direction(
                node
            )

            if direction in {
                "positive",
                "increase",
                "increased",
            }:

                positive += 1

            if direction in {
                "negative",
                "decrease",
                "decreased",
            }:

                negative += 1

            if direction in {
                "increase",
                "increased",
            }:

                increase += 1

            if direction in {
                "decrease",
                "decreased",
            }:

                decrease += 1

            serialized.append(
                self._serialize_entity(
                    node
                )
            )

        return MetricProfile(

            total_metrics=len(
                metric_nodes
            ),

            positive_metrics=positive,

            negative_metrics=negative,

            increase_metrics=increase,

            decrease_metrics=decrease,

            metrics=serialized,
        )

    # -------------------------------------------------------------------------

    @classmethod
    def _metric_direction(
        cls,
        node: Any,
    ) -> str:

        value = cls._text(
            node,
            "direction",
            "metric_direction",
            default="",
        ).casefold()

        if value:

            return value

        metadata = cls._metadata(
            node
        )

        value = metadata.get(
            "direction",
            metadata.get(
                "metric_direction",
                "",
            ),
        )

        return str(
            value
        ).casefold()

    # =========================================================================
    # DOMAIN PROFILE
    # =========================================================================

    def _build_domain_profile(
        self,
        nodes: list[Any],
    ) -> DomainProfile:

        domains = Counter()

        business_areas = Counter()

        for node in nodes:

            domain = self._domain(
                node
            )

            business_area = self._business_area(
                node
            )

            if domain:

                domains[
                    domain
                ] += 1

            if business_area:

                business_areas[
                    business_area
                ] += 1

        # ---------------------------------------------------------------------
        # Important:
        #
        # Do NOT leave domains empty simply because some graph nodes use
        # business_area instead of domain.
        #
        # We preserve actual domain values and separately preserve business
        # areas.
        # ---------------------------------------------------------------------

        return DomainProfile(

            domains=dict(
                domains
            ),

            business_areas=dict(
                business_areas
            ),
        )

    # =========================================================================
    # MODIFIER PROFILE
    # =========================================================================

    def _build_modifier_profile(
        self,
        nodes: list[Any],
    ) -> ModifierProfile:

        categories = Counter()

        total = 0

        executive = 0

        for node in nodes:

            entity_type = self._entity_type(
                node
            )

            category = self._category(
                node
            ).casefold()

            metadata = self._metadata(
                node
            )

            modifier_flag = (
                entity_type in self.MODIFIER_TYPES
                or bool(
                    metadata.get(
                        "modifier",
                        False,
                    )
                )
                or bool(
                    metadata.get(
                        "is_modifier",
                        False,
                    )
                )
            )

            if not modifier_flag:

                continue

            total += 1

            modifier_category = (
                category
                or self._text(
                    node,
                    "modifier_type",
                    default="modifier",
                ).casefold()
            )

            categories[
                modifier_category
            ] += 1

            if (
                "executive"
                in modifier_category
                or "executive"
                in entity_type
            ):

                executive += 1

        return ModifierProfile(

            total_modifiers=total,

            executive_modifiers=executive,

            categories=dict(
                categories
            ),
        )

    # =========================================================================
    # IMPACT PROFILE
    # =========================================================================

    def _build_impact_profile(
        self,
        nodes: list[Any],
    ) -> ImpactProfile:

        weighted = []

        values = []

        for node in nodes:

            weight = self._impact_weight(
                node
            )

            if weight <= 0:

                continue

            record = self._serialize_entity(
                node
            )

            record[
                "impact_weight"
            ] = weight

            weighted.append(
                record
            )

            values.append(
                weight
            )

        total = sum(
            values
        )

        average = (
            total / len(values)
            if values
            else 0.0
        )

        maximum = (
            max(values)
            if values
            else 0.0
        )

        weighted.sort(
            key=lambda item: float(
                item.get(
                    "impact_weight",
                    0.0,
                )
                or 0.0
            ),
            reverse=True,
        )

        return ImpactProfile(

            total_impact=round(
                total,
                4,
            ),

            average_impact=round(
                average,
                4,
            ),

            maximum_impact=round(
                maximum,
                4,
            ),

            entity_count=len(
                weighted
            ),

            weighted_entities=weighted,
        )

    # =========================================================================
    # BUSINESS STATEMENT PROFILE
    # =========================================================================

    def _extract_business_statements(
        self,
        knowledge_graph: Any,
        explicit_statements: Optional[
            Iterable[Any]
        ],
    ) -> list[Any]:

        if explicit_statements is not None:

            return list(
                explicit_statements
            )

        for attribute in (
            "business_statements",
            "statements",
        ):

            value = getattr(
                knowledge_graph,
                attribute,
                None,
            )

            if value is None:

                continue

            if isinstance(
                value,
                dict,
            ):

                return list(
                    value.values()
                )

            try:

                return list(
                    value
                )

            except TypeError:

                continue

        # Some graph implementations store statements in metadata.

        metadata = getattr(
            knowledge_graph,
            "metadata",
            None,
        )

        if isinstance(
            metadata,
            dict,
        ):

            value = metadata.get(
                "business_statements"
            )

            if value is not None:

                try:

                    return list(
                        value
                    )

                except TypeError:

                    pass

        return []

    # -------------------------------------------------------------------------

    def _build_business_statement_profile(
        self,
        statements: list[Any],
    ) -> BusinessStatementProfile:

        records = []

        for statement in statements:

            if isinstance(
                statement,
                dict,
            ):

                record = dict(
                    statement
                )

            else:

                record = {
                    "statement_id": self._text(
                        statement,
                        "statement_id",
                        "id",
                    ),

                    "canonical": self._text(
                        statement,
                        "canonical",
                    ),

                    "text": self._text(
                        statement,
                        "text",
                        "source_text",
                    ),

                    "normalized": self._text(
                        statement,
                        "normalized",
                    ),

                    "confidence": self._float(
                        statement,
                        "confidence",
                    ),

                    "achievement": self._bool(
                        statement,
                        "achievement",
                    ),

                    "quantified": self._bool(
                        statement,
                        "quantified",
                    ),

                    "impact": self._text(
                        statement,
                        "impact",
                    ),

                    "business_value": self._text(
                        statement,
                        "business_value",
                    ),

                    "business_area": self._text(
                        statement,
                        "business_area",
                    ),
                }

            records.append(
                record
            )

        return BusinessStatementProfile(

            total_statements=len(
                records
            ),

            statements=records,
        )

    # =========================================================================
    # SUMMARY PROFILE
    # =========================================================================

    @staticmethod
    def _build_summary_profile(
        achievement_profile: AchievementProfile,
        leadership_profile: LeadershipProfile,
        seniority_profile: SeniorityProfile,
        impact_profile: ImpactProfile,
        ats_profile: ATSProfile,
    ) -> SummaryProfile:

        # Keep the component scores separate.
        #
        # Overall score is intentionally a readable aggregate rather than
        # modifying any component score.

        overall_score = round(
            (
                achievement_profile.overall_score
                + leadership_profile.score
                + seniority_profile.score
                + impact_profile.average_impact
                + ats_profile.score
            ),
            4,
        )

        return SummaryProfile(

            overall_score=overall_score,

            impact_score=impact_profile.average_impact,

            ats_score=ats_profile.score,

            achievement_score=achievement_profile.overall_score,

            leadership_score=leadership_profile.score,

            seniority_score=seniority_profile.score,

            career_level=seniority_profile.level,
        )

    # =========================================================================
    # PROFILE CONFIDENCE
    # =========================================================================

    @classmethod
    def _profile_confidence(
        cls,
        nodes: list[Any],
        edges: list[Any],
        achievements: AchievementProfile,
        ats: ATSProfile,
        statements: BusinessStatementProfile,
    ) -> float:

        if not nodes:

            return 0.0

        confidence_values = []

        for node in nodes:

            value = cls._value(
                node,
                "confidence",
                default=None,
            )

            try:

                if value is not None:

                    confidence_values.append(
                        float(value)
                    )

            except (
                TypeError,
                ValueError,
            ):

                pass

        entity_confidence = (
            sum(
                confidence_values
            )
            / len(
                confidence_values
            )
            if confidence_values
            else 1.0
        )

        # Structural confidence.

        node_factor = 1.0 if nodes else 0.0

        edge_factor = (
            1.0
            if edges
            else 0.0
        )

        achievement_factor = (
            1.0
            if achievements.achievement_count
            else 0.5
        )

        statement_factor = (
            1.0
            if statements.total_statements
            else 0.5
        )

        # ATS is optional. It must NOT destroy profile confidence merely
        # because ATS data is not yet available.

        ats_factor = (
            1.0
            if ats.entity_count
            else 0.9
        )

        confidence = (
            entity_confidence
            * node_factor
            * edge_factor
            * achievement_factor
            * statement_factor
            * ats_factor
        )

        return round(
            max(
                0.0,
                min(
                    confidence,
                    1.0,
                ),
            ),
            4,
        )


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================


def build_knowledge_profile(
    knowledge_graph: Any,
    business_statements: Optional[
        Iterable[Any]
    ] = None,
    top_n: int = 10,
) -> KnowledgeProfile:
    """
    Convenience function.
    """

    builder = KnowledgeProfileBuilder(
        top_n=top_n
    )

    return builder.build(
        knowledge_graph=knowledge_graph,
        business_statements=business_statements,
    )


# ============================================================================
# PUBLIC EXPORTS
# ============================================================================

__all__ = [
    "KnowledgeProfileBuilder",
    "build_knowledge_profile",
]