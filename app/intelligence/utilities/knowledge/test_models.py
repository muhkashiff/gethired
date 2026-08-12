from pathlib import Path
import sys


# =====================================================================
# PROJECT ROOT
# =====================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[4]


if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )

"""
BusinessStatementBuilder Regression Test

Enterprise V12

Purpose
-------
Verify that BusinessStatementBuilder remains compatible
after the recent Enterprise pipeline upgrades.

Contract under test:

SemanticEntity + SemanticDependency
                ↓
      BusinessStatementBuilder
                ↓
        list[BusinessStatement]

This test intentionally does NOT involve:
- KnowledgeGraph
- KnowledgeGraphBuilder
- Reasoners
- Pipeline
- ProfileBuilder

The BusinessStatementBuilder must work independently.
"""

from app.intelligence.utilities.knowledge.semantic_reasoning.business_statement_builder import (
    BusinessStatementBuilder,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticEntity,
    SemanticDependency,
)


# ==============================================================
# TEST HELPERS
# ==============================================================


def make_entity(
    entity_id,
    entity_type,
    canonical,
    statement_id="STATEMENT_1",
    category="",
    business_area="",
    confidence=0.95,
):
    """
    Create a minimal SemanticEntity compatible with the
    current BusinessStatementBuilder contract.
    """

    return SemanticEntity(
        entity_id=entity_id,
        entity_type=entity_type,
        canonical=canonical,
        original=canonical,
        matched_text=canonical,
        category=category,
        business_area=business_area,
        confidence=confidence,
        statement_id=statement_id,
        metadata={
            "primary_domain": business_area,
        },
    )


def make_dependency(
    source_entity,
    target_entity,
    dependency_type="RELATES_TO",
    confidence=0.90,
):
    """
    Create a minimal SemanticDependency.

    Adjust the constructor fields here only if the current
    SemanticDependency model uses different names.
    """

    return SemanticDependency(
        source_entity=source_entity,
        target_entity=target_entity,
        dependency_type=dependency_type,
        confidence=confidence,
    )


# ==============================================================
# TEST 1
# BASIC BUSINESS STATEMENT CREATION
# ==============================================================


def test_business_statement_builder_creates_statement():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
        ),

        make_entity(
            "METRIC_1",
            "metric",
            "yield",
        ),

        make_entity(
            "MEASUREMENT_1",
            "measurement",
            "99%",
        ),

    ]

    dependencies = [

        make_dependency(
            "ACTION_1",
            "METRIC_1",
        ),

        make_dependency(
            "METRIC_1",
            "MEASUREMENT_1",
        ),

    ]

    statements = builder.build(
        entities=entities,
        dependencies=dependencies,
    )

    # ----------------------------------------------------------
    # Output contract
    # ----------------------------------------------------------

    assert isinstance(
        statements,
        list,
    )

    assert len(statements) == 1

    statement = statements[0]

    # ----------------------------------------------------------
    # Statement identity
    # ----------------------------------------------------------

    assert statement.statement_id == "STATEMENT_1"

    # ----------------------------------------------------------
    # Entities
    # ----------------------------------------------------------

    assert len(statement.entities) == 3

    entity_ids = {
        entity.entity_id
        for entity in statement.entities
    }

    assert entity_ids == {
        "ACTION_1",
        "METRIC_1",
        "MEASUREMENT_1",
    }


# ==============================================================
# TEST 2
# ACTION → METRIC RELATION
# ==============================================================


def test_action_metric_relation_is_created():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
        ),

        make_entity(
            "METRIC_1",
            "metric",
            "yield",
        ),

    ]

    dependencies = []

    statements = builder.build(
        entities=entities,
        dependencies=dependencies,
    )

    statement = statements[0]

    relations = statement.relations

    assert len(relations) >= 1

    matching = [

        relation

        for relation in relations

        if (
            relation.source_id == "ACTION_1"
            and relation.target_id == "METRIC_1"
            and relation.relation_type == "AFFECTS"
        )
    ]

    assert len(matching) == 1


# ==============================================================
# TEST 3
# METRIC → MEASUREMENT
# ==============================================================


def test_metric_measurement_relation_is_created():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "METRIC_1",
            "metric",
            "yield",
        ),

        make_entity(
            "MEASUREMENT_1",
            "measurement",
            "99%",
        ),

    ]

    statements = builder.build(
        entities=entities,
        dependencies=[],
    )

    statement = statements[0]

    matching = [

        relation

        for relation in statement.relations

        if (
            relation.source_id == "METRIC_1"
            and relation.target_id == "MEASUREMENT_1"
            and relation.relation_type == "MEASURED_BY"
        )
    ]

    assert len(matching) == 1


# ==============================================================
# TEST 4
# ACTION → SKILL
# ==============================================================


