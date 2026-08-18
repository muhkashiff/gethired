"""
Enterprise Resume -> Knowledge Profile
Enterprise Diagnostic Test

Purpose
-------
This is a DATA INSPECTION diagnostic.

It does NOT assume that every downstream stage is populated.

It prints the actual data produced by every stage so that we can
identify exactly where information is lost.

Pipeline
--------
Resume Text
    ↓
EnterpriseResumePipeline
    ↓
KnowledgeDocument
    ↓
KnowledgeSentence[]
    ↓
KnowledgeFact[]
    ↓
KnowledgeInterpretation
    ↓
Semantic Entities
    ↓
Relations
    ↓
Dependencies
    ↓
BusinessStatement[]
    ↓
KnowledgeGraph
    ↓
KnowledgeProfile

IMPORTANT
---------
This diagnostic deliberately avoids model __repr__() because some
knowledge models may contain convenience properties that are not
compatible with the current architecture.
"""

from __future__ import annotations

import traceback
from dataclasses import fields, is_dataclass
from typing import Any


# ============================================================================
# PIPELINE
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

Quality Assurance Specialist with 15+ years experience in food
manufacturing, FMCG, supply chain and retail.

Led implementation of FSSC 22000 requirements.

Implemented HACCP and BRCGS food safety systems.

Improved production yield from 70% to 99%.

Reduced customer complaints through root cause analysis.

Performed inventory reconciliation.

Used Lean Management and Six Sigma.

Used ISO 9001 quality management system.

Used Python SQL PostgreSQL pandas scikit-learn Power BI Tableau.

Completed Data Analytics training from University of Toronto.

Certified PCQI Human Food.

Certified HACCP Level 4.

Certified Lead Auditor ISO 9001.

Certified Lead Auditor Food Safety.

Managed quality assurance activities, production improvement,
inventory control, customer complaints, food safety systems and
business operations.

