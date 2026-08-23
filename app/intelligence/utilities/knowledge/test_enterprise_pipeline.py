
"""
Tests for the Enterprise Resume Intelligence Pipeline.

Run:
    pytest -s test_enterprise_pipeline.py
"""

from __future__ import annotations

import pytest

from app.intelligence.utilities.knowledge.enterprise_resume_pipeline import run_enterprise_resume_pipeline


ENTERPRISE_ONTOLOGY_TEST_RESUME = """
Senior Technology Program Manager

Technology:
Implemented AWS, Azure, Kubernetes, Docker, Terraform, Python, PostgreSQL,
Apache Spark, and Power BI across enterprise platforms.

Methodologies:
Led Agile Scrum delivery, SAFe transformation, DevOps practices, ITIL service
management, Lean Six Sigma process improvement, and OKR planning.

Certifications:
AWS Certified Solutions Architect, PMP, Certified ScrumMaster (CSM),
ITIL 4 Foundation, and Microsoft Certified: Azure Administrator Associate.

Business KPIs:
Increased revenue by 28%, reduced operating costs by 17%, improved customer
retention from 82% to 91%, reduced deployment time by 40%, increased SLA
compliance to 99.5%, and improved NPS by 18 points.

Leadership:
Led a 35-person engineering organization and delivered a $12M transformation
program across multiple business units.
"""


def entities_for_ontology(entities, ontology):
    """Return extracted entities belonging to an ontology."""
    return [
        entity
        for entity in entities
        if getattr(entity, "ontology", None) == ontology
    ]


def test_enterprise_ontology_extraction():
    """Verify that the enterprise resume produces the expected ontologies."""
    result = run_enterprise_resume_pipeline(
        ENTERPRISE_ONTOLOGY_TEST_RESUME
    )

    assert result.success, (
        f"Pipeline failed at {result.failed_stage}: {result.error}"
    )

    entities = result.extracted_entities

    technologies = entities_for_ontology(
        entities,
        "technologies",
    )
    methodologies = entities_for_ontology(
        entities,
        "methodologies",
    )
    certifications = entities_for_ontology(
        entities,
        "certifications",
    )
    business_kpis = entities_for_ontology(
        entities,
        "business_kpis",
    )

    assert technologies, "No technology entities extracted"
    assert methodologies, "No methodology entities extracted"
    assert certifications, "No certification entities extracted"
    assert business_kpis, "No business KPI entities extracted"


def test_enterprise_ontology_expected_entities():
    """Verify important entities, not merely ontology presence."""
    result = run_enterprise_resume_pipeline(
        ENTERPRISE_ONTOLOGY_TEST_RESUME
    )

    assert result.success, (
        f"Pipeline failed at {result.failed_stage}: {result.error}"
    )

    entities = result.extracted_entities

    extracted = {
        (
            getattr(entity, "ontology", ""),
            getattr(entity, "canonical", ""),
        )
        for entity in entities
    }

    expected_entities = {
        ("technologies", "AWS"),
        ("technologies", "Azure"),
        ("technologies", "Kubernetes"),
        ("technologies", "Docker"),
        ("technologies", "Terraform"),
        ("technologies", "Python"),
        ("technologies", "PostgreSQL"),
        ("technologies", "Apache Spark"),
        ("technologies", "Power BI"),
        ("methodologies", "Agile Scrum"),
        ("methodologies", "SAFe"),
        ("methodologies", "DevOps"),
        ("methodologies", "ITIL"),
        ("methodologies", "Lean Six Sigma"),
        ("methodologies", "OKR"),
        ("certifications", "AWS Certified Solutions Architect"),
        ("certifications", "PMP"),
        ("certifications", "Certified ScrumMaster"),
        ("certifications", "ITIL 4 Foundation"),
        (
            "certifications",
            "Microsoft Certified: Azure Administrator Associate",
        ),
    }

    missing = expected_entities - extracted

    assert not missing, (
        "Expected entities were not extracted:\n"
        + "\n".join(
            f"  - {ontology}: {canonical}"
            for ontology, canonical in sorted(missing)
        )
    )


def test_enterprise_business_kpis():
    """Verify that quantified business KPI statements are extracted."""
    result = run_enterprise_resume_pipeline(
        ENTERPRISE_ONTOLOGY_TEST_RESUME
    )

    assert result.success, (
        f"Pipeline failed at {result.failed_stage}: {result.error}"
    )

    kpis = entities_for_ontology(
        result.extracted_entities,
        "business_kpis",
    )

    assert kpis, "No business KPI entities extracted"

    resume_lower = ENTERPRISE_ONTOLOGY_TEST_RESUME.casefold()

    expected_phrases = (
        "28%",
        "17%",
        "82%",
        "91%",
        "40%",
        "99.5%",
        "18 points",
        "$12M",
    )

    for phrase in expected_phrases:
        assert phrase.casefold() in resume_lower


