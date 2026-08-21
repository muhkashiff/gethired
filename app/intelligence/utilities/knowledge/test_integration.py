"""
Project Pipeline Integration Tests

Enterprise V13
==============================

Purpose
-------

This test file validates the real project-level object flow.

The project pipeline is intentionally tested as an integration boundary:

    DocumentInput
        ↓
    ProjectPipeline
        ↓
    RoutedDocument
        ↓
    KnowledgePipelineRequest
        ↓
    Enterprise Knowledge Pipeline
        ↓
    KnowledgePipelineResponse
        ↓
    KnowledgeProfile
        ↓
    DocumentKnowledgeProfile
        ↓
    JD Requirement Classifier
        ↓
    JDRequirementProfile

Important
---------

These tests intentionally PRINT ACTUAL OBJECTS.

The purpose is not merely:

    PASSED

The purpose is to inspect what objects are actually moving
through the system.

No production objects are mocked.

No KnowledgeProfile is manually constructed.

No JDRequirementProfile is manually constructed.

The real Enterprise pipeline is used.
"""

from __future__ import annotations

from pprint import pformat
from typing import Any

import pytest


# ============================================================================
# PROJECT PIPELINE IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline import (
    ProjectPipeline,
    ProjectPipelineResult,
    DocumentInput,
    DocumentType,
)


# ============================================================================
# PHASE 2 IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.jd_requirements.requirement_classifier import (
    JDRequirementProfile,
)


# ============================================================================
# TEST DOCUMENTS
# ============================================================================


RESUME_TEXT = """
John Smith

Quality Assurance and Food Safety professional with experience in
food manufacturing, retail operations, quality control, and customer
service.

Professional Experience

Quality Assurance Supervisor
ABC Foods
2019 - 2024

Led food safety and quality assurance activities across manufacturing
operations. Managed HACCP implementation, internal audits, corrective
actions, supplier quality, and regulatory compliance.

Reduced product defects by 28 percent through process improvement
and preventive quality controls.

Trained and supervised a team of 12 quality employees.

Quality Inspector
XYZ Manufacturing
2016 - 2019

Performed quality inspections, documentation, sampling, and corrective
action follow-up.

Retail Associate
Retail Company
2014 - 2016

Provided customer service, handled inventory, supported retail
operations, and resolved customer issues.
"""


JD_TEXT = """
Quality Assurance Lead

We are seeking a Quality Assurance Lead to oversee food safety and
quality operations.

Requirements:

Minimum 5 years of Food Safety experience is required.

At least 3 years of experience in food manufacturing is required.

HACCP certification is required.

Bachelor's degree in Food Science or a related field is required.

Strong quality assurance and auditing skills are required.

Experience in retail operations is preferred.

Experience in customer service is preferred.

The successful candidate will lead quality improvement initiatives,
manage corrective actions, support regulatory compliance, and supervise
quality personnel.
"""


# ============================================================================
# PRINT HELPERS
# ============================================================================


def print_separator(
    title: str,
    width: int = 100,
) -> None:
    """
    Print a clearly visible diagnostic section.
    """

    print()
    print("=" * width)
    print(title)
    print("=" * width)


def print_checkpoint(
    title: str,
    value: Any,
) -> None:
    """
    Print an actual pipeline object.

    repr() is attempted first because many enterprise models
    provide diagnostic __repr__ implementations.

    If repr() itself fails, print the type and __dict__ instead.
    """

    print_separator(
        title
    )

    print(
        "TYPE:"
    )

    print(
        type(value)
    )

    print(
        "\nOBJECT:"
    )

    try:

        print(
            pformat(
                value,
                width=120,
                sort_dicts=False,
            )
        )

    except Exception as exc:

        print(
            "[repr FAILED]"
        )

        print(
            "Exception:",
            repr(exc),
        )

        print(
            "\nRAW __dict__:"
        )

        try:

            print(
                pformat(
                    getattr(
                        value,
                        "__dict__",
                        {},
                    ),
                    width=120,
                    sort_dicts=False,
                )
            )

        except Exception as dict_exc:

            print(
                "[__dict__ FAILED]",
                repr(dict_exc),
            )


