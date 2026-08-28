"""
JD Requirement Models
=====================

Enterprise Phase 2
------------------

Structured requirement boundary between:

    DocumentKnowledgeProfile
                |
                v
        JDRequirementClassifier
                |
                v
          JDRequirement
                |
                v
       JDRequirementProfile

Architecture
------------

RequirementType
    = WHAT the JD is asking for.

RequirementPriority
    = HOW important/strict the requirement is.

RequirementClass
    = Backward-compatible alias for older Phase-2 code.

Experience is explicitly scoped by:

    - domain
    - functional area
    - technology
    - methodology
    - responsibility
    - general

This prevents the later matcher from incorrectly treating:

    10 years general labor

as equivalent to:

    5 years Food Safety

The models themselves do not perform extraction, NLP, matching, or ATS
calculation.
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
    Canonical semantic type of a JD requirement.

    This answers:

        "WHAT is being requested?"
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

    LANGUAGE = "language"

    LOCATION = "location"

    WORK_AUTHORIZATION = "work_authorization"

    EMPLOYMENT_TYPE = "employment_type"

    SCHEDULE = "schedule"

    TRAVEL = "travel"

    COMPENSATION = "compensation"

    OTHER = "other"

    UNKNOWN = "unknown"


# ============================================================================
# REQUIREMENT PRIORITY
# ============================================================================


class RequirementPriority(str, Enum):
    """
    Importance / strictness of a requirement.

    REQUIRED
        The JD explicitly requires the item.

    PREFERRED
        The JD explicitly prefers/desires the item but does not make it
        mandatory.

    CONTEXTUAL
        The statement is informative/background/context rather than an
        explicit mandatory or preferred requirement.
    """

    REQUIRED = "required"

    PREFERRED = "preferred"

    CONTEXTUAL = "contextual"


# ============================================================================
# REQUIREMENT CLASS - COMPATIBILITY LAYER
# ============================================================================


class RequirementClass(str, Enum):
    """
    Backward-compatible Phase-2 requirement classification.

    IMPORTANT
    ---------

    Older classifier/test code used the name ``RequirementClass`` for
    requirement priority.

    The canonical model now uses:

        RequirementPriority

    However, removing RequirementClass would break older imports and tests.

    Therefore RequirementClass intentionally represents the SAME semantic
    dimension as RequirementPriority.

    This is NOT the requirement semantic type.

    Example:

        RequirementType.EXPERIENCE
        RequirementPriority.PREFERRED

    may also be viewed through:

        RequirementClass.REQUIRED_PREFERENCE

    for compatibility with older Phase-2 code.
    """

    REQUIRED = "required"

    REQUIRED_PREFERENCE = "preferred"

    CONTEXTUAL = "contextual"

    @classmethod
    def from_priority(
        cls,
        priority: RequirementPriority,
    ) -> "RequirementClass":
        """
        Convert canonical RequirementPriority to compatibility class.
        """

        if not isinstance(
            priority,
            RequirementPriority,
        ):
            raise TypeError(
                "priority must be RequirementPriority."
            )

        if priority == RequirementPriority.REQUIRED:
            return cls.REQUIRED

        if priority == RequirementPriority.PREFERRED:
            return cls.REQUIRED_PREFERENCE

        return cls.CONTEXTUAL

    def to_priority(
        self,
    ) -> RequirementPriority:
        """
        Convert compatibility RequirementClass into canonical priority.
        """

        if self == RequirementClass.REQUIRED:
            return RequirementPriority.REQUIRED

        if self == RequirementClass.REQUIRED_PREFERENCE:
            return RequirementPriority.PREFERRED

        return RequirementPriority.CONTEXTUAL


# ============================================================================
# EXPERIENCE CATEGORY
# ============================================================================


class ExperienceCategory(str, Enum):
    """
    Semantic category of requested experience.

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
            Store Management

    TECHNOLOGY
        Technology/platform experience.

        Examples:
            SAP
            Salesforce

    METHODOLOGY
        Methodology/process experience.

        Examples:
            Lean
            Six Sigma

    RESPONSIBILITY
        Experience performing a responsibility.

        Examples:
            Auditing
            Team Leadership
            Regulatory Compliance

    GENERAL
        Generic experience where no more specific semantic classification
        can safely be established.

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

    This object does not perform extraction.

    It preserves evidence so later matching/analyzing stages can explain
    why the requirement exists.
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    requirement_id: str

    # ------------------------------------------------------------------
    # Canonical classification
    # ------------------------------------------------------------------

    requirement_type: RequirementType

    priority: RequirementPriority

    # ------------------------------------------------------------------
    # Subject
    # ------------------------------------------------------------------

    subject: str

    # ------------------------------------------------------------------
    # Existing knowledge references
    # ------------------------------------------------------------------

    entity_id: str = ""

    domain: str = ""

    # ------------------------------------------------------------------
    # Experience classification
    # ------------------------------------------------------------------

    experience_domain: str = ""

    experience_category: ExperienceCategory = (
        ExperienceCategory.UNKNOWN
    )

    # ------------------------------------------------------------------
    # Evidence
    # ------------------------------------------------------------------

    evidence: str = ""

    source_statement: str = ""

    # ------------------------------------------------------------------
    # Confidence
    # ------------------------------------------------------------------

    confidence: float = 0.0

    # ------------------------------------------------------------------
    # Convenience flags
    # ------------------------------------------------------------------

    mandatory: bool = False

    preferred: bool = False

    # ------------------------------------------------------------------
    # Experience metadata
    # ------------------------------------------------------------------

    minimum_years: Optional[float] = None

    # ------------------------------------------------------------------
    # Additional metadata
    # ------------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # ------------------------------------------------------------------
    # Compatibility property
    # ------------------------------------------------------------------

    @property
    def requirement_class(
        self,
    ) -> RequirementClass:
        """
        Backward-compatible view of priority.

        New code should use:

            requirement.priority

        Older code may continue using:

            requirement.requirement_class
        """

        return RequirementClass.from_priority(
            self.priority
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(
        self,
    ) -> None:
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

        if self.minimum_years is not None:
            try:
                years = float(
                    self.minimum_years
                )
            except (
                TypeError,
                ValueError,
            ) as exc:
                raise ValueError(
                    "JDRequirement.minimum_years "
                    "must be numeric."
                ) from exc

            if years < 0:
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
        # Experience validation
        # --------------------------------------------------------------

        if (
            self.requirement_type
            == RequirementType.EXPERIENCE
        ):
            if not (
                self.experience_domain.strip()
                if isinstance(
                    self.experience_domain,
                    str,
                )
                else False
            ) and not self.subject.strip():
                raise ValueError(
                    "Experience requirements "
                    "must identify an experience domain "
                    "or subject."
                )


# ============================================================================
# JD REQUIREMENT PROFILE
# ============================================================================


@dataclass(frozen=True)
class JDRequirementProfile:
    """
    Structured requirement projection of a Job Description.

    The underlying DocumentKnowledgeProfile remains untouched.

    This profile is the formal Phase-2 output.
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
    # Priority counts
    # ------------------------------------------------------------------

    required_count: int = 0

    preferred_count: int = 0

    contextual_count: int = 0

    # ------------------------------------------------------------------
    # Requirement type counts
    # ------------------------------------------------------------------

    qualification_count: int = 0

    skill_count: int = 0

    experience_count: int = 0

    responsibility_count: int = 0

    # ------------------------------------------------------------------
    # Experience category counts
    # ------------------------------------------------------------------

    domain_experience_count: int = 0

    functional_experience_count: int = 0

    technology_experience_count: int = 0

    methodology_experience_count: int = 0

    responsibility_experience_count: int = 0

    general_experience_count: int = 0

    # ------------------------------------------------------------------
    # Overall confidence
    # ------------------------------------------------------------------

    confidence: float = 0.0

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    @property
    def total_count(
        self,
    ) -> int:
        """
        Return total requirement count.
        """

        return len(
            self.requirements
        )

    @property
    def type_counts(
        self,
    ) -> dict[str, int]:
        """
        Return counts for every RequirementType.
        """

        return {
            item.value: sum(
                requirement.requirement_type == item
                for requirement in self.requirements
            )
            for item in RequirementType
        }

    @property
    def priority_counts(
        self,
    ) -> dict[str, int]:
        """
        Return counts for every RequirementPriority.
        """

        return {
            item.value: sum(
                requirement.priority == item
                for requirement in self.requirements
            )
            for item in RequirementPriority
        }

    @property
    def class_counts(
        self,
    ) -> dict[str, int]:
        """
        Backward-compatible requirement-class counts.

        Preferred requirements are represented using the legacy key:

            "preferred"

        which corresponds to:

            RequirementClass.REQUIRED_PREFERENCE
        """

        return {
            RequirementClass.REQUIRED.value: sum(
                requirement.priority
                == RequirementPriority.REQUIRED
                for requirement in self.requirements
            ),
            RequirementClass.REQUIRED_PREFERENCE.value: sum(
                requirement.priority
                == RequirementPriority.PREFERRED
                for requirement in self.requirements
            ),
            RequirementClass.CONTEXTUAL.value: sum(
                requirement.priority
                == RequirementPriority.CONTEXTUAL
                for requirement in self.requirements
            ),
        }

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(
        self,
    ) -> None:
        """
        Validate all derived counters.
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
            for requirement in requirements
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
            for requirement in requirements
        )

        expected_preferred = sum(
            requirement.priority
            == RequirementPriority.PREFERRED
            for requirement in requirements
        )

        expected_contextual = sum(
            requirement.priority
            == RequirementPriority.CONTEXTUAL
            for requirement in requirements
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
            for requirement in requirements
        )

        expected_skill = sum(
            requirement.requirement_type
            == RequirementType.SKILL
            for requirement in requirements
        )

        expected_experience = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            for requirement in requirements
        )

        expected_responsibility = sum(
            requirement.requirement_type
            == RequirementType.RESPONSIBILITY
            for requirement in requirements
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

        expected_domain = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.DOMAIN
            for requirement in requirements
        )

        expected_functional = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.FUNCTIONAL
            for requirement in requirements
        )

        expected_technology = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.TECHNOLOGY
            for requirement in requirements
        )

        expected_methodology = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.METHODOLOGY
            for requirement in requirements
        )

        expected_responsibility_experience = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.RESPONSIBILITY
            for requirement in requirements
        )

        expected_general = sum(
            requirement.requirement_type
            == RequirementType.EXPERIENCE
            and requirement.experience_category
            == ExperienceCategory.GENERAL
            for requirement in requirements
        )

        if (
            self.domain_experience_count
            != expected_domain
        ):
            raise ValueError(
                "domain_experience_count does not "
                "match requirements."
            )

        if (
            self.functional_experience_count
            != expected_functional
        ):
            raise ValueError(
                "functional_experience_count does not "
                "match requirements."
            )

        if (
            self.technology_experience_count
            != expected_technology
        ):
            raise ValueError(
                "technology_experience_count does not "
                "match requirements."
            )

        if (
            self.methodology_experience_count
            != expected_methodology
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
            != expected_general
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
        requirements: list[JDRequirement]
        | tuple[JDRequirement, ...],
        *,
        metadata: dict[str, Any] | None = None,
    ) -> "JDRequirementProfile":
        """
        Build a complete profile from requirement objects.

        All counters are derived from the actual requirements.
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
                metadata=dict(
                    metadata or {}
                ),
            )

        confidence = (
            sum(
                float(
                    requirement.confidence
                )
                for requirement in items
            )
            / len(items)
        )

        return cls(
            requirements=items,

            required_count=sum(
                requirement.priority
                == RequirementPriority.REQUIRED
                for requirement in items
            ),

            preferred_count=sum(
                requirement.priority
                == RequirementPriority.PREFERRED
                for requirement in items
            ),

            contextual_count=sum(
                requirement.priority
                == RequirementPriority.CONTEXTUAL
                for requirement in items
            ),

            qualification_count=sum(
                requirement.requirement_type
                == RequirementType.QUALIFICATION
                for requirement in items
            ),

            skill_count=sum(
                requirement.requirement_type
                == RequirementType.SKILL
                for requirement in items
            ),

            experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                for requirement in items
            ),

            responsibility_count=sum(
                requirement.requirement_type
                == RequirementType.RESPONSIBILITY
                for requirement in items
            ),

            domain_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.DOMAIN
                for requirement in items
            ),

            functional_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.FUNCTIONAL
                for requirement in items
            ),

            technology_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.TECHNOLOGY
                for requirement in items
            ),

            methodology_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.METHODOLOGY
                for requirement in items
            ),

            responsibility_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.RESPONSIBILITY
                for requirement in items
            ),

            general_experience_count=sum(
                requirement.requirement_type
                == RequirementType.EXPERIENCE
                and requirement.experience_category
                == ExperienceCategory.GENERAL
                for requirement in items
            ),

            confidence=round(
                confidence,
                4,
            ),

            metadata=dict(
                metadata or {}
            ),
        )


# ============================================================================
# PUBLIC EXPORTS
# ============================================================================


__all__ = [
    "RequirementType",
    "RequirementPriority",
    "RequirementClass",
    "ExperienceCategory",
    "JDRequirement",
    "JDRequirementProfile",
]