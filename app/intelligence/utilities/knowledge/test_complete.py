"""
Enterprise Resume -> Knowledge Profile
Enterprise V14

NEW ARCHITECTURE INTEGRATION TEST

Pipeline
--------
Resume Text
    ↓
EnterpriseResumePipeline
    ↓
Section Detection
    ↓
KnowledgeDocument
    ↓
KnowledgeSentence[]
    ↓
KnowledgeFact[]
    ↓
KnowledgeInterpretation
    ↓
KnowledgeEntity[]
    ↓
SemanticResolver
    ↓
BusinessStatementBuilder
    ↓
BusinessStatement[]
    ↓
KnowledgeGraphBuilder
    ↓
KnowledgeGraph
    ↓
ProfileBuilder
    ↓
KnowledgeProfile

Purpose
-------
This test validates DATA FLOW between every stage.

It deliberately does NOT require:

    MatchResult
    legacy semantic architecture
    old ProfileBuilder architecture
    old BusinessStatement construction

Technology terminology:
    technologie

Methodology terminology:
    methodologie
"""

from __future__ import annotations

import traceback
from typing import Any


# ============================================================================
# PIPELINE IMPORT
# ============================================================================

from app.intelligence.utilities.knowledge.enterprise_resume_pipeline import (
    EnterpriseResumePipeline,
)


# ============================================================================
# TEST RESUME
# ============================================================================

TEST_RESUME = """
Muhammad Kashif

Quality Assurance & Food Safety Professional

Quality Assurance Specialist and Business Operations Leader with
15+ years of experience across food and beverage manufacturing,
FMCG, supply chain, distribution, retail, and data analytics.

Led implementation of FSSC 22000 requirements and successfully
achieved facility certification.

Implemented HACCP and BRCGS food safety requirements.

Improved production yield from 70% to 99% through teamwork,
process control, and data-based decision making.

Reduced customer complaints through root cause analysis and
corrective action.

Managed incoming raw materials and resolved bottle bursting
issues through quality investigation.

Performed stock reconciliation and inventory control.

Used Lean Management and Six Sigma methodologies for process
improvement.

Used ISO 9001 quality management systems and internal auditing.

Worked with HACCP, FSSC 22000, BRCGS, ISO 9001, and preventive
controls.

Led quality assurance teams and provided food safety training.

Used Python, SQL, PostgreSQL, pandas, scikit-learn, Power BI,
Tableau, Flask, Docker, and MySQL for data analytics and
business intelligence.

Completed Data Analytics training from University of Toronto.

Certified Preventive Control Qualified Individual for Human Food.

Certified HACCP Level 4 and Food Safety Level 4.

Certified Lead Auditor QMS ISO 9001.

Certified Lead Auditor Global Standard for Food Safety.

Managed business operations including yield improvement,
inventory management, customer complaint resolution, supplier
management, and quality assurance.

Increased yield from 70% to 99%.

Reduced customer complaints through corrective actions.

Improved operational performance through data-driven decisions.
"""


# ============================================================================
# OUTPUT HELPERS
# ============================================================================

def banner(title: str) -> None:

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def section(title: str) -> None:

    print()
    print("-" * 80)
    print(title)
    print("-" * 80)


def safe_get(
    obj: Any,
    name: str,
    default=None,
):
    """
    Safe attribute access.

    Also supports dictionaries because some pipeline stages may expose
    intermediate structures as dictionaries.
    """

    if obj is None:
        return default

    if isinstance(obj, dict):
        return obj.get(
            name,
            default,
        )

    return getattr(
        obj,
        name,
        default,
    )


def as_list(value) -> list:

    if value is None:
        return []

    if isinstance(
        value,
        list,
    ):
        return value

    if isinstance(
        value,
        tuple,
    ):
        return list(value)

    if isinstance(
        value,
        set,
    ):
        return list(value)

    return [value]


def require(
    condition: bool,
    message: str,
) -> None:

    if not condition:

        raise AssertionError(
            message
        )


# ============================================================================
# GENERIC COLLECTION ACCESS
# ============================================================================

def get_collection(
    obj,
    names,
) -> list:

    for name in names:

        value = safe_get(
            obj,
            name,
            None,
        )

        if value is not None:

            return as_list(
                value
            )

    return []


# ============================================================================
# ENTITY TYPE
# ============================================================================

def entity_type(
    entity,
) -> str:

    return str(
        safe_get(
            entity,
            "entity_type",
            "",
        )
    ).strip().casefold()


# ============================================================================
# ENTITY CANONICAL
# ============================================================================

