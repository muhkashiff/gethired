"""
JD Requirement Classifier Unit Tests
=====================================

Phase 2 - JD-specific interpretation metadata.

These tests verify:

    DocumentKnowledgeProfile
            ↓
    JDRequirementClassifier
            ↓
    JDRequirementProfile

The tests deliberately use lightweight test doubles for the underlying
profile components so that the classifier can be tested independently from
the Enterprise Knowledge Pipeline.

The Enterprise integration test belongs in a separate test file.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile import (
    KnowledgeProfile,
)

from app.intelligence.utilities.knowledge.jd_requirements.requirement_classifier import (
    JDRequirementClassifier,
)

from app.intelligence.utilities.knowledge.jd_requirements.requirement_models import (
    JDRequirement,
    JDRequirementProfile,
    RequirementPriority,
    RequirementType,
)


# ============================================================================
# TEST HELPERS
# ============================================================================


@dataclass
class FakeEntityProfile:
    """
    Minimal entity profile required by DocumentKnowledgeProfile.
    """

    entities: list[dict] = field(
        default_factory=list
    )

    total_entities: int = 0


@dataclass
class FakeBusinessStatementProfile:
    """
    Minimal business statement profile required by DocumentKnowledgeProfile.
    """

    statements: list[dict] = field(
        default_factory=list
    )

    total_statements: int = 0


def make_document_profile(
    *,
    entities: list[dict] | None = None,
    statements: list[dict] | None = None,
    document_type: DocumentType = DocumentType.JD,
) -> DocumentKnowledgeProfile:
    """
    Build a minimal DocumentKnowledgeProfile for isolated tests.

    The real Enterprise KnowledgeProfile is not executed here.
    """

    entities = entities or []

    statements = statements or []

    profile = KnowledgeProfile()

    profile.entities = FakeEntityProfile(
        entities=entities,
        total_entities=len(
            entities
        ),
    )

    profile.business_statements = (
        FakeBusinessStatementProfile(
            statements=statements,
            total_statements=len(
                statements
            ),
        )
    )

    return DocumentKnowledgeProfile(
        document_type=document_type,
        profile=profile,
    )


# ============================================================================
# MODEL TESTS
# ============================================================================


class TestJDRequirementModels:
    """
    Tests for JDRequirement and JDRequirementProfile.
    """

    def test_requirement_can_be_created(self):

        requirement = JDRequirement(
            requirement_id="jdreq:skill:haccp",

            requirement_type=(
                RequirementType.SKILL
            ),

            priority=(
                RequirementPriority.REQUIRED
            ),

            subject="HACCP",

            confidence=0.90,

            mandatory=True,

            preferred=False,
        )

        assert isinstance(
            requirement,
            JDRequirement,
        )

        assert (
            requirement.subject
            == "HACCP"
        )

        assert (
            requirement.priority
            == RequirementPriority.REQUIRED
        )

        assert (
            requirement.requirement_type
            == RequirementType.SKILL
        )

    def test_required_requirement_must_be_mandatory(self):

        with pytest.raises(
            ValueError
        ):

            JDRequirement(
                requirement_id="test",

                requirement_type=(
                    RequirementType.SKILL
                ),

                priority=(
                    RequirementPriority.REQUIRED
                ),

                subject="HACCP",

                confidence=0.90,

                mandatory=False,

                preferred=False,
            )

    def test_preferred_requirement_must_be_preferred(self):

        with pytest.raises(
            ValueError
        ):

            JDRequirement(
                requirement_id="test",

                requirement_type=(
                    RequirementType.SKILL
                ),

                priority=(
                    RequirementPriority.PREFERRED
                ),

                subject="HACCP",

                confidence=0.90,

                mandatory=False,

                preferred=False,
            )

    def test_confidence_must_be_between_zero_and_one(self):

        with pytest.raises(
            ValueError
        ):

            JDRequirement(
                requirement_id="test",

                requirement_type=(
                    RequirementType.SKILL
                ),

                priority=(
                    RequirementPriority.CONTEXTUAL
                ),

                subject="HACCP",

                confidence=1.5,
            )

    def test_requirement_profile_counts_are_derived(self):

        requirements = [

            JDRequirement(
                requirement_id="required-skill",

                requirement_type=(
                    RequirementType.SKILL
                ),

                priority=(
                    RequirementPriority.REQUIRED
                ),

                subject="HACCP",

                confidence=0.90,

                mandatory=True,
            ),

            JDRequirement(
                requirement_id="preferred-domain",

                requirement_type=(
                    RequirementType.DOMAIN
                ),

                priority=(
                    RequirementPriority.PREFERRED
                ),

                subject="Retail",

                confidence=0.80,

                preferred=True,
            ),

            JDRequirement(
                requirement_id="contextual-experience",

                requirement_type=(
                    RequirementType.EXPERIENCE
                ),

                priority=(
                    RequirementPriority.CONTEXTUAL
                ),

                subject="Manufacturing",

                confidence=0.70,

                minimum_years=3,
            ),
        ]

        profile = (
            JDRequirementProfile
            .from_requirements(
                requirements
            )
        )

        assert (
            profile.required_count
            == 1
        )

        assert (
            profile.preferred_count
            == 1
        )

        assert (
            profile.contextual_count
            == 1
        )

        assert (
            profile.skill_count
            == 1
        )

        assert (
            profile.experience_count
            == 1
        )

        assert (
            profile.qualification_count
            == 0
        )

        assert (
            profile.responsibility_count
            == 0
        )

        assert (
            profile.confidence
            == pytest.approx(
                0.80
            )
        )


# ============================================================================
# CLASSIFIER TESTS
# ============================================================================


class TestJDRequirementClassifier:
    """
    Isolated unit tests for JDRequirementClassifier.
    """

    def setup_method(self):

        self.classifier = (
            JDRequirementClassifier()
        )

    # ------------------------------------------------------------------
    # INPUT CONTRACT
    # ------------------------------------------------------------------

    def test_classifier_accepts_jd_profile(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "HACCP certification "
                        "is required."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "skill",

                    "canonical": "HACCP",

                    "confidence": 0.90,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        assert isinstance(
            result,
            JDRequirementProfile,
        )

    def test_classifier_rejects_resume_profile(self):

        profile = make_document_profile(
            document_type=(
                DocumentType.RESUME
            )
        )

        with pytest.raises(
            ValueError
        ):

            self.classifier.process(
                profile
            )

    def test_classifier_rejects_invalid_input(self):

        with pytest.raises(
            TypeError
        ):

            self.classifier.process(
                "not a profile"
            )

    # ------------------------------------------------------------------
    # SKILL
    # ------------------------------------------------------------------

    def test_skill_entity_becomes_skill_requirement(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "HACCP experience "
                        "is required."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "skill",

                    "canonical": "HACCP",

                    "confidence": 0.90,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        assert (
            len(
                result.requirements
            )
            == 1
        )

        requirement = (
            result.requirements[0]
        )

        assert (
            requirement.requirement_type
            == RequirementType.SKILL
        )

        assert (
            requirement.subject
            == "HACCP"
        )

    # ------------------------------------------------------------------
    # TECHNOLOGY
    # ------------------------------------------------------------------

    def test_technology_entity_becomes_technology_requirement(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "SAP experience "
                        "is required."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "technology",

                    "canonical": "SAP",

                    "confidence": 0.88,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        requirement = (
            result.requirements[0]
        )

        assert (
            requirement.requirement_type
            == RequirementType.TECHNOLOGY
        )

        assert (
            requirement.subject
            == "SAP"
        )

    # ------------------------------------------------------------------
    # CERTIFICATION
    # ------------------------------------------------------------------

    def test_certification_entity_becomes_certification_requirement(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "FSSC 22000 "
                        "certification is required."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "certification",

                    "canonical": "FSSC 22000",

                    "confidence": 0.92,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        requirement = (
            result.requirements[0]
        )

        assert (
            requirement.requirement_type
            == RequirementType.CERTIFICATION
        )

        assert (
            requirement.subject
            == "FSSC 22000"
        )

    # ------------------------------------------------------------------
    # DOMAIN
    # ------------------------------------------------------------------

    def test_domain_entity_becomes_domain_requirement(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "Food Safety "
                        "experience is required."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "domain",

                    "canonical": "Food Safety",

                    "confidence": 0.90,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        requirement = (
            result.requirements[0]
        )

        assert (
            requirement.requirement_type
            == RequirementType.DOMAIN
        )

        assert (
            requirement.subject
            == "Food Safety"
        )

    # ------------------------------------------------------------------
    # STANDARD
    # ------------------------------------------------------------------

    def test_standard_entity_becomes_qualification_requirement(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "HACCP standard "
                        "knowledge is required."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "standard",

                    "canonical": "HACCP",

                    "confidence": 0.90,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        requirement = (
            result.requirements[0]
        )

        assert (
            requirement.requirement_type
            == RequirementType.QUALIFICATION
        )

    # ------------------------------------------------------------------
    # REQUIRED PRIORITY
    # ------------------------------------------------------------------

    def test_required_language_creates_required_requirement(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "HACCP certification "
                        "is required."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "certification",

                    "canonical": "HACCP",

                    "confidence": 0.90,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        requirement = (
            result.requirements[0]
        )

        assert (
            requirement.priority
            == RequirementPriority.REQUIRED
        )

        assert (
            requirement.mandatory
            is True
        )

        assert (
            requirement.preferred
            is False
        )

    # ------------------------------------------------------------------
    # PREFERRED PRIORITY
    # ------------------------------------------------------------------

    def test_preferred_language_creates_preferred_requirement(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "Retail experience "
                        "is preferred."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "domain",

                    "canonical": "Retail",

                    "confidence": 0.80,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        requirement = (
            result.requirements[0]
        )

        assert (
            requirement.priority
            == RequirementPriority.PREFERRED
        )

        assert (
            requirement.preferred
            is True
        )

        assert (
            requirement.mandatory
            is False
        )

    # ------------------------------------------------------------------
    # CONTEXTUAL PRIORITY
    # ------------------------------------------------------------------

    def test_unqualified_requirement_is_contextual(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "Experience in "
                        "manufacturing."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "domain",

                    "canonical": "Manufacturing",

                    "confidence": 0.80,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        requirement = (
            result.requirements[0]
        )

        assert (
            requirement.priority
            == RequirementPriority.CONTEXTUAL
        )

    # ------------------------------------------------------------------
    # EXPERIENCE
    # ------------------------------------------------------------------

    def test_experience_requirement_extracts_years(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "Minimum 5 years "
                        "of experience "
                        "in Food Safety."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "domain",

                    "canonical": "Food Safety",

                    "confidence": 0.90,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        experience_requirements = [
            requirement
            for requirement
            in result.requirements
            if (
                requirement.requirement_type
                == RequirementType.EXPERIENCE
            )
        ]

        assert (
            len(
                experience_requirements
            )
            == 1
        )

        requirement = (
            experience_requirements[0]
        )

        assert (
            requirement.minimum_years
            == 5.0
        )

        assert (
            requirement.priority
            == RequirementPriority.REQUIRED
        )

        assert (
            requirement.subject
            == "Food Safety"
        )

    def test_experience_subject_uses_domain_entity(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "5 years of "
                        "experience required."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "domain",

                    "canonical": "Retail",

                    "confidence": 0.85,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        experience = next(
            requirement
            for requirement
            in result.requirements
            if (
                requirement.requirement_type
                == RequirementType.EXPERIENCE
            )
        )

        assert (
            experience.subject
            == "Retail"
        )

        assert (
            experience.minimum_years
            == 5.0
        )

    # ------------------------------------------------------------------
    # EXPERIENCE METADATA
    # ------------------------------------------------------------------

    def test_experience_metadata_takes_precedence(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "Experience "
                        "required."
                    ),

                    "metadata": {
                        "minimum_years": 7,
                    },
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "domain",

                    "canonical": "Food Safety",

                    "confidence": 0.90,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        experience = next(
            requirement
            for requirement
            in result.requirements
            if (
                requirement.requirement_type
                == RequirementType.EXPERIENCE
            )
        )

        assert (
            experience.minimum_years
            == 7.0
        )

    # ------------------------------------------------------------------
    # DUPLICATE PROTECTION
    # ------------------------------------------------------------------

    def test_duplicate_entity_is_not_added_twice(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "HACCP is required."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "skill",

                    "canonical": "HACCP",

                    "confidence": 0.90,
                },

                {
                    "entity_id": "E2",

                    "statement_id": "S1",

                    "entity_type": "skill",

                    "canonical": "HACCP",

                    "confidence": 0.80,
                },
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        haccp_requirements = [
            requirement
            for requirement
            in result.requirements
            if (
                requirement.subject
                == "HACCP"
            )
        ]

        assert (
            len(
                haccp_requirements
            )
            == 1
        )

    # ------------------------------------------------------------------
    # EMPTY PROFILE
    # ------------------------------------------------------------------

    def test_empty_jd_profile_returns_empty_requirement_profile(self):

        profile = make_document_profile()

        result = (
            self.classifier.process(
                profile
            )
        )

        assert isinstance(
            result,
            JDRequirementProfile,
        )

        assert (
            result.requirements
            == ()
        )

        assert (
            result.required_count
            == 0
        )

        assert (
            result.preferred_count
            == 0
        )

        assert (
            result.contextual_count
            == 0
        )

        assert (
            result.confidence
            == 0.0
        )

    # ------------------------------------------------------------------
    # CONFIDENCE
    # ------------------------------------------------------------------

    def test_requirement_confidence_is_clamped(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "HACCP is required."
                    ),
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "skill",

                    "canonical": "HACCP",

                    "confidence": 2.0,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        requirement = (
            result.requirements[0]
        )

        assert (
            0.0
            <= requirement.confidence
            <= 1.0
        )

    # ------------------------------------------------------------------
    # SOURCE EVIDENCE
    # ------------------------------------------------------------------

    def test_requirement_preserves_source_evidence(self):

        source_text = (
            "HACCP certification "
            "is required."
        )

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": source_text,
                }
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "certification",

                    "canonical": "HACCP",

                    "confidence": 0.90,
                }
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        requirement = (
            result.requirements[0]
        )

        assert (
            requirement.evidence
            == source_text
        )

        assert (
            requirement.source_statement
            == source_text
        )

    # ------------------------------------------------------------------
    # MULTIPLE REQUIREMENTS
    # ------------------------------------------------------------------

    def test_multiple_jd_requirements_are_classified(self):

        profile = make_document_profile(
            statements=[
                {
                    "statement_id": "S1",

                    "text": (
                        "Minimum 5 years "
                        "of Food Safety experience "
                        "is required."
                    ),
                },

                {
                    "statement_id": "S2",

                    "text": (
                        "HACCP certification "
                        "is required."
                    ),
                },

                {
                    "statement_id": "S3",

                    "text": (
                        "Retail experience "
                        "is preferred."
                    ),
                },
            ],

            entities=[
                {
                    "entity_id": "E1",

                    "statement_id": "S1",

                    "entity_type": "domain",

                    "canonical": "Food Safety",

                    "confidence": 0.90,
                },

                {
                    "entity_id": "E2",

                    "statement_id": "S2",

                    "entity_type": "certification",

                    "canonical": "HACCP",

                    "confidence": 0.90,
                },

                {
                    "entity_id": "E3",

                    "statement_id": "S3",

                    "entity_type": "domain",

                    "canonical": "Retail",

                    "confidence": 0.80,
                },
            ],
        )

        result = (
            self.classifier.process(
                profile
            )
        )

        assert (
            result.required_count
            == 2
        )

        assert (
            result.preferred_count
            == 1
        )

        assert (
            result.experience_count
            == 1
        )

        assert (
            result.qualification_count
            == 0
        )

        subjects = {
            requirement.subject
            for requirement
            in result.requirements
        }

        assert (
            "Food Safety"
            in subjects
        )

        assert (
            "HACCP"
            in subjects
        )

        assert (
            "Retail"
            in subjects
        )