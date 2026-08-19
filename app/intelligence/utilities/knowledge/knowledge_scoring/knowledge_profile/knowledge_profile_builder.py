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
        debug: bool = False,  
    ) -> None:

        self.top_n = max(
            int(top_n),
            1,
        )
        self.debug = debug  
    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def build(
        self,
        knowledge_graph: Any = None,
        graph: Any = None,
        business_statements: Optional[Iterable[Any]] = None,
        # NEW: Additional parameters for compatibility with pipeline
        semantic_entities: list = None,
        extracted_entities: list = None,
        result: Any = None,
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
        
        NEW: Additional parameters for pipeline compatibility:
            semantic_entities: List of semantic entities from pipeline
            extracted_entities: List of extracted entities from pipeline
            result: Full pipeline result object
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

        # ---------------------------------------------------------------------
        # BUSINESS STATEMENTS - ENHANCED EXTRACTION
        # ---------------------------------------------------------------------
        
        statements = self._extract_business_statements(
            knowledge_graph=knowledge_graph,
            explicit_statements=business_statements,
            result=result,  # Pass result for additional extraction
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
    def _domain(
        cls,
        entity: Any,
    ) -> str:
        """
        Extract domain from entity.
        Checks: domain, primary_domain, business_area, category, entity_type
        """
        # Primary: domain field
        value = cls._text(
            entity,
            "domain",
            "primary_domain",
            default="",
        )
        
        if value:
            return value
        
        # Secondary: business_area
        value = cls._text(
            entity,
            "business_area",
            default="",
        )
        
        if value:
            return value
        
        # Tertiary: category
        value = cls._text(
            entity,
            "category",
            default="",
        )
        
        if value:
            return value
        
        # Fallback: entity_type
        value = cls._text(
            entity,
            "entity_type",
            "type",
            default="",
        )
    
        return value

    @classmethod
    def _business_area(
        cls,
        entity: Any,
    ) -> str:
        """
        Extract business_area from entity.
        Checks: business_area, category, domain, entity_type
        """
        # Primary: business_area
        value = cls._text(
            entity,
            "business_area",
            default="",
        )
        
        if value:
            return value
        
        # Secondary: category
        value = cls._text(
            entity,
            "category",
            default="",
        )
        
        if value:
            return value
        
        # Tertiary: domain
        value = cls._text(
            entity,
            "domain",
            "primary_domain",
            default="",
        )
        
        if value:
            return value
        
        # Fallback: entity_type
        value = cls._text(
            entity,
            "entity_type",
            "type",
            default="",
        )
        
        return value
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
        Important: This preserves the important semantic information.
        """

        metadata = cls._metadata(entity)

        result = {
            "node_id": cls._node_id(entity),
            "entity_id": cls._entity_id(entity),
            "label": cls._label(entity),
            "canonical": cls._text(entity, "canonical"),
            "normalized": cls._text(entity, "normalized"),
            "entity_type": cls._entity_type(entity),
            "category": cls._category(entity),
            "domain": cls._domain(entity),
            "business_area": cls._business_area(entity),
            "description": cls._text(entity, "description"),
            "confidence": cls._float(entity, "confidence", default=0.0),
            "impact_weight": cls._impact_weight(entity),
            "achievement": cls._bool(entity, "achievement"),
            "quantified": cls._bool(entity, "quantified"),
        }

        # Preserve ATS fields
        ats = cls._extract_ats(entity)
        if ats:
            result["ats"] = ats

        # Preserve metric direction if present
        direction = cls._metric_direction(entity)
        if direction and direction != "neutral":
            result["metric_direction"] = direction

        # Preserve ALL metadata
        if metadata:
            result["metadata"] = dict(metadata)

        # If entity has direct metadata attribute
        if hasattr(entity, 'metadata') and isinstance(entity.metadata, dict):
            if not result.get("metadata"):
                result["metadata"] = {}
            result["metadata"].update(entity.metadata)

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
        Also checks impact_weight as ATS proxy.
        """

        metadata = cls._metadata(entity)
        ats_metadata = metadata.get("ats")

        result = {}

        # Direct attributes - check for impact_weight
        for key in (
            "ats_score",
            "ats_weight",
            "ats_match",
            "ats_matched",
            "matched",
            "keyword_match",
            "keyword_score",
            "impact_weight",  # <-- ADD THIS
        ):
            value = cls._value(entity, key, default=None)
            if value is not None:
                result[key] = value

        # Direct metadata - check for impact_weight
        for key in (
            "ats_score",
            "ats_weight",
            "ats_match",
            "ats_matched",
            "matched",
            "keyword_match",
            "keyword_score",
            "impact_weight",  # <-- ADD THIS
        ):
            if key in metadata:
                result[key] = metadata[key]

        # Nested ATS metadata
        if isinstance(ats_metadata, dict):
            result["ats"] = dict(ats_metadata)

        # If we have impact_weight but no ats_score, use impact_weight as ats_score
        if "impact_weight" in result and "ats_score" not in result:
            result["ats_score"] = result["impact_weight"]

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
        
        ATS weight is derived from impact_weight.
        If impact_weight exists, use it as ATS score.
        Otherwise fallback to confidence.
        """
        
        matched = []
        scores = []
        
        impact_weight_count = 0
        confidence_count = 0
        
        for node in nodes:
            # Try to get impact_weight as ATS proxy
            impact_weight = self._impact_weight(node)
            
            # If impact_weight exists, use it as ATS score
            if impact_weight > 0:
                ats = {
                    "ats_score": impact_weight,
                    "ats_weight": impact_weight,
                    "keyword_score": impact_weight,
                    "matched": impact_weight >= 0.5,
                    "keyword_match": impact_weight >= 0.5,
                }
                impact_weight_count += 1
            else:
                # Fallback to confidence
                confidence = self._float(node, "confidence", default=0.0)
                if confidence > 0:
                    ats = {
                        "ats_score": confidence,
                        "ats_weight": confidence,
                        "keyword_score": confidence,
                        "matched": confidence >= 0.5,
                        "keyword_match": confidence >= 0.5,
                    }
                    confidence_count += 1
                else:
                    # Skip entities with no data
                    continue

            # Get score from ATS data
            score = self._ats_score_from_data(ats)
            is_matched = self._ats_is_matched(ats)

            if score is not None:
                scores.append(score)

            # If matched or has score, add to results
            if is_matched or score is not None:
                record = self._serialize_entity(node)
                record["ats_score"] = score if score is not None else 0.0
                record["ats_matched"] = is_matched
                record["ats_source"] = "impact_weight" if impact_weight > 0 else "confidence"
                matched.append(record)

        # Calculate average score
        if not scores:
            # If no scores, use entity count to give a minimal score
            if len(nodes) > 0:
                score = 0.5
            else:
                score = 0.0
        else:
            score = round(sum(scores) / len(scores), 4)

        return ATSProfile(
            score=score,
            entity_count=len(matched),
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
        """
        Build seniority profile from graph nodes with debug output.
        """
        
        from collections import Counter
        
        actions = {}
        indicators = []
        score_values = []
        domain_counter = Counter()
        
        # Debug
        print(f"\n[DEBUG] Building Seniority Profile...")
        action_nodes_found = 0
        seniority_actions_found = 0

        for node in nodes:
            # Check if this is an action node
            if self._entity_type(node) != "action":
                continue
            
            action_nodes_found += 1

            label = self._label(node)
            normalized = label.casefold()

            # Check if this is a seniority indicator
            if normalized not in self.SENIORITY_INDICATORS:
                continue

            seniority_actions_found += 1
            
            # Track the action
            actions[label] = actions.get(label, 0) + 1
            score_values.append(self.SENIORITY_INDICATORS[normalized])
            
            if normalized in {"lead", "manage", "direct", "head", "own", "oversee"}:
                if normalized not in indicators:
                    indicators.append(normalized)
            
            # Extract domain
            domain = self._domain(node)
            if not domain:
                domain = self._business_area(node)
            if not domain:
                domain = self._category(node)
            
            if domain:
                domain_clean = str(domain).strip().lower()
                if domain_clean and domain_clean not in ['unknown', 'none']:
                    domain_counter[domain_clean] += 1
                    print(f"[DEBUG] Seniority action '{label}' in domain: {domain_clean}")

        print(f"[DEBUG] Action nodes found: {action_nodes_found}")
        print(f"[DEBUG] Seniority actions found: {seniority_actions_found}")
        print(f"[DEBUG] Domains found: {dict(domain_counter)}")

        if not score_values:
            return SeniorityProfile()

        score = round(
            sum(score_values) / len(score_values),
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
            domains=dict(domain_counter),
            indicators=indicators,
        )
    # =========================================================================
    # METRIC PROFILE
    # =========================================================================

    def _build_metric_profile(
        self,
        nodes: list[Any],
    ) -> MetricProfile:
        """
        Build metric profile with proper direction detection.
        """
        
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
            
            # Determine positive/negative
            if direction in {
                "positive",
                "increase",
                "increased",
                "improved",
                "higher",
                "better",
                "good",
            }:
                positive += 1

            if direction in {
                "negative",
                "decrease",
                "decreased",
                "reduced",
                "lower",
                "worse",
                "bad",
            }:
                negative += 1

            # Determine increase/decrease
            if direction in {
                "increase",
                "increased",
                "positive",
                "improved",
                "higher",
                "better",
            }:
                increase += 1

            if direction in {
                "decrease",
                "decreased",
                "negative",
                "reduced",
                "lower",
                "worse",
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

    @classmethod
    def _metric_direction(
        cls,
        node: Any,
    ) -> str:
        """
        Determine the direction of a metric.
        
        Checks:
        1. Explicit direction field
        2. Metric name (e.g., "Customer Complaints" = negative, "Production Yield" = positive)
        3. Metadata
        4. Context from achievement/quantified status
        """
        
        # First check explicit direction field
        value = cls._text(
            node,
            "direction",
            "metric_direction",
            "trend",
            default="",
        ).casefold()

        if value:
            return value

        # Check metadata
        metadata = cls._metadata(node)
        
        if isinstance(metadata, dict):
            # Check for direction in metadata
            for key in ["direction", "metric_direction", "trend"]:
                if key in metadata:
                    value = str(metadata[key]).casefold()
                    if value:
                        return value
            
            # Check for metric_type in metadata
            metric_type = metadata.get("metric_type", "")
            if metric_type:
                if "positive" in str(metric_type).casefold():
                    return "positive"
                if "negative" in str(metric_type).casefold():
                    return "negative"
        
        # Determine from metric name/canonical
        canonical = cls._label(node).casefold()
        entity_id = cls._entity_id(node).casefold()
        
        # Metrics that are inherently negative (lower is better)
        negative_metrics = {
            "complaints", "defects", "errors", "failures", "issues",
            "problems", "downtime", "waste", "scrap", "rework",
            "attrition", "turnover", "absenteeism", "cost",
            "expense", "loss", "damage", "risk", "incident",
            "customer complaints", "complaint rate", "defect rate"
        }
        
        # Metrics that are inherently positive (higher is better)
        positive_metrics = {
            "yield", "efficiency", "productivity", "quality",
            "satisfaction", "retention", "growth", "revenue",
            "profit", "margin", "production yield", "output",
            "throughput", "uptime", "availability", "accuracy",
            "completion", "delivery", "performance"
        }
        
        # Check if metric is negative
        for term in negative_metrics:
            if term in canonical or term in entity_id:
                return "negative"
        
        # Check if metric is positive
        for term in positive_metrics:
            if term in canonical or term in entity_id:
                return "positive"
        
        # Check metadata for metric type
        if isinstance(metadata, dict):
            metric_name = metadata.get("metric_name", "").casefold()
            metric_type = metadata.get("metric_type", "").casefold()
            
            if "complaint" in metric_name or "defect" in metric_name:
                return "negative"
            if "yield" in metric_name or "efficiency" in metric_name:
                return "positive"
        
        # Check if quantified and achievement
        is_achievement = cls._bool(node, "achievement", default=False)
        is_quantified = cls._bool(node, "quantified", default=False)
        
        if is_achievement and is_quantified:
            # If it's an achievement and quantified, likely positive
            return "positive"
        
        # Default: neutral
        return "neutral"
    # =========================================================================
    # DOMAIN PROFILE
    # =========================================================================

    def _build_domain_profile(
        self,
        nodes: list[Any],
    ) -> DomainProfile:
        """
        Build domain profile from graph nodes.
        
        Extracts domains from:
        1. domain field (primary)
        2. business_area field (secondary)
        3. category field (tertiary)
        4. entity_type (fallback)
        """
        
        domains = Counter()
        business_areas = Counter()
        
        # Track how many domains were found from each source
        domain_sources = {
            'domain_field': 0,
            'business_area': 0,
            'category': 0,
            'entity_type': 0,
            'unknown': 0
        }

        for node in nodes:
            # Try to get domain from various fields
            domain = self._domain(node)
            
            if domain:
                domain_sources['domain_field'] += 1
            else:
                # Try business_area
                domain = self._business_area(node)
                if domain:
                    domain_sources['business_area'] += 1
                else:
                    # Try category
                    domain = self._category(node)
                    if domain:
                        domain_sources['category'] += 1
                    else:
                        # Try entity_type
                        entity_type = self._entity_type(node)
                        if entity_type and entity_type not in ['unknown', '']:
                            domain = entity_type
                            domain_sources['entity_type'] += 1
                        else:
                            domain_sources['unknown'] += 1
            
            # Get business_area
            business_area = self._business_area(node)
            if not business_area:
                business_area = self._category(node)
            if not business_area and domain:
                business_area = domain

            # Clean and normalize domain
            if domain:
                domain_clean = str(domain).strip().lower()
                if domain_clean and domain_clean not in ['unknown', 'none']:
                    domains[domain_clean] += 1

            # Clean and normalize business_area
            if business_area:
                business_clean = str(business_area).strip().lower()
                if business_clean and business_clean not in ['unknown', 'none']:
                    business_areas[business_clean] += 1

        # If domains is empty but business_areas has data, 
        # use business_areas as domains
        if not domains and business_areas:
            domains = business_areas.copy()

        # Debug output
        if self.debug:
            print(f"\n[DEBUG] Domain Profile:")
            print(f"  Domain sources: {domain_sources}")
            print(f"  Domains found: {len(domains)}")
            print(f"  Business areas found: {len(business_areas)}")
            if domains:
                print(f"  Sample domains: {list(domains.keys())[:5]}")
            if business_areas:
                print(f"  Sample business areas: {list(business_areas.keys())[:5]}")

        return DomainProfile(
            domains=dict(domains),
            business_areas=dict(business_areas),
        )
    # =========================================================================
    # MODIFIER PROFILE
    # =========================================================================

        # Update MODIFIER_TYPES at the class level
    MODIFIER_TYPES = {
        "modifier",
        "executive_modifier",
        "strategic_modifier",
        "ownership_modifier",
        "scale_modifier",
        "scope_modifier",
        # Added for your data
        "leadership",
        "management",
        "executive",
        "senior",
        "director",
        "action",  # Your actions like "Lead" are modifiers
    }

    def _build_modifier_profile(
        self,
        nodes: list[Any],
    ) -> ModifierProfile:
        """
        Build modifier profile from graph nodes.
        
        Detects modifiers from:
        1. entity_type in MODIFIER_TYPES
        2. metadata flags (modifier, is_modifier)
        3. category field (Leadership, Management, etc.)
        4. business_area field (Leadership, Management, etc.)
        5. canonical name containing modifier keywords
        """
        
        categories = Counter()
        total = 0
        executive = 0
        
        # Modifier keywords for detection
        MODIFIER_KEYWORDS = {
            "leadership", "management", "executive", "strategic", 
            "senior", "director", "principal", "head",
            "enterprise", "global", "corporate", "professional",
            "expert", "advanced", "certified", "specialized",
            "technical", "functional", "operational", "tactical",
            "lead", "manage", "supervise", "oversee"
        }
        
        EXECUTIVE_KEYWORDS = {
            "executive", "director", "vp", "vice president", 
            "chief", "cfo", "ceo", "cto", "coo", 
            "president", "managing director", "principal", "head",
            "leadership", "management", "senior"
        }

        for node in nodes:
            # Get all relevant fields
            entity_type = self._entity_type(node)
            category = self._category(node).casefold()
            business_area = self._business_area(node).casefold()
            canonical = self._label(node).casefold()
            metadata = self._metadata(node)
            
            # Check for modifier flags
            modifier_flag = (
                entity_type in self.MODIFIER_TYPES
                or bool(metadata.get("modifier", False))
                or bool(metadata.get("is_modifier", False))
            )
            
            # If no explicit flag, check fields for keywords
            if not modifier_flag:
                combined_text = f"{entity_type} {category} {business_area} {canonical}"
                for keyword in MODIFIER_KEYWORDS:
                    if keyword in combined_text:
                        modifier_flag = True
                        break
            
            if not modifier_flag:
                continue
            
            total += 1
            
            # Determine modifier category (prioritize: category > business_area > entity_type > canonical)
            modifier_category = (
                category 
                or business_area 
                or entity_type 
                or self._text(node, "modifier_type", default="")
            )
            
            if not modifier_category:
                modifier_category = canonical or "modifier"
            
            categories[modifier_category] += 1
            
            # Check if executive modifier
            if (
                "executive" in modifier_category
                or "executive" in entity_type
                or any(kw in modifier_category for kw in EXECUTIVE_KEYWORDS)
                or any(kw in entity_type for kw in EXECUTIVE_KEYWORDS)
                or any(kw in category for kw in EXECUTIVE_KEYWORDS)
                or any(kw in business_area for kw in EXECUTIVE_KEYWORDS)
                or any(kw in canonical for kw in EXECUTIVE_KEYWORDS)
            ):
                executive += 1

        return ModifierProfile(
            total_modifiers=total,
            executive_modifiers=executive,
            categories=dict(categories),
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
    # BUSINESS STATEMENT PROFILE - ENHANCED
    # =========================================================================

    def _extract_business_statements(
        self,
        knowledge_graph: Any,
        explicit_statements: Optional[
            Iterable[Any]
        ],
        result: Any = None,  # NEW: extract from result
    ) -> list[Any]:
        """
        Extract business statements from multiple sources.
        """
        
        statements = []
        
        # Source 1: Explicit statements parameter
        if explicit_statements is not None:
            try:
                statements.extend(list(explicit_statements))
            except TypeError:
                pass
        
        # Source 2: From result object
        if result is not None:
            # Try different attribute names
            for attr in [
                "business_statements",
                "statements",
                "business_statement",
                "business_statement_list",
            ]:
                try:
                    value = getattr(result, attr, None)
                    if value is not None:
                        try:
                            statements.extend(list(value))
                            break
                        except TypeError:
                            pass
                except Exception:
                    pass
            
            # If result is a dict
            if isinstance(result, dict):
                for key in [
                    "business_statements",
                    "statements",
                    "business_statement",
                ]:
                    if key in result:
                        try:
                            statements.extend(list(result[key]))
                            break
                        except (TypeError, ValueError):
                            pass
        
        # Source 3: From knowledge graph
        if not statements:
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
                    statements.extend(list(value.values()))
                    break

                try:
                    statements.extend(list(value))
                    break
                except TypeError:
                    continue

        # Source 4: From knowledge graph metadata
        if not statements:
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
                        statements.extend(list(value))
                    except TypeError:
                        pass

        return statements

    # -------------------------------------------------------------------------

    def _build_business_statement_profile(
        self,
        statements: list[Any],
    ) -> BusinessStatementProfile:
        """
        Build BusinessStatementProfile from extracted statements.
        """

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
    # NEW: Additional parameters for pipeline compatibility
    semantic_entities: list = None,
    extracted_entities: list = None,
    result: Any = None,
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
        semantic_entities=semantic_entities,
        extracted_entities=extracted_entities,
        result=result,
    )


# ============================================================================
# PUBLIC EXPORTS
# ============================================================================

__all__ = [
    "KnowledgeProfileBuilder",
    "build_knowledge_profile",
]