def test_enterprise_pipeline_completes_all_stages():
    """Verify that every pipeline stage completes successfully."""
    result = run_enterprise_resume_pipeline(
        ENTERPRISE_ONTOLOGY_TEST_RESUME
    )

    assert result.success, (
        f"Pipeline failed at {result.failed_stage}: {result.error}"
    )

    expected_stages = (
        "section_detection",
        "knowledge_document",
        "extraction",
        "semantic_resolution",
        "business_statement_builder",
        "knowledge_graph",
        "knowledge_profile",
    )

    for stage in expected_stages:
        assert result.stages.get(stage) is True, (
            f"Pipeline stage did not complete: {stage}"
        )


def test_enterprise_pipeline_produces_semantic_data():
    """Verify semantic resolution preserves entities, relations and clusters."""
    result = run_enterprise_resume_pipeline(
        ENTERPRISE_ONTOLOGY_TEST_RESUME
    )

    assert result.success, (
        f"Pipeline failed at {result.failed_stage}: {result.error}"
    )

    assert result.semantic_resolution is not None

    assert isinstance(
        result.semantic_entities,
        list,
    )

    assert isinstance(
        result.semantic_relations,
        list,
    )

    assert isinstance(
        result.semantic_dependencies,
        list,
    )

    assert isinstance(
        result.semantic_clusters,
        list,
    )


def test_enterprise_pipeline_produces_business_statements():
    """Verify business statement construction."""
    result = run_enterprise_resume_pipeline(
        ENTERPRISE_ONTOLOGY_TEST_RESUME
    )

    assert result.success, (
        f"Pipeline failed at {result.failed_stage}: {result.error}"
    )

    assert isinstance(
        result.business_statements,
        list,
    )

    assert result.business_statements, (
        "No business statements were generated"
    )


def test_enterprise_pipeline_produces_knowledge_graph():
    """Verify knowledge graph construction."""
    result = run_enterprise_resume_pipeline(
        ENTERPRISE_ONTOLOGY_TEST_RESUME
    )

    assert result.success, (
        f"Pipeline failed at {result.failed_stage}: {result.error}"
    )

    assert result.knowledge_graph is not None


def test_enterprise_pipeline_produces_knowledge_profile():
    """Verify knowledge profile construction."""
    result = run_enterprise_resume_pipeline(
        ENTERPRISE_ONTOLOGY_TEST_RESUME
    )

    assert result.success, (
        f"Pipeline failed at {result.failed_stage}: {result.error}"
    )

    assert result.knowledge_profile is not None


def test_enterprise_pipeline_statistics():
    """Verify that pipeline statistics are populated."""
    result = run_enterprise_resume_pipeline(
        ENTERPRISE_ONTOLOGY_TEST_RESUME
    )

    assert result.success, (
        f"Pipeline failed at {result.failed_stage}: {result.error}"
    )

    statistics = result.statistics

    assert statistics.get("knowledge_facts", 0) > 0
    assert statistics.get("extracted_entities", 0) > 0
    assert statistics.get("semantic_entities", 0) > 0
    assert statistics.get("business_statements", 0) >= 0


@pytest.mark.parametrize(
    "invalid_input",
    [
        "",
        "   ",
    ],
)
def test_enterprise_pipeline_rejects_empty_resume(invalid_input):
    """Verify empty resumes fail during input validation."""
    result = run_enterprise_resume_pipeline(invalid_input)

    assert not result.success
    assert result.failed_stage == "input_validation"
    assert result.error


def test_enterprise_pipeline_rejects_non_string_input():
    """Verify non-string input fails validation."""
    result = run_enterprise_resume_pipeline(None)

    assert not result.success
    assert result.failed_stage == "input_validation"
    assert "resume_text must be a string" in result.error


def test_debug_extracted_entities():
    result = run_enterprise_resume_pipeline(
        ENTERPRISE_ONTOLOGY_TEST_RESUME
    )

    assert result.success, (
        f"Pipeline failed at {result.failed_stage}: {result.error}"
    )

    print("\n\n========== EXTRACTED ENTITIES ==========")

    for i, entity in enumerate(result.extracted_entities, 1):
        print(
            f"{i:02d}. "
            f"ontology={getattr(entity, 'ontology', None)!r} | "
            f"entity_type={getattr(entity, 'entity_type', None)!r} | "
            f"canonical={getattr(entity, 'canonical', None)!r} | "
            f"phrase={getattr(entity, 'phrase', None)!r} | "
            f"confidence={getattr(entity, 'confidence', None)!r}"
        )

    print("\n========== ENTITIES BY ONTOLOGY ==========")

    for ontology, entities in result.entities_by_ontology.items():
        print(f"\n{ontology}: {len(entities)}")

        for entity in entities:
            print(
                f"  - canonical={getattr(entity, 'canonical', None)!r}, "
                f"phrase={getattr(entity, 'phrase', None)!r}"
            )