def entity_canonical(
    entity,
) -> str:

    return str(
        safe_get(
            entity,
            "canonical",
            "",
        )
    ).strip()


# ============================================================================
# ENTITY INSPECTION
# ============================================================================

def print_entity(
    entity,
    index: int,
) -> None:

    print(
        f"\n[{index}]"
    )

    print(
        "entity_id      :",
        safe_get(
            entity,
            "entity_id",
            "",
        ),
    )

    print(
        "canonical      :",
        safe_get(
            entity,
            "canonical",
            "",
        ),
    )

    print(
        "entity_type    :",
        safe_get(
            entity,
            "entity_type",
            "",
        ),
    )

    print(
        "ontology_name  :",
        safe_get(
            entity,
            "ontology_name",
            "",
        ),
    )

    print(
        "business_area  :",
        safe_get(
            entity,
            "business_area",
            "",
        ),
    )

    print(
        "confidence     :",
        safe_get(
            entity,
            "confidence",
            None,
        ),
    )

    print(
        "impact_weight  :",
        safe_get(
            entity,
            "impact_weight",
            None,
        ),
    )

    print(
        "matched_phrase :",
        safe_get(
            entity,
            "matched_phrase",
            "",
        ),
    )


# ============================================================================
# STAGE STATUS
# ============================================================================

def validate_pipeline_stages(
    result,
) -> None:

    section(
        "PIPELINE STAGES"
    )

    stages = safe_get(
        result,
        "stages",
        {},
    )

    if not isinstance(
        stages,
        dict,
    ):
        stages = {}

    for name, passed in stages.items():

        print(
            f"{name:<30} : "
            f"{'PASS' if passed else 'FAIL'}"
        )

    print()

    failed_stage = safe_get(
        result,
        "failed_stage",
        "",
    )

    error = safe_get(
        result,
        "error",
        None,
    )

    if failed_stage:

        print(
            "FAILED STAGE :",
            failed_stage,
        )

        print(
            "ERROR        :",
            error,
        )


# ============================================================================
# KNOWLEDGE DOCUMENT
# ============================================================================

def validate_knowledge_document(
    result,
) -> None:

    section(
        "1. KNOWLEDGE DOCUMENT"
    )

    document = safe_get(
        result,
        "document",
        None,
    )

    require(
        document is not None,
        "KnowledgeDocument was not created.",
    )

    sentences = get_collection(
        document,
        (
            "sentences",
        ),
    )

    facts = get_collection(
        document,
        (
            "facts",
        ),
    )

    print(
        "Document type :",
        type(document).__name__,
    )

    print(
        "Sentences     :",
        len(sentences),
    )

    print(
        "Facts         :",
        len(facts),
    )

    confidence = safe_get(
        document,
        "confidence",
        None,
    )

    print(
        "Confidence    :",
        confidence,
    )

    require(
        len(sentences) > 0,
        "KnowledgeDocument contains zero sentences.",
    )

    require(
        len(facts) > 0,
        "KnowledgeDocument contains zero KnowledgeFacts.",
    )

    print(
        "\nPASS — KnowledgeDocument created."
    )


# ============================================================================
# KNOWLEDGE FACT FLOW
# ============================================================================

def validate_knowledge_facts(
    result,
) -> None:

    section(
        "2. KNOWLEDGE FACT FLOW"
    )

    document = safe_get(
        result,
        "document",
        None,
    )

    facts = get_collection(
        document,
        (
            "facts",
        ),
    )

    if not facts:

        facts = get_collection(
            result,
            (
                "facts",
                "knowledge_facts",
            ),
        )

    print(
        "KnowledgeFact count :",
        len(facts),
    )

    require(
        len(facts) > 0,
        "No KnowledgeFact objects reached the pipeline.",
    )

    interpretation_count = 0
    entity_count = 0
    achievement_count = 0
    quantified_count = 0

    for index, fact in enumerate(
        facts[:20],
        start=1,
    ):

        interpretation = safe_get(
            fact,
            "interpretation",
            None,
        )

        if interpretation is not None:

            interpretation_count += 1

        entities = get_collection(
            interpretation,
            (
                "entities",
            ),
        )

        entity_count += len(
            entities
        )

        if safe_get(
            fact,
            "achievement",
            False,
        ):
            achievement_count += 1

        if safe_get(
            fact,
            "quantified",
            False,
        ):
            quantified_count += 1

        print(
            f"\nFACT [{index}]"
        )

        print(
            "text          :",
            str(
                safe_get(
                    fact,
                    "text",
                    "",
                )
            )[:180],
        )

        print(
            "achievement   :",
            safe_get(
                fact,
                "achievement",
                False,
            ),
        )

        print(
            "quantified    :",
            safe_get(
                fact,
                "quantified",
                False,
            ),
        )

        print(
            "interpretation:",
            type(
                interpretation
            ).__name__
            if interpretation is not None
            else None,
        )

        print(
            "entities      :",
            len(
                entities
            ),
        )

    print(
        "\nFacts inspected              :",
        min(
            len(facts),
            20,
        ),
    )

    print(
        "Facts with interpretation   :",
        interpretation_count,
    )

    print(
        "Embedded entities inspected :",
        entity_count,
    )

    print(
        "Achievement facts           :",
        achievement_count,
    )

    print(
        "Quantified facts            :",
        quantified_count,
    )

    require(
        interpretation_count > 0,
        "KnowledgeFacts do not contain KnowledgeInterpretation objects.",
    )


