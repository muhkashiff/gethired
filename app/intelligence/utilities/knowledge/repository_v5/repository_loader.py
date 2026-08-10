"""
Enterprise Repository Loader
Enterprise V5

Responsibility:

Ontology JSON
    ↓
RepositoryEntity

The loader does NOT perform matching.
The loader does NOT build indexes.
The loader does NOT generate surface forms.

It only converts repository JSON records into
RepositoryEntity objects while preserving
ontology-specific information in metadata.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .repository_entity import RepositoryEntity


class RepositoryLoader:
    """
    Converts ontology JSON data into RepositoryEntity objects.
    """

    ####################################################################
    # STANDARD REPOSITORY ENTITY FIELDS
    ####################################################################

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

    ####################################################################
    # LOAD
    ####################################################################

    def load(
        self,
        ontology_name: str,
        path: str | Path,
    ) -> list[RepositoryEntity]:

        ################################################################
        # READ JSON
        ################################################################

        with open(
            path,
            "r",
            encoding="utf8",
        ) as file:

            raw = json.load(file)

        ################################################################
        # SUPPORT BOTH:
        #
        # [
        #     {...},
        #     {...}
        # ]
        #
        # AND:
        #
        # {
        #     "ACTION_001": {...},
        #     "ACTION_002": {...}
        # }
        ################################################################

        if isinstance(raw, dict):

            iterator = raw.values()

        elif isinstance(raw, list):

            iterator = raw

        else:

            raise ValueError(
                "Ontology JSON must contain "
                "either an object or an array."
            )

        ################################################################
        # BUILD ENTITIES
        ################################################################

        entities: list[RepositoryEntity] = []

        for item in iterator:

            if not isinstance(item, dict):

                raise ValueError(
                    "Every ontology entry must "
                    "be a JSON object."
                )

            entity = self._build_entity(
                ontology_name=ontology_name,
                item=item,
            )

            entities.append(entity)

        return entities

    ####################################################################
    # BUILD ENTITY
    ####################################################################

    def _build_entity(
        self,
        ontology_name: str,
        item: dict[str, Any],
    ) -> RepositoryEntity:
        """
        Convert one JSON record into RepositoryEntity.
        """

        ################################################################
        # METADATA
        ################################################################

        metadata = self._build_metadata(
            item
        )

        ################################################################
        # CANONICAL
        ################################################################

        canonical = self._string_value(
            item.get("canonical", "")
        )

        ################################################################
        # NORMALIZED
        ################################################################

        normalized = self._string_value(
            item.get(
                "normalized",
                canonical.casefold(),
            )
        )

        ################################################################
        # ALIASES
        ################################################################

        aliases = self._build_aliases(
            item.get("aliases", [])
        )

        ################################################################
        # ENTITY TYPE
        ################################################################

        entity_type = self._string_value(
            item.get(
                "entity_type",
                self._default_entity_type(
                    ontology_name
                ),
            )
        )

        ################################################################
        # BUILD RepositoryEntity
        ################################################################

        return RepositoryEntity(

            ############################################################
            # IDENTITY
            ############################################################

            entity_id=self._string_value(
                item.get("entity_id", "")
            ),

            canonical=canonical,

            normalized=normalized,

            aliases=aliases,

            ############################################################
            # LINGUISTICS
            ############################################################

            base=self._string_value(
                item.get("base", "")
            ),

            past=self._string_value(
                item.get("past", "")
            ),

            gerund=self._string_value(
                item.get("gerund", "")
            ),

            plural=self._string_value(
                item.get("plural", "")
            ),

            singular=self._string_value(
                item.get("singular", "")
            ),

            ############################################################
            # NAMING
            ############################################################

            abbreviation=self._string_value(
                item.get("abbreviation", "")
            ),

            short_name=self._string_value(
                item.get("short_name", "")
            ),

            ############################################################
            # CLASSIFICATION
            ############################################################

            category=self._string_value(
                item.get("category", "")
            ),

            entity_type=entity_type,

            ontology_name=ontology_name,

            ############################################################
            # ENTERPRISE CONTEXT
            ############################################################

            domain=self._string_value(
                item.get("domain", "")
            ),

            business_area=self._string_value(
                item.get("business_area", "")
            ),

            description=self._string_value(
                item.get("description", "")
            ),

            ############################################################
            # SCORING
            ############################################################

            impact_weight=self._float_value(
                item.get(
                    "impact_weight",
                    1.0,
                )
            ),

            ############################################################
            # SEMANTIC
            ############################################################

            business_meaning=self._string_value(
                item.get("business_meaning", "")
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

            ############################################################
            # REPOSITORY CONTROL
            ############################################################

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

            ############################################################
            # ONTOLOGY-SPECIFIC DATA
            ############################################################

            metadata=metadata,
        )

    ####################################################################
    # METADATA
    ####################################################################

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

        ################################################################
        # AUTOMATIC EXTRA FIELDS
        ################################################################

        extra_fields = {

            key: value

            for key, value in item.items()

            if key not in self._STANDARD_FIELDS
        }

        ################################################################
        # EXPLICIT METADATA
        ################################################################

        explicit_metadata = item.get(
            "metadata",
            {},
        )

        if not isinstance(
            explicit_metadata,
            dict,
        ):

            raise ValueError(
                "Ontology metadata must be "
                "a JSON object."
            )

        ################################################################
        # EXPLICIT METADATA WINS
        ################################################################

        return {
            **extra_fields,
            **explicit_metadata,
        }

    ####################################################################
    # ALIASES
    ####################################################################

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

        aliases = []

        for alias in value:

            if alias is None:
                continue

            alias = str(alias).strip()

            if not alias:
                continue

            aliases.append(alias)

        return aliases

    ####################################################################
    # DEFAULT ENTITY TYPE
    ####################################################################

    @staticmethod
    def _default_entity_type(
        ontology_name: str,
    ) -> str:
        """
        Derive the default entity type from ontology name.

        Examples:

        actions      -> action
        skills       -> skill
        standards    -> standard
        technologies -> technologie

        The repository JSON should normally provide
        the explicit entity_type.
        """

        if ontology_name.endswith("s"):

            return ontology_name[:-1]

        return ontology_name

    ####################################################################
    # SAFE STRING
    ####################################################################

    @staticmethod
    def _string_value(
        value: Any,
    ) -> str:

        if value is None:
            return ""

        return str(value).strip()

    ####################################################################
    # SAFE FLOAT
    ####################################################################

    @staticmethod
    def _float_value(
        value: Any,
    ) -> float:

        if value is None:
            return 0.0

        try:

            return float(value)

        except (
            TypeError,
            ValueError,
        ):

            raise ValueError(
                f"Invalid numeric repository value: "
                f"{value!r}"
            )

    ####################################################################
    # SAFE BOOLEAN
    ####################################################################

    @staticmethod
    def _bool_value(
        value: Any,
    ) -> bool:

        if isinstance(
            value,
            bool,
        ):

            return value

        if isinstance(
            value,
            str,
        ):

            normalized = value.casefold().strip()

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