def print_attribute(
    object_name: str,
    obj: Any,
    attribute: str,
) -> Any:
    """
    Safely print one attribute.

    Returns the actual value.
    """

    try:

        value = getattr(
            obj,
            attribute,
        )

    except Exception as exc:

        print(
            f"{object_name}.{attribute}: "
            f"[ERROR] {exc!r}"
        )

        return None

    print(
        f"{object_name}.{attribute}:"
    )

    print(
        pformat(
            value,
            width=120,
            sort_dicts=False,
        )
    )

    return value


# ============================================================================
# KNOWLEDGE DOCUMENT DIAGNOSTICS
# ============================================================================


def print_knowledge_document_debug(
    document: Any,
) -> None:
    """
    Deep diagnostic dump for KnowledgeDocument.
    """

    print_separator(
        "KNOWLEDGE DOCUMENT DEEP DEBUG"
    )

    print(
        "TYPE:",
        type(document),
    )

    print(
        "\nRAW OBJECT:"
    )

    try:

        print(
            pformat(
                document,
                width=120,
                sort_dicts=False,
            )
        )

    except Exception as exc:

        print(
            "repr failed:",
            repr(exc),
        )

    print_separator(
        "KNOWLEDGE DOCUMENT ATTRIBUTES"
    )

    attributes = [
        "sentences",
        "facts",
        "statistics",
        "confidence",
        "raw_text",
        "source",
        "parsed",
        "entities",
        "entity_count",
        "semantic_entity_count",
        "facts_with_interpretation",
        "facts_with_entities",
        "sentence_count",
        "fact_count",
    ]

    for attribute in attributes:

        print_attribute(
            "KnowledgeDocument",
            document,
            attribute,
        )

    facts = getattr(
        document,
        "facts",
        [],
    )

    print_separator(
        f"KNOWLEDGE FACTS ({len(facts)})"
    )

    for index, fact in enumerate(
        facts,
        start=1,
    ):

        print(
            f"\n--- FACT {index} ---"
        )

        print(
            "TYPE:",
            type(fact),
        )

        print(
            "repr:"
        )

        try:

            print(
                pformat(
                    fact,
                    width=120,
                    sort_dicts=False,
                )
            )

        except Exception as exc:

            print(
                "repr FAILED:",
                repr(exc),
            )

        for attribute in [
            "fact_id",
            "text",
            "source",
            "achievement",
            "quantified",
            "confidence",
            "sentence_index",
            "fact_index",
            "metadata",
            "interpretation",
            "semantic_entities",
            "semantic_entity_count",
            "has_semantic_entities",
        ]:

            print_attribute(
                f"Fact[{index}]",
                fact,
                attribute,
            )

        interpretation = getattr(
            fact,
            "interpretation",
            None,
        )

        if interpretation is None:
            continue

        print_separator(
            f"INTERPRETATION FOR FACT {index}",
            width=80,
        )

        print(
            "TYPE:",
            type(interpretation),
        )

        for attribute in [
            "entities",
            "semantic_entities",
            "entity_count",
            "semantic_entity_count",
            "has_entities",
            "has_semantic_entities",
            "achievement",
            "quantified",
            "semantic_type",
            "business_area",
            "primary_domain",
            "confidence",
            "overall_impact_weight",
            "explanation",
        ]:

            print_attribute(
                f"Fact[{index}].Interpretation",
                interpretation,
                attribute,
            )


# ============================================================================
# DOCUMENT KNOWLEDGE PROFILE DIAGNOSTICS
# ============================================================================


def print_profile_contents(
    result: ProjectPipelineResult,
) -> None:
    """
    Print DocumentKnowledgeProfile and its important components.
    """

    profile = (
        result.document_profile
    )

    print_separator(
        "DOCUMENT KNOWLEDGE PROFILE"
    )

    print(
        "TYPE:",
        type(profile),
    )

    try:

        print(
            pformat(
                profile,
                width=120,
                sort_dicts=False,
            )
        )

    except Exception as exc:

        print(
            "repr FAILED:",
            repr(exc),
        )

    print_separator(
        "DOCUMENT PROFILE ATTRIBUTES"
    )

    attributes = [
        "document_type",
        "is_resume",
        "is_jd",
        "knowledge_profile",
        "jd_requirement_profile",
        "metadata",
    ]

    for attribute in attributes:

        print_attribute(
            "DocumentKnowledgeProfile",
            profile,
            attribute,
        )

    knowledge_profile = getattr(
        profile,
        "knowledge_profile",
        None,
    )

    if knowledge_profile is not None:

        print_separator(
            "KNOWLEDGE PROFILE"
        )

        print(
            "TYPE:",
            type(knowledge_profile),
        )

        try:

            print(
                pformat(
                    knowledge_profile,
                    width=120,
                    sort_dicts=False,
                )
            )

        except Exception as exc:

            print(
                "repr FAILED:",
                repr(exc),
            )