# ============================================================================
# SEMANTIC RESOLUTION
# ============================================================================

def validate_semantic_resolution(
    result,
) -> None:

    section(
        "3. SEMANTIC RESOLUTION"
    )

    entities = get_collection(
        result,
        (
            "semantic_entities",
            "resolved_entities",
            "entities",
        ),
    )

    dependencies = get_collection(
        result,
        (
            "semantic_dependencies",
            "dependencies",
        ),
    )

    interpretations = get_collection(
        result,
        (
            "interpretations",
            "semantic_interpretations",
        ),
    )

    print(
        "Semantic entities :",
        len(entities),
    )

    print(
        "Dependencies      :",
        len(dependencies),
    )

    print(
        "Interpretations   :",
        len(interpretations),
    )

    require(
        len(entities) > 0,
        (
            "SemanticResolver produced zero entities. "
            "KnowledgeFacts exist, but no entities reached semantic resolution."
        ),
    )

    print(
        "\nResolved entities:"
    )

    for index, entity in enumerate(
        entities[:30],
        start=1,
    ):

        print_entity(
            entity,
            index,
        )

    print(
        "\nPASS — entities reached SemanticResolver."
    )


# ============================================================================
# ENTITY TYPE COVERAGE
# ============================================================================

def validate_entity_coverage(
    result,
) -> None:

    section(
        "4. SEMANTIC ENTITY COVERAGE"
    )

    entities = get_collection(
        result,
        (
            "semantic_entities",
            "resolved_entities",
            "entities",
        ),
    )

    counts = {}

    for entity in entities:

        kind = entity_type(
            entity
        )

        if not kind:

            kind = "unknown"

        counts[kind] = (
            counts.get(
                kind,
                0,
            )
            + 1
        )

    for kind, count in sorted(
        counts.items()
    ):

        print(
            f"{kind:<25} : {count}"
        )

    technologie_count = sum(
        count
        for kind, count in counts.items()
        if kind in {
            "technologie",
            "technologies",
            "technology",
        }
    )

    certification_count = sum(
        count
        for kind, count in counts.items()
        if kind in {
            "certification",
            "certifications",
        }
    )

    methodologie_count = sum(
        count
        for kind, count in counts.items()
        if kind in {
            "methodologie",
            "methodologies",
            "methodology",
        }
    )

    print(
        "\nTechnologie entities :",
        technologie_count,
    )

    print(
        "Certification entities:",
        certification_count,
    )

    print(
        "Methodologie entities :",
        methodologie_count,
    )

    require(
        technologie_count > 0,
        "Technology entities did not reach semantic resolution.",
    )

    require(
        certification_count > 0,
        "Certification entities did not reach semantic resolution.",
    )

    require(
        methodologie_count > 0,
        "Methodology entities did not reach semantic resolution.",
    )


# ============================================================================
# BUSINESS STATEMENT BUILDER
# ============================================================================

