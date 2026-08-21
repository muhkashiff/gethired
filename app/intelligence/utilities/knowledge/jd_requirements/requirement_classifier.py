"""
JD Requirement Classifier
=========================

Enterprise Phase 2
-------------------

Interpret an existing DocumentKnowledgeProfile for a Job Description
into a JDRequirementProfile.

Architecture
------------

    DocumentInput
          |
          v
    Knowledge Pipeline
          |
          v
    KnowledgeProfile
          |
          v
    DocumentKnowledgeProfile
          |
          v
    BusinessStatement objects
          |
          v
    JDRequirementClassifier
          |
          v
    JDRequirement objects
          |
          v
    JDRequirementProfile

Important
---------

This classifier is an interpretation layer.

It does NOT:

    - extract text
    - perform NLP extraction
    - rebuild the KnowledgeGraph
    - create SemanticEntity objects
    - create BusinessStatement objects
    - perform resume/JD matching
    - calculate ATS scores

Object-oriented boundary
------------------------

The preferred flow is:

    DocumentKnowledgeProfile
        -> BusinessStatement
        -> SemanticEntity
        -> JDRequirement
        -> JDRequirementProfile

The classifier does NOT convert enterprise objects back into dictionaries.

Compatibility
-------------

The existing KnowledgeProfile contains a BusinessStatementProfile whose
serialized statements may be dictionaries.

Therefore this classifier uses the following source priority:

    1. Original BusinessStatement objects exposed by source_result
    2. BusinessStatement objects exposed directly by source_result
    3. Serialized BusinessStatement dictionaries from the profile

This preserves the object-oriented pipeline while remaining compatible with
the current KnowledgeProfile projection.

Evidence
--------

Evidence is resolved from BusinessStatement in this order:

    source_text
    text
    canonical
    normalized

This is intentional.

source_text is the strongest explainability evidence because it represents
the originating document text rather than a classifier-generated sentence.
"""

from __future__ import annotations

import re
from typing import Any, Iterable

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.jd_requirements.requirement_models import (
    ExperienceCategory,
    JDRequirement,
    JDRequirementProfile,
    RequirementPriority,
    RequirementType,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    BusinessStatement,
    SemanticEntity,
)


# ============================================================================
# CLASSIFIER
# ============================================================================