# ============================================================================
# JD REQUIREMENT DIAGNOSTICS
# ============================================================================


def print_jd_requirements(
    result: ProjectPipelineResult,
) -> None:
    """
    Print the complete JDRequirementProfile and every
    individual requirement.

    This is deliberately verbose because this test is being
    used as an integration diagnostic.
    """

    print_separator(
        "JD REQUIREMENT PROFILE"
    )

    profile = (
        result.jd_requirement_profile
    )

    print(
        "TYPE:",
        type(profile),
    )

    print(
        "\nPROFILE:"
    )

    try:

        print(
            pformat(
                profile,
                width=120,
                sort_dicts=False,
            )
        )

    except Exception as exc:

        print(
            "PROFILE repr FAILED:",
            repr(exc),
        )

    if profile is None:

        print(
            "\nJD REQUIREMENT PROFILE IS NONE"
        )

        return

    print_separator(
        "JD REQUIREMENT PROFILE COUNTS",
        width=80,
    )

    for attribute in [
        "required_count",
        "preferred_count",
        "contextual_count",
        "qualification_count",
        "skill_count",
        "experience_count",
        "responsibility_count",
        "confidence",
    ]:

        print_attribute(
            "JDRequirementProfile",
            profile,
            attribute,
        )

    requirements = getattr(
        profile,
        "requirements",
        [],
    )

    print_separator(
        f"INDIVIDUAL JD REQUIREMENTS ({len(requirements)})"
    )

    for index, requirement in enumerate(
        requirements,
        start=1,
    ):

        print()
        print(
            "-" * 90
        )

        print(
            f"REQUIREMENT #{index}"
        )

        print(
            "-" * 90
        )

        print(
            "TYPE:",
            type(requirement),
        )

        print(
            "\nRAW OBJECT:"
        )

        try:

            print(
                pformat(
                    requirement,
                    width=120,
                    sort_dicts=False,
                )
            )

        except Exception as exc:

            print(
                "repr FAILED:",
                repr(exc),
            )

        for attribute in [
            "requirement_id",
            "requirement_type",
            "priority",
            "subject",
            "entity_id",
            "domain",
            "evidence",
            "source_statement",
            "confidence",
            "mandatory",
            "preferred",
            "minimum_years",
            "metadata",
        ]:

            print_attribute(
                f"Requirement[{index}]",
                requirement,
                attribute,
            )


# ============================================================================
# REQUIREMENT EVIDENCE AUDIT
# ============================================================================


def audit_requirement_evidence(
    result: ProjectPipelineResult,
) -> list[Any]:
    """
    Identify requirements whose evidence/source statement is missing.

    Returns a list of problematic requirements.
    """

    profile = (
        result.jd_requirement_profile
    )

    requirements = getattr(
        profile,
        "requirements",
        [],
    )

    print_separator(
        "PHASE 2 REQUIREMENT EVIDENCE AUDIT"
    )

    print(
        f"Total requirements: {len(requirements)}"
    )

    bad_requirements = []

    for index, requirement in enumerate(
        requirements,
        start=1,
    ):

        evidence = getattr(
            requirement,
            "evidence",
            None,
        )

        source_statement = getattr(
            requirement,
            "source_statement",
            None,
        )

        evidence_ok = bool(
            evidence
            and str(evidence).strip()
        )

        source_statement_ok = bool(
            source_statement
            and str(source_statement).strip()
        )

        print()
        print(
            f"Requirement #{index}"
        )

        print(
            "ID:",
            repr(
                getattr(
                    requirement,
                    "requirement_id",
                    None,
                )
            ),
        )

        print(
            "TYPE:",
            repr(
                getattr(
                    requirement,
                    "requirement_type",
                    None,
                )
            ),
        )

        print(
            "SUBJECT:",
            repr(
                getattr(
                    requirement,
                    "subject",
                    None,
                )
            ),
        )

        print(
            "EVIDENCE:",
            repr(
                evidence
            ),
        )

        print(
            "SOURCE STATEMENT:",
            repr(
                source_statement
            ),
        )

        print(
            "EVIDENCE OK:",
            evidence_ok,
        )

        print(
            "SOURCE STATEMENT OK:",
            source_statement_ok,
        )

        if not evidence_ok:

            bad_requirements.append(
                requirement
            )

            print(
                "*** MISSING EVIDENCE ***"
            )

        if not source_statement_ok:

            print(
                "*** MISSING SOURCE STATEMENT ***"
            )

    print_separator(
        "EVIDENCE AUDIT SUMMARY",
        width=80,
    )

    print(
        "Total requirements:",
        len(requirements),
    )

    print(
        "Requirements with valid evidence:",
        sum(
            bool(
                getattr(
                    requirement,
                    "evidence",
                    None,
                )
                and str(
                    getattr(
                        requirement,
                        "evidence",
                        "",
                    )
                ).strip()
            )
            for requirement in requirements
        ),
    )

    print(
        "Requirements with missing evidence:",
        len(bad_requirements),
    )

    if bad_requirements:

        print(
            "\nBAD REQUIREMENT IDS:"
        )

        for requirement in bad_requirements:

            print(
                " -",
                getattr(
                    requirement,
                    "requirement_id",
                    "<missing>",
                ),
            )

    else:

        print(
            "\nAll requirements contain evidence."
        )

    return bad_requirements