def validate_business_statement_builder(
    result,
) -> None:

    section(
        "5. BUSINESS STATEMENT BUILDER"
    )

    statements = get_collection(
        result,
        (
            "business_statements",
            "statements",
            "business_statement_results",
        ),
    )

    print(
        "Business statements :",
        len(statements),
    )

    require(
        len(statements) > 0,
        (
            "BusinessStatementBuilder produced "
            "zero BusinessStatement objects."
        ),
    )

    total_entities = 0
    total_relations = 0

    for index, statement in enumerate(
        statements[:30],
        start=1,
    ):

        entities = get_collection(
            statement,
            (
                "entities",
            ),
        )

        relations = get_collection(
            statement,
            (
                "relations",
            ),
        )

        total_entities += len(
            entities
        )

        total_relations += len(
            relations
        )

        print(
            f"\nSTATEMENT [{index}]"
        )

        print(
            "statement_id :",
            safe_get(
                statement,
                "statement_id",
                "",
            ),
        )

        print(
            "label        :",
            safe_get(
                statement,
                "label",
                "",
            ),
        )

        print(
            "semantic_type:",
            safe_get(
                statement,
                "semantic_type",
                "",
            ),
        )

        print(
            "achievement  :",
            safe_get(
                statement,
                "achievement",
                False,
            ),
        )

        print(
            "entities     :",
            len(entities),
        )

        print(
            "relations    :",
            len(relations),
        )

        for entity in entities[:10]:

            print(
                "  ENTITY:",
                entity_canonical(
                    entity
                ),
                "|",
                entity_type(
                    entity
                ),
            )

        for relation in relations[:10]:

            print(
                "  RELATION:",
                safe_get(
                    relation,
                    "relation_type",
                    "",
                ),
                safe_get(
                    relation,
                    "source_id",
                    "",
                ),
                "->",
                safe_get(
                    relation,
                    "target_id",
                    "",
                ),
            )

    print(
        "\nTotal statement entities :",
        total_entities,
    )

    print(
        "Total statement relations:",
        total_relations,
    )

    require(
        total_entities > 0,
        "BusinessStatementBuilder produced statements without entities.",
    )

    require(
        total_relations > 0,
        "BusinessStatementBuilder produced statements without relations.",
    )

    print(
        "\nPASS — BusinessStatementBuilder produced populated statements."
    )


# ============================================================================
# KNOWLEDGE GRAPH
# ============================================================================

def validate_knowledge_graph(
    result,
) -> None:

    section(
        "6. KNOWLEDGE GRAPH"
    )

    graph = safe_get(
        result,
        "graph",
        None,
    )

    require(
        graph is not None,
        "KnowledgeGraph was not created.",
    )

    get_nodes = getattr(
        graph,
        "get_nodes",
        None,
    )

    get_edges = getattr(
        graph,
        "get_edges",
        None,
    )

    if callable(
        get_nodes
    ):

        nodes = as_list(
            get_nodes()
        )

    else:

        nodes = get_collection(
            graph,
            (
                "nodes",
            ),
        )

    if callable(
        get_edges
    ):

        edges = as_list(
            get_edges()
        )

    else:

        edges = get_collection(
            graph,
            (
                "edges",
            ),
        )

    print(
        "Graph nodes :",
        len(nodes),
    )

    print(
        "Graph edges :",
        len(edges),
    )

    require(
        len(nodes) > 0,
        "KnowledgeGraph contains zero nodes.",
    )

    require(
        len(edges) > 0,
        "KnowledgeGraph contains zero edges.",
    )

    technologie_nodes = []
    certification_nodes = []
    methodologie_nodes = []

    for node in nodes:

        kind = entity_type(
            node
        )

        if kind in {
            "technologie",
            "technologies",
            "technology",
        }:

            technologie_nodes.append(
                node
            )

        if kind in {
            "certification",
            "certifications",
        }:

            certification_nodes.append(
                node
            )

        if kind in {
            "methodologie",
            "methodologies",
            "methodology",
        }:

            methodologie_nodes.append(
                node
            )

    print(
        "\nTechnology nodes     :",
        len(
            technologie_nodes
        ),
    )

    print(
        "Certification nodes  :",
        len(
            certification_nodes
        ),
    )

    print(
        "Methodology nodes    :",
        len(
            methodologie_nodes
        ),
    )

    require(
        len(technologie_nodes) > 0,
        "Technology entities did not reach KnowledgeGraph.",
    )

    require(
        len(certification_nodes) > 0,
        "Certification entities did not reach KnowledgeGraph.",
    )

    require(
        len(methodologie_nodes) > 0,
        "Methodology entities did not reach KnowledgeGraph.",
    )

    print(
        "\nRepresentative graph nodes:"
    )

    for index, node in enumerate(
        nodes[:30],
        start=1,
    ):

        print_entity(
            node,
            index,
        )

    print(
        "\nPASS — KnowledgeGraph contains entity nodes and relations."
    )


# ============================================================================
# PROFILE
# ============================================================================

