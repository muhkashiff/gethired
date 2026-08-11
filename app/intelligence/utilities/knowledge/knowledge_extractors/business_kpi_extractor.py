
"""
Enterprise Business KPI Extractor
Enterprise V5

Responsibilities

• Resolve Business KPI entities from Repository
• Support canonical names
• Support aliases
• Support normalized names
• Return BusinessKPIKnowledge objects
• Preserve KPI-specific metadata
• Provide confidence and match information

Architecture

business_kpi.json
        ↓
RepositoryLoader
        ↓
RepositoryEntity
        ↓
Repository
        ↓
BusinessKPIExtractor
        ↓
BusinessKPIKnowledge
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from app.intelligence.utilities.knowledge.repository_v5.repository import (
    Repository,
)
from app.intelligence.utilities.knowledge.repository_v5.repository_entity import RepositoryEntity


######################################################################
# BUSINESS KPI KNOWLEDGE
######################################################################


@dataclass
class BusinessKPIKnowledge:
    """
    Structured result returned by BusinessKPIExtractor.

    This is an OBJECT, not a dictionary.
    """

    ##################################################################
    # MATCH RESULT
    ##################################################################

    found: bool = False

    confidence: float = 0.0

    original: str = ""

    canonical: str = ""

    normalized: str = ""

    ##################################################################
    # ENTITY IDENTITY
    ##################################################################

    entity_id: str = ""

    entity_type: str = ""

    ontology_name: str = ""

    category: str = ""

    business_area: str = ""

    ##################################################################
    # BUSINESS INFORMATION
    ##################################################################

    description: str = ""

    related_metrics: list[str] = field(
        default_factory=list
    )

    higher_is_better: bool = True

    impact_weight: float = 1.0

    ##################################################################
    # MATCH INFORMATION
    ##################################################################

    matched_phrase: str = ""

    matched_alias: bool = False

    match_type: str = ""

    ##################################################################
    # SOURCE ENTITY
    ##################################################################

    source: str = ""

    metadata: dict = field(
        default_factory=dict
    )

    kpi_object: Optional[RepositoryEntity] = None


######################################################################
# EXTRACTOR
######################################################################


class BusinessKPIExtractor:
    """
    Extract Business KPI knowledge from the Enterprise Repository.
    """

    ##################################################################
    # INITIALIZATION
    ##################################################################

    def __init__(
        self,
        repository: Repository,
    ) -> None:

        self.repository = repository

        self.ontology = "business_kpis"

    ##################################################################
    # EXTRACT
    ##################################################################

    def extract(
        self,
        phrase: str,
    ) -> BusinessKPIKnowledge:
        """
        Resolve a phrase into BusinessKPIKnowledge.

        Example:

            extract("Operational Excellence")

        returns:

            BusinessKPIKnowledge(...)
        """

        ################################################################
        # INVALID INPUT
        ################################################################

        if phrase is None:

            return BusinessKPIKnowledge(
                found=False,
                confidence=0.0,
                original="",
            )

        original = str(phrase)

        if not original.strip():

            return BusinessKPIKnowledge(
                found=False,
                confidence=0.0,
                original=original,
            )

        ################################################################
        # NORMALIZE
        ################################################################

        normalized_input = self.repository._normalize_lookup(
            original
        )

        if not normalized_input:

            return BusinessKPIKnowledge(
                found=False,
                confidence=0.0,
                original=original,
            )

        ################################################################
        # RESOLVE
        ################################################################

        entity = self.repository.find_entity(
            self.ontology,
            normalized_input,
        )

        ################################################################
        # NOT FOUND
        ################################################################

        if entity is None:

            return BusinessKPIKnowledge(
                found=False,
                confidence=0.0,
                original=original,
                normalized=normalized_input,
            )

        ################################################################
        # MATCH TYPE
        ################################################################

        match_type = self._determine_match_type(
            normalized_input,
            entity,
        )

        ################################################################
        # ALIAS
        ################################################################

        matched_alias = self._is_alias_match(
            normalized_input,
            entity,
        )

        ################################################################
        # MATCHED PHRASE
        ################################################################

        matched_phrase = self._find_matched_phrase(
            normalized_input,
            entity,
        )

        ################################################################
        # CONFIDENCE
        ################################################################

        confidence = self._calculate_confidence(
            match_type=match_type,
            matched_alias=matched_alias,
        )

        ################################################################
        # RELATED METRICS
        ################################################################

        related_metrics = self._extract_related_metrics(
            entity
        )

        ################################################################
        # BUILD KNOWLEDGE OBJECT
        ################################################################

        return BusinessKPIKnowledge(

            found=True,

            confidence=confidence,

            original=original,

            canonical=entity.canonical,

            normalized=entity.normalized,

            entity_id=entity.entity_id,

            entity_type=entity.entity_type,

            ontology_name=entity.ontology_name,

            category=entity.category,

            business_area=entity.business_area,

            description=entity.description,

            related_metrics=related_metrics,

            higher_is_better=entity.higher_is_better,

            impact_weight=entity.impact_weight,

            matched_phrase=matched_phrase,

            matched_alias=matched_alias,

            match_type=match_type,

            source=entity.source,

            metadata=entity.metadata.copy(),

            kpi_object=entity,
        )

    ##################################################################
    # RESOLVE
    ##################################################################

    def resolve(
        self,
        phrase: str,
    ) -> BusinessKPIKnowledge:
        """
        Alias for extract().
        """

        return self.extract(
            phrase
        )

    ##################################################################
    # MATCH TYPE
    ##################################################################

    def _determine_match_type(
        self,
        normalized_input: str,
        entity: RepositoryEntity,
    ) -> str:
        """
        Determine how the KPI was matched.
        """

        canonical = self.repository._normalize_lookup(
            entity.canonical
        )

        normalized = self.repository._normalize_lookup(
            entity.normalized
        )

        if normalized_input == canonical:

            return "canonical"

        if normalized_input == normalized:

            return "normalized"

        for alias in entity.aliases:

            normalized_alias = (
                self.repository._normalize_lookup(
                    alias
                )
            )

            if normalized_input == normalized_alias:

                return "alias"

        return "repository"

    ##################################################################
    # ALIAS MATCH
    ##################################################################

    def _is_alias_match(
        self,
        normalized_input: str,
        entity: RepositoryEntity,
    ) -> bool:
        """
        Determine whether the supplied phrase matched an alias.
        """

        for alias in entity.aliases:

            normalized_alias = (
                self.repository._normalize_lookup(
                    alias
                )
            )

            if normalized_input == normalized_alias:

                return True

        return False

    ##################################################################
    # MATCHED PHRASE
    ##################################################################

    def _find_matched_phrase(
        self,
        normalized_input: str,
        entity: RepositoryEntity,
    ) -> str:
        """
        Return the actual repository phrase that matched.
        """

        canonical = self.repository._normalize_lookup(
            entity.canonical
        )

        if normalized_input == canonical:

            return entity.canonical

        normalized = self.repository._normalize_lookup(
            entity.normalized
        )

        if normalized_input == normalized:

            return entity.normalized

        for alias in entity.aliases:

            normalized_alias = (
                self.repository._normalize_lookup(
                    alias
                )
            )

            if normalized_input == normalized_alias:

                return alias

        return ""

    ##################################################################
    # CONFIDENCE
    ##################################################################

    @staticmethod
    def _calculate_confidence(
        match_type: str,
        matched_alias: bool,
    ) -> float:
        """
        Calculate deterministic repository confidence.

        Exact canonical/normalized matches receive the
        highest confidence.

        Aliases receive slightly lower confidence.
        """

        if match_type == "canonical":

            return 0.99

        if match_type == "normalized":

            return 0.99

        if matched_alias:

            return 0.95

        return 0.90

    ##################################################################
    # RELATED METRICS
    ##################################################################

    @staticmethod
    def _extract_related_metrics(
        entity: RepositoryEntity,
    ) -> list[str]:
        """
        Extract related_metrics from ontology-specific metadata.
        """

        related_metrics = entity.metadata.get(
            "related_metrics",
            [],
        )

        if related_metrics is None:

            return []

        if not isinstance(
            related_metrics,
            list,
        ):

            return []

        return [
            str(metric).strip()

            for metric in related_metrics

            if metric is not None
            and str(metric).strip()
        ]

    ##################################################################
    # FIND MANY
    ##################################################################

    def extract_many(
        self,
        phrases: list[str],
    ) -> list[BusinessKPIKnowledge]:
        """
        Extract multiple Business KPIs.

        Duplicate entity IDs are removed.
        """

        results = []

        seen = set()

        for phrase in phrases:

            result = self.extract(
                phrase
            )

            if not result.found:

                continue

            if result.entity_id in seen:

                continue

            seen.add(
                result.entity_id
            )

            results.append(
                result
            )

        return results