# ============================================================================
# COMPLETE RESULT DEBUG
# ============================================================================


def print_complete_pipeline_result(
    result: ProjectPipelineResult,
) -> None:
    """
    Print the complete ProjectPipelineResult object and
    important top-level attributes.
    """

    print_separator(
        "COMPLETE PROJECT PIPELINE RESULT"
    )

    print(
        "TYPE:",
        type(result),
    )

    try:

        print(
            pformat(
                result,
                width=120,
                sort_dicts=False,
            )
        )

    except Exception as exc:

        print(
            "repr FAILED:",
            repr(exc),
        )

    print_separator(
        "PROJECT PIPELINE RESULT ATTRIBUTES"
    )

    attributes = [
        "document_input",
        "routed_document",
        "pipeline_request",
        "pipeline_response",
        "document_profile",
        "jd_requirement_profile",
    ]

    for attribute in attributes:

        print_attribute(
            "ProjectPipelineResult",
            result,
            attribute,
        )


# ============================================================================
# RESUME TEST
# ============================================================================


class TestProjectPipelineResume:
    """
    Validate real Resume object flow through project_pipeline.
    """

    def test_real_resume_object_flow(
        self,
    ) -> None:

        print_separator(
            "STARTING REAL RESUME PROJECT PIPELINE"
        )

        pipeline = (
            ProjectPipeline()
        )

        document_input = DocumentInput(
            text=RESUME_TEXT,
            document_type=DocumentType.RESUME,
        )

        result = (
            pipeline.process(
                document_input
            )
        )

        # ----------------------------------------------------------
        # COMPLETE RESULT
        # ----------------------------------------------------------

        print_complete_pipeline_result(
            result
        )

        # ----------------------------------------------------------
        # CHECKPOINTS
        # ----------------------------------------------------------

        print_checkpoint(
            "1. DocumentInput",
            result.document_input,
        )

        print_checkpoint(
            "2. RoutedDocument",
            result.routed_document,
        )

        print_checkpoint(
            "3. KnowledgePipelineRequest",
            result.pipeline_request,
        )

        print_checkpoint(
            "4. KnowledgePipelineResponse",
            result.pipeline_response,
        )

        print_checkpoint(
            "5. DocumentKnowledgeProfile",
            result.document_profile,
        )

        # ----------------------------------------------------------
        # DEEP KNOWLEDGE DOCUMENT DEBUG
        # ----------------------------------------------------------

        pipeline_response = (
            result.pipeline_response
        )

        knowledge_document = getattr(
            pipeline_response,
            "knowledge_document",
            None,
        )

        if knowledge_document is not None:

            print_knowledge_document_debug(
                knowledge_document
            )

        # ----------------------------------------------------------
        # PROFILE
        # ----------------------------------------------------------

        print_profile_contents(
            result
        )

        # ----------------------------------------------------------
        # CONTRACTS
        # ----------------------------------------------------------

        assert isinstance(
            result,
            ProjectPipelineResult,
        ), (
            "ProjectPipeline did not return "
            "ProjectPipelineResult."
        )

        assert (
            result.pipeline_response.success
            is True
        ), (
            "Knowledge pipeline failed."
        )

        assert (
            result.document_profile.is_resume
            is True
        ), (
            "Resume input was not represented "
            "as a resume profile."
        )

        assert (
            result.document_profile.is_jd
            is False
        ), (
            "Resume was incorrectly represented "
            "as a JD."
        )

        print_separator(
            "RESUME PROJECT PIPELINE TEST PASSED"
        )