def test_action_skill_relation_is_created():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "implemented",
        ),

        make_entity(
            "SKILL_1",
            "skill",
            "HACCP",
            category="Food Safety",
            business_area="Quality",
        ),

    ]

    statements = builder.build(
        entities=entities,
        dependencies=[],
    )

    statement = statements[0]

    matching = [

        relation

        for relation in statement.relations

        if (
            relation.source_id == "ACTION_1"
            and relation.target_id == "SKILL_1"
            and relation.relation_type == "REQUIRES"
        )
    ]

    assert len(matching) == 1


# ==============================================================
# TEST 5
# ACTION → STANDARD
# ==============================================================


def test_action_standard_relation_is_created():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "implemented",
        ),

        make_entity(
            "STANDARD_1",
            "standard",
            "FSSC 22000",
        ),

    ]

    statements = builder.build(
        entities=entities,
        dependencies=[],
    )

    statement = statements[0]

    matching = [

        relation

        for relation in statement.relations

        if (
            relation.source_id == "ACTION_1"
            and relation.target_id == "STANDARD_1"
            and relation.relation_type == "COMPLIES_WITH"
        )
    ]

    assert len(matching) == 1


# ==============================================================
# TEST 6
# ACTION → METHODOLOGY
# ==============================================================


def test_action_methodology_relation_is_created():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
        ),

        make_entity(
            "METHOD_1",
            "methodology",
            "Six Sigma",
        ),

    ]

    statements = builder.build(
        entities=entities,
        dependencies=[],
    )

    statement = statements[0]

    matching = [

        relation

        for relation in statement.relations

        if (
            relation.source_id == "ACTION_1"
            and relation.target_id == "METHOD_1"
            and relation.relation_type == "USES"
        )
    ]

    assert len(matching) == 1


# ==============================================================
# TEST 7
# ACTION → DOMAIN
# ==============================================================


def test_action_domain_relation_is_created():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
        ),

        make_entity(
            "DOMAIN_1",
            "domain",
            "Food Manufacturing",
            business_area="Quality Assurance",
        ),

    ]

    statements = builder.build(
        entities=entities,
        dependencies=[],
    )

    statement = statements[0]

    matching = [

        relation

        for relation in statement.relations

        if (
            relation.source_id == "ACTION_1"
            and relation.target_id == "DOMAIN_1"
            and relation.relation_type == "BELONGS_TO"
        )
    ]

    assert len(matching) == 1


# ==============================================================
# TEST 8
# MULTIPLE STATEMENTS MUST REMAIN SEPARATE
# ==============================================================


def test_entities_are_grouped_by_statement():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
            statement_id="STATEMENT_1",
        ),

        make_entity(
            "METRIC_1",
            "metric",
            "yield",
            statement_id="STATEMENT_1",
        ),

        make_entity(
            "ACTION_2",
            "action",
            "implemented",
            statement_id="STATEMENT_2",
        ),

        make_entity(
            "STANDARD_2",
            "standard",
            "FSSC 22000",
            statement_id="STATEMENT_2",
        ),

    ]

    statements = builder.build(
        entities=entities,
        dependencies=[],
    )

    assert len(statements) == 2

    statements_by_id = {

        statement.statement_id: statement

        for statement in statements

    }

    assert set(statements_by_id) == {
        "STATEMENT_1",
        "STATEMENT_2",
    }

    statement_1_ids = {
        entity.entity_id
        for entity in statements_by_id[
            "STATEMENT_1"
        ].entities
    }

    statement_2_ids = {
        entity.entity_id
        for entity in statements_by_id[
            "STATEMENT_2"
        ].entities
    }

    assert statement_1_ids == {
        "ACTION_1",
        "METRIC_1",
    }

    assert statement_2_ids == {
        "ACTION_2",
        "STANDARD_2",
    }


# ==============================================================
# TEST 9
# STATEMENT METADATA
# ==============================================================


def test_statement_metadata_is_populated():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
        ),

        make_entity(
            "METRIC_1",
            "metric",
            "yield",
        ),

        make_entity(
            "MEASUREMENT_1",
            "measurement",
            "99%",
        ),

        make_entity(
            "DOMAIN_1",
            "domain",
            "Food Manufacturing",
            business_area="Quality",
        ),

    ]

    statements = builder.build(
        entities=entities,
        dependencies=[],
    )

    statement = statements[0]

    # Label should contain action + target where available.
    assert statement.label

    # Metric should cause measured action classification.
    assert statement.semantic_type == "Measured Action"

    # Measurement should identify this as an achievement.
    assert statement.achievement is True

    # Domain should populate primary domain.
    assert statement.primary_domain == "Food Manufacturing"

    # Business area should be inherited from domain.
    assert statement.business_area == "Quality"


# ==============================================================
# TEST 10
# RELATION CONFIDENCE
# ==============================================================


