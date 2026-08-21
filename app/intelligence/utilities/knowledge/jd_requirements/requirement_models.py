"""
JD Requirement Models
=====================

Phase 2 - JD-specific interpretation metadata.

These models define the structured requirement boundary between the existing
DocumentKnowledgeProfile and the later matching/analyzing stages.

Architecture:

    Existing Enterprise Knowledge Pipeline
                    |
                    v
        DocumentKnowledgeProfile
                    |
                    v
             JDRequirement
                    |
                    v
          JDRequirementProfile

Important:

    These models do NOT perform extraction, NLP, graph construction, or
    resume/JD matching.

Experience is deliberately modeled as domain-specific evidence.

Example:

    Food Safety
        minimum_years = 5

is NOT equivalent to:

    General Labor
        years = 10

The future KnowledgeMatcher must compare experience by compatible domain,
functional area, or experience category rather than using total career years.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ============================================================================
# REQUIREMENT TYPE
# ============================================================================


class RequirementType(str, Enum):
    """
    Semantic category of a Job Description requirement.
    """

    SKILL = "skill"

    QUALIFICATION = "qualification"

    CERTIFICATION = "certification"

    EXPERIENCE = "experience"

    RESPONSIBILITY = "responsibility"

    DOMAIN = "domain"

    STANDARD = "standard"

    METRIC = "metric"

    EDUCATION = "education"

    TECHNOLOGY = "technology"

    METHODOLOGY = "methodology"

    UNKNOWN = "unknown"


# ============================================================================
# REQUIREMENT PRIORITY
# ============================================================================


class RequirementPriority(str, Enum):
    """
    Importance of a requirement within the Job Description.
    """

    REQUIRED = "required"

    PREFERRED = "preferred"

    CONTEXTUAL = "contextual"


# ============================================================================
# EXPERIENCE CATEGORY
# ============================================================================


class ExperienceCategory(str, Enum):
    """
    Classification of what kind of experience is being requested.

    DOMAIN
        Industry/domain experience.

        Examples:
            Food Safety
            Retail
            Manufacturing

    FUNCTIONAL
        Functional/job-family experience.

        Examples:
            Quality Assurance
            Customer Service
            Supply Chain

    TECHNOLOGY
        Experience specifically tied to a technology/platform.

        Examples:
            SAP
            Salesforce

    METHODOLOGY
        Experience tied to a methodology/process.

        Examples:
            Lean
            Six Sigma

    RESPONSIBILITY
        Experience performing a particular responsibility.

        Examples:
            Auditing
            Team Leadership
            Regulatory Compliance

    GENERAL
        Generic experience where the JD does not provide enough semantic
        information to classify it more specifically.

    UNKNOWN
        Classification could not be established.
    """

    DOMAIN = "domain"

    FUNCTIONAL = "functional"

    TECHNOLOGY = "technology"

    METHODOLOGY = "methodology"

    RESPONSIBILITY = "responsibility"

    GENERAL = "general"

    UNKNOWN = "unknown"


# ============================================================================
# JD REQUIREMENT
# ============================================================================


@dataclass(frozen=True)
class JDRequirement:
    """
    One structured requirement interpreted from an existing JD profile.

    This is an interpretation object.

    It does not perform extraction.

    It preserves evidence from the existing knowledge representation so that
    later stages can explain why a requirement exists.

    Experience requirements are explicitly scoped.

    Example:

        requirement_type = EXPERIENCE
        subject = "Food Safety"
        experience_domain = "Food Safety"
        experience_category = DOMAIN
        minimum_years = 5

    This allows the later matcher to distinguish:

        Food Safety - 5 years

    from:

        General Labor - 10 years
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    requirement_id: str

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    requirement_type: RequirementType

    priority: RequirementPriority

    # ------------------------------------------------------------------
    # Subject
    # ------------------------------------------------------------------

    subject: str

    # ------------------------------------------------------------------
    # Existing Knowledge References
    # ------------------------------------------------------------------

    entity_id: str = ""

    domain: str = ""

    # ------------------------------------------------------------------
    # Experience-Specific Classification
    # ------------------------------------------------------------------

    experience_domain: str = ""

    experience_category: ExperienceCategory = (
        ExperienceCategory.UNKNOWN
    )

    # ------------------------------------------------------------------
    # Evidence / Explainability
    # ------------------------------------------------------------------

    evidence: str = ""

    source_statement: str = ""

    # ------------------------------------------------------------------
    # Confidence
    # ------------------------------------------------------------------

    confidence: float = 0.0

    # ------------------------------------------------------------------
    # Convenience Semantic Flags
    # ------------------------------------------------------------------

    mandatory: bool = False

    preferred: bool = False

    # ------------------------------------------------------------------
    # Experience Metadata
    # ------------------------------------------------------------------

    minimum_years: Optional[float] = None

    # ------------------------------------------------------------------
    # Additional Metadata
    # ------------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Validate the requirement contract.
        """

        if (
            not isinstance(
                self.requirement_id,
                str,
            )
            or not self.requirement_id.strip()
        ):
            raise ValueError(
                "JDRequirement.requirement_id "
                "must be a non-empty string."
            )

        if not isinstance(
            self.requirement_type,
            RequirementType,
        ):
            raise TypeError(
                "JDRequirement.requirement_type "
                "must be RequirementType."
            )

        if not isinstance(
            self.priority,
            RequirementPriority,
        ):
            raise TypeError(
                "JDRequirement.priority "
                "must be RequirementPriority."
            )

        if (
            not isinstance(
                self.subject,
                str,
            )
            or not self.subject.strip()
        ):
            raise ValueError(
                "JDRequirement.subject "
                "must be a non-empty string."
            )

        if not isinstance(
            self.experience_category,
            ExperienceCategory,
        ):
            raise TypeError(
                "JDRequirement.experience_category "
                "must be ExperienceCategory."
            )

        try:

            confidence = float(
                self.confidence
            )

        except (
            TypeError,
            ValueError,
        ) as exc:

            raise ValueError(
                "JDRequirement.confidence "
                "must be numeric."
            ) from exc

        if not 0.0 <= confidence <= 1.0:

            raise ValueError(
                "JDRequirement.confidence "
                "must be between 0 and 1."
            )

        if (
            self.minimum_years is not None
            and float(
                self.minimum_years
            ) < 0
        ):

            raise ValueError(
                "JDRequirement.minimum_years "
                "cannot be negative."
            )

        expected_mandatory = (
            self.priority
            == RequirementPriority.REQUIRED
        )

        expected_preferred = (
            self.priority
            == RequirementPriority.PREFERRED
        )

        if (
            self.mandatory
            != expected_mandatory
        ):

            raise ValueError(
                "JDRequirement.mandatory "
                "must match requirement priority."
            )

        if (
            self.preferred
            != expected_preferred
        ):

            raise ValueError(
                "JDRequirement.preferred "
                "must match requirement priority."
            )

        # --------------------------------------------------------------
        # Experience-specific validation
        # --------------------------------------------------------------

        if (
            self.requirement_type
            == RequirementType.EXPERIENCE
        ):

            if not (
                self.experience_domain
                or self.subject
            ):

                raise ValueError(
                    "Experience requirements "
                    "must identify an experience domain "
                    "or subject."
                )

            if (
                self.minimum_years is not None
                and float(
                    self.minimum_years
                ) < 0
            ):

                raise ValueError(
                    "Experience minimum_years "
                    "cannot be negative."
                )


# ============================================================================
# JD REQUIREMENT PROFILE
# ============================================================================


@dataclass(frozen=True)
class JDRequirementProfile:
    """
    Structured requirement projection of a Job Description.

    The underlying DocumentKnowledgeProfile remains untouched.

    This profile is the formal output of Phase 2 requirement interpretation
    and becomes the input boundary for later matching logic.
    """

    # ------------------------------------------------------------------
    # Requirements
    # ------------------------------------------------------------------

    requirements: tuple[
        JDRequirement,
        ...
    ] = field(
        default_factory=tuple
    )

    # ------------------------------------------------------------------
    # Priority Counts
    # ------------------------------------------------------------------

    required_count: int = 0

    preferred_count: int = 0

    contextual_count: int = 0

    # ------------------------------------------------------------------
    # Requirement Type Counts
    # ------------------------------------------------------------------

    qualification_count: int = 0

    skill_count: int = 0

    experience_count: int = 0

    responsibility_count: int = 0

    # ------------------------------------------------------------------
    # Experience Classification Counts
    # ------------------------------------------------------------------

    domain_experience_count: int = 0

    functional_experience_count: int = 0

    technology_experience_count: int = 0

    methodology_experience_count: int = 0

    responsibility_experience_count: int = 0

    general_experience_count: int = 0

    # ------------------------------------------------------------------
    # Overall Interpretation Confidence
    # ------------------------------------------------------------------

    confidence: float = 0.0

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        """
        Validate all derived counters against the actual requirements.
        """

        requirements = tuple(
            self.requirements
        )

        object.__setattr__(
            self,
            "requirements",
            requirements,
        )

        if any(
            not isinstance(
                requirement,
                JDRequirement,
            )
            for requirement
            in requirements
        ):

            raise TypeError(
                "JDRequirementProfile.requirements "
                "must contain only JDRequirement objects."
            )

        # --------------------------------------------------------------
        # Priority counts
        # --------------------------------------------------------------

        expected_required = sum(
            requirement.priority
            == RequirementPriority.REQUIRED
            for requirement
            in requirements
        )

        expected_preferred = sum(
            requirement.priority
            == RequirementPriority.PREFERRED
            for requirement
            in requirements
        )

        expected_contextual = sum(
            requirement.priority
            == RequirementPriority.CONTEXTUAL
            for requirement
            in requirements
        )

        if (
            self.required_count
            != expected_required
        ):

            raise ValueError(
                "required_count does not "
                "match requirements."
            )

        if (
            self.preferred_count
            != expected_preferred
        ):

            raise ValueError(
                "preferred_count does not "
                "match requirements."
            )

        if (
            self.contextual_count
            != expected_contextual
        ):

            raise ValueError(
                "contextual_count does not "
                "match requirements."
            )

        # --------------------------------------------------------------
        # Requirement type counts
        # --------------------------------------------------------------

        expected_qualification = sum(
            requirement.requirement_type
            == RequirementType.QUALIFICATION
            for requirement
            in requirements
        )

        expected_skill = sum(
            requirement.requirement_type
            == RequirementType.SKILL
            for requirement
            in requirements
        )

        expected_experience = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            for requirement
            in requirements
        )

        expected_responsibility = sum(
            requirement.requirement_type
            == RequirementType.RESPONSIBILITY
            for requirement
            in requirements
        )

        if (
            self.qualification_count
            != expected_qualification
        ):

            raise ValueError(
                "qualification_count does not "
                "match requirements."
            )

        if (
            self.skill_count
            != expected_skill
        ):

            raise ValueError(
                "skill_count does not "
                "match requirements."
            )

        if (
            self.experience_count
            != expected_experience
        ):

            raise ValueError(
                "experience_count does not "
                "match requirements."
            )

        if (
            self.responsibility_count
            != expected_responsibility
        ):

            raise ValueError(
                "responsibility_count does not "
                "match requirements."
            )

        # --------------------------------------------------------------
        # Experience category counts
        # --------------------------------------------------------------

        expected_domain_experience = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.DOMAIN
            for requirement
            in requirements
        )

        expected_functional_experience = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.FUNCTIONAL
            for requirement
            in requirements
        )

        expected_technology_experience = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.TECHNOLOGY
            for requirement
            in requirements
        )

        expected_methodology_experience = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.METHODOLOGY
            for requirement
            in requirements
        )

        expected_responsibility_experience = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.RESPONSIBILITY
            for requirement
            in requirements
        )

        expected_general_experience = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.GENERAL
            for requirement
            in requirements
        )

        if (
            self.domain_experience_count
            != expected_domain_experience
        ):

            raise ValueError(
                "domain_experience_count does not "
                "match requirements."
            )

        if (
            self.functional_experience_count
            != expected_functional_experience
        ):

            raise ValueError(
                "functional_experience_count does not "
                "match requirements."
            )

        if (
            self.technology_experience_count
            != expected_technology_experience
        ):

            raise ValueError(
                "technology_experience_count does not "
                "match requirements."
            )

        if (
            self.methodology_experience_count
            != expected_methodology_experience
        ):

            raise ValueError(
                "methodology_experience_count does not "
                "match requirements."
            )

        if (
            self.responsibility_experience_count
            != expected_responsibility_experience
        ):

            raise ValueError(
                "responsibility_experience_count does not "
                "match requirements."
            )

        if (
            self.general_experience_count
            != expected_general_experience
        ):

            raise ValueError(
                "general_experience_count does not "
                "match requirements."
            )

        # --------------------------------------------------------------
        # Confidence
        # --------------------------------------------------------------

        try:

            confidence = float(
                self.confidence
            )

        except (
            TypeError,
            ValueError,
        ) as exc:

            raise ValueError(
                "JDRequirementProfile.confidence "
                "must be numeric."
            ) from exc

        if not 0.0 <= confidence <= 1.0:

            raise ValueError(
                "JDRequirementProfile.confidence "
                "must be between 0 and 1."
            )

    # =========================================================================
    # FACTORY
    # =========================================================================

    @classmethod
    def from_requirements(
        cls,
        requirements: list[JDRequirement],
    ) -> "JDRequirementProfile":
        """
        Build a complete profile from requirement objects.

        All summary counters are derived here rather than maintained manually.
        """

        items = tuple(
            requirements
        )

        if not items:

            return cls(
                requirements=(),

                required_count=0,

                preferred_count=0,

                contextual_count=0,

                qualification_count=0,

                skill_count=0,

                experience_count=0,

                responsibility_count=0,

                domain_experience_count=0,

                functional_experience_count=0,

                technology_experience_count=0,

                methodology_experience_count=0,

                responsibility_experience_count=0,

                general_experience_count=0,

                confidence=0.0,
            )

        confidence = (
            sum(
                requirement.confidence
                for requirement
                in items
            )
            / len(items)
        )

        return cls(
            requirements=items,

            required_count=sum(
                requirement.priority
                == RequirementPriority.REQUIRED
                for requirement
                in items
            ),

            preferred_count=sum(
                requirement.priority
                == RequirementPriority.PREFERRED
                for requirement
                in items
            ),

            contextual_count=sum(
                requirement.priority
                == RequirementPriority.CONTEXTUAL
                for requirement
                in items
            ),

            qualification_count=sum(
                requirement.requirement_type
                == RequirementType.QUALIFICATION
                for requirement
                in items
            ),

            skill_count=sum(
                requirement.requirement_type
                == RequirementType.SKILL
                for requirement
                in items
            ),

            experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                for requirement
                in items
            ),

            responsibility_count=sum(
                requirement.requirement_type
                == RequirementType.RESPONSIBILITY
                for requirement
                in items
            ),

            domain_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.DOMAIN
                for requirement
                in items
            ),

            functional_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.FUNCTIONAL
                for requirement
                in items
            ),

            technology_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.TECHNOLOGY
                for requirement
                in items
            ),

            methodology_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.METHODOLOGY
                for requirement
                in items
            ),

            responsibility_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.RESPONSIBILITY
                for requirement
                in items
            ),

            general_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.GENERAL
                for requirement
                in items
            ),

            confidence=round(
                confidence,
                4,
            ),
        )


# ============================================================================
# PUBLIC EXPORTS
# ============================================================================


__all__ = [
    "RequirementType",
    "RequirementPriority",
    "ExperienceCategory",
    "JDRequirement",
    "JDRequirementProfile",
]