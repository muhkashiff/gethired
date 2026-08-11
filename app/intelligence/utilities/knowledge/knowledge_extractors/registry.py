"""
Enterprise Knowledge Registry
Enterprise V5

Responsibility:
Centralized read-only access to ontology entities and relations.

The Registry does NOT:
- tokenize text
- match text
- calculate confidence
- rank matches
- perform reasoning
- extract actions
- extract targets
- extract metrics

Those responsibilities belong to other layers.
"""

from typing import Any, Dict, List, Optional


class KnowledgeRegistry:

    # ================================================================
    # INITIALIZATION
    # ================================================================

    def __init__(self, repository):

        self.repository = repository

        self._entity_cache: Dict[str, Any] = {}
        self._alias_cache: Dict[str, str] = {}

        self._build_cache()

    # ================================================================
    # BUILD CACHE
    # ================================================================

    def _build_cache(self) -> None:
        """
        Build a global entity cache from the existing Repository.

        Repository V5 stores entities inside:

            repository.cache.entity_indexes

        Structure:

            ontology_name
                ↓
            entity_id
                ↓
            EntityRepositoryRecord
        """

        entity_indexes = getattr(
            self.repository.cache,
            "entity_indexes",
            None,
        )

        if not isinstance(entity_indexes, dict):

            raise AttributeError(
                "Repository cache does not expose "
                "'entity_indexes'."
            )

        for ontology_name, entities in entity_indexes.items():

            if not isinstance(entities, dict):
                continue

            for entity_id, entity in entities.items():

                if not entity_id:
                    continue

                self._entity_cache[entity_id] = entity

                # ------------------------------------------------
                # CANONICAL
                # ------------------------------------------------

                canonical = getattr(
                    entity,
                    "canonical",
                    None,
                )

                if canonical:

                    normalized = self._normalize(
                        canonical
                    )

                    if normalized:
                        self._alias_cache[
                            normalized
                        ] = entity_id

                # ------------------------------------------------
                # ALIASES
                # ------------------------------------------------

                aliases = getattr(
                    entity,
                    "aliases",
                    [],
                )

                if isinstance(aliases, list):

                    for alias in aliases:

                        if not alias:
                            continue

                        normalized = self._normalize(
                            alias
                        )

                        if normalized:

                            self._alias_cache[
                                normalized
                            ] = entity_id

    # ================================================================
    # ENTITY LOOKUP
    # ================================================================

    def exists(
        self,
        entity_id: str,
    ) -> bool:

        return entity_id in self._entity_cache

    # ================================================================

    def get(
        self,
        entity_id: str,
    ) -> Optional[Any]:

        return self._entity_cache.get(
            entity_id
        )

    # ================================================================

    def require(
        self,
        entity_id: str,
    ) -> Any:

        entity = self.get(
            entity_id
        )

        if entity is None:

            raise KeyError(
                f"Unknown ontology entity: {entity_id}"
            )

        return entity

    # ================================================================
    # ALIAS RESOLUTION
    # ================================================================

    def resolve_alias(
        self,
        text: str,
    ) -> Optional[str]:

        normalized = self._normalize(
            text
        )

        if not normalized:
            return None

        return self._alias_cache.get(
            normalized
        )

    # ================================================================
    # CANONICAL
    # ================================================================

    def canonical(
        self,
        entity_id: str,
    ) -> Optional[str]:

        entity = self.get(
            entity_id
        )

        if entity is None:
            return None

        return getattr(
            entity,
            "canonical",
            None,
        )

    # ================================================================
    # CATEGORY
    # ================================================================

    def category(
        self,
        entity_id: str,
    ) -> Optional[str]:

        entity = self.get(
            entity_id
        )

        if entity is None:
            return None

        return getattr(
            entity,
            "category",
            None,
        )

    # ================================================================
    # ENTITY TYPE
    # ================================================================

    def entity_type(
        self,
        entity_id: str,
    ) -> Optional[str]:

        entity = self.get(
            entity_id
        )

        if entity is None:
            return None

        return getattr(
            entity,
            "entity_type",
            None,
        )

    # ================================================================
    # IMPACT WEIGHT
    # ================================================================

    def impact_weight(
        self,
        entity_id: str,
    ) -> float:

        entity = self.get(
            entity_id
        )

        if entity is None:
            return 0.0

        value = getattr(
            entity,
            "impact_weight",
            1.0,
        )

        try:
            return float(value)

        except (
            TypeError,
            ValueError,
        ):
            return 1.0

    # ================================================================
    # ALIASES
    # ================================================================

    def aliases(
        self,
        entity_id: str,
    ) -> List[str]:

        entity = self.get(
            entity_id
        )

        if entity is None:
            return []

        aliases = getattr(
            entity,
            "aliases",
            [],
        )

        return (
            aliases
            if isinstance(aliases, list)
            else []
        )

    # ================================================================
    # RELATIONS FROM
    # ================================================================

    def relations_from(
        self,
        entity_id: str,
    ) -> List[Any]:
        """
        Return all relations originating from entity_id.
        """

        finder = getattr(
            self.repository,
            "find_relations_by_source",
            None,
        )

        if callable(finder):

            return finder(
                entity_id
            )

        return []

    # ================================================================
    # RELATIONS TO
    # ================================================================

    def relations_to(
        self,
        entity_id: str,
    ) -> List[Any]:
        """
        Return all relations targeting entity_id.
        """

        finder = getattr(
            self.repository,
            "find_relations_by_target",
            None,
        )

        if callable(finder):

            return finder(
                entity_id
            )

        return []

    # ================================================================
    # RELATION BY ID
    # ================================================================

    def relation(
        self,
        relation_id: str,
    ) -> Optional[Any]:

        finder = getattr(
            self.repository,
            "find_relation",
            None,
        )

        if callable(finder):

            return finder(
                relation_id
            )

        return None

    # ================================================================
    # RELATIONS BY TYPE
    # ================================================================

    def relations_by_type(
        self,
        relation_type: str,
    ) -> List[Any]:

        finder = getattr(
            self.repository,
            "find_relations_by_type",
            None,
        )

        if callable(finder):

            return finder(
                relation_type
            )

        return []

    # ================================================================
    # VALIDATION
    # ================================================================

    def validate(
        self,
        entity_ids: List[str],
    ) -> Dict[str, Any]:

        valid = []
        invalid = []

        for entity_id in entity_ids:

            if self.exists(entity_id):

                valid.append(
                    entity_id
                )

            else:

                invalid.append(
                    entity_id
                )

        return {

            "valid": valid,

            "invalid": invalid,

            "valid_count": len(
                valid
            ),

            "invalid_count": len(
                invalid
            ),
        }

    # ================================================================
    # STATISTICS
    # ================================================================

    @property
    def entity_count(self) -> int:

        return len(
            self._entity_cache
        )

    # ================================================================

    @property
    def alias_count(self) -> int:

        return len(
            self._alias_cache
        )

    # ================================================================

    def stats(self) -> Dict[str, int]:

        return {

            "entity_count":
                self.entity_count,

            "alias_count":
                self.alias_count,
        }

    # ================================================================
    # NORMALIZATION
    # ================================================================

    @staticmethod
    def _normalize(
        value: str,
    ) -> str:

        if not isinstance(
            value,
            str,
        ):

            return ""

        return " ".join(
            value
                .casefold()
                .replace("-", " ")
                .replace("_", " ")
                .split()
        )