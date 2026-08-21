"""
Knowledge Match Enricher
========================

Phase 3.2

Object In
----------
KnowledgeMatchResult
+
DocumentKnowledgeProfile
+
JDRequirementProfile

Object Out
-----------
EnrichedKnowledgeMatchResult

The enricher does not replace the Phase 3.1 matcher.

It enriches the already-established matches with structured,
traceable candidate evidence.
"""

from __future__ import annotations

from typing import Any

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
)

from app.intelligence.utilities.knowledge.jd_requirements.requirement_models import (
    JDRequirementProfile,
)

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchResult,
    MatchBasis,
    MatchStatus,
)

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
    EnrichedRequirementMatch,
    MatchEvidence,
)


class KnowledgeMatchEnricher:
    """
    Phase 3.2 evidence enrichment boundary.

    Object In
        KnowledgeMatchResult
        +
        DocumentKnowledgeProfile
        +
        JDRequirementProfile

    Object Out
        EnrichedKnowledgeMatchResult
    """

    def process(
        self,
        match_result: KnowledgeMatchResult,
        resume_profile: DocumentKnowledgeProfile,
        jd_requirement_profile: JDRequirementProfile,
    ) -> EnrichedKnowledgeMatchResult:
        """
        Enrich an existing KnowledgeMatchResult.

        No matching decisions are recalculated here.
        """

        if not isinstance(
            match_result,
            KnowledgeMatchResult,
        ):

            raise TypeError(
                "KnowledgeMatchEnricher.process() "
                "expects KnowledgeMatchResult."
            )

        if not isinstance(
            resume_profile,
            DocumentKnowledgeProfile,
        ):

            raise TypeError(
                "KnowledgeMatchEnricher.process() "
                "expects a DocumentKnowledgeProfile."
            )

        if not isinstance(
            jd_requirement_profile,
            JDRequirementProfile,
        ):

            raise TypeError(
                "KnowledgeMatchEnricher.process() "
                "expects a JDRequirementProfile."
            )

        if not resume_profile.is_resume:

            raise TypeError(
                "KnowledgeMatchEnricher.process() "
                "requires a RESUME profile."
            )

        enriched_matches = []

        for match in match_result.matches:

            evidence = self._collect_evidence(
                match=match,
                resume_profile=resume_profile,
            )

            confidence = self._calculate_confidence(
                match=match,
                evidence=evidence,
            )

            enriched_matches.append(
                EnrichedRequirementMatch(
                    match=match,
                    evidence=tuple(
                        evidence
                    ),
                    evidence_count=len(
                        evidence
                    ),
                    enrichment_confidence=confidence,
                )
            )

        return EnrichedKnowledgeMatchResult.from_matches(
            match_result=match_result,
            matches=enriched_matches,
        )

    # =========================================================================
    # EVIDENCE COLLECTION
    # =========================================================================

    def _collect_evidence(
        self,
        *,
        match: Any,
        resume_profile: DocumentKnowledgeProfile,
    ) -> list[MatchEvidence]:
        """
        Collect evidence from the existing candidate profile.

        Phase 3.2 does not invent evidence.
        """

        evidence: list[MatchEvidence] = []

        if match.status == MatchStatus.UNMATCHED:

            return evidence

        profile = resume_profile.profile

        # --------------------------------------------------------------
        # ENTITY EVIDENCE
        # --------------------------------------------------------------

        if match.basis in (
            MatchBasis.ENTITY_ID,
            MatchBasis.CANONICAL,
        ):

            entities = getattr(
                getattr(
                    profile,
                    "entities",
                    None,
                ),
                "entities",
                [],
            )

            for entity in entities:

                entity_id = getattr(
                    entity,
                    "entity_id",
                    None,
                )

                canonical = getattr(
                    entity,
                    "canonical",
                    "",
                )

                if (
                    entity_id
                    and entity_id
                    in match.candidate_entity_ids
                ):

                    evidence.append(
                        MatchEvidence(
                            source="candidate_entity",
                            evidence=str(
                                canonical
                                or entity_id
                            ),
                            basis=match.basis,
                            candidate_entity_id=(
                                entity_id
                            ),
                            confidence=match.score,
                        )
                    )

        # --------------------------------------------------------------
        # STATEMENT EVIDENCE
        # --------------------------------------------------------------

        if match.basis == MatchBasis.STATEMENT_ENTITY:

            statements = getattr(
                getattr(
                    profile,
                    "business_statements",
                    None,
                ),
                "statements",
                [],
            )

            for statement in statements:

                text = self._statement_text(
                    statement
                )

                if not text:
                    continue

                evidence.append(
                    MatchEvidence(
                        source="business_statement",
                        evidence=text,
                        basis=MatchBasis.STATEMENT_ENTITY,
                        confidence=match.score,
                    )
                )

        # --------------------------------------------------------------
        # DOMAIN EVIDENCE
        # --------------------------------------------------------------

        if match.basis == MatchBasis.DOMAIN:

            domains = getattr(
                getattr(
                    profile,
                    "domains",
                    None,
                ),
                "domains",
                {},
            )

            if isinstance(
                domains,
                dict,
            ):

                for domain, value in domains.items():

                    try:
                        domain_score = float(
                            value
                        )
                    except (
                        TypeError,
                        ValueError,
                    ):

                        domain_score = 0.0

                    if domain_score <= 0:
                        continue

                    evidence.append(
                        MatchEvidence(
                            source="candidate_domain",
                            evidence=str(
                                domain
                            ),
                            basis=MatchBasis.DOMAIN,
                            domain=str(
                                domain
                            ),
                            confidence=min(
                                domain_score,
                                match.score,
                            ),
                        )
                    )

        return self._deduplicate_evidence(
            evidence
        )

    # =========================================================================
    # HELPERS
    # =========================================================================

    @staticmethod
    def _statement_text(
        statement: Any,
    ) -> str:
        """
        Extract statement text without changing the source object.
        """

        if isinstance(
            statement,
            str,
        ):

            return statement.strip()

        for attribute in (
            "statement",
            "text",
            "content",
            "source_statement",
        ):

            value = getattr(
                statement,
                attribute,
                None,
            )

            if isinstance(
                value,
                str,
            ) and value.strip():

                return value.strip()

        return ""

    @staticmethod
    def _deduplicate_evidence(
        evidence: list[MatchEvidence],
    ) -> list[MatchEvidence]:
        """
        Preserve order while removing duplicate evidence.
        """

        result: list[MatchEvidence] = []

        seen: set[
            tuple[
                str,
                str,
                str,
            ]
        ] = set()

        for item in evidence:

            key = (
                item.source,
                item.evidence,
                item.basis.value,
            )

            if key in seen:
                continue

            seen.add(
                key
            )

            result.append(
                item
            )

        return result

    @staticmethod
    def _calculate_confidence(
        *,
        match: Any,
        evidence: list[MatchEvidence],
    ) -> float:
        """
        Calculate enrichment confidence from actual evidence.

        This is NOT an ATS score.

        No evidence means zero enrichment confidence.
        """

        if not evidence:
            return 0.0

        return round(
            sum(
                item.confidence
                for item in evidence
            )
            / len(evidence),
            4,
        )


__all__ = [
    "KnowledgeMatchEnricher",
]