def test_relation_confidence_uses_lower_entity_confidence():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
            confidence=0.95,
        ),

        make_entity(
            "METRIC_1",
            "metric",
            "yield",
            confidence=0.70,
        ),

    ]

    statements = builder.build(
        entities=entities,
        dependencies=[],
    )

    statement = statements[0]

    relation = next(

        relation

        for relation in statement.relations

        if relation.relation_type == "AFFECTS"

    )

    assert relation.confidence == 0.70


# ==============================================================
# TEST 11
# EMPTY INPUT
# ==============================================================


def test_empty_input_returns_empty_list():

    builder = BusinessStatementBuilder()

    statements = builder.build(
        entities=[],
        dependencies=[],
    )

    assert isinstance(
        statements,
        list,
    )

    assert statements == []


# ==============================================================
# TEST 12
# DUPLICATE RELATION PROTECTION
# ==============================================================


def test_duplicate_relations_are_not_created():

    builder = BusinessStatementBuilder()

    action = make_entity(
        "ACTION_1",
        "action",
        "improved",
    )

    metric = make_entity(
        "METRIC_1",
        "metric",
        "yield",
    )

    statement = builder.build(
        entities=[
            action,
            metric,
        ],
        dependencies=[],
    )[0]

    matching = [

        relation

        for relation in statement.relations

        if (
            relation.source_id == "ACTION_1"
            and relation.target_id == "METRIC_1"
            and relation.relation_type == "AFFECTS"
        )
    ]

    assert len(matching) == 1


# ==============================================================
# TEST 13
# OBJECT → OBJECT RELATION SHOULD NOT BE INVENTED
# ==============================================================


def test_builder_does_not_invent_object_object_relation():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "OBJECT_1",
            "object",
            "production line",
        ),

        make_entity(
            "OBJECT_2",
            "object",
            "bottling line",
        ),

    ]

    statements = builder.build(
        entities=entities,
        dependencies=[],
    )

    statement = statements[0]

    assert statement.relations == []


# ==============================================================
# TEST 14
# BUSINESS STATEMENT OUTPUT CONTRACT
# ==============================================================


def test_output_contract():

    builder = BusinessStatementBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
        ),

        make_entity(
            "METRIC_1",
            "metric",
            "yield",
        ),

    ]

    statements = builder.build(
        entities=entities,
        dependencies=[],
    )

    assert statements

    statement = statements[0]

    # BusinessStatement contract
    assert hasattr(
        statement,
        "statement_id",
    )

    assert hasattr(
        statement,
        "entities",
    )

    assert hasattr(
        statement,
        "relations",
    )

    assert hasattr(
        statement,
        "label",
    )

    assert hasattr(
        statement,
        "semantic_type",
    )

    assert hasattr(
        statement,
        "primary_domain",
    )

    assert hasattr(
        statement,
        "business_area",
    )

    assert hasattr(
        statement,
        "achievement",
    )

    # Relation contract
    if statement.relations:

        relation = statement.relations[0]

        assert hasattr(
            relation,
            "source_id",
        )

        assert hasattr(
            relation,
            "target_id",
        )

        assert hasattr(
            relation,
            "relation_type",
        )

        assert hasattr(
            relation,
            "confidence",
        )

        assert hasattr(
            relation,
            "reasoning",
        )

        assert hasattr(
            relation,
            "metadata",
        )


# ==============================================================
# MANUAL RUNNER
# ==============================================================


if __name__ == "__main__":

    tests = [

        test_business_statement_builder_creates_statement,

        test_action_metric_relation_is_created,

        test_metric_measurement_relation_is_created,

        test_action_skill_relation_is_created,

        test_action_standard_relation_is_created,

        test_action_methodology_relation_is_created,

        test_action_domain_relation_is_created,

        test_entities_are_grouped_by_statement,

        test_statement_metadata_is_populated,

        test_relation_confidence_uses_lower_entity_confidence,

        test_empty_input_returns_empty_list,

        test_duplicate_relations_are_not_created,

        test_builder_does_not_invent_object_object_relation,

        test_output_contract,

    ]

    passed = 0

    failed = 0

    print()
    print("=" * 70)
    print("BUSINESS STATEMENT BUILDER REGRESSION TEST")
    print("=" * 70)

    for test in tests:

        try:

            test()

            print(
                f"PASS  {test.__name__}"
            )

            passed += 1

        except Exception as exc:

            print(
                f"FAIL  {test.__name__}"
            )

            print(
                f"      {type(exc).__name__}: {exc}"
            )

            failed += 1

    print()
    print("=" * 70)
    print(
        f"PASSED : {passed}"
    )
    print(
        f"FAILED : {failed}"
    )
    print("=" * 70)

    if failed:

        raise SystemExit(1)