# ============================================================================
# JD TEST
# ============================================================================


class TestProjectPipelineJD:
    """
    Validate real JD object flow through project_pipeline
    and Phase 2.
    """

    def test_real_jd_object_flow_through_phase_2(
        self,
    ) -> None:

        print_separator(
            "STARTING REAL JD PROJECT PIPELINE"
        )

        pipeline = (
            ProjectPipeline()
        )

        document_input = DocumentInput(
            text=JD_TEXT,
            document_type=DocumentType.JD,
        )

        result = (
            pipeline.process(
                document_input
            )
        )

        # ----------------------------------------------------------
        # COMPLETE RESULT
        # ----------------------------------------------------------

        print_complete_pipeline_result(
            result
        )

        # ----------------------------------------------------------
        # CHECKPOINTS
        # ----------------------------------------------------------

        print_checkpoint(
            "1. DocumentInput",
            result.document_input,
        )

        print_checkpoint(
            "2. RoutedDocument",
            result.routed_document,
        )

        print_checkpoint(
            "3. KnowledgePipelineRequest",
            result.pipeline_request,
        )

        print_checkpoint(
            "4. KnowledgePipelineResponse",
            result.pipeline_response,
        )

        print_checkpoint(
            "5. DocumentKnowledgeProfile",
            result.document_profile,
        )

        # ----------------------------------------------------------
        # DEEP KNOWLEDGE DOCUMENT DEBUG
        # ----------------------------------------------------------

        pipeline_response = (
            result.pipeline_response
        )

        knowledge_document = getattr(
            pipeline_response,
            "knowledge_document",
            None,
        )

        if knowledge_document is not None:

            print_knowledge_document_debug(
                knowledge_document
            )

        # ----------------------------------------------------------
        # PROFILE
        # ----------------------------------------------------------

        print_profile_contents(
            result
        )

        # ----------------------------------------------------------
        # JD REQUIREMENTS
        # ----------------------------------------------------------

        print_jd_requirements(
            result
        )

        # ----------------------------------------------------------
        # EVIDENCE AUDIT
        # ----------------------------------------------------------

        bad_requirements = (
            audit_requirement_evidence(
                result
            )
        )

        # ----------------------------------------------------------
        # BASIC CONTRACT
        # ----------------------------------------------------------

        assert isinstance(
            result,
            ProjectPipelineResult,
        ), (
            "ProjectPipeline did not return "
            "ProjectPipelineResult."
        )

        assert (
            result.pipeline_response.success
            is True
        ), (
            "Knowledge pipeline failed."
        )

        assert (
            result.document_profile.is_jd
            is True
        ), (
            "JD input was not represented "
            "as a JD profile."
        )

        assert (
            result.document_profile.is_resume
            is False
        ), (
            "JD was incorrectly represented "
            "as a resume."
        )

        # ----------------------------------------------------------
        # REQUIREMENT PROFILE
        # ----------------------------------------------------------

        assert isinstance(
            result.jd_requirement_profile,
            JDRequirementProfile,
        ), (
            "JD requirement classifier did not "
            "produce JDRequirementProfile."
        )

        requirements = (
            result
            .jd_requirement_profile
            .requirements
        )

        assert requirements, (
            "Real JD produced zero requirements."
        )

        # ----------------------------------------------------------
        # REQUIREMENT IDS
        # ----------------------------------------------------------

        missing_ids = [
            (
                index,
                requirement,
            )
            for index, requirement
            in enumerate(
                requirements,
                start=1,
            )
            if not getattr(
                requirement,
                "requirement_id",
                None,
            )
        ]

        assert not missing_ids, (
            "One or more JD requirements have "
            "missing requirement_id values:\n"
            + pformat(
                missing_ids,
                width=120,
            )
        )

        # ----------------------------------------------------------
        # EVIDENCE
        # ----------------------------------------------------------

        assert not bad_requirements, (
            "One or more REAL JD requirements "
            "have missing evidence.\n\n"
            "See the full PHASE 2 REQUIREMENT "
            "EVIDENCE AUDIT above.\n\n"
            "Bad requirements:\n"
            + pformat(
                bad_requirements,
                width=120,
                sort_dicts=False,
            )
        )

        # ----------------------------------------------------------
        # INDIVIDUAL STRUCTURED OBJECT CHECK
        # ----------------------------------------------------------

        for index, requirement in enumerate(
            requirements,
            start=1,
        ):

            assert (
                getattr(
                    requirement,
                    "subject",
                    None,
                )
                is not None
            ), (
                f"Requirement #{index} "
                f"has subject=None."
            )

            assert (
                getattr(
                    requirement,
                    "confidence",
                    None,
                )
                is not None
            ), (
                f"Requirement #{index} "
                f"has confidence=None."
            )

        print_separator(
            "JD PHASE 2 PROJECT PIPELINE TEST PASSED"
        )