class JDRequirementClassifier:
    """
    Interpret JD evidence already present in DocumentKnowledgeProfile.

    The classifier consumes existing enterprise objects.

    Preferred input:

        DocumentKnowledgeProfile
            -> BusinessStatement objects
            -> SemanticEntity objects

    Output:

        JDRequirementProfile
    """

    # ------------------------------------------------------------------
    # EXPERIENCE DETECTION
    # ------------------------------------------------------------------

    YEARS_PATTERN = re.compile(
        r"\b"
        r"(?:at\s+least\s+|minimum\s+|over\s+|more\s+than\s+)?"
        r"(\d+(?:\.\d+)?)"
        r"\s*\+?"
        r"\s*years?"
        r"\b",
        re.IGNORECASE,
    )

    # ------------------------------------------------------------------
    # REQUIRED LANGUAGE
    # ------------------------------------------------------------------

    REQUIRED_TERMS = (
        "required",
        "must",
        "mandatory",
        "essential",
        "minimum",
        "need to",
        "needs to",
        "shall",
        "required to",
    )

    # ------------------------------------------------------------------
    # PREFERRED LANGUAGE
    # ------------------------------------------------------------------

    PREFERRED_TERMS = (
        "preferred",
        "preferably",
        "desired",
        "desirable",
        "plus",
        "nice to have",
        "would be an advantage",
        "advantageous",
    )

    # ------------------------------------------------------------------
    # ENTITY TYPE -> REQUIREMENT TYPE
    # ------------------------------------------------------------------

    TYPE_BY_ENTITY = {
        "skill": RequirementType.SKILL,
        "technology": RequirementType.TECHNOLOGY,
        "methodology": RequirementType.METHODOLOGY,
        "certification": RequirementType.CERTIFICATION,
        "standard": RequirementType.QUALIFICATION,
        "domain": RequirementType.DOMAIN,
        "metric": RequirementType.METRIC,
        "kpi": RequirementType.METRIC,
        "education": RequirementType.EDUCATION,
        "qualification": RequirementType.QUALIFICATION,

        # Semantic action entities in a JD represent responsibilities.
        "action": RequirementType.RESPONSIBILITY,
        "responsibility": RequirementType.RESPONSIBILITY,
        "task": RequirementType.RESPONSIBILITY,

        # Functional/job-family entities are interpreted as experience
        # when they occur in an experience statement. They are not directly
        # emitted here unless the statement contains experience evidence.
        "function": RequirementType.RESPONSIBILITY,
        "functional_area": RequirementType.RESPONSIBILITY,
        "job_family": RequirementType.RESPONSIBILITY,
        "role": RequirementType.RESPONSIBILITY,
    }

    # ------------------------------------------------------------------
    # EXPERIENCE ENTITY TYPES
    # ------------------------------------------------------------------

    EXPERIENCE_ENTITY_TYPES = {
        "domain",
        "skill",
        "technology",
        "methodology",
        "function",
        "functional_area",
        "job_family",
        "role",
    }

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def process(
        self,
        document_profile: DocumentKnowledgeProfile,
    ) -> JDRequirementProfile:
        """
        Process one JD DocumentKnowledgeProfile.

        Object In
            DocumentKnowledgeProfile

        Object Out
            JDRequirementProfile
        """

        self._validate_document_profile(
            document_profile
        )

        statements = (
            self._extract_business_statements(
                document_profile
            )
        )

        requirements: list[
            JDRequirement
        ] = []

        seen: set[
            tuple[str, str, str]
        ] = set()

        # =================================================================
        # PRIMARY OBJECT PATH
        # =================================================================

        for statement in statements:

            statement_text = (
                self._statement_text(
                    statement
                )
            )

            if not statement_text:
                continue

            statement_entities = (
                self._statement_entities(
                    statement
                )
            )

            priority = (
                self._priority(
                    statement_text,
                    statement,
                )
            )

            # --------------------------------------------------------------
            # EXPERIENCE REQUIREMENT
            # --------------------------------------------------------------

            years = (
                self._minimum_years(
                    statement_text,
                    statement,
                )
            )

            experience_subject = ""

            if years is not None:

                experience_subject = (
                    self._experience_subject(
                        statement,
                        statement_entities,
                    )
                )

                experience_category = (
                    self._experience_category(
                        statement,
                        statement_entities,
                    )
                )

                requirement = (
                    self._make_requirement(
                        statement=statement,
                        requirement_type=(
                            RequirementType.EXPERIENCE
                        ),
                        priority=priority,
                        subject=experience_subject,
                        entity_id=(
                            self._experience_entity_id(
                                statement_entities
                            )
                        ),
                        domain=(
                            experience_subject
                            if (
                                experience_category
                                == ExperienceCategory.DOMAIN
                            )
                            else self._first_domain(
                                statement_entities
                            )
                        ),
                        experience_domain=(
                            experience_subject
                        ),
                        experience_category=(
                            experience_category
                        ),
                        minimum_years=years,
                        confidence=(
                            self._experience_confidence(
                                statement,
                                statement_entities,
                            )
                        ),
                    )
                )

                self._append_unique(
                    requirements,
                    seen,
                    requirement,
                )

            # --------------------------------------------------------------
            # ENTITY-BACKED REQUIREMENTS
            # --------------------------------------------------------------

            for entity in statement_entities:

                requirement_type = (
                    self._requirement_type(
                        entity,
                        statement,
                    )
                )

                if requirement_type is None:
                    continue

                subject = (
                    self._entity_subject(
                        entity
                    )
                )

                if not subject:
                    continue

                # ----------------------------------------------------------
                # Avoid duplicate DOMAIN when the same statement already
                # generated a domain-specific EXPERIENCE requirement.
                # ----------------------------------------------------------

                if (
                    years is not None
                    and requirement_type
                    == RequirementType.DOMAIN
                    and self._same_subject(
                        subject,
                        experience_subject,
                    )
                ):
                    continue

                # ----------------------------------------------------------
                # FUNCTION / ROLE / JOB FAMILY
                #
                # If there is explicit years evidence, the experience
                # requirement already represents the experience dimension.
                # Do not manufacture a second responsibility requirement
                # merely because the semantic entity is a function.
                # ----------------------------------------------------------

                if (
                    years is not None
                    and requirement_type
                    == RequirementType.RESPONSIBILITY
                    and self._entity_type(
                        entity
                    )
                    in {
                        "function",
                        "functional_area",
                        "job_family",
                        "role",
                    }
                ):
                    continue

                requirement = (
                    self._make_requirement(
                        statement=statement,
                        requirement_type=(
                            requirement_type
                        ),
                        priority=priority,
                        subject=subject,
                        entity_id=(
                            self._entity_id(
                                entity
                            )
                        ),
                        domain=(
                            self._entity_domain(
                                entity
                            )
                        ),
                        confidence=(
                            self._entity_confidence(
                                entity,
                                self._confidence(
                                    statement,
                                    0.75,
                                ),
                            )
                        ),
                    )
                )

                self._append_unique(
                    requirements,
                    seen,
                    requirement,
                )

        # =================================================================
        # PROFILE-DATA FALLBACK
        # =================================================================

        if not requirements:

            self._classify_profile_fallback(
                document_profile=document_profile,
                requirements=requirements,
                seen=seen,
            )

        return (
            JDRequirementProfile.from_requirements(
                requirements
            )
        )

    # =========================================================================
    # DOCUMENT VALIDATION
    # =========================================================================

    @staticmethod
    def _validate_document_profile(
        document_profile: DocumentKnowledgeProfile,
    ) -> None:

        if not isinstance(
            document_profile,
            DocumentKnowledgeProfile,
        ):
            raise TypeError(
                "JDRequirementClassifier.process() "
                "expects a DocumentKnowledgeProfile."
            )

        if (
            document_profile.document_type
            != DocumentType.JD
        ):
            raise ValueError(
                "JDRequirementClassifier.process() "
                "only accepts a JD profile."
            )

    # =========================================================================
    # BUSINESS STATEMENT EXTRACTION
    # =========================================================================

    @classmethod
    def _extract_business_statements(
        cls,
        document_profile: DocumentKnowledgeProfile,
    ) -> list[Any]:
        """
        Retrieve the best available BusinessStatement representation.

        Priority:

            1. source_result.business_statements
            2. source_result.result.business_statements
            3. profile.business_statements.statements

        The first two are preferred because they preserve actual
        BusinessStatement objects.
        """

        source_result = getattr(
            document_profile,
            "source_result",
            None,
        )

        candidates = (
            cls._find_business_statements(
                source_result
            )
        )

        if candidates:
            return candidates

        profile = getattr(
            document_profile,
            "profile",
            None,
        )

        business_statement_profile = getattr(
            profile,
            "business_statements",
            None,
        )

        if business_statement_profile is None:
            return []

        statements = getattr(
            business_statement_profile,
            "statements",
            None,
        )

        if statements is None:
            return []

        try:
            return list(
                statements
            )
        except TypeError:
            return []

    @classmethod
    def _find_business_statements(
        cls,
        obj: Any,
    ) -> list[Any]:
        """
        Recursively inspect known pipeline result boundaries.

        This is deliberately narrow.

        It does not walk arbitrary object graphs.
        """

        if obj is None:
            return []

        if isinstance(
            obj,
            (list, tuple),
        ):

            values = [
                item
                for item in obj
                if isinstance(
                    item,
                    BusinessStatement,
                )
            ]

            if values:
                return values

            return []

        direct = getattr(
            obj,
            "business_statements",
            None,
        )

        if direct is not None:

            try:
                values = list(
                    direct
                )
            except TypeError:
                values = []

            if values:
                return values

        nested_result = getattr(
            obj,
            "result",
            None,
        )

        if (
            nested_result is not None
            and nested_result is not obj
        ):
            values = (
                cls._find_business_statements(
                    nested_result
                )
            )

            if values:
                return values

        nested_response = getattr(
            obj,
            "knowledge_pipeline_response",
            None,
        )

        if (
            nested_response is not None
            and nested_response is not obj
        ):
            values = (
                cls._find_business_statements(
                    nested_response
                )
            )

            if values:
                return values

        return []

    # =========================================================================
    # STATEMENT ENTITIES
    # =========================================================================

    @classmethod
    def _statement_entities(
        cls,
        statement: Any,
    ) -> list[Any]:
        """
        Return SemanticEntity objects belonging to a BusinessStatement.

        The BusinessStatement is the semantic grouping boundary.
        """

        entities = getattr(
            statement,
            "entities",
            None,
        )

        if entities is not None:

            try:
                values = list(
                    entities
                )
            except TypeError:
                values = []

            if values:
                return values

        # Serialized BusinessStatement compatibility.
        if isinstance(
            statement,
            dict,
        ):

            value = statement.get(
                "entities",
                [],
            )

            if isinstance(
                value,
                (list, tuple),
            ):
                return list(value)

        # If the BusinessStatement was constructed with explicit
        # semantic components but the aggregate list is empty, recover
        # the components without creating new objects.
        values = []

        for name in (
            "action",
            "target",
            "domain",
            "metric",
        ):

            entity = getattr(
                statement,
                name,
                None,
            )

            if entity is not None:
                values.append(
                    entity
                )

        return values

    # =========================================================================
    # REQUIREMENT CLASSIFICATION
    # =========================================================================

    def _requirement_type(
        self,
        entity: Any,
        statement: Any,
    ) -> RequirementType | None:
        """
        Determine requirement type from an existing SemanticEntity.
        """

        metadata = self._metadata(
            entity
        )

        explicit = (
            self._first_text(
                metadata,
                entity,
                "requirement_type",
                "requirement_category",
            )
        )

        if explicit:

            normalized = (
                self._normalize_enum_text(
                    explicit
                )
            )

            for item in RequirementType:

                if normalized in {
                    item.value,
                    item.name.casefold(),
                }:
                    return item

        entity_type = (
            self._entity_type(
                entity
            )
        )

        if entity_type in self.TYPE_BY_ENTITY:
            return self.TYPE_BY_ENTITY[
                entity_type
            ]

        semantic_type = (
            self._first_text(
                self._metadata(statement),
                statement,
                "semantic_type",
                "statement_type",
                "category",
            )
            .casefold()
        )

        if (
            semantic_type
            in {
                "responsibility",
                "responsibilities",
                "task",
                "tasks",
                "contribution",
            }
            and entity_type
            in {
                "action",
                "responsibility",
            }
        ):
            return RequirementType.RESPONSIBILITY

        return None

    # =========================================================================
    # PRIORITY
    # =========================================================================

    def _priority(
        self,
        text: str,
        statement: Any,
    ) -> RequirementPriority:

        metadata = self._metadata(
            statement
        )

        explicit = (
            self._first_text(
                metadata,
                statement,
                "priority",
                "importance",
                "requirement_priority",
            )
            .casefold()
        )

        if explicit in {
            "required",
            "mandatory",
            "essential",
        }:
            return RequirementPriority.REQUIRED

        if explicit in {
            "preferred",
            "desired",
            "desirable",
        }:
            return RequirementPriority.PREFERRED

        if explicit in {
            "contextual",
            "context",
            "informational",
        }:
            return RequirementPriority.CONTEXTUAL

        normalized = (
            text.casefold()
        )

        if any(
            term in normalized
            for term
            in self.REQUIRED_TERMS
        ):
            return RequirementPriority.REQUIRED

        if any(
            term in normalized
            for term
            in self.PREFERRED_TERMS
        ):
            return RequirementPriority.PREFERRED

        return RequirementPriority.CONTEXTUAL

    # =========================================================================
    # ENTITY PRIORITY
    # =========================================================================

    def _priority_from_entity(
        self,
        entity: Any,
    ) -> RequirementPriority:

        metadata = self._metadata(
            entity
        )

        value = (
            self._first_text(
                metadata,
                entity,
                "priority",
                "importance",
                "requirement_priority",
            )
            .casefold()
        )

        if value in {
            "required",
            "mandatory",
            "essential",
        }:
            return RequirementPriority.REQUIRED

        if value in {
            "preferred",
            "desired",
            "desirable",
        }:
            return RequirementPriority.PREFERRED

        return RequirementPriority.CONTEXTUAL

    # =========================================================================
    # EXPERIENCE YEARS
    # =========================================================================

    def _minimum_years(
        self,
        text: str,
        statement: Any,
    ) -> float | None:

        metadata = self._metadata(
            statement
        )

        for key in (
            "minimum_years",
            "years_required",
            "years_experience",
        ):

            value = (
                metadata.get(
                    key
                )
            )

            if value is None:
                value = self._value(
                    statement,
                    key,
                )

            if value is None:
                continue

            try:

                numeric_value = float(
                    value
                )

                if numeric_value >= 0:
                    return numeric_value

            except (
                TypeError,
                ValueError,
            ):
                pass

        match = (
            self.YEARS_PATTERN.search(
                text or ""
            )
        )

        if match:
            return float(
                match.group(1)
            )

        return None

    # =========================================================================
    # EXPERIENCE SUBJECT
    # =========================================================================

    def _experience_subject(
        self,
        statement: Any,
        entities: list[Any],
    ) -> str:
        """
        Resolve the semantic subject of an experience requirement.
        """

        metadata = self._metadata(
            statement
        )

        explicit = (
            self._first_text(
                metadata,
                statement,
                "experience_domain",
                "experience_subject",
                "experience_area",
            )
        )

        if explicit:
            return explicit

        # Prefer a structured domain.
        for entity in entities:

            entity_type = (
                self._entity_type(
                    entity
                )
            )

            if entity_type == "domain":

                subject = (
                    self._entity_subject(
                        entity
                    )
                )

                if subject:
                    return subject

        # Then functional / technology / methodology / skill evidence.
        for entity in entities:

            entity_type = (
                self._entity_type(
                    entity
                )
            )

            if entity_type in {
                "skill",
                "technology",
                "methodology",
                "function",
                "functional_area",
                "job_family",
                "role",
            }:

                subject = (
                    self._entity_subject(
                        entity
                    )
                )

                if subject:
                    return subject

        # Finally use the BusinessStatement semantic target.
        for name in (
            "target",
            "domain",
            "action",
        ):

            entity = getattr(
                statement,
                name,
                None,
            )

            if entity is not None:

                subject = (
                    self._entity_subject(
                        entity
                    )
                )

                if subject:
                    return subject

        statement_text = (
            self._statement_text(
                statement
            )
        )

        # Do not silently return an entire long sentence as an experience
        # subject when a structured subject cannot be established.
        if statement_text:
            return self._clean_experience_text(
                statement_text
            )

        return "professional experience"

    # =========================================================================
    # EXPERIENCE CATEGORY
    # =========================================================================

    def _experience_category(
        self,
        statement: Any,
        entities: list[Any],
    ) -> ExperienceCategory:

        metadata = self._metadata(
            statement
        )

        explicit = self._first_text(
            metadata,
            statement,
            "experience_category",
            "experience_type",
        )

        if explicit:

            normalized = (
                self._normalize_enum_text(
                    explicit
                )
            )

            for category in ExperienceCategory:

                if normalized in {
                    category.value,
                    category.name.casefold(),
                }:
                    return category

        for entity in entities:

            entity_type = (
                self._entity_type(
                    entity
                )
            )

            if entity_type == "domain":
                return ExperienceCategory.DOMAIN

            if entity_type == "technology":
                return ExperienceCategory.TECHNOLOGY

            if entity_type == "methodology":
                return ExperienceCategory.METHODOLOGY

            if entity_type in {
                "function",
                "functional_area",
                "job_family",
                "role",
            }:
                return ExperienceCategory.FUNCTIONAL

            if entity_type in {
                "responsibility",
                "action",
                "task",
            }:
                return ExperienceCategory.RESPONSIBILITY

        return ExperienceCategory.GENERAL

    # =========================================================================
    # EXPERIENCE ENTITY
    # =========================================================================

    @classmethod
    def _experience_entity_id(
        cls,
        entities: list[Any],
    ) -> str:

        for entity in entities:

            entity_type = (
                cls._entity_type(
                    entity
                )
            )

            if entity_type in cls.EXPERIENCE_ENTITY_TYPES:

                entity_id = (
                    cls._entity_id(
                        entity
                    )
                )

                if entity_id:
                    return entity_id

        return ""

    # =========================================================================
    # EXPERIENCE CONFIDENCE
    # =========================================================================

    @classmethod
    def _experience_confidence(
        cls,
        statement: Any,
        entities: list[Any],
    ) -> float:

        statement_confidence = (
            cls._confidence(
                statement,
                0.75,
            )
        )

        entity_confidences = []

        for entity in entities:

            value = (
                cls._value(
                    entity,
                    "confidence",
                )
            )

            try:

                if value is not None:
                    entity_confidences.append(
                        float(value)
                    )

            except (
                TypeError,
                ValueError,
            ):
                pass

        if not entity_confidences:
            return statement_confidence

        entity_confidence = (
            sum(
                entity_confidences
            )
            / len(
                entity_confidences
            )
        )

        return cls._clamp(
            (
                statement_confidence
                + entity_confidence
            )
            / 2.0
        )

    # =========================================================================
    # REQUIREMENT CONSTRUCTION
    # =========================================================================

    def _make_requirement(
        self,
        statement: Any,
        requirement_type: RequirementType,
        priority: RequirementPriority,
        subject: str,
        entity_id: str = "",
        domain: str = "",
        experience_domain: str = "",
        experience_category: ExperienceCategory = (
            ExperienceCategory.UNKNOWN
        ),
        minimum_years: float | None = None,
        confidence: float = 0.0,
    ) -> JDRequirement:

        statement_id = self._text(
            statement,
            "statement_id",
            "id",
        )

        evidence = (
            self._statement_evidence(
                statement
            )
        )

        requirement_id = (
            self._requirement_id(
                statement_id=statement_id,
                entity_id=entity_id,
                requirement_type=(
                    requirement_type
                ),
                subject=subject,
            )
        )

        return JDRequirement(
            requirement_id=requirement_id,

            requirement_type=(
                requirement_type
            ),

            priority=priority,

            subject=subject,

            entity_id=entity_id,

            domain=domain,

            experience_domain=(
                experience_domain
            ),

            experience_category=(
                experience_category
            ),

            evidence=evidence,

            source_statement=evidence,

            confidence=self._clamp(
                confidence
            ),

            mandatory=(
                priority
                == RequirementPriority.REQUIRED
            ),

            preferred=(
                priority
                == RequirementPriority.PREFERRED
            ),

            minimum_years=minimum_years,

            metadata={
                "source": (
                    "document_knowledge_profile"
                ),
                "statement_id": statement_id,
                "statement_type": (
                    type(statement).__name__
                ),
            },
        )

    # =========================================================================
    # DUPLICATE PROTECTION
    # =========================================================================

    @staticmethod
    def _append_unique(
        requirements: list[JDRequirement],
        seen: set[
            tuple[str, str, str]
        ],
        requirement: JDRequirement,
    ) -> None:

        key = (
            requirement.requirement_type.value,

            requirement.subject.casefold(),

            (
                str(
                    requirement.minimum_years
                )
                if requirement.requirement_type
                == RequirementType.EXPERIENCE
                else ""
            ),
        )

        if key in seen:
            return

        seen.add(
            key
        )

        requirements.append(
            requirement
        )

    # =========================================================================
    # REQUIREMENT ID
    # =========================================================================

    @staticmethod
    def _requirement_id(
        statement_id: str,
        entity_id: str,
        requirement_type: RequirementType,
        subject: str,
    ) -> str:

        seed = (
            entity_id
            or statement_id
            or subject
        )

        safe = (
            re.sub(
                r"[^a-z0-9]+",
                "-",
                seed.casefold(),
            )
            .strip("-")
        )

        return (
            f"jdreq:"
            f"{requirement_type.value}:"
            f"{safe or 'unknown'}"
        )

    # =========================================================================
    # PROFILE FALLBACK
    # =========================================================================

    def _classify_profile_fallback(
        self,
        document_profile: DocumentKnowledgeProfile,
        requirements: list[JDRequirement],
        seen: set[
            tuple[str, str, str]
        ],
    ) -> None:
        """
        Last-resort compatibility path.

        This path is used only when the original BusinessStatement objects
        cannot be recovered.

        It consumes serialized profile entities.

        Evidence is still taken from the serialized statement when available.
        """

        profile = getattr(
            document_profile,
            "profile",
            None,
        )

        business_statement_profile = getattr(
            profile,
            "business_statements",
            None,
        )

        statements = getattr(
            business_statement_profile,
            "statements",
            [],
        )

        entity_profile = getattr(
            profile,
            "entities",
            None,
        )

        profile_entities = getattr(
            entity_profile,
            "entities",
            [],
        )

        if not statements:
            return

        # If the serialized BusinessStatement contains its own entities,
        # use them. This is preferable to unrelated profile-wide entities.
        for statement in statements:

            statement_text = (
                self._statement_text(
                    statement
                )
            )

            statement_entities = (
                self._statement_entities(
                    statement
                )
            )

            if not statement_entities:
                statement_entities = (
                    self._match_profile_entities(
                        statement,
                        profile_entities,
                    )
                )

            if not statement_entities:
                continue

            priority = (
                self._priority(
                    statement_text,
                    statement,
                )
            )

            years = (
                self._minimum_years(
                    statement_text,
                    statement,
                )
            )

            experience_subject = ""

            if years is not None:

                experience_subject = (
                    self._experience_subject(
                        statement,
                        statement_entities,
                    )
                )

                experience_category = (
                    self._experience_category(
                        statement,
                        statement_entities,
                    )
                )

                requirement = (
                    self._make_requirement(
                        statement=statement,
                        requirement_type=(
                            RequirementType.EXPERIENCE
                        ),
                        priority=priority,
                        subject=experience_subject,
                        entity_id=(
                            self._experience_entity_id(
                                statement_entities
                            )
                        ),
                        domain=(
                            experience_subject
                            if (
                                experience_category
                                == ExperienceCategory.DOMAIN
                            )
                            else self._first_domain(
                                statement_entities
                            )
                        ),
                        experience_domain=(
                            experience_subject
                        ),
                        experience_category=(
                            experience_category
                        ),
                        minimum_years=years,
                        confidence=(
                            self._experience_confidence(
                                statement,
                                statement_entities,
                            )
                        ),
                    )
                )

                self._append_unique(
                    requirements,
                    seen,
                    requirement,
                )

            for entity in statement_entities:

                requirement_type = (
                    self._requirement_type(
                        entity,
                        statement,
                    )
                )

                if requirement_type is None:
                    continue

                subject = (
                    self._entity_subject(
                        entity
                    )
                )

                if not subject:
                    continue

                if (
                    years is not None
                    and requirement_type
                    == RequirementType.DOMAIN
                    and self._same_subject(
                        subject,
                        experience_subject,
                    )
                ):
                    continue

                requirement = (
                    self._make_requirement(
                        statement=statement,
                        requirement_type=(
                            requirement_type
                        ),
                        priority=priority,
                        subject=subject,
                        entity_id=(
                            self._entity_id(
                                entity
                            )
                        ),
                        domain=(
                            self._entity_domain(
                                entity
                            )
                        ),
                        confidence=(
                            self._entity_confidence(
                                entity,
                                0.60,
                            )
                        ),
                    )
                )

                self._append_unique(
                    requirements,
                    seen,
                    requirement,
                )

    # =========================================================================
    # PROFILE ENTITY MATCHING
    # =========================================================================

    @classmethod
    def _match_profile_entities(
        cls,
        statement: Any,
        profile_entities: Iterable[Any],
    ) -> list[Any]:

        statement_id = cls._text(
            statement,
            "statement_id",
            "id",
        )

        if not statement_id:
            return []

        result = []

        for entity in profile_entities:

            entity_statement_id = (
                cls._text(
                    entity,
                    "statement_id",
                )
            )

            if (
                entity_statement_id
                and entity_statement_id
                == statement_id
            ):
                result.append(
                    entity
                )

        return result

    # =========================================================================
    # SUBJECT COMPARISON
    # =========================================================================

    @staticmethod
    def _same_subject(
        left: str,
        right: str,
    ) -> bool:

        if not left or not right:
            return False

        normalize = (
            lambda value:
            re.sub(
                r"\s+",
                " ",
                value.casefold().strip(),
            )
        )

        return (
            normalize(left)
            == normalize(right)
        )

    # =========================================================================
    # ENTITY SUBJECT
    # =========================================================================

    @classmethod
    def _entity_subject(
        cls,
        entity: Any,
    ) -> str:

        return cls._text(
            entity,
            "canonical",
            "label",
            "normalized",
            "name",
            "original",
            "text",
        )

    # =========================================================================
    # ENTITY ID
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
            "canonical_id",
        )

    # =========================================================================
    # ENTITY TYPE
    # =========================================================================

    @classmethod
    def _entity_type(
        cls,
        entity: Any,
    ) -> str:

        return (
            cls._text(
                entity,
                "entity_type",
                "type",
            )
            .casefold()
        )

    # =========================================================================
    # ENTITY DOMAIN
    # =========================================================================

    @classmethod
    def _entity_domain(
        cls,
        entity: Any,
    ) -> str:

        return cls._text(
            entity,
            "domain",
            "business_area",
            "category",
        )

    # =========================================================================
    # FIRST DOMAIN
    # =========================================================================

    @classmethod
    def _first_domain(
        cls,
        entities: Iterable[Any],
    ) -> str:

        for entity in entities:

            domain = (
                cls._entity_domain(
                    entity
                )
            )

            if domain:
                return domain

        return ""

    # =========================================================================
    # STATEMENT EVIDENCE
    # =========================================================================

    @classmethod
    def _statement_evidence(
        cls,
        statement: Any,
    ) -> str:
        """
        Resolve source evidence.

        Strongest -> weakest:

            source_text
            text
            canonical
            normalized
        """

        return cls._text(
            statement,
            "source_text",
            "text",
            "canonical",
            "normalized",
        )

    # =========================================================================
    # STATEMENT TEXT
    # =========================================================================

    @classmethod
    def _statement_text(
        cls,
        statement: Any,
    ) -> str:

        return cls._text(
            statement,
            "source_text",
            "text",
            "canonical",
            "normalized",
        )

    # =========================================================================
    # METADATA
    # =========================================================================

    @staticmethod
    def _metadata(
        obj: Any,
    ) -> dict[str, Any]:

        if obj is None:
            return {}

        if isinstance(
            obj,
            dict,
        ):

            value = obj.get(
                "metadata",
                {},
            )

        else:

            value = getattr(
                obj,
                "metadata",
                {},
            )

        if isinstance(
            value,
            dict,
        ):
            return value

        return {}

    # =========================================================================
    # FIRST TEXT
    # =========================================================================

    @classmethod
    def _first_text(
        cls,
        metadata: dict[str, Any],
        obj: Any,
        *names: str,
    ) -> str:

        for name in names:

            value = metadata.get(
                name
            )

            if (
                value is not None
                and str(value).strip()
            ):
                return str(
                    value
                ).strip()

            value = cls._value(
                obj,
                name,
            )

            if (
                value is not None
                and str(value).strip()
            ):
                return str(
                    value
                ).strip()

        return ""

    # =========================================================================
    # GENERIC VALUE
    # =========================================================================

    @staticmethod
    def _value(
        obj: Any,
        name: str,
        default: Any = None,
    ) -> Any:

        if obj is None:
            return default

        if isinstance(
            obj,
            dict,
        ):
            return obj.get(
                name,
                default,
            )

        return getattr(
            obj,
            name,
            default,
        )

    # =========================================================================
    # TEXT
    # =========================================================================

    @classmethod
    def _text(
        cls,
        obj: Any,
        *names: str,
    ) -> str:

        for name in names:

            value = cls._value(
                obj,
                name,
            )

            if (
                value is not None
                and str(value).strip()
            ):
                return str(
                    value
                ).strip()

        return ""

    # =========================================================================
    # CONFIDENCE
    # =========================================================================

    @classmethod
    def _confidence(
        cls,
        obj: Any,
        default: float,
    ) -> float:

        value = cls._value(
            obj,
            "confidence",
            default,
        )

        try:

            return cls._clamp(
                float(value)
            )

        except (
            TypeError,
            ValueError,
        ):

            return cls._clamp(
                default
            )

    # =========================================================================
    # ENTITY CONFIDENCE
    # =========================================================================

    @classmethod
    def _entity_confidence(
        cls,
        entity: Any,
        default: float,
    ) -> float:

        return cls._confidence(
            entity,
            default,
        )

    # =========================================================================
    # NORMALIZE ENUM TEXT
    # =========================================================================

    @staticmethod
    def _normalize_enum_text(
        value: str,
    ) -> str:

        return (
            value
            .casefold()
            .replace(
                "-",
                "_",
            )
            .replace(
                " ",
                "_",
            )
            .strip()
        )

    # =========================================================================
    # CLEAN EXPERIENCE TEXT
    # =========================================================================

    @staticmethod
    def _clean_experience_text(
        text: str,
    ) -> str:

        value = re.sub(
            r"\b(?:at\s+least\s+|minimum\s+)?"
            r"\d+(?:\.\d+)?\s*\+?\s*years?\b",
            "",
            text,
            flags=re.IGNORECASE,
        )

        value = re.sub(
            r"\s+",
            " ",
            value,
        ).strip(
            " ,;:-"
        )

        return value or "professional experience"

    # =========================================================================
    # CLAMP
    # =========================================================================

    @staticmethod
    def _clamp(
        value: float,
    ) -> float:

        return round(
            max(
                0.0,
                min(
                    float(value),
                    1.0,
                ),
            ),
            4,
        )


# ============================================================================
# PUBLIC EXPORTS
# ============================================================================


__all__ = [
    "JDRequirementClassifier",
]