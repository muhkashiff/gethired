# Repository Loader

"""
Enterprise Repository Loader
Enterprise V5

Responsibility
--------------

Ontology JSON
    ↓
RepositoryEntity

The loader does NOT perform matching.
The loader does NOT build indexes.
The loader does NOT generate surface forms.

It only converts repository JSON records into
RepositoryEntity objects while preserving
ontology-specific information in metadata.

Canonical Entity Types
----------------------

RepositoryLoader is the canonical boundary between
repository JSON and the runtime knowledge system.

Therefore repository entity types are normalized here.

Examples:

    actions         -> action
    skills          -> skill
    technologies    -> technology
    certifications  -> certification
    standards       -> standard
    methodologies   -> methodology
    metrics         -> metric
    measurements    -> measurement
    domains         -> domain
    targets         -> target
    modifiers       -> modifier
    practices       -> practice
    kpis            -> kpi
    business_kpis   -> business_kpi

Legacy values are also normalized:

    technologie    -> technology
    methodologie   -> methodology

This prevents vocabulary conflicts between:

    repository
    matcher
    technology extractor
    interpretation model
    metadata builder
    semantic statistics
    knowledge profile
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .repository_entity import RepositoryEntity


class RepositoryLoader:
    """
    Converts ontology JSON data into RepositoryEntity objects.

    This class is intentionally responsible only for repository
    loading and normalization.

    It does not:

    - perform matching
    - build matcher indexes
    - generate surface forms
    - calculate profile scores
    """

    # ==============================================================
    # STANDARD REPOSITORY ENTITY FIELDS
    # ==============================================================

    _STANDARD_FIELDS = frozenset(
        {
            "entity_id",
            "canonical",
            "normalized",
            "aliases",

            # Linguistic fields
            "base",
            "past",
            "gerund",
            "plural",
            "singular",

            # Naming fields
            "abbreviation",
            "short_name",

            # Classification
            "category",
            "entity_type",
            "ontology_name",

            # Enterprise context
            "domain",
            "business_area",
            "description",

            # Business KPI relationships
            "related_metrics",

            # Scoring
            "impact_weight",

            # Semantic fields
            "business_meaning",
            "preferred_direction",
            "preferred_unit",
            "higher_is_better",

            # Repository control
            "searchable",
            "active",
            "source",

            # Explicit metadata
            "metadata",
        }
    )

    # ==============================================================
    # CANONICAL ONTOLOGY -> ENTITY TYPE MAP
    # ==============================================================

    _ONTOLOGY_ENTITY_TYPES = {
        "actions": "action",
        "skills": "skill",
        "technologies": "technology",
        "certifications": "certification",
        "standards": "standard",
        "methodologies": "methodology",
        "metrics": "metric",
        "measurements": "measurement",
        "domains": "domain",
        "targets": "target",
        "modifiers": "modifier",
        "practices": "practice",
        "kpis": "kpi",
        "business_kpis": "business_kpi",
    }

    # ==============================================================
    # LEGACY ENTITY TYPE ALIASES
    # ==============================================================
    #
    # These exist only for backward compatibility with older
    # repository JSON records or previously generated objects.
    #
    # Runtime code should use only the canonical values.
    # ==============================================================

    _ENTITY_TYPE_ALIASES = {
        "technologie": "technology",
        "methodologie": "methodology",
    }

    # ==============================================================
    # LOAD
    # ==============================================================

    def load(
        self,
        ontology_name: str,
        path: str | Path,
    ) -> list[RepositoryEntity]:
        """
        Load ontology JSON and convert every record into
        a RepositoryEntity.

        Supports both:

            [
                {...},
                {...}
            ]

        and:

            {
                "ENTITY_001": {...},
                "ENTITY_002": {...}
            }
        """

        # ----------------------------------------------------------
        # Normalize ontology name
        # ----------------------------------------------------------

        normalized_ontology = self._normalize_ontology_name(
            ontology_name
        )

        # ----------------------------------------------------------
        # Read JSON
        # ----------------------------------------------------------

        with open(
            path,
            "r",
            encoding="utf8",
        ) as file:
            raw = json.load(file)

        # ----------------------------------------------------------
        # Support object or array
        # ----------------------------------------------------------

        if isinstance(raw, dict):
            iterator = raw.values()

        elif isinstance(raw, list):
            iterator = raw

        else:
            raise ValueError(
                "Ontology JSON must contain either "
                "an object or an array."
            )

        # ----------------------------------------------------------
        # Build entities
        # ----------------------------------------------------------

        entities: list[RepositoryEntity] = []

        for item in iterator:

            if not isinstance(item, dict):
                raise ValueError(
                    "Every ontology entry must be a JSON object."
                )

            entity = self._build_entity(
                ontology_name=normalized_ontology,
                item=item,
            )

            entities.append(entity)

        return entities

    # ==============================================================
    # BUILD ENTITY
    # ==============================================================

    def _build_entity(
        self,
        ontology_name: str,
        item: dict[str, Any],
    ) -> RepositoryEntity:
        """
        Convert one JSON record into RepositoryEntity.
        """

        # ----------------------------------------------------------
        # Metadata
        # ----------------------------------------------------------

        metadata = self._build_metadata(
            item
        )

        # ----------------------------------------------------------
        # Canonical
        # ----------------------------------------------------------

        canonical = self._string_value(
            item.get(
                "canonical",
                "",
            )
        )

        # ----------------------------------------------------------
        # Normalized
        # ----------------------------------------------------------

        normalized = self._string_value(
            item.get(
                "normalized",
                canonical.casefold(),
            )
        )

        # ----------------------------------------------------------
        # Aliases
        # ----------------------------------------------------------

        aliases = self._build_aliases(
            item.get(
                "aliases",
                [],
            )
        )

        # ----------------------------------------------------------
        # Entity type
        #
        # IMPORTANT:
        #
        # This is where "technologie" becomes "technology".
        # ----------------------------------------------------------

        raw_entity_type = item.get(
            "entity_type",
            self._default_entity_type(
                ontology_name
            ),
        )

        entity_type = self._normalize_entity_type(
            raw_entity_type
        )

        # ----------------------------------------------------------
        # Build RepositoryEntity
        # ----------------------------------------------------------

        return RepositoryEntity(

            # ======================================================
            # IDENTITY
            # ======================================================

            entity_id=self._string_value(
                item.get(
                    "entity_id",
                    "",
                )
            ),

            canonical=canonical,

            normalized=normalized,

            aliases=aliases,

            # ======================================================
            # LINGUISTICS
            # ======================================================

            base=self._string_value(
                item.get(
                    "base",
                    "",
                )
            ),

            past=self._string_value(
                item.get(
                    "past",
                    "",
                )
            ),

            gerund=self._string_value(
                item.get(
                    "gerund",
                    "",
                )
            ),

            plural=self._string_value(
                item.get(
                    "plural",
                    "",
                )
            ),

            singular=self._string_value(
                item.get(
                    "singular",
                    "",
                )
            ),

            # ======================================================
            # NAMING
            # ======================================================

            abbreviation=self._string_value(
                item.get(
                    "abbreviation",
                    "",
                )
            ),

            short_name=self._string_value(
                item.get(
                    "short_name",
                    "",
                )
            ),

            # ======================================================
            # CLASSIFICATION
            # ======================================================

            category=self._string_value(
                item.get(
                    "category",
                    "",
                )
            ),

            entity_type=entity_type,

            ontology_name=ontology_name,

            # ======================================================
            # ENTERPRISE CONTEXT
            # ======================================================

            domain=self._string_value(
                item.get(
                    "domain",
                    "",
                )
            ),

            business_area=self._string_value(
                item.get(
                    "business_area",
                    "",
                )
            ),

            description=self._string_value(
                item.get(
                    "description",
                    "",
                )
            ),

            related_metrics=self._build_related_metrics(
                item.get(
                    "related_metrics",
                    [],
                )
            ),

            # ======================================================
            # SCORING
            # ======================================================

            impact_weight=self._float_value(
                item.get(
                    "impact_weight",
                    1.0,
                )
            ),

            # ======================================================
            # SEMANTIC
            # ======================================================

            business_meaning=self._string_value(
                item.get(
                    "business_meaning",
                    "",
                )
            ),

            preferred_direction=self._string_value(
                item.get(
                    "preferred_direction",
                    "",
                )
            ),

            preferred_unit=self._string_value(
                item.get(
                    "preferred_unit",
                    "",
                )
            ),

            higher_is_better=self._bool_value(
                item.get(
                    "higher_is_better",
                    True,
                )
            ),

            # ======================================================
            # REPOSITORY CONTROL
            # ======================================================

            searchable=self._bool_value(
                item.get(
                    "searchable",
                    True,
                )
            ),

            active=self._bool_value(
                item.get(
                    "active",
                    True,
                )
            ),

            source=self._string_value(
                item.get(
                    "source",
                    ontology_name,
                )
            ),

            # ======================================================
            # ONTOLOGY-SPECIFIC DATA
            # ======================================================

            metadata=metadata,
        )

    # ==============================================================
    # METADATA
    # ==============================================================

    def _build_metadata(
        self,
        item: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Preserve every ontology-specific field that is not represented
        directly on RepositoryEntity.

        Explicit JSON metadata takes priority over automatically
        preserved ontology-specific fields.
        """

        # ----------------------------------------------------------
        # Automatic extra fields
        # ----------------------------------------------------------

        extra_fields = {
            key: value
            for key, value in item.items()
            if key not in self._STANDARD_FIELDS
        }

        # ----------------------------------------------------------
        # Explicit metadata
        # ----------------------------------------------------------

        explicit_metadata = item.get(
            "metadata",
            {},
        )

        if not isinstance(
            explicit_metadata,
            dict,
        ):
            raise ValueError(
                "Ontology metadata must be a JSON object."
            )

        # ----------------------------------------------------------
        # Explicit metadata wins
        # ----------------------------------------------------------

        return {
            **extra_fields,
            **explicit_metadata,
        }

    # ==============================================================
    # ALIASES
    # ==============================================================

    @staticmethod
    def _build_aliases(
        value: Any,
    ) -> list[str]:
        """
        Normalize aliases into a clean list of strings.
        """

        if value is None:
            return []

        if not isinstance(
            value,
            list,
        ):
            raise ValueError(
                "Ontology aliases must be a JSON array."
            )

        aliases: list[str] = []

        for alias in value:

            if alias is None:
                continue

            alias = str(alias).strip()

            if not alias:
                continue

            aliases.append(alias)

        return aliases

    # ==============================================================
    # RELATED METRICS
    # ==============================================================

    @staticmethod
    def _build_related_metrics(
        value: Any,
    ) -> list[str]:
        """
        Normalize related metrics into a clean list of strings.
        """

        if value is None:
            return []

        if not isinstance(
            value,
            list,
        ):
            raise ValueError(
                "Ontology related_metrics must be "
                "a JSON array."
            )

        metrics: list[str] = []

        for metric in value:

            if metric is None:
                continue

            metric = str(metric).strip()

            if not metric:
                continue

            metrics.append(metric)

        return metrics

    # ==============================================================
    # DEFAULT ENTITY TYPE
    # ==============================================================

    @classmethod
    def _default_entity_type(
        cls,
        ontology_name: str,
    ) -> str:
        """
        Derive the canonical entity type from ontology name.

        Examples:

            actions        -> action
            skills         -> skill
            technologies   -> technology
            certifications -> certification
            methodologies  -> methodology
            metrics        -> metric
            business_kpis  -> business_kpi
        """

        normalized_ontology = (
            cls._normalize_ontology_name(
                ontology_name
            )
        )

        # ----------------------------------------------------------
        # Explicit canonical mapping
        # ----------------------------------------------------------

        entity_type = cls._ONTOLOGY_ENTITY_TYPES.get(
            normalized_ontology
        )

        if entity_type:
            return entity_type

        # ----------------------------------------------------------
        # Generic fallback
        # ----------------------------------------------------------

        if normalized_ontology.endswith("s"):
            return normalized_ontology[:-1]

        return normalized_ontology

    # ==============================================================
    # NORMALIZE ENTITY TYPE
    # ==============================================================

    @classmethod
    def _normalize_entity_type(
        cls,
        entity_type: Any,
    ) -> str:
        """
        Normalize a repository entity type to the canonical
        runtime vocabulary.

        This protects the runtime from legacy repository values.

        Examples:

            technologie  -> technology
            methodologie -> methodology
            technology   -> technology
            methodology  -> methodology
        """

        normalized = (
            cls._string_value(
                entity_type
            )
            .casefold()
        )

        if not normalized:
            return ""

        return cls._ENTITY_TYPE_ALIASES.get(
            normalized,
            normalized,
        )

    # ==============================================================
    # NORMALIZE ONTOLOGY NAME
    # ==============================================================

    @staticmethod
    def _normalize_ontology_name(
        ontology_name: Any,
    ) -> str:
        """
        Normalize ontology collection names.

        Ontology names remain plural collection names.

        Example:

            technologies
            methodologies
            business_kpis
        """

        return (
            str(
                ontology_name
                if ontology_name is not None
                else ""
            )
            .strip()
            .casefold()
        )

    # ==============================================================
    # SAFE STRING
    # ==============================================================

    @staticmethod
    def _string_value(
        value: Any,
    ) -> str:
        """
        Convert a repository value safely into a string.
        """

        if value is None:
            return ""

        return str(value).strip()

    # ==============================================================
    # SAFE FLOAT
    # ==============================================================

    @staticmethod
    def _float_value(
        value: Any,
    ) -> float:
        """
        Convert a repository value safely into a float.
        """

        if value is None:
            return 0.0

        try:
            return float(value)

        except (
            TypeError,
            ValueError,
        ) as error:

            raise ValueError(
                "Invalid numeric repository value: "
                f"{value!r}"
            ) from error

    # ==============================================================
    # SAFE BOOLEAN
    # ==============================================================

    @staticmethod
    def _bool_value(
        value: Any,
    ) -> bool:
        """
        Convert a repository value safely into a boolean.
        """

        if isinstance(
            value,
            bool,
        ):
            return value

        if isinstance(
            value,
            str,
        ):

            normalized = (
                value
                .casefold()
                .strip()
            )

            if normalized in {
                "true",
                "yes",
                "1",
            }:
                return True

            if normalized in {
                "false",
                "no",
                "0",
            }:
                return False

        return bool(value)