Improved operational performance through data-based decision making.
"""


# ============================================================================
# DISPLAY
# ============================================================================

WIDTH = 110


def banner(title: str) -> None:
    print()
    print("=" * WIDTH)
    print(title)
    print("=" * WIDTH)


def section(title: str) -> None:
    print()
    print("-" * WIDTH)
    print(title)
    print("-" * WIDTH)


def subsection(title: str) -> None:
    print()
    print("." * WIDTH)
    print(title)
    print("." * WIDTH)


# ============================================================================
# SAFE OBJECT ACCESS
# ============================================================================

def safe_get(obj: Any, name: str, default: Any = None) -> Any:

    if obj is None:
        return default

    if isinstance(obj, dict):
        return obj.get(name, default)

    try:
        return getattr(obj, name)
    except Exception:
        return default


def safe_type_name(obj: Any) -> str:

    if obj is None:
        return "None"

    return type(obj).__name__


def safe_module(obj: Any) -> str:

    if obj is None:
        return ""

    return getattr(
        type(obj),
        "__module__",
        "",
    )


def as_list(value: Any) -> list:

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, set):
        return list(value)

    return [value]


# ============================================================================
# SAFE VALUE FORMATTER
# ============================================================================

def safe_value(value: Any, max_length: int = 500) -> str:
    """
    Safely display a value without invoking dangerous model __repr__().
    """

    if value is None:
        return "None"

    if isinstance(value, (str, int, float, bool)):
        text = str(value)

    elif isinstance(value, dict):
        text = "{"

        parts = []

        for key, item in value.items():

            try:
                item_text = safe_value(
                    item,
                    max_length=200,
                )
            except Exception:
                item_text = "<unprintable>"

            parts.append(
                f"{key!s}: {item_text}"
            )

        text += ", ".join(parts)
        text += "}"

    elif isinstance(value, (list, tuple, set)):

        items = []

        for item in list(value)[:20]:

            try:
                items.append(
                    safe_value(
                        item,
                        max_length=150,
                    )
                )
            except Exception:
                items.append("<unprintable>")

        if isinstance(value, tuple):
            text = "(" + ", ".join(items) + ")"
        elif isinstance(value, set):
            text = "{" + ", ".join(items) + "}"
        else:
            text = "[" + ", ".join(items) + "]"

        if len(value) > 20:
            text += f" ... +{len(value) - 20} more"

    else:

        text = (
            f"<{type(value).__name__} "
            f"object>"
        )

    if len(text) > max_length:
        text = text[:max_length] + "..."

    return text


# ============================================================================
# SAFE DATACLASS INSPECTION
# ============================================================================

def dataclass_field_names(obj: Any) -> list[str]:

    try:

        if is_dataclass(obj):

            return [
                field.name
                for field in fields(obj)
            ]

    except Exception:
        pass

    return []


def print_object_fields(
    obj: Any,
    indent: int = 2,
    skip: set[str] | None = None,
    max_value_length: int = 500,
) -> None:

    if obj is None:
        print(" " * indent + "None")
        return

    skip = skip or set()

    prefix = " " * indent

    names = dataclass_field_names(obj)

    if not names:

        if isinstance(obj, dict):

            for name, value in obj.items():

                if name in skip:
                    continue

                print(
                    f"{prefix}{name:<30}: "
                    f"{safe_value(value, max_value_length)}"
                )

            return

        print(
            f"{prefix}Type: {type(obj).__name__}"
        )

        return

    for name in names:

        if name in skip:
            continue

        try:
            value = safe_get(
                obj,
                name,
                None,
            )

            # Never directly use repr(value)
            text = safe_value(
                value,
                max_value_length,
            )

            print(
                f"{prefix}{name:<30}: {text}"
            )

        except Exception as exc:

            print(
                f"{prefix}{name:<30}: "
                f"<ERROR READING FIELD: {exc}>"
            )


# ============================================================================
# PIPELINE RESULT
# ============================================================================

def print_pipeline_result(result: Any) -> None:

    section(
        "PIPELINE RESULT"
    )

    print(
        "Type   :",
        safe_type_name(result),
    )

    print(
        "Module :",
        safe_module(result),
    )

    print(
        "Fields:"
    )

    names = dataclass_field_names(result)

    if names:

        for name in names:

            value = safe_get(
                result,
                name,
                None,
            )

            if isinstance(value, list):
                descriptor = (
                    f"list[{len(value)}]"
                )

            elif isinstance(value, dict):
                descriptor = (
                    f"dict[{len(value)}]"
                )

            else:
                descriptor = safe_type_name(
                    value
                )

            print(
                f"  {name:<35}: {descriptor}"
            )


# ============================================================================
# PIPELINE STAGES
# ============================================================================

def print_pipeline_stages(result: Any) -> None:

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
        print(
            "No stage dictionary available."
        )
        return

    for name, status in stages.items():

        print(
            f"{name:<40}: "
            f"{'PASS' if status else 'FAIL'}"
        )

    print()

    print(
        "success      :",
        safe_get(
            result,
            "success",
            None,
        ),
    )

    print(
        "failed_stage :",
        safe_get(
            result,
            "failed_stage",
            None,
        ),
    )

    print(
        "error        :",
        safe_value(
            safe_get(
                result,
                "error",
                None,
            )
        ),
    )

    print(
        "confidence   :",
        safe_get(
            result,
            "confidence",
            None,
        ),
    )


# ============================================================================
# KNOWLEDGE DOCUMENT
# ============================================================================

def print_knowledge_document(
    result: Any,
) -> None:

    section(
        "1. KNOWLEDGE DOCUMENT"
    )

    document = safe_get(
        result,
        "knowledge_document",
        None,
    )

    print(
        "Type       :",
        safe_type_name(document),
    )

    print(
        "Module     :",
        safe_module(document),
    )

    if document is None:

        print(
            "\nWARNING: KnowledgeDocument is None."
        )

        return

    sentences = as_list(
        safe_get(
            document,
            "sentences",
            [],
        )
    )

    facts = as_list(
        safe_get(
            document,
            "facts",
            [],
        )
    )

    print(
        "Sentences  :",
        len(sentences),
    )

    print(
        "Facts      :",
        len(facts),
    )

    print(
        "Confidence :",
        safe_get(
            document,
            "confidence",
            None,
        ),
    )

    print(
        "Source     :",
        safe_get(
            document,
            "source",
            None,
        ),
    )

    print(
        "Parsed     :",
        safe_get(
            document,
            "parsed",
            None,
        ),
    )

    # ----------------------------------------------------------------
    # SENTENCES
    # ----------------------------------------------------------------

    subsection(
        "ALL KNOWLEDGE SENTENCES"
    )

    for index, sentence in enumerate(
        sentences,
        start=1,
    ):

        text = safe_get(
            sentence,
            "text",
            "",
        )

        sentence_facts = as_list(
            safe_get(
                sentence,
                "facts",
                [],
            )
        )

        print(
            f"{index:03d}. "
            f"text={safe_value(text, 300)}"
        )

        print(
            f"      facts={len(sentence_facts)}"
        )

    # ----------------------------------------------------------------
    # FACTS
    # ----------------------------------------------------------------

    subsection(
        "ALL KNOWLEDGE FACTS"
    )

    for index, fact in enumerate(
        facts,
        start=1,
    ):

        print(
            f"\nFACT [{index}]"
        )

        print(
            "  text          :",
            safe_get(
                fact,
                "text",
                "",
            ),
        )

        print(
            "  fact_id       :",
            safe_get(
                fact,
                "fact_id",
                "",
            ),
        )

        print(
            "  sentence_index:",
            safe_get(
                fact,
                "sentence_index",
                None,
            ),
        )

        print(
            "  achievement   :",
            safe_get(
                fact,
                "achievement",
                False,
            ),
        )

        print(
            "  quantified    :",
            safe_get(
                fact,
                "quantified",
                False,
            ),
        )

        print(
            "  confidence    :",
            safe_get(
                fact,
                "confidence",
                None,
            ),
        )

        interpretation = safe_get(
            fact,
            "interpretation",
            None,
        )

        print(
            "  interpretation:",
            safe_type_name(
                interpretation
            ),
        )


# ============================================================================
# SEMANTIC INTERPRETATION
# ============================================================================

def get_main_interpretation(
    result: Any,
) -> Any:

    interpretations = as_list(
        safe_get(
            result,
            "interpretations",
            [],
        )
    )

    if not interpretations:
        return None

    return interpretations[0]


def print_semantic_interpretation(
    result: Any,
) -> None:

    section(
        "2. SEMANTIC INTERPRETATION"
    )

    interpretations = as_list(
        safe_get(
            result,
            "interpretations",
            [],
        )
    )

    print(
        "Interpretation count:",
        len(interpretations),
    )

    for index, interpretation in enumerate(
        interpretations,
        start=1,
    ):

        print(
            f"\nINTERPRETATION [{index:03d}]"
        )

        print(
            "Type   :",
            safe_type_name(
                interpretation
            ),
        )

        print(
            "Module :",
            safe_module(
                interpretation
            ),
        )

        # ------------------------------------------------------------
        # IMPORTANT:
        # Never print interpretation directly.
        # ------------------------------------------------------------

        print(
            "\nFields:"
        )

        print_object_fields(
            interpretation,
            indent=2,
            max_value_length=300,
        )

        # ------------------------------------------------------------
        # ENTITIES
        # ------------------------------------------------------------

        entities = as_list(
            safe_get(
                interpretation,
                "entities",
                [],
            )
        )

        relations = as_list(
            safe_get(
                interpretation,
                "relations",
                [],
            )
        )

        dependencies = as_list(
            safe_get(
                interpretation,
                "dependencies",
                [],
            )
        )

        clusters = as_list(
            safe_get(
                interpretation,
                "clusters",
                [],
            )
        )

        print()
        print(
            "Entities     :",
            len(entities),
        )

        print(
            "Relations    :",
            len(relations),
        )

        print(
            "Dependencies :",
            len(dependencies),
        )

        print(
            "Clusters     :",
            len(clusters),
        )

        # ------------------------------------------------------------
        # ALL ENTITIES
        # ------------------------------------------------------------

        subsection(
            "ALL SEMANTIC ENTITIES"
        )

        print_all_entities(
            entities
        )

        # ------------------------------------------------------------
        # ALL RELATIONS
        # ------------------------------------------------------------

        subsection(
            "ALL SEMANTIC RELATIONS"
        )

        print_all_relations(
            relations
        )

        # ------------------------------------------------------------
        # ALL DEPENDENCIES
        # ------------------------------------------------------------

        subsection(
            "ALL SEMANTIC DEPENDENCIES"
        )

        print_all_dependencies(
            dependencies
        )

        # ------------------------------------------------------------
        # CLUSTERS
        # ------------------------------------------------------------

        subsection(
            "SEMANTIC CLUSTERS"
        )

        print_all_clusters(
            clusters
        )


# ============================================================================
# ENTITY PRINTING
# ============================================================================

def print_entity(
    entity: Any,
    index: int,
) -> None:

    print(
        f"\n[ENTITY {index:03d}]"
    )

    print(
        "  entity_id      :",
        safe_get(
            entity,
            "entity_id",
            "",
        ),
    )

    print(
        "  canonical      :",
        safe_get(
            entity,
            "canonical",
            "",
        ),
    )

    print(
        "  normalized     :",
        safe_get(
            entity,
            "normalized",
            "",
        ),
    )

    print(
        "  entity_type    :",
        safe_get(
            entity,
            "entity_type",
            "",
        ),
    )

    print(
        "  ontology_name  :",
        safe_get(
            entity,
            "ontology_name",
            "",
        ),
    )

    print(
        "  category       :",
        safe_get(
            entity,
            "category",
            "",
        ),
    )

    print(
        "  business_area  :",
        safe_get(
            entity,
            "business_area",
            "",
        ),
    )

    print(
        "  domain         :",
        safe_get(
            entity,
            "domain",
            "",
        ),
    )

    print(
        "  confidence     :",
        safe_get(
            entity,
            "confidence",
            None,
        ),
    )

    print(
        "  impact_weight  :",
        safe_get(
            entity,
            "impact_weight",
            None,
        ),
    )

    print(
        "  matched_phrase :",
        safe_get(
            entity,
            "matched_phrase",
            "",
        ),
    )

    print(
        "  matched_alias  :",
        safe_get(
            entity,
            "matched_alias",
            False,
        ),
    )


def print_all_entities(
    entities: list,
) -> None:

    if not entities:

        print(
            "NO SEMANTIC ENTITIES."
        )

        return

    for index, entity in enumerate(
        entities,
        start=1,
    ):

        print_entity(
            entity,
            index,
        )


# ============================================================================
# ENTITY TYPE DISTRIBUTION
# ============================================================================

def print_entity_distribution(
    result: Any,
) -> None:

    section(
        "3. ENTITY DISTRIBUTION"
    )

    entities = as_list(
        safe_get(
            result,
            "semantic_entities",
            [],
        )
    )

    if not entities:

        interpretation = get_main_interpretation(
            result
        )

        entities = as_list(
            safe_get(
                interpretation,
                "entities",
                [],
            )
        )

    counts = {}

    for entity in entities:

        entity_type = str(
            safe_get(
                entity,
                "entity_type",
                "unknown",
            )
        ).strip().casefold()

        if not entity_type:
            entity_type = "unknown"

        counts[entity_type] = (
            counts.get(
                entity_type,
                0,
            )
            + 1
        )

    for entity_type, count in sorted(
        counts.items()
    ):

        print(
            f"{entity_type:<30}: {count}"
        )

    print(
        "\nTotal entities:",
        len(entities),
    )


# ============================================================================
# RELATIONS
# ============================================================================

def print_relation(
    relation: Any,
    index: int,
) -> None:

    print(
        f"\n[RELATION {index:03d}]"
    )

    print(
        "  relation_type :",
        safe_get(
            relation,
            "relation_type",
            safe_get(
                relation,
                "type",
                "",
            ),
        ),
    )

    print(
        "  source_id     :",
        safe_get(
            relation,
            "source_id",
            safe_get(
                relation,
                "source",
                "",
            ),
        ),
    )

    print(
        "  target_id     :",
        safe_get(
            relation,
            "target_id",
            safe_get(
                relation,
                "target",
                "",
            ),
        ),
    )

    print(
        "  confidence    :",
        safe_get(
            relation,
            "confidence",
            None,
        ),
    )

    print(
        "  impact_weight :",
        safe_get(
            relation,
            "impact_weight",
            None,
        ),
    )


def print_all_relations(
    relations: list,
) -> None:

    if not relations:

        print(
            "NO SEMANTIC RELATIONS."
        )

        return

    for index, relation in enumerate(
        relations,
        start=1,
    ):

        print_relation(
            relation,
            index,
        )


# ============================================================================
# DEPENDENCIES
# ============================================================================

def print_dependency(
    dependency: Any,
    index: int,
) -> None:

    print(
        f"\n[DEPENDENCY {index:03d}]"
    )

    print(
        "  type        :",
        safe_get(
            dependency,
            "dependency_type",
            safe_get(
                dependency,
                "type",
                "",
            ),
        ),
    )

    print(
        "  source      :",
        safe_get(
            dependency,
            "source_id",
            safe_get(
                dependency,
                "source",
                "",
            ),
        ),
    )

    print(
        "  target      :",
        safe_get(
            dependency,
            "target_id",
            safe_get(
                dependency,
                "target",
                "",
            ),
        ),
    )

    print(
        "  confidence  :",
        safe_get(
            dependency,
            "confidence",
            None,
        ),
    )


def print_all_dependencies(
    dependencies: list,
) -> None:

    if not dependencies:

        print(
            "NO SEMANTIC DEPENDENCIES."
        )

        return

    for index, dependency in enumerate(
        dependencies,
        start=1,
    ):

        print_dependency(
            dependency,
            index,
        )


# ============================================================================
# CLUSTERS
# ============================================================================

def print_all_clusters(
    clusters: list,
) -> None:

    if not clusters:

        print(
            "NO SEMANTIC CLUSTERS."
        )

        return

    for index, cluster in enumerate(
        clusters,
        start=1,
    ):

        print(
            f"\n[CLUSTER {index:03d}]"
        )

        if isinstance(
            cluster,
            dict,
        ):

            for key, value in cluster.items():

                print(
                    f"  {key:<25}: "
                    f"{safe_value(value, 300)}"
                )

        else:

            print_object_fields(
                cluster,
                indent=2,
                max_value_length=300,
            )


# ============================================================================
# BUSINESS STATEMENTS
# ============================================================================

def print_business_statements(
    result: Any,
) -> None:

    section(
        "4. BUSINESS STATEMENTS"
    )

    statements = as_list(
        safe_get(
            result,
            "business_statements",
            [],
        )
    )

    print(
        "Business statement count:",
        len(statements),
    )

    if not statements:

        print()
        print(
            "NO BUSINESS STATEMENTS WERE GENERATED."
        )

        print()
        print(
            "This diagnostic does NOT treat that as "
            "a test failure."
        )

        print(
            "It means the semantic data reached this "
            "stage but no BusinessStatement objects "
            "were produced."
        )

        return

    for index, statement in enumerate(
        statements,
        start=1,
    ):

        print(
            f"\n[BUSINESS STATEMENT {index:03d}]"
        )

        print_object_fields(
            statement,
            indent=2,
            max_value_length=500,
        )


# ============================================================================
# KNOWLEDGE GRAPH
# ============================================================================

def get_graph_nodes(
    graph: Any,
) -> list:

    if graph is None:
        return []

    method = getattr(
        graph,
        "get_nodes",
        None,
    )

    if callable(method):

        try:
            return as_list(
                method()
            )
        except Exception:
            return []

    return as_list(
        safe_get(
            graph,
            "nodes",
            [],
        )
    )


def get_graph_edges(
    graph: Any,
) -> list:

    if graph is None:
        return []

    method = getattr(
        graph,
        "get_edges",
        None,
    )

    if callable(method):

        try:
            return as_list(
                method()
            )
        except Exception:
            return []

    return as_list(
        safe_get(
            graph,
            "edges",
            [],
        )
    )


def print_knowledge_graph(
    result: Any,
) -> None:

    section(
        "5. KNOWLEDGE GRAPH"
    )

    graph = safe_get(
        result,
        "knowledge_graph",
        None,
    )

    print(
        "Type   :",
        safe_type_name(graph),
    )

    print(
        "Module :",
        safe_module(graph),
    )

    if graph is None:

        print(
            "\nKnowledgeGraph is None."
        )

        return

    nodes = get_graph_nodes(
        graph
    )

    edges = get_graph_edges(
        graph
    )

    print(
        "Nodes:",
        len(nodes),
    )

    print(
        "Edges:",
        len(edges),
    )

    subsection(
        "GRAPH NODE TYPE DISTRIBUTION"
    )

    counts = {}

    for node in nodes:

        kind = str(
            safe_get(
                node,
                "entity_type",
                "unknown",
            )
        ).strip().casefold()

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
            f"{kind:<30}: {count}"
        )

    subsection(
        "ALL KNOWLEDGE GRAPH NODES"
    )

    if not nodes:

        print(
            "NO GRAPH NODES."
        )

    for index, node in enumerate(
        nodes,
        start=1,
    ):

        print_entity(
            node,
            index,
        )

    subsection(
        "ALL KNOWLEDGE GRAPH EDGES"
    )

    if not edges:

        print(
            "NO GRAPH EDGES."
        )

    for index, edge in enumerate(
        edges,
        start=1,
    ):

        print(
            f"\n[EDGE {index:03d}]"
        )

        print_object_fields(
            edge,
            indent=2,
            max_value_length=300,
        )


# ============================================================================
# KNOWLEDGE PROFILE
# ============================================================================

def print_profile_component(
    title: str,
    component: Any,
) -> None:

    subsection(
        title
    )

    if component is None:

        print(
            "None"
        )

        return

    print(
        "Type   :",
        safe_type_name(component),
    )

    print(
        "Module :",
        safe_module(component),
    )

    print(
        "Fields:"
    )

    print_object_fields(
        component,
        indent=2,
        max_value_length=700,
    )


def print_knowledge_profile(
    result: Any,
) -> None:

    section(
        "6. KNOWLEDGE PROFILE — COMPLETE OUTPUT"
    )

    profile = safe_get(
        result,
        "knowledge_profile",
        None,
    )

    if profile is None:

        print(
            "KnowledgeProfile is None."
        )

        return

    print(
        "Type   :",
        safe_type_name(profile),
    )

    print(
        "Module :",
        safe_module(profile),
    )

    print(
        "Confidence:",
        safe_get(
            profile,
            "confidence",
            None,
        ),
    )

    # ------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------

    print_profile_component(
        "6.1 SUMMARY PROFILE",
        safe_get(
            profile,
            "summary",
            None,
        ),
    )

    # ------------------------------------------------------------
    # ENTITIES
    # ------------------------------------------------------------

    print_profile_component(
        "6.2 ENTITY PROFILE",
        safe_get(
            profile,
            "entities",
            None,
        ),
    )

    # ------------------------------------------------------------
    # ACHIEVEMENTS
    # ------------------------------------------------------------

    print_profile_component(
        "6.3 ACHIEVEMENT PROFILE",
        safe_get(
            profile,
            "achievements",
            safe_get(
                profile,
                "achievement",
                None,
            ),
        ),
    )

    # ------------------------------------------------------------
    # LEADERSHIP
    # ------------------------------------------------------------

    print_profile_component(
        "6.4 LEADERSHIP PROFILE",
        safe_get(
            profile,
            "leadership",
            None,
        ),
    )

    # ------------------------------------------------------------
    # SENIORITY
    # ------------------------------------------------------------

    print_profile_component(
        "6.5 SENIORITY PROFILE",
        safe_get(
            profile,
            "seniority",
            None,
        ),
    )

    # ------------------------------------------------------------
    # METRICS
    # ------------------------------------------------------------

    print_profile_component(
        "6.6 METRIC PROFILE",
        safe_get(
            profile,
            "metrics",
            None,
        ),
    )

    # ------------------------------------------------------------
    # DOMAINS
    # ------------------------------------------------------------

    print_profile_component(
        "6.7 DOMAIN PROFILE",
        safe_get(
            profile,
            "domains",
            None,
        ),
    )

    # ------------------------------------------------------------
    # MODIFIERS
    # ------------------------------------------------------------

    print_profile_component(
        "6.8 MODIFIER PROFILE",
        safe_get(
            profile,
            "modifiers",
            None,
        ),
    )

    # ------------------------------------------------------------
    # IMPACT
    # ------------------------------------------------------------

    print_profile_component(
        "6.9 IMPACT PROFILE",
        safe_get(
            profile,
            "impact",
            None,
        ),
    )

    # ------------------------------------------------------------
    # ATS
    # ------------------------------------------------------------

    print_profile_component(
        "6.10 ATS PROFILE",
        safe_get(
            profile,
            "ats",
            None,
        ),
    )

    # ------------------------------------------------------------
    # BUSINESS STATEMENTS
    # ------------------------------------------------------------

    print_profile_component(
        "6.11 BUSINESS STATEMENT PROFILE",
        safe_get(
            profile,
            "business_statements",
            None,
        ),
    )


# ============================================================================
# PROFILE EXECUTIVE SUMMARY
# ============================================================================

def print_executive_summary(
    result: Any,
) -> None:

    section(
        "7. PROFILE EXECUTIVE SUMMARY"
    )

    profile = safe_get(
        result,
        "knowledge_profile",
        None,
    )

    if profile is None:

        print(
            "KnowledgeProfile unavailable."
        )

        return

    summary = safe_get(
        profile,
        "summary",
        None,
    )

    achievements = safe_get(
        profile,
        "achievements",
        safe_get(
            profile,
            "achievement",
            None,
        ),
    )

    leadership = safe_get(
        profile,
        "leadership",
        None,
    )

    seniority = safe_get(
        profile,
        "seniority",
        None,
    )

    metrics = safe_get(
        profile,
        "metrics",
        None,
    )

    domains = safe_get(
        profile,
        "domains",
        None,
    )

    modifiers = safe_get(
        profile,
        "modifiers",
        None,
    )

    impact = safe_get(
        profile,
        "impact",
        None,
    )

    ats = safe_get(
        profile,
        "ats",
        None,
    )

    print(
        "Profile confidence       :",
        safe_get(
            profile,
            "confidence",
            None,
        ),
    )

    print()

    print(
        "Overall score            :",
        safe_get(
            summary,
            "overall_score",
            None,
        ),
    )

    print(
        "Impact score             :",
        safe_get(
            summary,
            "impact_score",
            None,
        ),
    )

    print(
        "ATS score                :",
        safe_get(
            summary,
            "ats_score",
            None,
        ),
    )

    print(
        "Achievement score       :",
        safe_get(
            summary,
            "achievement_score",
            None,
        ),
    )

    print(
        "Leadership score        :",
        safe_get(
            summary,
            "leadership_score",
            None,
        ),
    )

    print(
        "Seniority score         :",
        safe_get(
            summary,
            "seniority_score",
            None,
        ),
    )

    print(
        "Career level             :",
        safe_get(
            summary,
            "career_level",
            None,
        ),
    )

    print()

    print(
        "Achievement count       :",
        safe_get(
            achievements,
            "achievement_count",
            None,
        ),
    )

    print(
        "Quantified achievements :",
        safe_get(
            achievements,
            "quantified_count",
            None,
        ),
    )

    print(
        "Top achievements        :",
        safe_value(
            safe_get(
                achievements,
                "top_achievements",
                [],
            ),
            1000,
        ),
    )

    print()

    print(
        "Leadership level        :",
        safe_get(
            leadership,
            "level",
            None,
        ),
    )

    print(
        "Executive actions       :",
        safe_get(
            leadership,
            "executive_actions",
            None,
        ),
    )

    print()

    print(
        "Seniority level         :",
        safe_get(
            seniority,
            "level",
            None,
        ),
    )

    print(
        "Seniority indicators    :",
        safe_value(
            safe_get(
                seniority,
                "indicators",
                [],
            ),
            1000,
        ),
    )

    print()

    print(
        "Total metrics           :",
        safe_get(
            metrics,
            "total_metrics",
            None,
        ),
    )

    print(
        "Positive metrics        :",
        safe_get(
            metrics,
            "positive_metrics",
            None,
        ),
    )

    print(
        "Negative metrics        :",
        safe_get(
            metrics,
            "negative_metrics",
            None,
        ),
    )

    print(
        "Increase metrics        :",
        safe_get(
            metrics,
            "increase_metrics",
            None,
        ),
    )

    print(
        "Decrease metrics        :",
        safe_get(
            metrics,
            "decrease_metrics",
            None,
        ),
    )

    print()

    print(
        "Domains                 :",
        safe_value(
            safe_get(
                domains,
                "domains",
                {},
            ),
            1000,
        ),
    )

    print(
        "Business areas          :",
        safe_value(
            safe_get(
                domains,
                "business_areas",
                {},
            ),
            1000,
        ),
    )

    print()

    print(
        "Total modifiers         :",
        safe_get(
            modifiers,
            "total_modifiers",
            None,
        ),
    )

    print(
        "Executive modifiers     :",
        safe_get(
            modifiers,
            "executive_modifiers",
            None,
        ),
    )

    print()

    print(
        "Total impact            :",
        safe_get(
            impact,
            "total_impact",
            None,
        ),
    )

    print(
        "Average impact          :",
        safe_get(
            impact,
            "average_impact",
            None,
        ),
    )

    print(
        "Maximum impact          :",
        safe_get(
            impact,
            "maximum_impact",
            None,
        ),
    )

    print()

    print(
        "ATS entity count        :",
        safe_get(
            ats,
            "entity_count",
            None,
        ),
    )

    print(
        "ATS matched entities    :",
        safe_value(
            safe_get(
                ats,
                "matched_entities",
                [],
            ),
            1000,
        ),
    )


# ============================================================================
# RAW PIPELINE STATISTICS
# ============================================================================

def print_statistics(
    result: Any,
) -> None:

    section(
        "8. FINAL PIPELINE STATISTICS"
    )

    statistics = safe_get(
        result,
        "statistics",
        {},
    )

    if not isinstance(
        statistics,
        dict,
    ):

        print(
            "Statistics unavailable."
        )

        return

    for key, value in statistics.items():

        print(
            f"{key:<40}: "
            f"{safe_value(value, 500)}"
        )

    # ------------------------------------------------------------
    # Also print direct result counts
    # ------------------------------------------------------------

    print()

    resume_text = safe_get(
        result,
        "resume_text",
        "",
    )

    document = safe_get(
        result,
        "knowledge_document",
        None,
    )

    semantic_entities = as_list(
        safe_get(
            result,
            "semantic_entities",
            [],
        )
    )

    statements = as_list(
        safe_get(
            result,
            "business_statements",
            [],
        )
    )

    graph = safe_get(
        result,
        "knowledge_graph",
        None,
    )

    profile = safe_get(
        result,
        "knowledge_profile",
        None,
    )

    print(
        "Resume characters        :",
        len(resume_text),
    )

    print(
        "Knowledge sentences      :",
        len(
            as_list(
                safe_get(
                    document,
                    "sentences",
                    [],
                )
            )
        ),
    )

    print(
        "Knowledge facts          :",
        len(
            as_list(
                safe_get(
                    document,
                    "facts",
                    [],
                )
            )
        ),
    )

    print(
        "Extracted entities       :",
        len(
            as_list(
                safe_get(
                    result,
                    "extracted_entities",
                    [],
                )
            )
        ),
    )

    print(
        "Semantic entities        :",
        len(
            semantic_entities
        ),
    )

    print(
        "Semantic dependencies    :",
        len(
            as_list(
                safe_get(
                    result,
                    "semantic_dependencies",
                    [],
                )
            )
        ),
    )

    print(
        "Business statements      :",
        len(statements),
    )

    print(
        "KnowledgeGraph nodes     :",
        len(
            get_graph_nodes(
                graph
            )
        ),
    )

    print(
        "KnowledgeGraph edges     :",
        len(
            get_graph_edges(
                graph
            )
        ),
    )

    print(
        "KnowledgeProfile         :",
        "YES" if profile is not None else "NO",
    )

    print(
        "KnowledgeProfile score   :",
        safe_get(
            safe_get(
                profile,
                "summary",
                None,
            ),
            "overall_score",
            None,
        ),
    )


# ============================================================================
# DATA LOSS ANALYSIS
# ============================================================================

def print_data_flow_analysis(
    result: Any,
) -> None:

    section(
        "9. DATA FLOW ANALYSIS"
    )

    document = safe_get(
        result,
        "knowledge_document",
        None,
    )

    facts = as_list(
        safe_get(
            document,
            "facts",
            [],
        )
    )

    interpretation = get_main_interpretation(
        result
    )

    semantic_entities = as_list(
        safe_get(
            interpretation,
            "entities",
            [],
        )
    )

    relations = as_list(
        safe_get(
            interpretation,
            "relations",
            [],
        )
    )

    dependencies = as_list(
        safe_get(
            interpretation,
            "dependencies",
            [],
        )
    )

    statements = as_list(
        safe_get(
            result,
            "business_statements",
            [],
        )
    )

    graph = safe_get(
        result,
        "knowledge_graph",
        None,
    )

    nodes = get_graph_nodes(
        graph
    )

    edges = get_graph_edges(
        graph
    )

    profile = safe_get(
        result,
        "knowledge_profile",
        None,
    )

    print(
        "KnowledgeDocument facts       :",
        len(facts),
    )

    print(
        "Semantic entities             :",
        len(semantic_entities),
    )

    print(
        "Semantic relations            :",
        len(relations),
    )

    print(
        "Semantic dependencies         :",
        len(dependencies),
    )

    print(
        "Business statements           :",
        len(statements),
    )

    print(
        "KnowledgeGraph nodes          :",
        len(nodes),
    )

    print(
        "KnowledgeGraph edges          :",
        len(edges),
    )

    print(
        "KnowledgeProfile              :",
        "AVAILABLE"
        if profile is not None
        else "MISSING",
    )

    print()

    print(
        "DATA FLOW:"
    )

    print(
        f"  Facts              {len(facts):>5}"
        "  → Semantic entities"
        f" {len(semantic_entities):>5}"
    )

    print(
        f"  Semantic entities  {len(semantic_entities):>5}"
        "  → Relations"
        f"         {len(relations):>5}"
    )

    print(
        f"  Relations          {len(relations):>5}"
        "  → Statements"
        f"       {len(statements):>5}"
    )

    print(
        f"  Statements         {len(statements):>5}"
        "  → Graph nodes"
        f"       {len(nodes):>5}"
    )

    print(
        f"  Graph nodes        {len(nodes):>5}"
        "  → Profile"
        f"           "
        f"{'AVAILABLE' if profile else 'EMPTY'}"
    )

    print()

    # ------------------------------------------------------------
    # Diagnostic interpretation
    # ------------------------------------------------------------

    if semantic_entities and not statements:

        print(
            "WARNING:"
        )

        print(
            "Semantic resolution is producing entities, "
            "but BusinessStatementBuilder is producing ZERO statements."
        )

        print(
            "This is the first major information-loss point."
        )

    if statements and not nodes:

        print(
            "WARNING:"
        )

        print(
            "Business statements exist, but KnowledgeGraph "
            "contains no usable nodes."
        )

    if nodes and profile:

        print(
            "KnowledgeGraph → KnowledgeProfile "
            "data flow is populated."
        )

    if not nodes:

        print(
            "KnowledgeGraph currently contains no useful "
            "semantic entity nodes."
        )

    if profile:

        profile_confidence = safe_get(
            profile,
            "confidence",
            0.0,
        )

        if not profile_confidence:

            print(
                "WARNING: KnowledgeProfile exists but "
                "confidence is 0."
            )


# ============================================================================
# RAW ENTITY LIST BY TYPE
# ============================================================================

def print_entities_grouped_by_type(
    result: Any,
) -> None:

    section(
        "10. ENTITIES GROUPED BY TYPE"
    )

    interpretation = get_main_interpretation(
        result
    )

    entities = as_list(
        safe_get(
            interpretation,
            "entities",
            [],
        )
    )

    groups = {}

    for entity in entities:

        kind = str(
            safe_get(
                entity,
                "entity_type",
                "unknown",
            )
        ).strip()

        groups.setdefault(
            kind,
            [],
        ).append(
            entity
        )

    for kind in sorted(
        groups
    ):

        group = groups[kind]

        print()
        print(
            f"{kind.upper()} "
            f"({len(group)})"
        )

        print(
            "-" * 70
        )

        for entity in group:

            print(
                f"  {safe_get(entity, 'entity_id', '')}"
                f" | "
                f"{safe_get(entity, 'canonical', '')}"
                f" | confidence="
                f"{safe_get(entity, 'confidence', None)}"
            )


# ============================================================================
# MAIN
# ============================================================================

def test_enterprise_resume_pipeline():

    banner(
        "ENTERPRISE RESUME → KNOWLEDGE PROFILE DIAGNOSTIC"
    )

    print(
        "\nRunning complete enterprise diagnostic..."
    )

    # ----------------------------------------------------------------
    # IMPORT DIAGNOSTICS
    # ----------------------------------------------------------------

    section(
        "IMPORT DIAGNOSTICS"
    )

    try:

        from app.intelligence.utilities.knowledge.semantic_reasoning.business_statement_builder import (
            BusinessStatementBuilder,
        )

        print(
            "[PASS] BusinessStatementBuilder imported:"
        )

        print(
            "  Class  :",
            BusinessStatementBuilder,
        )

        print(
            "  Module :",
            BusinessStatementBuilder.__module__,
        )

        try:

            builder = BusinessStatementBuilder()

            print(
                "[PASS] BusinessStatementBuilder instantiated."
            )

            print(
                "  Builder class   :",
                type(builder).__name__,
            )

            print(
                "  Builder methods :",
                [
                    name
                    for name in dir(builder)
                    if not name.startswith("_")
                ],
            )

        except Exception as exc:

            print(
                "[WARNING] Could not instantiate "
                "BusinessStatementBuilder:"
            )

            print(
                repr(exc)
            )

    except Exception as exc:

        print(
            "[FAIL] BusinessStatementBuilder import:"
        )

        print(
            repr(exc)
        )

    try:

        from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.knowledge_profile_builder import (
            KnowledgeProfileBuilder,
        )

        print(
            "\n[PASS] KnowledgeProfileBuilder imported:"
        )

        print(
            "  Class  :",
            KnowledgeProfileBuilder,
        )

        print(
            "  Module :",
            KnowledgeProfileBuilder.__module__,
        )

    except Exception as exc:

        print(
            "\n[FAIL] KnowledgeProfileBuilder import:"
        )

        print(
            repr(exc)
        )

    # ----------------------------------------------------------------
    # PIPELINE
    # ----------------------------------------------------------------

    try:

        pipeline = EnterpriseResumePipeline()

        print()
        print(
            "Pipeline class :",
            type(pipeline).__name__,
        )

        print(
            "Pipeline module:",
            type(pipeline).__module__,
        )

        print(
            "\nExecuting pipeline..."
        )

        result = pipeline.run(
            TEST_RESUME
        )

        # ------------------------------------------------------------
        # PRINT EVERYTHING
        # ------------------------------------------------------------

        print_pipeline_result(
            result
        )

        print_pipeline_stages(
            result
        )

        print_knowledge_document(
            result
        )

        print_semantic_interpretation(
            result
        )

        print_entity_distribution(
            result
        )

        print_business_statements(
            result
        )

        print_knowledge_graph(
            result
        )

        print_knowledge_profile(
            result
        )

        print_executive_summary(
            result
        )

        print_statistics(
            result
        )

        print_data_flow_analysis(
            result
        )

        print_entities_grouped_by_type(
            result
        )

        # ------------------------------------------------------------
        # COMPLETE
        # ------------------------------------------------------------

        banner(
            "ENTERPRISE PIPELINE DIAGNOSTIC COMPLETE"
        )

        print(
            "\nPipeline execution finished."
        )

        print(
            "The diagnostic intentionally does not fail "
            "because downstream objects are empty."
        )

        return result

    except Exception as exc:

        banner(
            "ENTERPRISE PIPELINE EXECUTION FAILED"
        )

        print(
            "\nException type:",
            type(exc).__name__,
        )

        print(
            "Exception:",
            str(exc),
        )

        print(
            "\nTraceback:"
        )

        traceback.print_exc()

        raise


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":

    test_enterprise_resume_pipeline()