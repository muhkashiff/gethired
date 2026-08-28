"""
JD Requirement Classifier
=========================

Enterprise Phase 2.

Transforms an existing DocumentKnowledgeProfile into a
JDRequirementProfile.

Architecture:

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
    BusinessStatement
          |
          v
    JDRequirementClassifier
          |
          v
    JDRequirement
          |
          v
    JDRequirementProfile

IMPORTANT
---------

This component does NOT:

    - extract documents
    - rebuild the knowledge graph
    - create semantic entities
    - create business statements
    - perform resume/JD matching
    - calculate ATS scores

RequirementType answers:

    WHAT is requested?

RequirementPriority answers:

    HOW important is it?

Example:

    "5 years of Food Safety experience is required."

        RequirementType = EXPERIENCE
        Priority        = REQUIRED

Example:

    "Industry experience in restaurants is highly preferred."

        RequirementType = EXPERIENCE
        Priority        = PREFERRED
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
    RequirementClass,
    RequirementPriority,
    RequirementType,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    BusinessStatement,
    SemanticEntity,
)

from app.intelligence.utilities.knowledge.jd_requirements.jd_non_ontology_extractor import (
    JDNonOntologyEvidence,
    JDNonOntologyExtractor,
)


# ============================================================================
# CLASSIFIER
# ============================================================================


class JDRequirementClassifier:
    """
    Interpret JD evidence already present in DocumentKnowledgeProfile.
    """

    # =========================================================================
    # EXPERIENCE YEARS
    # =========================================================================

    YEARS_PATTERN = re.compile(
        r"\b"
        r"(?:at\s+least\s+|minimum\s+|over\s+|more\s+than\s+)?"
        r"(\d+(?:\.\d+)?)"
        r"\s*\+?"
        r"\s*years?"
        r"\b",
        re.IGNORECASE,
    )

    # =========================================================================
    # REQUIRED LANGUAGE
    # =========================================================================

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
        "non-negotiable",
        "must-have",
    )

    # =========================================================================
    # PREFERRED LANGUAGE
    # =========================================================================

    PREFERRED_TERMS = (
        "preferred",
        "preferably",
        "preferable",
        "desired",
        "desirable",
        "plus",
        "nice to have",
        "would be an advantage",
        "advantageous",
        "highly prefer",
        "highly preferred",
        "strongly preferred",
        "bonus",
        "an advantage",
        "considered an advantage",
    )

    # =========================================================================
    # PREFERENCE ACTION TERMS
    # =========================================================================

    PREFERENCE_ACTION_TERMS = {
        "prefer",
        "preferred",
        "preferably",
        "preferable",
        "desired",
        "desirable",
        "advantageous",
        "plus",
        "bonus",
    }

    # =========================================================================
    # ENTITY -> REQUIREMENT TYPE
    # =========================================================================

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

        # Semantic actions represent responsibilities.
        "action": RequirementType.RESPONSIBILITY,
        "responsibility": RequirementType.RESPONSIBILITY,
        "task": RequirementType.RESPONSIBILITY,

        # Functional/job-family entities are only emitted as responsibilities
        # when they are not part of a years-of-experience statement.
        "function": RequirementType.RESPONSIBILITY,
        "functional_area": RequirementType.RESPONSIBILITY,
        "job_family": RequirementType.RESPONSIBILITY,
        "role": RequirementType.RESPONSIBILITY,
    }

    # =========================================================================
    # EXPERIENCE ENTITY TYPES
    # =========================================================================

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
    # INITIALIZATION
    # =========================================================================

    def __init__(
        self,
        non_ontology_extractor: JDNonOntologyExtractor | None = None,
    ) -> None:

        self.non_ontology_extractor = (
            non_ontology_extractor
            if non_ontology_extractor is not None
            else JDNonOntologyExtractor()
        )

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def process(
        self,
        document_profile: DocumentKnowledgeProfile,
    ) -> JDRequirementProfile:
        """
        Process one JD DocumentKnowledgeProfile.
        """

        self._validate_document_profile(
            document_profile
        )

        statements = (
            self._extract_business_statements(
                document_profile
            )
        )

        source_text = self._source_text(
            document_profile
        )

        structured_evidence = (
            self.non_ontology_extractor.extract(
                source_text
            )
            if source_text
            else []
        )

        requirements: list[JDRequirement] = []

        seen: set[
            tuple[str, str, str]
        ] = set()

        # =====================================================================
        # PRIMARY BUSINESS-STATEMENT PATH
        # =====================================================================

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

            section_context = (
                self.non_ontology_extractor.context_for_text(
                    statement_text,
                    source_text,
                )
                if source_text
                else None
            )

            priority = self._priority(
                statement_text,
                self._metadata(
                    statement
                ),
            )

            created_for_statement = False
            has_priority_requirement = False

            # --------------------------------------------------------------
            # EXPERIENCE
            # --------------------------------------------------------------

            years = self._minimum_years(
                statement_text,
                statement,
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

                created_for_statement = True
                if requirement.priority == priority:
                    has_priority_requirement = True

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

                created_for_statement = True
                if requirement.priority == priority:
                    has_priority_requirement = True

            # --------------------------------------------------------------
            # FALLBACK: statement has explicit priority but no requirement with that priority
            # --------------------------------------------------------------

            if (
                priority != RequirementPriority.CONTEXTUAL
                and not has_priority_requirement
            ):
                fallback_subject = self._extract_priority_subject(
                    statement_text
                )
                if fallback_subject:
                    fallback_type = self._infer_requirement_type_from_text(
                        fallback_subject
                    )
                    requirement = self._make_requirement(
                        statement=statement,
                        requirement_type=fallback_type,
                        priority=priority,
                        subject=fallback_subject,
                        entity_id="",
                        domain="",
                        confidence=self._clamp(
                            self._confidence(statement, 0.60)
                        ),
                    )
                    self._append_unique(
                        requirements,
                        seen,
                        requirement,
                    )

        # =====================================================================
        # NON-ONTOLOGY REQUIREMENTS
        # =====================================================================

        self._append_non_ontology_requirements(
            structured_evidence=structured_evidence,
            requirements=requirements,
            seen=seen,
        )

        # =====================================================================
        # PROFILE FALLBACK
        # =====================================================================

        if not requirements:

            self._classify_profile_fallback(
                document_profile=document_profile,
                requirements=requirements,
                seen=seen,
            )

        # =====================================================================
        # GLOBAL FALLBACK: scan raw source text for any priority language
        # =====================================================================

        self._extract_priority_requirements_from_text(
            source_text=source_text,
            requirements=requirements,
            seen=seen,
        )

        # =====================================================================
        # METADATA
        # =====================================================================

        type_counts: dict[str, int] = {}

        for requirement in requirements:

            key = (
                requirement.requirement_type.value
            )

            type_counts[key] = (
                type_counts.get(
                    key,
                    0,
                )
                + 1
            )

        priority_counts: dict[str, int] = {}

        for requirement in requirements:

            key = (
                requirement.priority.value
            )

            priority_counts[key] = (
                priority_counts.get(
                    key,
                    0,
                )
                + 1
            )

        non_ontology_counts: dict[str, int] = {}

        for evidence in structured_evidence:

            non_ontology_counts[
                evidence.kind
            ] = (
                non_ontology_counts.get(
                    evidence.kind,
                    0,
                )
                + 1
            )

        return JDRequirementProfile.from_requirements(
            requirements,
            metadata={
                "source": (
                    "jd_requirement_classifier"
                ),
                "non_ontology_evidence_count": (
                    len(
                        structured_evidence
                    )
                ),
                "non_ontology_type_counts": (
                    non_ontology_counts
                ),
                "requirement_type_counts": (
                    type_counts
                ),
                "requirement_priority_counts": (
                    priority_counts
                ),
            },
        )

    # =========================================================================
    # PRIORITY (text first, metadata fallback)
    # =========================================================================

    def _priority(
        self,
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> RequirementPriority:
        """
        Determine requirement priority.

        ORDER:
            1. Explicit required language in the text -> REQUIRED
            2. Explicit preferred language in the text -> PREFERRED
            3. Metadata priority (if provided) -> as mapped
            4. Otherwise -> CONTEXTUAL
        """

        normalized = (
            str(
                text or ""
            )
            .casefold()
            .strip()
        )

        if self._contains_required_language(
            normalized
        ):
            return RequirementPriority.REQUIRED

        if self._contains_preferred_language(
            normalized
        ):
            return RequirementPriority.PREFERRED

        metadata = metadata or {}

        metadata_value = (
            metadata.get(
                "priority"
            )
            or metadata.get(
                "requirement_priority"
            )
            or metadata.get(
                "requirement_class"
            )
            or metadata.get(
                "importance"
            )
        )

        if metadata_value is not None:
            metadata_priority = self._priority_from_value(
                metadata_value
            )
            if metadata_priority is not None:
                return metadata_priority

        return RequirementPriority.CONTEXTUAL

    # =========================================================================
    # PRIORITY VALUE
    # =========================================================================

    @staticmethod
    def _priority_from_value(
        value: Any,
    ) -> RequirementPriority | None:
        """
        Convert arbitrary upstream priority metadata into RequirementPriority.
        """

        if isinstance(
            value,
            RequirementPriority,
        ):
            return value

        if isinstance(
            value,
            RequirementClass,
        ):
            return value.to_priority()

        normalized = (
            str(
                value or ""
            )
            .strip()
            .casefold()
            .replace(
                "-",
                "_",
            )
            .replace(
                " ",
                "_",
            )
        )

        if normalized in {
            "required",
            "mandatory",
            "essential",
            "must",
        }:
            return RequirementPriority.REQUIRED

        if normalized in {
            "preferred",
            "prefer",
            "preferably",
            "preferable",
            "desired",
            "desirable",
            "required_preference",
            "highly_preferred",
            "strongly_preferred",
            "advantageous",
            "plus",
            "bonus",
            "nice_to_have",
        }:
            return RequirementPriority.PREFERRED

        if normalized in {
            "contextual",
            "context",
            "informational",
            "information",
            "background",
        }:
            return RequirementPriority.CONTEXTUAL

        return None

    # =========================================================================
    # REQUIRED LANGUAGE
    # =========================================================================

    def _contains_required_language(
        self,
        text: str,
    ) -> bool:
        """
        Return True when the text contains explicit mandatory language.
        """

        if not text:
            return False

        patterns = (
            r"\brequired\b",
            r"\bmandatory\b",
            r"\bessential\b",
            r"\bmust\b",
            r"\bneed\s+to\b",
            r"\bneeds\s+to\b",
            r"\bshall\b",
            r"\brequired\s+to\b",
            r"\bminimum\b",
            r"\bnon[-\s]?negotiable\b",
            r"\bmust[-\s]?have\b",
        )

        return any(
            re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )
            for pattern in patterns
        )

    # =========================================================================
    # PREFERRED LANGUAGE
    # =========================================================================

    def _contains_preferred_language(
        self,
        text: str,
    ) -> bool:
        """
        Return True when the text contains explicit preferred language.

        Handles:

            preferred
            highly preferred
            strongly preferred
            preferably
            desired
            desirable
            nice to have
            plus
            bonus
            advantage
            advantageous
        """

        if not text:
            return False

        patterns = (
            r"\bpreferred\b",
            r"\bpreferably\b",
            r"\bpreferable\b",
            r"\bhighly\s+preferred\b",
            r"\bstrongly\s+preferred\b",
            r"\bdesired\b",
            r"\bdesirable\b",
            r"\bnice\s+to\s+have\b",
            r"\bwould\s+be\s+an?\s+advantage\b",
            r"\bconsidered\s+an?\s+advantage\b",
            r"\ban?\s+advantage\b",
            r"\badvantageous\b",
            r"\bplus\b",
            r"\bbonus\b",
        )

        return any(
            re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )
            for pattern in patterns
        )

    # =========================================================================
    # REQUIREMENT TYPE
    # =========================================================================

    def _requirement_type(
        self,
        entity: Any,
        statement: Any,
    ) -> RequirementType | None:
        """
        Determine what type of requirement an entity represents.
        """

        if self._is_preference_action(
            entity
        ):
            return None

        entity_type = (
            self._entity_type(
                entity
            )
        )

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

        if entity_type in self.TYPE_BY_ENTITY:
            return self.TYPE_BY_ENTITY[
                entity_type
            ]

        semantic_type = (
            self._first_text(
                self._metadata(
                    statement
                ),
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
    # PREFERENCE ACTION GUARD
    # =========================================================================

    @classmethod
    def _is_preference_action(
        cls,
        entity: Any,
    ) -> bool:
        """
        Prevent semantic action entities such as "Prefer" from becoming
        fake responsibilities.
        """

        entity_type = cls._entity_type(
            entity
        )

        if entity_type not in {
            "action",
            "responsibility",
            "task",
        }:
            return False

        subject = cls._entity_subject(
            entity
        )

        if not subject:
            return False

        normalized = re.sub(
            r"\s+",
            " ",
            subject.casefold().strip(),
        )

        return (
            normalized
            in cls.PREFERENCE_ACTION_TERMS
        )

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

            value = metadata.get(
                key
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

        match = self.YEARS_PATTERN.search(
            text or ""
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

        # Domain is the strongest experience dimension.
        for entity in entities:

            if (
                self._entity_type(
                    entity
                )
                == "domain"
            ):

                subject = (
                    self._entity_subject(
                        entity
                    )
                )

                if subject:
                    return subject

        # Then functional/technical dimensions.
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

        # Statement-level fallback.
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

            if entity_type in (
                cls.EXPERIENCE_ENTITY_TYPES
            ):

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

            value = cls._value(
                entity,
                "confidence",
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
        """
        Construct a JDRequirement using the canonical model contract.
        """

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
                "priority": priority.value,
                "requirement_class": (
                    RequirementClass.from_priority(
                        priority
                    ).value
                ),
            },
        )

    # =========================================================================
    # DUPLICATE PROTECTION / PRIORITY PRESERVATION
    # =========================================================================

    @staticmethod
    def _append_unique(
        requirements: list[JDRequirement],
        seen: set[
            tuple[str, str, str]
        ],
        requirement: JDRequirement,
    ) -> None:
        """
        Append a JDRequirement while preserving the strongest priority.

        Duplicate requirements are identified by:

            requirement_type
            subject
            minimum_years (for EXPERIENCE)

        Priority is intentionally NOT part of the duplicate key.

        If the same requirement is encountered multiple times with different
        priorities, the strongest priority is retained:

            REQUIRED > PREFERRED > CONTEXTUAL
        """

        key = (
            requirement.requirement_type.value,
            requirement.subject.casefold().strip(),
            (
                str(requirement.minimum_years)
                if (
                    requirement.requirement_type
                    == RequirementType.EXPERIENCE
                )
                else ""
            ),
        )

        if key not in seen:
            seen.add(key)
            requirements.append(requirement)
            return

        priority_rank = {
            RequirementPriority.CONTEXTUAL: 0,
            RequirementPriority.PREFERRED: 1,
            RequirementPriority.REQUIRED: 2,
        }

        new_rank = priority_rank.get(
            requirement.priority,
            0,
        )

        for index, existing in enumerate(requirements):

            existing_key = (
                existing.requirement_type.value,
                existing.subject.casefold().strip(),
                (
                    str(existing.minimum_years)
                    if (
                        existing.requirement_type
                        == RequirementType.EXPERIENCE
                    )
                    else ""
                ),
            )

            if existing_key != key:
                continue

            existing_rank = priority_rank.get(
                existing.priority,
                0,
            )

            if new_rank > existing_rank:
                requirements[index] = requirement

            return

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
    # SOURCE TEXT
    # =========================================================================

    @staticmethod
    def _source_text(
        document_profile: DocumentKnowledgeProfile,
    ) -> str:

        source_result = getattr(
            document_profile,
            "source_result",
            None,
        )

        if source_result is None:
            return ""

        for name in (
            "resume_text",
            "jd_text",
            "source_text",
            "text",
        ):

            value = getattr(
                source_result,
                name,
                "",
            )

            if (
                isinstance(
                    value,
                    str,
                )
                and value.strip()
            ):
                return value.strip()

        return ""

    # =========================================================================
    # BUSINESS STATEMENT EXTRACTION
    # =========================================================================

    @classmethod
    def _extract_business_statements(
        cls,
        document_profile: DocumentKnowledgeProfile,
    ) -> list[Any]:
        """
        Retrieve BusinessStatement objects from known pipeline boundaries.
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

    # =========================================================================
    # FIND BUSINESS STATEMENTS
    # =========================================================================

    @classmethod
    def _find_business_statements(
        cls,
        obj: Any,
    ) -> list[Any]:

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
                return list(
                    value
                )

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
    # NON-ONTOLOGY REQUIREMENTS
    # =========================================================================

    def _append_non_ontology_requirements(
        self,
        *,
        structured_evidence: list[
            JDNonOntologyEvidence
        ],
        requirements: list[JDRequirement],
        seen: set[
            tuple[str, str, str]
        ],
    ) -> None:

        if not structured_evidence:
            return

        ontology_evidence = {
            self._normalize_evidence(
                requirement.evidence
            )
            for requirement in requirements
            if requirement.evidence
        }

        for evidence in structured_evidence:

            normalized = (
                self._normalize_evidence(
                    evidence.evidence
                )
            )

            if (
                normalized in ontology_evidence
                and evidence.kind
                not in {
                    "education",
                    "language",
                    "location",
                    "work_authorization",
                    "employment_type",
                    "schedule",
                    "travel",
                    "compensation",
                }
            ):
                continue

            requirement_type = {
                "education": RequirementType.EDUCATION,
                "experience": RequirementType.EXPERIENCE,
                "language": RequirementType.LANGUAGE,
                "location": RequirementType.LOCATION,
                "work_authorization": (
                    RequirementType.WORK_AUTHORIZATION
                ),
                "employment_type": (
                    RequirementType.EMPLOYMENT_TYPE
                ),
                "schedule": RequirementType.SCHEDULE,
                "travel": RequirementType.TRAVEL,
                "compensation": RequirementType.COMPENSATION,
                "certification": RequirementType.CERTIFICATION,
                "responsibility": (
                    RequirementType.RESPONSIBILITY
                ),
                "qualification": (
                    RequirementType.QUALIFICATION
                ),
            }.get(
                evidence.kind,
                RequirementType.OTHER,
            )

            priority = self._priority(
                evidence.evidence,
                {
                    "priority": evidence.priority,
                },
            )

            if evidence.kind in {
                "qualification",
                "certification",
                "experience",
            }:

                subject_norm = (
                    self._normalize_evidence(
                        evidence.subject
                    )
                )

                duplicate = False

                for existing in requirements:

                    if (
                        existing.requirement_type
                        not in {
                            RequirementType.SKILL,
                            RequirementType.TECHNOLOGY,
                            RequirementType.METHODOLOGY,
                            RequirementType.CERTIFICATION,
                            RequirementType.DOMAIN,
                            RequirementType.QUALIFICATION,
                            RequirementType.EXPERIENCE,
                        }
                    ):
                        continue

                    existing_subject = (
                        self._normalize_evidence(
                            existing.subject
                        )
                    )

                    if not subject_norm:
                        continue

                    if (
                        subject_norm
                        == existing_subject
                        or subject_norm
                        in existing_subject
                        or existing_subject
                        in subject_norm
                    ):
                        duplicate = True
                        break

                    target_tokens = set(
                        subject_norm.split()
                    )

                    existing_tokens = set(
                        existing_subject.split()
                    )

                    overlap = (
                        len(
                            target_tokens
                            & existing_tokens
                        )
                        / max(
                            len(
                                target_tokens
                                | existing_tokens
                            ),
                            1,
                        )
                    )

                    if overlap >= 0.65:
                        duplicate = True
                        break

                if duplicate:
                    continue

            if evidence.kind == "responsibility":

                if any(
                    requirement.requirement_type
                    == RequirementType.RESPONSIBILITY
                    and self._normalize_evidence(
                        requirement.evidence
                    )
                    == normalized
                    for requirement in requirements
                ):
                    continue

            experience_category = (
                ExperienceCategory.GENERAL
                if evidence.kind == "experience"
                else ExperienceCategory.UNKNOWN
            )

            requirement = JDRequirement(
                requirement_id=(
                    self._structured_requirement_id(
                        evidence
                    )
                ),

                requirement_type=(
                    requirement_type
                ),

                priority=priority,

                subject=(
                    evidence.subject
                    or evidence.evidence
                ),

                entity_id="",

                domain="",

                experience_domain=(
                    evidence.subject
                    if evidence.kind == "experience"
                    else ""
                ),

                experience_category=(
                    experience_category
                ),

                evidence=(
                    evidence.evidence
                ),

                source_statement=(
                    evidence.evidence
                ),

                confidence=self._clamp(
                    evidence.confidence
                ),

                mandatory=(
                    priority
                    == RequirementPriority.REQUIRED
                ),

                preferred=(
                    priority
                    == RequirementPriority.PREFERRED
                ),

                minimum_years=(
                    evidence.minimum_years
                ),

                metadata={
                    **(
                        evidence.metadata
                        if isinstance(
                            evidence.metadata,
                            dict,
                        )
                        else {}
                    ),
                    "section": (
                        evidence.section
                    ),
                    "line_number": (
                        evidence.line_number
                    ),
                    "evidence_kind": (
                        evidence.kind
                    ),
                    "priority": (
                        priority.value
                    ),
                    "requirement_class": (
                        RequirementClass.from_priority(
                            priority
                        ).value
                    ),
                },
            )

            self._append_unique(
                requirements,
                seen,
                requirement,
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

            if not statement_entities:

                statement_entities = (
                    self._match_profile_entities(
                        statement,
                        profile_entities,
                    )
                )

            priority = self._priority(
                statement_text,
                self._metadata(
                    statement
                ),
            )

            years = (
                self._minimum_years(
                    statement_text,
                    statement,
                )
            )

            experience_subject = ""

            created_for_statement = False
            has_priority_requirement = False

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
                            if experience_category
                            == ExperienceCategory.DOMAIN
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

                created_for_statement = True
                if requirement.priority == priority:
                    has_priority_requirement = True

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

                created_for_statement = True
                if requirement.priority == priority:
                    has_priority_requirement = True

            if (
                priority != RequirementPriority.CONTEXTUAL
                and not has_priority_requirement
            ):
                fallback_subject = self._extract_priority_subject(
                    statement_text
                )
                if fallback_subject:
                    fallback_type = self._infer_requirement_type_from_text(
                        fallback_subject
                    )
                    requirement = self._make_requirement(
                        statement=statement,
                        requirement_type=fallback_type,
                        priority=priority,
                        subject=fallback_subject,
                        entity_id="",
                        domain="",
                        confidence=self._clamp(
                            self._confidence(statement, 0.60)
                        ),
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
    # NORMALIZE ENUM
    # =========================================================================

    @staticmethod
    def _normalize_enum_text(
        value: str,
    ) -> str:

        return (
            str(
                value or ""
            )
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
    # NORMALIZE EVIDENCE
    # =========================================================================

    @staticmethod
    def _normalize_evidence(
        value: str,
    ) -> str:

        return re.sub(
            r"\s+",
            " ",
            re.sub(
                r"[^\w+#]+",
                " ",
                str(
                    value or ""
                ).casefold(),
            ),
        ).strip()

    # =========================================================================
    # STRUCTURED REQUIREMENT ID
    # =========================================================================

    @classmethod
    def _structured_requirement_id(
        cls,
        evidence: JDNonOntologyEvidence,
    ) -> str:

        seed = cls._normalize_evidence(
            evidence.subject
            or evidence.evidence
        )

        seed = (
            re.sub(
                r"[^a-z0-9]+",
                "-",
                seed,
            )
            .strip("-")
            or "unknown"
        )

        return (
            f"jdreq:"
            f"nonontology:"
            f"{evidence.kind}:"
            f"{seed}"
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

        return (
            value
            or "professional experience"
        )

    # =========================================================================
    # EXTRACT SUBJECT FROM PRIORITY STATEMENT
    # =========================================================================

    @classmethod
    def _extract_priority_subject(
        cls,
        text: str,
    ) -> str:
        """
        Remove common priority phrases (required, preferred, etc.) and return
        a cleaned subject.
        """
        if not text:
            return ""

        cleaned = re.sub(
            r"\b(?:is\s+)?(?:highly\s+|strongly\s+)?(?:required|preferred|preferable|desired|desirable|advantageous|mandatory|essential|nice to have|an advantage|considered an advantage|would be an advantage)\b",
            "",
            text,
            flags=re.IGNORECASE,
        )
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" .,;:-")
        return cleaned or text

    # =========================================================================
    # INFER REQUIREMENT TYPE FROM TEXT
    # =========================================================================

    @classmethod
    def _infer_requirement_type_from_text(
        cls,
        text: str,
    ) -> RequirementType:
        """
        Heuristically choose a requirement type based on keywords in the text.
        """
        text_lower = text.casefold()
        if "experience" in text_lower or "years" in text_lower:
            return RequirementType.EXPERIENCE
        if "skill" in text_lower or "ability" in text_lower:
            return RequirementType.SKILL
        if "education" in text_lower or "degree" in text_lower:
            return RequirementType.EDUCATION
        if "certification" in text_lower or "certified" in text_lower:
            return RequirementType.CERTIFICATION
        return RequirementType.QUALIFICATION

    # =========================================================================
    # GLOBAL FALLBACK: scan raw source text for priority sentences
    # =========================================================================

    def _extract_priority_requirements_from_text(
        self,
        source_text: str,
        requirements: list[JDRequirement],
        seen: set,
    ) -> None:
        """
        Ultimate fallback: scan the entire source text for any sentence
        containing explicit priority language and create a requirement.
        This ensures that even if the statement extraction or non-ontology
        extractor missed it, we still capture it.
        """
        if not source_text:
            return

        # Check if we already have at least one REQUIRED and one PREFERRED
        has_required = any(
            req.priority == RequirementPriority.REQUIRED
            for req in requirements
        )
        has_preferred = any(
            req.priority == RequirementPriority.PREFERRED
            for req in requirements
        )

        # If both are already present, no need to scan.
        if has_required and has_preferred:
            return

        # Split into sentences (simple split on period, but keep periods in numbers)
        # We'll use a more robust approach: split on '. ' and handle cases.
        sentences = re.split(r'(?<=[.!?])\s+', source_text)
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Determine priority from text
            priority = self._priority_from_text(sentence)
            if priority == RequirementPriority.CONTEXTUAL:
                continue

            # Skip if we already have this priority and we are not missing it
            if priority == RequirementPriority.REQUIRED and has_required:
                continue
            if priority == RequirementPriority.PREFERRED and has_preferred:
                continue

            # Extract subject
            subject = self._extract_priority_subject(sentence)
            if not subject:
                continue

            # Infer type
            req_type = self._infer_requirement_type_from_text(subject)

            # Create a dummy statement object to satisfy _make_requirement
            # We'll use a simple dict with the required fields.
            dummy_statement = {
                "source_text": sentence,
                "text": sentence,
                "metadata": {},
                "statement_id": f"global_fallback_{hash(sentence)}",
            }

            requirement = self._make_requirement(
                statement=dummy_statement,
                requirement_type=req_type,
                priority=priority,
                subject=subject,
                entity_id="",
                domain="",
                confidence=self._clamp(0.60),
            )

            self._append_unique(requirements, seen, requirement)

            # Update flags after adding
            if priority == RequirementPriority.REQUIRED:
                has_required = True
            elif priority == RequirementPriority.PREFERRED:
                has_preferred = True

            # If we now have both, we can stop scanning
            if has_required and has_preferred:
                break

    # =========================================================================
    # PRIORITY FROM TEXT (direct, no metadata)
    # =========================================================================

    def _priority_from_text(
        self,
        text: str,
    ) -> RequirementPriority:
        """
        Determine priority solely from the text content.
        """
        if not text:
            return RequirementPriority.CONTEXTUAL

        normalized = text.casefold().strip()
        if self._contains_required_language(normalized):
            return RequirementPriority.REQUIRED
        if self._contains_preferred_language(normalized):
            return RequirementPriority.PREFERRED
        return RequirementPriority.CONTEXTUAL

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