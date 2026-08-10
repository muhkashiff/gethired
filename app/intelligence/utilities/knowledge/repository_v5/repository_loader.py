"""
Enterprise Repository Loader

Loads ontology JSON files into RepositoryEntity objects while preserving
ontology-specific fields inside RepositoryEntity.metadata.
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

    _STANDARD_FIELDS = frozenset(
        {
            "entity_id",
            "canonical",
            "normalized",
            "aliases",
            "base",
            "past",
            "gerund",
            "plural",
            "singular",
            "abbreviation",
            "short_name",
            "category",
            "entity_type",
            "ontology_name",
            "domain",
            "business_area",
            "description",
            "impact_weight",
            "business_meaning",
            "preferred_direction",
            "preferred_unit",
            "higher_is_better",
            "searchable",
            "active",
            "source",
            "metadata",
        }
    )

    def load(
        self,
        ontology_name: str,
        path: str | Path,
    ) -> list[RepositoryEntity]:
        with open(
            path,
            "r",
            encoding="utf8",
        ) as file:
            raw = json.load(file)

        iterator = raw.values() if isinstance(raw, dict) else raw

        entities: list[RepositoryEntity] = []

        for item in iterator:
            if not isinstance(item, dict):
                raise ValueError(
                    "Every ontology entry must be a JSON object."
                )

            metadata = self._build_metadata(item)

            entity = RepositoryEntity(
                entity_id=item.get("entity_id", ""),
                canonical=item.get("canonical", ""),
                normalized=item.get(
                    "normalized",
                    item.get("canonical", "").lower(),
                ),
                aliases=item.get("aliases", []),

                base=item.get("base", ""),
                past=item.get("past", ""),
                gerund=item.get("gerund", ""),
                plural=item.get("plural", ""),
                singular=item.get("singular", ""),
                abbreviation=item.get("abbreviation", ""),
                short_name=item.get("short_name", ""),

                category=item.get("category", ""),
                entity_type=item.get(
                    "entity_type",
                    ontology_name[:-1]
                    if ontology_name.endswith("s")
                    else ontology_name,
                ),
                ontology_name=ontology_name,

                domain=item.get("domain", ""),
                business_area=item.get(
                    "business_area",
                    "",
                ),
                description=item.get(
                    "description",
                    "",
                ),

                impact_weight=item.get(
                    "impact_weight",
                    1.0,
                ),
                business_meaning=item.get(
                    "business_meaning",
                    "",
                ),
                preferred_direction=item.get(
                    "preferred_direction",
                    "",
                ),
                preferred_unit=item.get(
                    "preferred_unit",
                    "",
                ),
                higher_is_better=item.get(
                    "higher_is_better",
                    True,
                ),

                searchable=item.get(
                    "searchable",
                    True,
                ),
                active=item.get(
                    "active",
                    True,
                ),

                source=item.get(
                    "source",
                    ontology_name,
                ),

                metadata=metadata,
            )

            entities.append(entity)

        return entities

    def _build_metadata(
        self,
        item: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Preserve every ontology-specific field not represented directly
        on RepositoryEntity.

        Explicit JSON metadata is retained and takes priority over
        automatically preserved fields.
        """
        extra_fields = {
            key: value
            for key, value in item.items()
            if key not in self._STANDARD_FIELDS
        }

        explicit_metadata = item.get(
            "metadata",
            {},
        )

        if not isinstance(explicit_metadata, dict):
            raise ValueError(
                "Ontology metadata must be a JSON object."
            )

        return {
            **extra_fields,
            **explicit_metadata,
        }