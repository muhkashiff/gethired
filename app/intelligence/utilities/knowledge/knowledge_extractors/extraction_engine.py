"""
Enterprise Knowledge Extraction Engine
Enterprise V5

Responsibility
--------------

Orchestrates ontology-specific extraction after the
KnowledgeV5Pipeline has already performed:

    Tokenization
    Matching
    Confidence scoring
    Overlap resolution
    Ranking

The ExtractionEngine does NOT:

    - tokenize
    - normalize
    - perform fuzzy matching
    - calculate confidence
    - resolve overlaps
    - rank matches
    - perform reasoning

Those responsibilities belong to the existing
KnowledgeV5Pipeline and later Reasoner layer.

Pipeline
--------

Sentence
    ↓
KnowledgeV5Pipeline
    ↓
List[MatchResult]
    ↓
ExtractionEngine
    ↓
ExtractionResult
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional


# =====================================================================
# EXTRACTION ENGINE
# =====================================================================

class ExtractionEngine:

    """
    Central orchestration layer for ontology extraction.

    The engine receives already-ranked MatchResult objects
    from KnowledgeV5Pipeline and delegates them to the
    appropriate ontology buckets.
    """

    # =================================================================
    # INITIALIZATION
    # =================================================================

    def __init__(
        self,
        registry,
        skill_extractor=None,
        action_extractor=None,
        target_extractor=None,
        domain_extractor=None,
        metric_extractor=None,
        standard_extractor=None,
        technology_extractor=None,
        methodology_extractor=None,
        business_kpi_extractor=None,
        certification_extractor=None,
    ) -> None:

        self.registry = registry

        self.skill_extractor = skill_extractor
        self.action_extractor = action_extractor
        self.target_extractor = target_extractor
        self.domain_extractor = domain_extractor
        self.metric_extractor = metric_extractor
        self.standard_extractor = standard_extractor

        self.technology_extractor = (
            technology_extractor
        )

        self.methodology_extractor = (
            methodology_extractor
        )

        self.business_kpi_extractor = (
            business_kpi_extractor
        )

        self.certification_extractor = (
            certification_extractor
        )

    # =================================================================
    # PUBLIC API
    # =================================================================

    def extract(
        self,
        matches: Iterable[Any],
        ontology: Optional[str] = None,
    ) -> Dict[str, Any]:

        """
        Extract structured knowledge from ranked MatchResults.

        Parameters
        ----------
        matches:
            Output from KnowledgeV5Pipeline.run().

        ontology:
            Optional authoritative ontology name.

            When supplied, all matches from this pipeline pass are
            routed to that ontology bucket instead of relying entirely
            on repository entity_type metadata.

            This is useful because KnowledgeV5Pipeline.run(
                "technologies", ...
            )
            already establishes the extraction ontology.

        Returns
        -------
        dict
            Structured extraction result.
        """

        matches = list(
            matches or []
        )

        result = self._empty_result()

        # Normalize optional ontology.
        if ontology is not None:

            ontology = str(
                ontology
            ).strip().lower()

        # =============================================================
        # PROCESS MATCHES
        # =============================================================

        for match in matches:

            entity_id = self._entity_id(
                match
            )

            if not entity_id:
                continue

            entity = self.registry.get(
                entity_id
            )

            if entity is None:
                continue

            # ---------------------------------------------------------
            # IMPORTANT
            #
            # If the caller supplied the ontology used by
            # KnowledgeV5Pipeline.run(), that ontology is authoritative.
            #
            # Otherwise fall back to entity_type.
            # ---------------------------------------------------------

            if ontology:

                entity_type = self._ontology_to_entity_type(
                    ontology
                )

            else:

                entity_type = self._entity_type(
                    match,
                    entity,
                )

            self._add_match(
                result,
                entity_type,
                match,
                entity,
            )

        # =============================================================
        # OPTIONAL EXTRACTOR HOOKS
        # =============================================================

        result = self._run_extractors(
            result,
            matches,
        )

        # =============================================================
        # FINAL COUNTS
        # =============================================================

        self._update_counts(
            result
        )

        return result

    # =================================================================
    # SINGLE SENTENCE CONVENIENCE API
    # =================================================================

    def extract_sentence(
        self,
        pipeline,
        ontology,
        sentence,
    ) -> Dict[str, Any]:

        """
        Runs KnowledgeV5Pipeline for one ontology and sends the
        resulting matches through the extraction engine.

        The ontology is explicitly passed into extract() so the
        requested ontology cannot be lost because of an inconsistent
        repository entity_type.
        """

        matches = pipeline.run(
            ontology,
            sentence,
        )

        return self.extract(
            matches,
            ontology=ontology,
        )

    # =================================================================
    # EMPTY RESULT
    # =================================================================

    @staticmethod
    def _empty_result() -> Dict[str, Any]:

        return {

            "skills": [],
            "actions": [],
            "targets": [],
            "domains": [],
            "metrics": [],
            "standards": [],
            "technologies": [],
            "methodologies": [],
            "certifications": [],
            "business_kpis": [],

            "all_entities": [],

            "counts": {

                "skills": 0,
                "actions": 0,
                "targets": 0,
                "domains": 0,
                "metrics": 0,
                "standards": 0,
                "technologies": 0,
                "methodologies": 0,
                "certifications": 0,
                "business_kpis": 0,
                "all_entities": 0,
            },
        }

    # =================================================================
    # ENTITY ID
    # =================================================================

    @staticmethod
    def _entity_id(
        match: Any,
    ) -> Optional[str]:

        """
        Extract entity_id from either an object or dictionary.
        """

        if match is None:
            return None

        # -------------------------------------------------------------
        # Object
        # -------------------------------------------------------------

        entity_id = getattr(
            match,
            "entity_id",
            None,
        )

        if entity_id:
            return str(
                entity_id
            )

        # -------------------------------------------------------------
        # Dictionary
        # -------------------------------------------------------------

        if isinstance(
            match,
            dict,
        ):

            entity_id = match.get(
                "entity_id"
            )

            if entity_id:
                return str(
                    entity_id
                )

            # ---------------------------------------------------------
            # Some MatchResult implementations use nested entity.
            # ---------------------------------------------------------

            entity = match.get(
                "entity"
            )

            if isinstance(
                entity,
                dict,
            ):

                entity_id = entity.get(
                    "entity_id"
                )

                if entity_id:
                    return str(
                        entity_id
                    )

            else:

                entity_id = getattr(
                    entity,
                    "entity_id",
                    None,
                )

                if entity_id:

                    return str(
                        entity_id
                    )

        return None

    # =================================================================
    # ONTOLOGY → ENTITY TYPE
    # =================================================================

    @staticmethod
    def _ontology_to_entity_type(
        ontology: str,
    ) -> str:

        """
        Convert an ontology collection name into the canonical
        internal entity type used by _add_match().
        """

        ontology_map = {

            "skills": "skill",

            "actions": "action",

            "targets": "target",

            "domains": "domain",

            "metrics": "metric",

            "standards": "standard",

            "technologies": "technology",

            "methodologies": "methodology",

            "certifications": "certification",

            "business_kpis": "business_kpi",
        }

        return ontology_map.get(
            ontology,
            ontology,
        )

    # =================================================================
    # ENTITY TYPE
    # =================================================================

    @staticmethod
    def _entity_type(
        match: Any,
        entity: Any,
    ) -> str:

        """
        Determine ontology/entity type.

        RepositoryEntity normally exposes entity_type.

        Falls back to MatchResult and finally entity ID prefix.
        """

        # -------------------------------------------------------------
        # Repository Entity
        # -------------------------------------------------------------

        entity_type = getattr(
            entity,
            "entity_type",
            None,
        )

        if entity_type:

            return str(
                entity_type
            ).lower()

        if isinstance(
            entity,
            dict,
        ):

            entity_type = entity.get(
                "entity_type"
            )

            if entity_type:

                return str(
                    entity_type
                ).lower()

        # -------------------------------------------------------------
        # MatchResult
        # -------------------------------------------------------------

        entity_type = getattr(
            match,
            "entity_type",
            None,
        )

        if entity_type:

            return str(
                entity_type
            ).lower()

        if isinstance(
            match,
            dict,
        ):

            entity_type = match.get(
                "entity_type"
            )

            if entity_type:

                return str(
                    entity_type
                ).lower()

        # -------------------------------------------------------------
        # Entity ID fallback
        # -------------------------------------------------------------

        entity_id = ExtractionEngine._entity_id(
            match
        )

        if entity_id:

            prefix = entity_id.split(
                "_",
                1,
            )[0].upper()

            prefix_map = {

                "SKILL": "skill",

                "ACT": "action",

                "TGT": "target",

                "DOMAIN": "domain",

                "KPI": "metric",

                "BKPI": "business_kpi",

                "STD": "standard",

                "CERT": "certification",

                "TECH": "technology",

                "METH": "methodology",
            }

            return prefix_map.get(
                prefix,
                prefix.lower(),
            )

        return "unknown"

    # =================================================================
    # ADD MATCH
    # =================================================================

    def _add_match(
        self,
        result: Dict[str, Any],
        entity_type: str,
        match: Any,
        entity: Any,
    ) -> None:

        # -------------------------------------------------------------
        # Normalize type
        # -------------------------------------------------------------

        entity_type = str(
            entity_type
        ).lower().strip()

        # -------------------------------------------------------------
        # Type map
        # -------------------------------------------------------------

        type_map = {

            "skill": "skills",

            "action": "actions",
            "act": "actions",

            "target": "targets",
            "tgt": "targets",

            "domain": "domains",

            "metric": "metrics",
            "kpi": "metrics",

            "standard": "standards",
            "std": "standards",

            "technology": "technologies",
            "technologies": "technologies",
            "tech": "technologies",

            "methodology": "methodologies",
            "methodologies": "methodologies",
            "meth": "methodologies",

            "certification": "certifications",
            "certifications": "certifications",
            "cert": "certifications",

            "business_kpi": "business_kpis",
            "business_kpis": "business_kpis",
            "bkpi": "business_kpis",
        }

        result_key = type_map.get(
            entity_type
        )

        # -------------------------------------------------------------
        # Unknown type
        # -------------------------------------------------------------

        if result_key is None:
            return

        # -------------------------------------------------------------
        # Build record
        # -------------------------------------------------------------

        record = self._build_record(
            match,
            entity,
        )

        # -------------------------------------------------------------
        # Duplicate entity protection
        # -------------------------------------------------------------

        if self._contains_entity(
            result[result_key],
            record["entity_id"],
        ):

            return

        # -------------------------------------------------------------
        # Add
        # -------------------------------------------------------------

        result[result_key].append(
            record
        )

        # -------------------------------------------------------------
        # All entities
        # -------------------------------------------------------------

        if not self._contains_entity(
            result["all_entities"],
            record["entity_id"],
        ):

            result["all_entities"].append(
                record
            )

    # =================================================================
    # BUILD RECORD
    # =================================================================

    def _build_record(
        self,
        match: Any,
        entity: Any,
    ) -> Dict[str, Any]:

        entity_id = self._entity_id(
            match
        )

        canonical = self._entity_value(
            entity,
            "canonical",
        )

        category = self._entity_value(
            entity,
            "category",
        )

        domain = self._entity_value(
            entity,
            "domain",
        )

        business_area = self._entity_value(
            entity,
            "business_area",
        )

        impact_weight = self._entity_value(
            entity,
            "impact_weight",
        )

        # -------------------------------------------------------------
        # MATCH INFORMATION
        # -------------------------------------------------------------

        confidence = self._match_value(
            match,
            "confidence",
        )

        score = self._match_value(
            match,
            "score",
        )

        text = self._match_value(
            match,
            "text",
        )

        matched_text = self._match_value(
            match,
            "matched_text",
        )

        # -------------------------------------------------------------
        # TEXT FALLBACK
        # -------------------------------------------------------------

        if matched_text is None:
            matched_text = text

        # -------------------------------------------------------------
        # RECORD
        # -------------------------------------------------------------

        return {

            "entity_id": entity_id,

            "canonical": canonical,

            "matched_text": matched_text,

            "category": category,

            "domain": domain,

            "business_area": business_area,

            "impact_weight": impact_weight,

            "confidence": confidence,

            "score": score,
        }

    # =================================================================
    # ENTITY VALUE
    # =================================================================

    @staticmethod
    def _entity_value(
        entity: Any,
        key: str,
    ) -> Any:

        if entity is None:
            return None

        # -------------------------------------------------------------
        # Object
        # -------------------------------------------------------------

        value = getattr(
            entity,
            key,
            None,
        )

        if value is not None:
            return value

        # -------------------------------------------------------------
        # Dictionary
        # -------------------------------------------------------------

        if isinstance(
            entity,
            dict,
        ):

            return entity.get(
                key
            )

        return None

    # =================================================================
    # MATCH VALUE
    # =================================================================

    @staticmethod
    def _match_value(
        match: Any,
        key: str,
    ) -> Any:

        if match is None:
            return None

        # -------------------------------------------------------------
        # Object
        # -------------------------------------------------------------

        value = getattr(
            match,
            key,
            None,
        )

        if value is not None:
            return value

        # -------------------------------------------------------------
        # Dictionary
        # -------------------------------------------------------------

        if isinstance(
            match,
            dict,
        ):

            return match.get(
                key
            )

        return None

    # =================================================================
    # DUPLICATE CHECK
    # =================================================================

    @staticmethod
    def _contains_entity(
        records: List[Dict[str, Any]],
        entity_id: str,
    ) -> bool:

        for record in records:

            if record.get(
                "entity_id"
            ) == entity_id:

                return True

        return False

    # =================================================================
    # EXTRACTOR HOOKS
    # =================================================================

    def _run_extractors(
        self,
        result: Dict[str, Any],
        matches: List[Any],
    ) -> Dict[str, Any]:

        """
        Run optional specialized extractors.

        Extractors are deliberately optional.
        """

        extractor_map = [

            (
                "skill_extractor",
                "skills",
            ),

            (
                "action_extractor",
                "actions",
            ),

            (
                "target_extractor",
                "targets",
            ),

            (
                "domain_extractor",
                "domains",
            ),

            (
                "metric_extractor",
                "metrics",
            ),

            (
                "standard_extractor",
                "standards",
            ),

            (
                "technology_extractor",
                "technologies",
            ),

            (
                "methodology_extractor",
                "methodologies",
            ),

            (
                "certification_extractor",
                "certifications",
            ),

            (
                "business_kpi_extractor",
                "business_kpis",
            ),
        ]

        for attribute_name, result_key in extractor_map:

            extractor = getattr(
                self,
                attribute_name,
                None,
            )

            if extractor is None:
                continue

            extracted = self._call_extractor(
                extractor,
                matches,
            )

            self._merge_extracted(
                result,
                result_key,
                extracted,
            )

        return result

    # =================================================================
    # CALL EXTRACTOR
    # =================================================================

    @staticmethod
    def _call_extractor(
        extractor,
        matches,
    ):

        # -------------------------------------------------------------
        # Preferred API
        # -------------------------------------------------------------

        if hasattr(
            extractor,
            "extract",
        ):

            return extractor.extract(
                matches
            )

        # -------------------------------------------------------------
        # Callable extractor
        # -------------------------------------------------------------

        if callable(
            extractor
        ):

            return extractor(
                matches
            )

        return []

    # =================================================================
    # MERGE EXTRACTOR RESULT
    # =================================================================

    def _merge_extracted(
        self,
        result: Dict[str, Any],
        result_key: str,
        extracted,
    ) -> None:

        if extracted is None:
            return

        # -------------------------------------------------------------
        # Single record
        # -------------------------------------------------------------

        if isinstance(
            extracted,
            dict,
        ):

            extracted = [
                extracted
            ]

        # -------------------------------------------------------------
        # Invalid
        # -------------------------------------------------------------

        if not isinstance(
            extracted,
            (list, tuple),
        ):

            return

        # -------------------------------------------------------------
        # MERGE
        # -------------------------------------------------------------

        for record in extracted:

            if not isinstance(
                record,
                dict,
            ):

                continue

            entity_id = record.get(
                "entity_id"
            )

            if not entity_id:
                continue

            if self._contains_entity(
                result[result_key],
                entity_id,
            ):

                continue

            result[result_key].append(
                record
            )

            # ---------------------------------------------------------
            # ALL ENTITIES
            # ---------------------------------------------------------

            if not self._contains_entity(
                result["all_entities"],
                entity_id,
            ):

                result["all_entities"].append(
                    record
                )

    # =================================================================
    # COUNTS
    # =================================================================

    @staticmethod
    def _update_counts(
        result: Dict[str, Any],
    ) -> None:

        # IMPORTANT:
        # "certifications" must match the result key.
        #
        # The old code used:
        #     "certification"
        #
        # which does not exist in the result dictionary.

        for key in (
            "skills",
            "actions",
            "targets",
            "domains",
            "metrics",
            "standards",
            "technologies",
            "methodologies",
            "certifications",
            "business_kpis",
            "all_entities",
        ):

            result["counts"][key] = len(
                result[key]
            )