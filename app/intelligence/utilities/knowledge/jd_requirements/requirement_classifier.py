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
        "highly prefer",
        "highly preferred",
    )

    # ------------------------------------------------------------------
    # PREFERENCE ACTION GUARD
    # ------------------------------------------------------------------
    #
    # Some upstream extraction paths may still produce an "action"
    # SemanticEntity for words such as "prefer", even when those words
    # have been removed from actions.json.
    #
    # These are requirement-priority signals, NOT candidate
    # responsibilities.
    #
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

        source_text = self._source_text(document_profile)
        structured_evidence = self.non_ontology_extractor.extract(
            source_text
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

            section_context = self.non_ontology_extractor.context_for_text(
                statement_text,
                source_text,
            )

            priority = (
                self._priority(
                    statement_text,
                    statement,
                    section_context=section_context,
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
        # NON-ONTOLOGY REQUIREMENTS
        # =================================================================

        self._append_non_ontology_requirements(
            structured_evidence=structured_evidence,
            requirements=requirements,
            seen=seen,
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

        type_counts = {}
        for requirement in requirements:
            key = requirement.requirement_type.value
            type_counts[key] = type_counts.get(key, 0) + 1

        non_ontology_counts = {}
        for evidence in structured_evidence:
            non_ontology_counts[evidence.kind] = (
                non_ontology_counts.get(evidence.kind, 0) + 1
            )

        return (
            JDRequirementProfile.from_requirements(
                requirements,
                metadata={
                    "source": "jd_requirement_classifier",
                    "non_ontology_evidence_count": len(structured_evidence),
                    "non_ontology_type_counts": non_ontology_counts,
                    "requirement_type_counts": type_counts,
                },
            )
        )

    # =========================================================================
    # SOURCE TEXT
    # =========================================================================

    @staticmethod
    def _source_text(document_profile: DocumentKnowledgeProfile) -> str:
        source_result = getattr(document_profile, "source_result", None)
        text = getattr(source_result, "resume_text", "") if source_result is not None else ""
        if isinstance(text, str) and text.strip():
            return text.strip()
        return ""

    # =========================================================================
    # NON-ONTOLOGY REQUIREMENTS
    # =========================================================================

    def _append_non_ontology_requirements(
        self,
        *,
        structured_evidence: list[JDNonOntologyEvidence],
        requirements: list[JDRequirement],
        seen: set[tuple[str, str, str]],
    ) -> None:
        """Add only evidence that the ontology layer cannot safely supply."""
        if not structured_evidence:
            return

        ontology_evidence = {
            self._normalize_evidence(requirement.evidence)
            for requirement in requirements
            if requirement.evidence
        }

        for evidence in structured_evidence:
            normalized = self._normalize_evidence(evidence.evidence)

            # If the exact source sentence already produced an ontology-backed
            # requirement, keep the ontology object as the canonical concept.
            # Education/language/location/etc. are still added when the line has
            # no equivalent requirement type.
            if normalized in ontology_evidence and evidence.kind not in {
                "education",
                "language",
                "location",
                "work_authorization",
                "employment_type",
                "schedule",
                "travel",
                "compensation",
            }:
                continue

            # Generic non-ontology qualification/certification/experience
            # evidence should not duplicate a strong ontology-backed concept
            # from the same source sentence.  Education/language/location and
            # other structural kinds remain additive because they are not
            # reliably represented by ontology JSON.
            if evidence.kind in {"qualification", "certification", "experience"}:
                subject_norm = self._normalize_evidence(evidence.subject)
                target_tokens = set(subject_norm.split())
                duplicate = False
                if target_tokens:
                    for existing in requirements:
                        existing_type = existing.requirement_type.value
                        if existing_type not in {
                            "skill", "technology", "methodology", "certification",
                            "domain", "qualification", "experience",
                        }:
                            continue
                        existing_subject = self._normalize_evidence(existing.subject)
                        existing_tokens = set(existing_subject.split())
                        if subject_norm == existing_subject or subject_norm in existing_subject or existing_subject in subject_norm:
                            duplicate = True
                            break
                        overlap = len(target_tokens & existing_tokens) / max(len(target_tokens | existing_tokens), 1)
                        if overlap >= 0.65:
                            duplicate = True
                            break
                if duplicate:
                    continue

            requirement_type = {
                "education": RequirementType.EDUCATION,
                "experience": RequirementType.EXPERIENCE,
                "language": RequirementType.LANGUAGE,
                "location": RequirementType.LOCATION,
                "work_authorization": RequirementType.WORK_AUTHORIZATION,
                "employment_type": RequirementType.EMPLOYMENT_TYPE,
                "schedule": RequirementType.SCHEDULE,
                "travel": RequirementType.TRAVEL,
                "compensation": RequirementType.COMPENSATION,
                "certification": RequirementType.CERTIFICATION,
                "responsibility": RequirementType.RESPONSIBILITY,
                "qualification": RequirementType.QUALIFICATION,
            }.get(evidence.kind, RequirementType.OTHER)

            # Avoid adding a generic responsibility when ontology extraction
            # already produced an action-backed responsibility from the same
            # sentence.
            if evidence.kind == "responsibility":
                if any(
                    requirement.requirement_type == RequirementType.RESPONSIBILITY
                    and self._normalize_evidence(requirement.evidence) == normalized
                    for requirement in requirements
                ):
                    continue

            requirement = JDRequirement(
                requirement_id=self._structured_requirement_id(evidence),
                requirement_type=requirement_type,
                priority=RequirementPriority(evidence.priority),
                subject=evidence.subject,
                entity_id="",
                domain="",
                experience_domain=(evidence.subject if evidence.kind == "experience" else ""),
                experience_category=(
                    ExperienceCategory.GENERAL
                    if evidence.kind == "experience"
                    else ExperienceCategory.UNKNOWN
                ),
                evidence=evidence.evidence,
                source_statement=evidence.evidence,
                confidence=self._clamp(evidence.confidence),
                mandatory=evidence.priority == "required",
                preferred=evidence.priority == "preferred",
                minimum_years=evidence.minimum_years,
                metadata={
                    **evidence.metadata,
                    "section": evidence.section,
                    "line_number": evidence.line_number,
                    "evidence_kind": evidence.kind,
                },
            )

            self._append_unique(requirements, seen, requirement)

    @staticmethod
    def _normalize_evidence(value: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"[^\w+#]+", " ", str(value or "").casefold())).strip()

    @classmethod
    def _structured_requirement_id(cls, evidence: JDNonOntologyEvidence) -> str:
        seed = cls._normalize_evidence(evidence.subject or evidence.evidence)
        seed = re.sub(r"[^a-z0-9]+", "-", seed).strip("-") or "unknown"
        return f"jdreq:nonontology:{evidence.kind}:{seed}"

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
    # PREFERENCE ACTION GUARD
    # =========================================================================

    @classmethod
    def _is_preference_action(
        cls,
        entity: Any,
    ) -> bool:
        """
        Return True when an action entity is actually a preference/prioritization
        marker rather than a genuine candidate responsibility.

        Example:

            SemanticEntity(
                entity_type="action",
                canonical="Prefer",
            )

        must NOT become:

            RequirementType.RESPONSIBILITY

        because "Prefer" expresses requirement preference, not a job duty.
        """

        entity_type = cls._entity_type(entity)

        if entity_type not in {
            "action",
            "responsibility",
            "task",
        }:
            return False

        subject = cls._entity_subject(entity)

        if not subject:
            return False

        normalized = re.sub(
            r"\s+",
            " ",
            subject.casefold().strip(),
        )

        return normalized in cls.PREFERENCE_ACTION_TERMS

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

            IMPORTANT
            ---------
            Fix A:
            Requirement classification must never be based on a malformed
            action such as "Prefer" being treated as a responsibility.

            The entity type is resolved FIRST and is then used consistently
            throughout this method.
            """

            # ==============================================================
            # 1. RESOLVE ENTITY TYPE FIRST
            # ==============================================================

            entity_type = (
                self._entity_type(
                    entity
                )
            )

            # ==============================================================
            # 2. IGNORE PREFERENCE MARKER AS AN ENTITY REQUIREMENT
            # ==============================================================

            # Words such as "Prefer", "Preferred", "Desired", etc. are
            # priority signals. They are NOT candidate responsibilities.
            #
            # IMPORTANT:
            # We only suppress the malformed semantic ACTION entity here.
            # The containing BusinessStatement is still processed normally.
            #
            # Therefore:
            #
            #     "Industry experience in restaurants is highly preferred."
            #
            # becomes a preferred EXPERIENCE/DOMAIN requirement rather than:
            #
            #     responsibility -> Prefer
            #
            if self._is_preference_action(entity):
                return None
            # ==============================================================
            # 3. EXPLICIT REQUIREMENT TYPE FROM ENTITY METADATA
            # ==============================================================

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

            # ==============================================================
            # 4. ENTITY TYPE MAPPING
            # ==============================================================

            if entity_type in self.TYPE_BY_ENTITY:

                return self.TYPE_BY_ENTITY[
                    entity_type
                ]

            # ==============================================================
            # 5. STATEMENT-LEVEL SEMANTIC TYPE
            # ==============================================================

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

            # ==============================================================
            # 6. NO SAFE CLASSIFICATION
            # ==============================================================

            return None
    # =========================================================================
    # PRIORITY
    # =========================================================================

    def _priority(
        self,
        text: str,
        statement: Any,
            *,
        section_context: Any = None,
        ) -> RequirementPriority:
        """
        Determine the priority/strictness of a JD requirement.

        Priority resolution order:

            1. Explicit non-contextual metadata
            required / mandatory / essential
            preferred / desired / desirable

            2. Explicit priority language in the actual statement text

            3. Explicit contextual metadata

            4. Default CONTEXTUAL

        IMPORTANT
        ---------

        The Enterprise knowledge pipeline may assign a default
        ``contextual`` priority to a BusinessStatement.

        That value must NOT override explicit language in the
        actual JD text.

        Example:

            metadata:
                priority = "contextual"

            text:
                "Industry experience in restaurants is highly preferred."

        Result:

            RequirementPriority.PREFERRED

        This keeps the classifier faithful to the actual JD language.
        """

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
            .strip()
            .casefold()
        )

        normalized = (
            str(text or "")
            .strip()
            .casefold()
        )

        # =====================================================================
        # 1. EXPLICIT NON-CONTEXTUAL METADATA
        # =====================================================================
        #
        # If the upstream pipeline explicitly says REQUIRED or PREFERRED,
        # respect that decision.
        #
        # We deliberately do NOT immediately return CONTEXTUAL here because
        # contextual is often merely the default classification assigned by
        # the upstream semantic layer.
        # =====================================================================

        if explicit in {
            "required",
            "mandatory",
            "essential",
        }:
            return RequirementPriority.REQUIRED

        if explicit in {
            "preferred",
            "preferable",
            "preferably",
            "desired",
            "desirable",
        }:
            return RequirementPriority.PREFERRED

        # =====================================================================
        # 2. ACTUAL JD TEXT
        # =====================================================================
        #
        # Textual language is authoritative when it explicitly communicates
        # requirement strictness.
        #
        # REQUIRED must be checked before PREFERRED so that a sentence such as:
        #
        #     "Preferred candidates must have..."
        #
        # is interpreted according to the stronger explicit requirement.
        #
        # More importantly, a default metadata value of "contextual" must not
        # hide phrases such as:
        #
        #     highly preferred
        #     strongly preferred
        #     must
        #     required
        #     mandatory
        # =====================================================================

        if self._contains_required_language(
            normalized
        ):
            return RequirementPriority.REQUIRED

        if self._contains_preferred_language(
            normalized
        ):
            return RequirementPriority.PREFERRED

        # =====================================================================
        # 3. EXPLICIT CONTEXTUAL METADATA
        # =====================================================================

        if explicit in {
            "contextual",
            "context",
            "informational",
            "information",
            "background",
        }:
            return RequirementPriority.CONTEXTUAL

        # =====================================================================
        # 4. DEFAULT
        # =====================================================================

        return RequirementPriority.CONTEXTUAL


    # =========================================================================
    # PRIORITY LANGUAGE HELPERS
    # =========================================================================

    def _contains_required_language(
        self,
        text: str,
    ) -> bool:
        """
        Return True when the text contains explicit mandatory language.

        Word/phrase matching is used instead of raw substring matching where
        possible so words such as "requirement" do not accidentally behave like
        the phrase "required".
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


    def _contains_preferred_language(
        self,
        text: str,
    ) -> bool:
        """
        Return True when the JD explicitly describes something as preferred.

        Handles normal and strengthened wording such as:

            preferred
            highly preferred
            strongly preferred
            preferably
            desired
            desirable
            nice to have
            plus
            a plus
            advantage
            advantageous
            would be an advantage
            considered an advantage
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