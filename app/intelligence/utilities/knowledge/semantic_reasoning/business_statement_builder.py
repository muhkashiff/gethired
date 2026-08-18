"""
Enterprise Business Statement Builder - FIXED V2
Enterprise V18

FIX: Force grouping using clusters from SemanticResolution
"""

from __future__ import annotations

from typing import Any, Iterable, Optional, Dict, List, Set
import logging
import uuid

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    BusinessStatement,
    SemanticEntity,
    StatementRelation,
    SemanticDependency,
    SemanticCluster,
    SemanticResolution,
)

logger = logging.getLogger(__name__)


class BusinessStatementBuilder:
    """
    Convert semantic resolver output into BusinessStatement objects.
    PRIORITIZES CLUSTERS for grouping.
    """

    def __init__(self) -> None:
        """Initialize the builder."""
        self.statements: List[BusinessStatement] = []
        self.logger = logger

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def build(
        self,
        semantic_resolution: Any = None,
        entities: Optional[Iterable[Any]] = None,
        dependencies: Optional[Iterable[Any]] = None,
        clusters: Optional[Iterable[Any]] = None,
    ) -> list[BusinessStatement]:
        """
        Build BusinessStatement objects.
        
        CRITICAL: Pass clusters from semantic_resolution to enable grouping.
        """
        self.logger.info("Starting BusinessStatementBuilder.build()")

        # ---------------------------------------------------------------------
        # Extract semantic entities
        # ---------------------------------------------------------------------
        semantic_entities = self._extract_entities(semantic_resolution, entities)
        self.logger.info(f"Extracted {len(semantic_entities)} semantic entities")

        if not semantic_entities:
            self.logger.warning("No semantic entities found")
            return []

        # ---------------------------------------------------------------------
        # Extract semantic dependencies
        # ---------------------------------------------------------------------
        semantic_dependencies = self._extract_dependencies(semantic_resolution, dependencies)
        self.logger.info(f"Extracted {len(semantic_dependencies)} semantic dependencies")

        # ---------------------------------------------------------------------
        # Extract clusters - THIS IS THE KEY FIX
        # ---------------------------------------------------------------------
        semantic_clusters = self._extract_clusters(semantic_resolution, clusters)
        self.logger.info(f"Extracted {len(semantic_clusters)} semantic clusters")

        # ---------------------------------------------------------------------
        # Build entity lookup
        # ---------------------------------------------------------------------
        entity_map = self._build_entity_map(semantic_entities)

        # ---------------------------------------------------------------------
        # GROUP BY CLUSTERS (Primary strategy)
        # ---------------------------------------------------------------------
        groups = self._group_by_clusters(semantic_clusters, entity_map)

        # If clusters produced groups, use them
        if groups:
            self.logger.info(f"Created {len(groups)} groups from clusters")
        else:
            self.logger.warning("No groups from clusters - trying fallback grouping")
            groups = self._group_by_relations(semantic_entities, semantic_dependencies)

        # If still no groups, fallback to individual entities
        if not groups:
            self.logger.warning("No groups from relations - creating individual statements")
            groups = self._group_individual_entities(semantic_entities)

        # ---------------------------------------------------------------------
        # Build statements from groups
        # ---------------------------------------------------------------------
        statements: list[BusinessStatement] = []

        for group_id, group_entities in groups.items():
            if not group_entities:
                continue

            # Find dependencies for this group
            group_deps = self._find_dependencies_for_group(
                group_entities, semantic_dependencies, entity_map
            )

            statement = self._create_statement(
                group_id, group_entities, group_deps, entity_map
            )

            if statement and statement.is_valid:
                statements.append(statement)

        self.logger.info(f"Generated {len(statements)} business statements")
        return statements

    # =========================================================================
    # EXTRACTION METHODS
    # =========================================================================

    @staticmethod
    def _extract_entities(resolution: Any, entities: Optional[Iterable[Any]]) -> list[Any]:
        """Extract entities from resolution or direct input."""
        if entities is not None:
            return list(entities)

        if resolution is None:
            return []

        # Try common field names
        for field in ("entities", "semantic_entities"):
            val = getattr(resolution, field, None)
            if val is not None:
                return list(val)

        return []

    @staticmethod
    def _extract_dependencies(resolution: Any, dependencies: Optional[Iterable[Any]]) -> list[Any]:
        """Extract dependencies from resolution or direct input."""
        if dependencies is not None:
            return list(dependencies)

        if resolution is None:
            return []

        result = []
        for field in ("dependencies", "semantic_dependencies", "relations", "semantic_relations"):
            val = getattr(resolution, field, None)
            if val is not None:
                result.extend(list(val))

        return result

    @staticmethod
    def _extract_clusters(resolution: Any, clusters: Optional[Iterable[Any]]) -> list[Any]:
        """Extract clusters from resolution or direct input."""
        if clusters is not None:
            return list(clusters)

        if resolution is None:
            return []

        # Try common field names
        val = getattr(resolution, "clusters", None)
        if val is not None:
            return list(val)

        return []

    # =========================================================================
    # ENTITY MAP
    # =========================================================================

    @staticmethod
    def _build_entity_map(entities: list[Any]) -> Dict[str, Any]:
        """Build entity_id → entity map."""
        result = {}
        for entity in entities:
            entity_id = BusinessStatementBuilder._get_entity_id(entity)
            if entity_id:
                result[entity_id] = entity
        return result

    # =========================================================================
    # GROUPING STRATEGIES
    # =========================================================================

    def _group_by_clusters(
        self,
        clusters: list[Any],
        entity_map: Dict[str, Any]
    ) -> Dict[str, List[Any]]:
        """
        PRIMARY STRATEGY: Group entities by their clusters.
        
        This is the key fix - clusters from the semantic resolver
        contain the correct groupings.
        """
        groups: Dict[str, List[Any]] = {}
        assigned: Set[str] = set()

        for cluster in clusters:
            # Get cluster ID
            cluster_id = getattr(cluster, "cluster_id", None)
            if not cluster_id:
                cluster_id = getattr(cluster, "id", f"cluster_{uuid.uuid4().hex[:8]}")

            # Get entity IDs from cluster
            entity_ids = getattr(cluster, "entity_ids", None)
            if not entity_ids:
                entity_ids = getattr(cluster, "members", [])
            if not entity_ids:
                entity_ids = getattr(cluster, "entities", [])

            # Convert to list if needed
            if not isinstance(entity_ids, list):
                entity_ids = list(entity_ids) if entity_ids else []

            if not entity_ids:
                self.logger.debug(f"Cluster {cluster_id} has no entity IDs")
                continue

            # Get actual entity objects
            group_key = f"cluster_{cluster_id}"
            groups[group_key] = []

            for entity_id in entity_ids:
                if entity_id in entity_map:
                    entity = entity_map[entity_id]
                    groups[group_key].append(entity)
                    assigned.add(entity_id)

            if groups[group_key]:
                self.logger.debug(
                    f"Cluster {cluster_id}: {len(groups[group_key])} entities, "
                    f"labels: {getattr(cluster, 'label', 'N/A')}"
                )

        # Log results
        total_grouped = sum(len(g) for g in groups.values())
        self.logger.info(f"Grouped {total_grouped} entities across {len(groups)} clusters")

        return groups

    def _group_by_relations(
        self,
        entities: list[Any],
        dependencies: list[Any]
    ) -> Dict[str, List[Any]]:
        """
        FALLBACK STRATEGY: Group by action-target relationships.
        """
        groups: Dict[str, List[Any]] = {}
        entity_map = self._build_entity_map(entities)

        # Build source → targets map
        source_map: Dict[str, List[tuple]] = {}
        for dep in dependencies:
            source_id = self._get_dependency_source(dep)
            target_id = self._get_dependency_target(dep)
            rel_type = self._get_relation_type(dep)

            if source_id and target_id:
                if source_id not in source_map:
                    source_map[source_id] = []
                source_map[source_id].append((target_id, rel_type))

        # Group by action
        for entity in entities:
            entity_id = self._get_entity_id(entity)
            entity_type = self._get_entity_type(entity)

            if entity_type in {"action", "act"} and entity_id in source_map:
                group_key = f"action_{entity_id}"
                groups[group_key] = [entity]

                # Add targets
                for target_id, rel_type in source_map[entity_id]:
                    if target_id in entity_map:
                        groups[group_key].append(entity_map[target_id])

                # Add related domains and metrics
                for dep in dependencies:
                    dep_source = self._get_dependency_source(dep)
                    dep_target = self._get_dependency_target(dep)
                    if dep_source == entity_id and dep_target in entity_map:
                        target = entity_map[dep_target]
                        if target not in groups[group_key]:
                            ttype = self._get_entity_type(target)
                            if ttype in {"domain", "metric", "kpi"}:
                                groups[group_key].append(target)

        return groups

    def _group_individual_entities(self, entities: list[Any]) -> Dict[str, List[Any]]:
        """FINAL FALLBACK: Create individual statements for important entities."""
        groups = {}

        # Prioritize actions and targets
        for entity in entities:
            entity_id = self._get_entity_id(entity)
            entity_type = self._get_entity_type(entity)

            if entity_type in {"action", "act", "target", "skill", "standard", "certification"}:
                groups[f"single_{entity_id}"] = [entity]

        # If no groups, put all in one
        if not groups and entities:
            groups["all_entities"] = entities

        return groups

    # =========================================================================
    # DEPENDENCY HELPERS
    # =========================================================================

    def _find_dependencies_for_group(
        self,
        group_entities: list[Any],
        all_dependencies: list[Any],
        entity_map: Dict[str, Any]
    ) -> list[Any]:
        """Find dependencies relevant to this group."""
        entity_ids = {self._get_entity_id(e) for e in group_entities}
        entity_ids.discard("")

        result = []
        for dep in all_dependencies:
            source = self._get_dependency_source(dep)
            target = self._get_dependency_target(dep)

            if source in entity_ids or target in entity_ids:
                result.append(dep)

        return result

    # =========================================================================
    # STATEMENT CREATION
    # =========================================================================

    def _create_statement(
        self,
        group_id: str,
        entities: list[Any],
        dependencies: list[Any],
        entity_map: Dict[str, Any]
    ) -> Optional[BusinessStatement]:
        """Create a BusinessStatement from a group of entities."""
        if not entities:
            return None

        # Remove duplicates
        seen = set()
        unique_entities = []
        for e in entities:
            eid = self._get_entity_id(e)
            if eid and eid not in seen:
                seen.add(eid)
                unique_entities.append(e)

        if not unique_entities:
            return None

        # Find components
        action = self._find_entity_by_type(unique_entities, {"action", "act"})
        target = self._find_entity_by_type(unique_entities, {"target", "skill", "technology", "certification", "standard"})
        domain = self._find_entity_by_type(unique_entities, {"domain", "business_area"})
        metric = self._find_entity_by_type(unique_entities, {"metric", "kpi", "business_kpi"})

        # Build text
        text = self._build_statement_text(action, target, domain, metric, unique_entities)

        # Build statement
        try:
            statement = BusinessStatement(
                statement_id=f"BS-{uuid.uuid4().hex[:8]}",
                canonical=text,
                text=text,
                normalized=text.casefold() if text else "",
                fact_id=self._get_fact_id(unique_entities),
                sentence_index=self._get_sentence_index(unique_entities),
                source_text=text,
                source="resume",
                action=action,
                target=target,
                domain=domain,
                metric=metric,
                entities=unique_entities,
                relations=[d for d in dependencies if isinstance(d, StatementRelation)],
                dependencies=dependencies,
                achievement=self._check_achievement(unique_entities),
                quantified=self._check_quantified(unique_entities),
                impact=self._get_impact(metric, unique_entities),
                business_value=self._get_business_value(unique_entities),
                category=self._get_category(action, target, domain, metric),
                business_area=self._get_business_area(domain, unique_entities),
                confidence=self._calculate_confidence(unique_entities),
                impact_weight=self._calculate_impact_weight(unique_entities),
                metadata={
                    "group_id": group_id,
                    "entity_count": len(unique_entities),
                    "entity_ids": [self._get_entity_id(e) for e in unique_entities],
                    "entity_types": [self._get_entity_type(e) for e in unique_entities],
                }
            )
            return statement
        except Exception as e:
            self.logger.error(f"Failed to create statement: {e}")
            return None

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    @staticmethod
    def _get_entity_id(entity: Any) -> str:
        for attr in ("entity_id", "id", "canonical_id"):
            val = getattr(entity, attr, None)
            if val:
                return str(val).strip()
        return ""

    @staticmethod
    def _get_entity_type(entity: Any) -> str:
        return str(getattr(entity, "entity_type", "") or "").strip().casefold()

    @staticmethod
    def _get_entity_name(entity: Any) -> str:
        for attr in ("canonical", "name", "normalized", "original", "label", "text"):
            val = getattr(entity, attr, None)
            if val:
                return str(val).strip()
        return ""

    @staticmethod
    def _get_dependency_source(dep: Any) -> str:
        for attr in ("source_id", "source_entity_id", "from_id", "source"):
            val = getattr(dep, attr, None)
            if val:
                if not isinstance(val, (str, int, float)):
                    nested = getattr(val, "entity_id", None)
                    if nested:
                        return str(nested).strip()
                return str(val).strip()
        return ""

    @staticmethod
    def _get_dependency_target(dep: Any) -> str:
        for attr in ("target_id", "target_entity_id", "to_id", "target"):
            val = getattr(dep, attr, None)
            if val:
                if not isinstance(val, (str, int, float)):
                    nested = getattr(val, "entity_id", None)
                    if nested:
                        return str(nested).strip()
                return str(val).strip()
        return ""

    @staticmethod
    def _get_relation_type(dep: Any) -> str:
        for attr in ("relation_type", "relation", "type"):
            val = getattr(dep, attr, None)
            if val:
                return str(val).upper().strip()
        return "RELATED_TO"

    @staticmethod
    def _get_fact_id(entities: list[Any]) -> str:
        for e in entities:
            val = getattr(e, "fact_id", None) or getattr(e, "source_fact_id", None)
            if val:
                return str(val).strip()
        return ""

    @staticmethod
    def _get_sentence_index(entities: list[Any]) -> int:
        for e in entities:
            val = getattr(e, "sentence_index", -1)
            try:
                val = int(val)
                if val >= 0:
                    return val
            except (TypeError, ValueError):
                continue
        return -1

    @staticmethod
    def _find_entity_by_type(entities: list[Any], types: set[str]) -> Optional[Any]:
        """Find first entity matching any of the types."""
        for entity in entities:
            etype = BusinessStatementBuilder._get_entity_type(entity)
            if etype and any(t in etype for t in types):
                return entity
        return None

    @staticmethod
    def _build_statement_text(
        action: Optional[Any],
        target: Optional[Any],
        domain: Optional[Any],
        metric: Optional[Any],
        entities: list[Any]
    ) -> str:
        """Build a human-readable statement text."""
        parts = []

        # Action + Target
        if action:
            action_name = BusinessStatementBuilder._get_entity_name(action)
            if action_name:
                parts.append(action_name)

        if target:
            target_name = BusinessStatementBuilder._get_entity_name(target)
            if target_name:
                parts.append(target_name)

        # If no action/target, use domain
        if not parts and domain:
            parts.append(BusinessStatementBuilder._get_entity_name(domain))

        # If still nothing, use first entity name
        if not parts and entities:
            parts.append(BusinessStatementBuilder._get_entity_name(entities[0]) or "Professional Achievement")

        # Add metric if present and quantified
        if metric and BusinessStatementBuilder._check_quantified([metric]):
            metric_name = BusinessStatementBuilder._get_entity_name(metric)
            if metric_name:
                parts.append(f"resulting in {metric_name}")

        return " ".join(parts) if parts else "Professional Achievement"

    @staticmethod
    def _check_achievement(entities: list[Any]) -> bool:
        for e in entities:
            if getattr(e, "achievement", False):
                return True
        return False

    @staticmethod
    def _check_quantified(entities: list[Any]) -> bool:
        for e in entities:
            if getattr(e, "quantified", False):
                return True
        return False

    @staticmethod
    def _get_impact(metric: Optional[Any], entities: list[Any]) -> str:
        if metric:
            return BusinessStatementBuilder._get_entity_name(metric)
        for e in entities:
            impact = getattr(e, "impact", None)
            if impact:
                return str(impact)
        return ""

    @staticmethod
    def _get_business_value(entities: list[Any]) -> str:
        for e in entities:
            val = getattr(e, "business_value", None) or getattr(e, "business_meaning", None)
            if val:
                return str(val)
        return ""

    @staticmethod
    def _get_category(
        action: Optional[Any],
        target: Optional[Any],
        domain: Optional[Any],
        metric: Optional[Any]
    ) -> str:
        if action and target:
            return "achievement"
        elif action:
            return "action_statement"
        elif metric:
            return "metric_statement"
        elif domain:
            return "domain_statement"
        else:
            return "professional_statement"

    @staticmethod
    def _get_business_area(domain: Optional[Any], entities: list[Any]) -> str:
        if domain:
            area = getattr(domain, "business_area", None) or BusinessStatementBuilder._get_entity_name(domain)
            if area:
                return area
        for e in entities:
            area = getattr(e, "business_area", None)
            if area:
                return str(area)
        return ""

    @staticmethod
    def _calculate_confidence(entities: list[Any]) -> float:
        confidences = []
        for e in entities:
            conf = getattr(e, "confidence", None)
            if conf is not None:
                try:
                    confidences.append(float(conf))
                except (TypeError, ValueError):
                    pass
        if not confidences:
            return 0.5
        return round(sum(confidences) / len(confidences), 4)

    @staticmethod
    def _calculate_impact_weight(entities: list[Any]) -> float:
        weights = []
        for e in entities:
            w = getattr(e, "impact_weight", None)
            if w is not None:
                try:
                    weights.append(float(w))
                except (TypeError, ValueError):
                    pass
        if not weights:
            return 1.0
        return round(max(weights), 4)


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================

def build_business_statements(
    semantic_resolution: Any = None,
    entities: Optional[Iterable[Any]] = None,
    dependencies: Optional[Iterable[Any]] = None,
    clusters: Optional[Iterable[Any]] = None,
) -> list[BusinessStatement]:
    """Convenience API for building business statements."""
    builder = BusinessStatementBuilder()
    return builder.build(
        semantic_resolution=semantic_resolution,
        entities=entities,
        dependencies=dependencies,
        clusters=clusters,
    )


__all__ = ["BusinessStatementBuilder", "build_business_statements"]