def validate_knowledge_profile(
    result,
) -> None:

    section(
        "7. KNOWLEDGE PROFILE"
    )

    profile = safe_get(
        result,
        "profile",
        None,
    )

    require(
        profile is not None,
        "KnowledgeProfile was not created.",
    )

    print(
        "Profile type :",
        type(profile).__name__,
    )

    print(
        "Confidence   :",
        safe_get(
            profile,
            "confidence",
            None,
        ),
    )

    components = (
        "summary",
        "achievement",
        "leadership",
        "seniority",
        "metrics",
        "domains",
        "modifiers",
    )

    for component in components:

        value = safe_get(
            profile,
            component,
            None,
        )

        print(
            f"{component:<15}:",
            type(value).__name__
            if value is not None
            else None,
        )

        require(
            value is not None,
            (
                f"KnowledgeProfile.{component} "
                "is missing."
            ),
        )

    print(
        "\nPASS — KnowledgeProfile created."
    )


# ============================================================================
# PROFILE ENTITY FLOW
# ============================================================================

def validate_profile_entity_flow(
    result,
) -> None:

    section(
        "8. FINAL ENTITY FLOW INSPECTION"
    )

    graph = safe_get(
        result,
        "graph",
        None,
    )

    profile = safe_get(
        result,
        "profile",
        None,
    )

    require(
        graph is not None,
        "Cannot inspect final entity flow: graph missing.",
    )

    require(
        profile is not None,
        "Cannot inspect final entity flow: profile missing.",
    )

    get_nodes = getattr(
        graph,
        "get_nodes",
        None,
    )

    if callable(
        get_nodes
    ):

        nodes = as_list(
            get_nodes()
        )

    else:

        nodes = get_collection(
            graph,
            (
                "nodes",
            ),
        )

    type_counts = {}

    for node in nodes:

        kind = entity_type(
            node
        )

        type_counts[kind] = (
            type_counts.get(
                kind,
                0,
            )
            + 1
        )

    print(
        "KnowledgeGraph entity distribution:"
    )

    for kind, count in sorted(
        type_counts.items()
    ):

        print(
            f"  {kind:<25} : {count}"
        )

    print(
        "\nKnowledgeProfile:"
    )

    print(
        "  type       :",
        type(profile).__name__,
    )

    print(
        "  confidence :",
        safe_get(
            profile,
            "confidence",
            None,
        ),
    )

    print(
        "\nPASS — final entity flow inspected."
    )


# ============================================================================
# FINAL PIPELINE TEST
# ============================================================================

def test_enterprise_resume_pipeline():

    banner(
        "ENTERPRISE RESUME -> KNOWLEDGE PROFILE"
    )

    print(
        "\nStarting NEW enterprise pipeline..."
    )

    try:

        pipeline = (
            EnterpriseResumePipeline()
        )

        result = pipeline.run(
            TEST_RESUME
        )

        # ------------------------------------------------------------
        # STAGE 0 — PIPELINE STATUS
        # ------------------------------------------------------------

        validate_pipeline_stages(
            result
        )

        # ------------------------------------------------------------
        # STAGE 1 — DOCUMENT
        # ------------------------------------------------------------

        validate_knowledge_document(
            result
        )

        # ------------------------------------------------------------
        # STAGE 2 — FACTS
        # ------------------------------------------------------------

        validate_knowledge_facts(
            result
        )

        # ------------------------------------------------------------
        # STAGE 3 — SEMANTIC RESOLUTION
        # ------------------------------------------------------------

        validate_semantic_resolution(
            result
        )

        # ------------------------------------------------------------
        # STAGE 4 — ENTITY COVERAGE
        # ------------------------------------------------------------

        validate_entity_coverage(
            result
        )

        # ------------------------------------------------------------
        # STAGE 5 — BUSINESS STATEMENT BUILDER
        # ------------------------------------------------------------

        validate_business_statement_builder(
            result
        )

        # ------------------------------------------------------------
        # STAGE 6 — KNOWLEDGE GRAPH
        # ------------------------------------------------------------

        validate_knowledge_graph(
            result
        )

        # ------------------------------------------------------------
        # STAGE 7 — PROFILE
        # ------------------------------------------------------------

        validate_knowledge_profile(
            result
        )

        # ------------------------------------------------------------
        # FINAL FLOW
        # ------------------------------------------------------------

        validate_profile_entity_flow(
            result
        )

        # ------------------------------------------------------------
        # FINAL
        # ------------------------------------------------------------

        banner(
            "ENTERPRISE PIPELINE TEST PASSED"
        )

        print(
            "\nAll new architecture stages completed."
        )

        return result

    except Exception as exc:

        banner(
            "ENTERPRISE PIPELINE TEST FAILED"
        )

        print(
            "\nException:"
        )

        print(
            repr(exc)
        )

        print(
            "\nTraceback:"
        )

        traceback.print_exc()

        raise


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":

    test_enterprise_resume_pipeline()