# ============================================================================
# SHARED ARCHITECTURE TEST
# ============================================================================


class TestProjectPipelineSharedArchitecture:
    """
    Verify that Resume and JD use the same project pipeline.
    """

    def test_resume_and_jd_use_same_project_pipeline(
        self,
    ) -> None:

        print_separator(
            "SHARED PROJECT PIPELINE ARCHITECTURE TEST"
        )

        pipeline = (
            ProjectPipeline()
        )

        resume_result = (
            pipeline.process(
                DocumentInput(
                    text=RESUME_TEXT,
                    document_type=DocumentType.RESUME,
                )
            )
        )

        jd_result = (
            pipeline.process(
                DocumentInput(
                    text=JD_TEXT,
                    document_type=DocumentType.JD,
                )
            )
        )

        # ----------------------------------------------------------
        # PRINT BOTH RESULTS
        # ----------------------------------------------------------

        print_checkpoint(
            "RESUME PROJECT PIPELINE RESULT",
            resume_result,
        )

        print_checkpoint(
            "JD PROJECT PIPELINE RESULT",
            jd_result,
        )

        # ----------------------------------------------------------
        # TYPE CHECKS
        # ----------------------------------------------------------

        assert isinstance(
            resume_result,
            ProjectPipelineResult,
        ), (
            "Resume does not use ProjectPipelineResult."
        )

        assert isinstance(
            jd_result,
            ProjectPipelineResult,
        ), (
            "JD does not use ProjectPipelineResult."
        )

        # ----------------------------------------------------------
        # SAME RESULT TYPE
        # ----------------------------------------------------------

        assert (
            type(resume_result)
            is type(jd_result)
        ), (
            "Resume and JD are not using "
            "the same ProjectPipelineResult type."
        )

        # ----------------------------------------------------------
        # SAME PIPELINE RESPONSE TYPE
        # ----------------------------------------------------------

        assert (
            type(
                resume_result.pipeline_response
            )
            is type(
                jd_result.pipeline_response
            )
        ), (
            "Resume and JD do not use the "
            "same KnowledgePipelineResponse type."
        )

        # ----------------------------------------------------------
        # SAME DOCUMENT PROFILE ARCHITECTURE
        # ----------------------------------------------------------

        assert (
            type(
                resume_result.document_profile
            )
            is type(
                jd_result.document_profile
            )
        ), (
            "Resume and JD do not use the "
            "same DocumentKnowledgeProfile type."
        )

        # ----------------------------------------------------------
        # DIFFERENT DOCUMENT SEMANTICS
        # ----------------------------------------------------------

        assert (
            resume_result.document_profile.is_resume
            is True
        )

        assert (
            resume_result.document_profile.is_jd
            is False
        )

        assert (
            jd_result.document_profile.is_resume
            is False
        )

        assert (
            jd_result.document_profile.is_jd
            is True
        )

        # ----------------------------------------------------------
        # BOTH PIPELINES MUST SUCCEED
        # ----------------------------------------------------------

        assert (
            resume_result.pipeline_response.success
            is True
        )

        assert (
            jd_result.pipeline_response.success
            is True
        )

        print_separator(
            "SHARED PROJECT PIPELINE TEST PASSED"
        )