"""
Knowledge Matcher
=================

Phase 3 - Requirement-to-candidate matching.

The matcher compares:

    Resume DocumentKnowledgeProfile
                    +
    JDRequirementProfile
                    |
                    v
            KnowledgeMatcher
                    |
                    v
           KnowledgeMatchResult

The matcher does NOT modify either input.

Matching strategy
-----------------

1. Exact entity_id
2. Exact normalized canonical concept
3. Candidate business-statement entity
4. Compatible domain

The matcher is intentionally conservative.

It does NOT claim that a candidate has a requirement merely because
a vaguely similar word occurs somewhere in the profile.

Later phases can add richer semantic scoring without changing this
contract.
"""

from __future__ import annotations

import re
from typing import Any, Iterable, Optional

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.jd_requirements.requirement_models import (
    JDRequirement,
    JDRequirementProfile,
    RequirementType,
)

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchRequest,
    KnowledgeMatchResult,
    MatchBasis,
    MatchStatus,
    RequirementMatch,
)


class KnowledgeMatcher:
    """
    Match JD requirements against a resume knowledge profile.

    Object In
        KnowledgeMatchRequest

    Object Out
        KnowledgeMatchResult
    """

    # ------------------------------------------------------------------
    # SCORE POLICY
    # ------------------------------------------------------------------

    EXACT_ENTITY_SCORE = 1.0

    EXACT_CANONICAL_SCORE = 0.95

    STATEMENT_ENTITY_SCORE = 0.90

    DOMAIN_SCORE = 0.65

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def process(
        self,
        request: KnowledgeMatchRequest,
    ) -> KnowledgeMatchResult:
        """
        Match all JD requirements against the candidate profile.
        """

        if not isinstance(
            request,
            KnowledgeMatchRequest,
        ):

            raise TypeError(
                "KnowledgeMatcher.process() "
                "expects KnowledgeMatchRequest."
            )

        resume_profile = request.resume_profile

        jd_profile = (
            request.jd_requirement_profile
        )

        self._validate_resume_profile(
            resume_profile
        )

        if not isinstance(
            jd_profile,
            JDRequirementProfile,
        ):

            raise TypeError(
                "KnowledgeMatchRequest.jd_requirement_profile "
                "must be JDRequirementProfile."
            )

        matches: list[
            RequirementMatch
        ] = []

        candidate_entities = (
            self._extract_candidate_entities(
                resume_profile
            )
        )

        candidate_statements = (
            self._extract_candidate_statements(
                resume_profile
            )
        )

        for requirement in (
            jd_profile.requirements
        ):

            matches.append(
                self._match_requirement(
                    requirement=requirement,
                    candidate_entities=candidate_entities,
                    candidate_statements=candidate_statements,
                    resume_profile=resume_profile,
                )
            )

        return KnowledgeMatchResult.from_matches(
            matches
        )

    # =========================================================================
    # VALIDATION
    # =========================================================================

    @staticmethod
    def _validate_resume_profile(
        resume_profile: Any,
    ) -> None:
        """
        Validate the document boundary.

        We intentionally accept the existing wrapper rather than requiring
        a new ResumeKnowledgeProfile class.
        """

        if not isinstance(
            resume_profile,
            DocumentKnowledgeProfile,
        ):

            raise TypeError(
                "KnowledgeMatchRequest.resume_profile "
                "must be DocumentKnowledgeProfile."
            )

        if (
            resume_profile.document_type
            != DocumentType.RESUME
        ):

            raise ValueError(
                "KnowledgeMatcher requires a "
                "RESUME DocumentKnowledgeProfile."
            )

    # =========================================================================
    # REQUIREMENT MATCHING
    # =========================================================================

    def _match_requirement(
        self,
        requirement: JDRequirement,
        candidate_entities: list[Any],
        candidate_statements: list[Any],
        resume_profile: DocumentKnowledgeProfile,
    ) -> RequirementMatch:
        """
        Match one requirement.
        """

        # --------------------------------------------------------------
        # 1. Exact entity identity
        # --------------------------------------------------------------

        entity_matches = self._find_entity_id_matches(
            requirement,
            candidate_entities,
        )

        if entity_matches:

            evidence = self._entity_evidence(
                entity_matches
            )

            return self._build_match(
                requirement= requirement,
                status=MatchStatus.MATCHED,
                score=self.EXACT_ENTITY_SCORE,
                basis=MatchBasis.ENTITY_ID,
                candidate_entities=entity_matches,
                evidence=evidence,
                reason=(
                    "The candidate knowledge profile contains "
                    "the same ontology entity."
                ),
            )

        # --------------------------------------------------------------
        # 2. Exact canonical concept
        # --------------------------------------------------------------

        canonical_matches = (
            self._find_canonical_matches(
                requirement,
                candidate_entities,
            )
        )

        if canonical_matches:

            evidence = self._entity_evidence(
                canonical_matches
            )

            return self._build_match(
                requirement=requirement,
                status=MatchStatus.MATCHED,
                score=self.EXACT_CANONICAL_SCORE,
                basis=MatchBasis.CANONICAL,
                candidate_entities=canonical_matches,
                evidence=evidence,
                reason=(
                    "The candidate contains an "
                    "equivalent canonical concept."
                ),
            )

        # --------------------------------------------------------------
        # 3. Business statement evidence
        # --------------------------------------------------------------

        statement_matches = (
            self._find_statement_matches(
                requirement,
                candidate_statements,
            )
        )

        if statement_matches:

            evidence = tuple(
                self._statement_text(
                    statement
                )
                for statement
                in statement_matches
                if self._statement_text(
                    statement
                )
            )

            return self._build_match(
                requirement=requirement,
                status=MatchStatus.MATCHED,
                score=self.STATEMENT_ENTITY_SCORE,
                basis=MatchBasis.STATEMENT_ENTITY,
                candidate_entities=(
                    self._statement_entity_ids(
                        statement_matches
                    )
                ),
                evidence=evidence,
                reason=(
                    "The requirement concept is supported "
                    "by candidate business-statement evidence."
                ),
            )

        # --------------------------------------------------------------
        # 4. Domain compatibility
        # --------------------------------------------------------------

        domain_match = (
            self._find_domain_match(
                requirement,
                resume_profile,
            )
        )

        if domain_match:

            domain_name = domain_match

            return self._build_match(
                requirement=requirement,
                status=MatchStatus.PARTIAL,
                score=self.DOMAIN_SCORE,
                basis=MatchBasis.DOMAIN,
                candidate_entities=(),
                evidence=(
                    f"Candidate has domain evidence "
                    f"for {domain_name}.",
                ),
                reason=(
                    "The candidate has compatible domain evidence, "
                    "but no direct requirement-level entity evidence."
                ),
            )

        # --------------------------------------------------------------
        # 5. No evidence
        # --------------------------------------------------------------

        return self._build_match(
            requirement=requirement,
            status=MatchStatus.UNMATCHED,
            score=0.0,
            basis=MatchBasis.NONE,
            candidate_entities=(),
            evidence=(),
            reason=(
                "No direct candidate knowledge evidence "
                "was found for this requirement."
            ),
        )

    # =========================================================================
    # ENTITY MATCHING
    # =========================================================================

    @staticmethod
    def _find_entity_id_matches(
        requirement: JDRequirement,
        entities: list[Any],
    ) -> list[Any]:

        requirement_id = (
            str(
                requirement.entity_id
                or ""
            )
            .strip()
            .casefold()
        )

        if not requirement_id:

            return []

        return [
            entity
            for entity
            in entities
            if (
                str(
                    getattr(
                        entity,
                        "entity_id",
                        "",
                    )
                    or ""
                )
                .strip()
                .casefold()
                == requirement_id
            )
        ]

    @classmethod
    def _find_canonical_matches(
        cls,
        requirement: JDRequirement,
        entities: list[Any],
    ) -> list[Any]:

        subject = cls._normalize_text(
            requirement.subject
        )

        if not subject:

            return []

        matches = []

        for entity in entities:

            values = (
                getattr(
                    entity,
                    "canonical",
                    "",
                ),
                getattr(
                    entity,
                    "normalized",
                    "",
                ),
                getattr(
                    entity,
                    "label",
                    "",
                ),
                getattr(
                    entity,
                    "name",
                    "",
                ),
            )

            normalized_values = {
                cls._normalize_text(value)
                for value in values
                if value
            }

            if subject in normalized_values:

                matches.append(
                    entity
                )

        return matches

    # =========================================================================
    # BUSINESS STATEMENT MATCHING
    # =========================================================================

    @classmethod
    def _find_statement_matches(
        cls,
        requirement: JDRequirement,
        statements: list[Any],
    ) -> list[Any]:

        subject = cls._normalize_text(
            requirement.subject
        )

        if not subject:

            return []

        matches = []

        for statement in statements:

            statement_text = (
                cls._normalize_text(
                    cls._statement_text(
                        statement
                    )
                )
            )

            if (
                subject
                and subject in statement_text
            ):

                matches.append(
                    statement
                )
                continue

            entities = getattr(
                statement,
                "entities",
                [],
            ) or []

            for entity in entities:

                entity_values = (
                    getattr(
                        entity,
                        "entity_id",
                        "",
                    ),
                    getattr(
                        entity,
                        "canonical",
                        "",
                    ),
                    getattr(
                        entity,
                        "normalized",
                        "",
                    ),
                    getattr(
                        entity,
                        "label",
                        "",
                    ),
                )

                if any(
                    subject
                    == cls._normalize_text(
                        value
                    )
                    for value
                    in entity_values
                    if value
                ):

                    matches.append(
                        statement
                    )
                    break

        return matches

    # =========================================================================
    # DOMAIN MATCHING
    # =========================================================================

    @classmethod
    def _find_domain_match(
        cls,
        requirement: JDRequirement,
        resume_profile: DocumentKnowledgeProfile,
    ) -> Optional[str]:

        requirement_domain = (
            requirement.domain
            or requirement.experience_domain
        )

        if not requirement_domain:

            return None

        normalized_requirement = (
            cls._normalize_text(
                requirement_domain
            )
        )

        if not normalized_requirement:

            return None

        domains = getattr(
            resume_profile.domains,
            "domains",
            {},
        ) or {}

        business_areas = getattr(
            resume_profile.domains,
            "business_areas",
            {},
        ) or {}

        candidates = list(
            domains.keys()
        ) + list(
            business_areas.keys()
        )

        for candidate in candidates:

            normalized_candidate = (
                cls._normalize_text(
                    candidate
                )
            )

            if (
                normalized_candidate
                == normalized_requirement
            ):

                return str(
                    candidate
                )

        return None

    # =========================================================================
    # EXTRACTION
    # =========================================================================

    @staticmethod
    def _extract_candidate_entities(
        resume_profile: DocumentKnowledgeProfile,
    ) -> list[Any]:
        """
        Extract candidate entities from the existing EntityProfile.

        We use the existing profile boundary rather than modifying
        KnowledgeProfile.
        """

        entities = getattr(
            resume_profile.entities,
            "entities",
            [],
        )

        if entities is None:

            return []

        try:

            return list(
                entities
            )

        except TypeError:

            return []

    @staticmethod
    def _extract_candidate_statements(
        resume_profile: DocumentKnowledgeProfile,
    ) -> list[Any]:

        profile = (
            resume_profile.business_statements
        )

        statements = getattr(
            profile,
            "statements",
            [],
        )

        if statements is None:

            return []

        # BusinessStatementProfile currently stores serialized records.
        try:

            return list(
                statements
            )

        except TypeError:

            return []

    # =========================================================================
    # EVIDENCE
    # =========================================================================

    @staticmethod
    def _entity_evidence(
        entities: Iterable[Any],
    ) -> tuple[str, ...]:

        result = []

        for entity in entities:

            for attribute in (
                "canonical",
                "label",
                "name",
            ):

                value = getattr(
                    entity,
                    attribute,
                    None,
                )

                if value:

                    text = str(
                        value
                    ).strip()

                    if text:

                        result.append(
                            text
                        )
                        break

        return tuple(
            dict.fromkeys(
                result
            )
        )

    @staticmethod
    def _statement_entity_ids(
        statements: Iterable[Any],
    ) -> tuple[str, ...]:

        result = []

        for statement in statements:

            if isinstance(
                statement,
                dict,
            ):

                entity_ids = (
                    statement.get(
                        "entity_ids",
                        [],
                    )
                    or []
                )

                result.extend(
                    str(value)
                    for value
                    in entity_ids
                    if value
                )

            else:

                entities = getattr(
                    statement,
                    "entities",
                    [],
                ) or []

                for entity in entities:

                    entity_id = getattr(
                        entity,
                        "entity_id",
                        None,
                    )

                    if entity_id:

                        result.append(
                            str(
                                entity_id
                            )
                        )

        return tuple(
            dict.fromkeys(
                result
            )
        )

    @staticmethod
    def _statement_text(
        statement: Any,
    ) -> str:

        if isinstance(
            statement,
            dict,
        ):

            for key in (
                "source_text",
                "text",
                "canonical",
                "normalized",
            ):

                value = statement.get(
                    key
                )

                if value:

                    return str(
                        value
                    ).strip()

            return ""

        for attribute in (
            "source_text",
            "text",
            "canonical",
            "normalized",
        ):

            value = getattr(
                statement,
                attribute,
                None,
            )

            if value:

                return str(
                    value
                ).strip()

        return ""

    # =========================================================================
    # MATCH OBJECT
    # =========================================================================

    @staticmethod
    def _build_match(
        requirement: JDRequirement,
        status: MatchStatus,
        score: float,
        basis: MatchBasis,
        candidate_entities: Iterable[Any],
        evidence: Iterable[str],
        reason: str,
    ) -> RequirementMatch:

        entity_ids = []

        for entity in candidate_entities:

            if isinstance(
                entity,
                str,
            ):

                entity_ids.append(
                    entity
                )
                continue

            entity_id = getattr(
                entity,
                "entity_id",
                None,
            )

            if entity_id:

                entity_ids.append(
                    str(
                        entity_id
                    )
                )

        evidence_values = tuple(
            str(value).strip()
            for value
            in evidence
            if value
            and str(value).strip()
        )

        return RequirementMatch(
            requirement_id=(
                requirement.requirement_id
            ),

            requirement_subject=(
                requirement.subject
            ),

            requirement_type=(
                requirement.requirement_type.value
            ),

            priority=(
                requirement.priority.value
            ),

            status=status,

            score=round(
                float(score),
                4,
            ),

            basis=basis,

            candidate_entity_ids=tuple(
                dict.fromkeys(
                    entity_ids
                )
            ),

            candidate_evidence=(
                evidence_values
            ),

            evidence_count=len(
                evidence_values
            ),

            reason=reason,

            metadata={
                "requirement_entity_id": (
                    requirement.entity_id
                ),
                "requirement_domain": (
                    requirement.domain
                ),
                "experience_domain": (
                    requirement.experience_domain
                ),
                "experience_category": (
                    requirement.experience_category.value
                ),
            },
        )

    # =========================================================================
    # NORMALIZATION
    # =========================================================================

    @staticmethod
    def _normalize_text(
        value: Any,
    ) -> str:

        if value is None:

            return ""

        text = str(
            value
        ).casefold().strip()

        if not text:

            return ""

        text = re.sub(
            r"[^a-z0-9]+",
            " ",
            text,
        )

        return re.sub(
            r"\s+",
            " ",
            text,
        ).strip()


__all__ = [
    "KnowledgeMatcher",
]