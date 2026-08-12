"""
Enterprise Knowledge Graph Builder Regression Test

Enterprise V8

Purpose
-------

Verify that KnowledgeGraphBuilder correctly converts:

BusinessStatement
        ↓
GraphNode
        ↓
GraphEdge
        ↓
KnowledgeGraphBuildResult

This test intentionally does NOT involve:

- DependencyResolver
- SemanticRelationExtractor
- BusinessStatementBuilder
- KnowledgeGraphReasoners
- ProfileBuilder
- Full Enterprise Pipeline

The KnowledgeGraphBuilder must work independently.

Critical compatibility checks:

• SemanticEntity → GraphNode
• StatementRelation → GraphEdge
• KPI remains KPI
• BKPI remains BKPI
• metric remains metric
• measurement remains measurement
• confidence is preserved
• reasoning is preserved
• metadata is preserved
• duplicate nodes are protected
• duplicate relations are protected
• statements remain separate
• invalid relations are ignored
• empty input is supported
"""

from pathlib import Path
import sys


# =====================================================================
# PROJECT ROOT
# =====================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[4]

if str(PROJECT_ROOT) not in sys.path:

    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


# =====================================================================
# IMPORTS
# =====================================================================

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticEntity,
    StatementRelation,
    BusinessStatement,
)

from app.intelligence.utilities.knowledge.knowledge_graph.knowledge_graph_builder import (
    KnowledgeGraphBuilder,
)


# =====================================================================
# TEST HELPERS
# =====================================================================

def make_entity(
    entity_id,
    entity_type,
    canonical,
    statement_id="STATEMENT_1",
    category="",
    business_area="",
    confidence=0.95,
    ontology_name="",
    metadata=None,
):
    """
    Create a minimal SemanticEntity compatible with
    the current KnowledgeGraphBuilder contract.
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
        ontology_name=ontology_name,
        metadata=metadata or {},
    )


def make_relation(
    source_id,
    target_id,
    relation_type,
    confidence=0.90,
    reasoning="",
    metadata=None,
):
    """
    Create a minimal StatementRelation.
    """

    return StatementRelation(
        source_id=source_id,
        target_id=target_id,
        relation_type=relation_type,
        confidence=confidence,
        reasoning=reasoning,
        metadata=metadata or {},
    )


def make_statement(
    statement_id,
    entities,
    relations=None,
):
    """
    Create a minimal BusinessStatement.
    """

    statement = BusinessStatement()

    statement.statement_id = statement_id

    statement.entities.extend(
        entities
    )

    if relations:

        statement.relations.extend(
            relations
        )

    return statement


class MockSemanticResolution:

    """
    Minimal SemanticResolution-compatible object.

    KnowledgeGraphBuilder only needs:

        business_statements
    """

    def __init__(
        self,
        business_statements,
    ):

        self.business_statements = (
            business_statements
        )


# =====================================================================
# TEST 1
# BASIC GRAPH CREATION
# =====================================================================

def test_basic_graph_creation():

    builder = KnowledgeGraphBuilder()

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

    relation = make_relation(
        "ACTION_1",
        "METRIC_1",
        "AFFECTS",
        confidence=0.90,
        reasoning="improved affects yield",
    )

    statement = make_statement(
        "STATEMENT_1",
        entities,
        [relation],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    result = builder.build(
        resolution
    )

    assert result is not None

    assert result.graph is not None

    assert builder.node_count == 2

    assert builder.edge_count == 1


# =====================================================================
# TEST 2
# BUSINESS STATEMENT → GRAPH NODES
# =====================================================================

def test_entities_become_graph_nodes():

    builder = KnowledgeGraphBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
        ),

        make_entity(
            "KPI_1",
            "kpi",
            "yield",
        ),

        make_entity(
            "BKPI_1",
            "bkpi",
            "production efficiency",
        ),

        make_entity(
            "METRIC_1",
            "metric",
            "production rate",
        ),

        make_entity(
            "MEASUREMENT_1",
            "measurement",
            "99%",
        ),

    ]

    statement = make_statement(
        "STATEMENT_1",
        entities,
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    nodes = builder.get_nodes()

    assert len(nodes) == 5

    node_ids = {
        node.node_id
        for node in nodes
    }

    assert node_ids == {
        "ACTION_1",
        "KPI_1",
        "BKPI_1",
        "METRIC_1",
        "MEASUREMENT_1",
    }


# =====================================================================
# TEST 3
# KPI AND BKPI MUST REMAIN DISTINCT
# =====================================================================

def test_kpi_and_bkpi_remain_distinct():

    builder = KnowledgeGraphBuilder()

    kpi = make_entity(
        "KPI_1",
        "kpi",
        "yield",
    )

    bkpi = make_entity(
        "BKPI_1",
        "bkpi",
        "production efficiency",
    )

    statement = make_statement(
        "STATEMENT_1",
        [
            kpi,
            bkpi,
        ],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    kpi_node = builder.get_node(
        "KPI_1"
    )

    bkpi_node = builder.get_node(
        "BKPI_1"
    )

    assert kpi_node is not None

    assert bkpi_node is not None

    assert kpi_node.entity_type == "kpi"

    assert bkpi_node.entity_type == "bkpi"

    assert kpi_node.entity_type != (
        bkpi_node.entity_type
    )


# =====================================================================
# TEST 4
# METRIC MUST REMAIN DISTINCT FROM KPI/BKPI
# =====================================================================

def test_metric_remains_distinct():

    builder = KnowledgeGraphBuilder()

    entities = [

        make_entity(
            "KPI_1",
            "kpi",
            "yield",
        ),

        make_entity(
            "BKPI_1",
            "bkpi",
            "production efficiency",
        ),

        make_entity(
            "METRIC_1",
            "metric",
            "production rate",
        ),

    ]

    statement = make_statement(
        "STATEMENT_1",
        entities,
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    assert (
        builder.get_node(
            "KPI_1"
        ).entity_type
        == "kpi"
    )

    assert (
        builder.get_node(
            "BKPI_1"
        ).entity_type
        == "bkpi"
    )

    assert (
        builder.get_node(
            "METRIC_1"
        ).entity_type
        == "metric"
    )


# =====================================================================
# TEST 5
# MEASUREMENT NODE
# =====================================================================

def test_measurement_becomes_graph_node():

    builder = KnowledgeGraphBuilder()

    measurement = make_entity(
        "MEASUREMENT_1",
        "measurement",
        "99%",
    )

    statement = make_statement(
        "STATEMENT_1",
        [
            measurement,
        ],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    node = builder.get_node(
        "MEASUREMENT_1"
    )

    assert node is not None

    assert node.entity_type == (
        "measurement"
    )

    assert node.canonical == "99%"


# =====================================================================
# TEST 6
# STATEMENT RELATION → GRAPH EDGE
# =====================================================================

def test_statement_relation_becomes_graph_edge():

    builder = KnowledgeGraphBuilder()

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

    relation = make_relation(
        "ACTION_1",
        "METRIC_1",
        "AFFECTS",
        confidence=0.85,
        reasoning="improved affects yield",
    )

    statement = make_statement(
        "STATEMENT_1",
        [
            action,
            metric,
        ],
        [
            relation,
        ],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    edges = builder.get_edges()

    assert len(edges) == 1

    edge = edges[0]

    assert edge.source_id == (
        "ACTION_1"
    )

    assert edge.target_id == (
        "METRIC_1"
    )

    assert edge.relation == (
        "AFFECTS"
    )


# =====================================================================
# TEST 7
# EDGE CONFIDENCE
# =====================================================================

def test_edge_confidence_is_preserved():

    builder = KnowledgeGraphBuilder()

    action = make_entity(
        "ACTION_1",
        "action",
        "improved",
        confidence=0.95,
    )

    metric = make_entity(
        "METRIC_1",
        "metric",
        "yield",
        confidence=0.70,
    )

    relation = make_relation(
        "ACTION_1",
        "METRIC_1",
        "AFFECTS",
        confidence=0.70,
    )

    statement = make_statement(
        "STATEMENT_1",
        [
            action,
            metric,
        ],
        [
            relation,
        ],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    edge = builder.get_edges()[0]

    assert edge.confidence == 0.70


# =====================================================================
# TEST 8
# EDGE REASONING
# =====================================================================

def test_edge_reasoning_is_preserved():

    builder = KnowledgeGraphBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
        ),

        make_entity(
            "KPI_1",
            "kpi",
            "yield",
        ),

    ]

    relation = make_relation(
        "ACTION_1",
        "KPI_1",
        "AFFECTS",
        reasoning=(
            "improved affects yield"
        ),
    )

    statement = make_statement(
        "STATEMENT_1",
        entities,
        [relation],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    edge = builder.get_edges()[0]

    assert edge.reasoning == (
        "improved affects yield"
    )


# =====================================================================
# TEST 9
# NODE METADATA
# =====================================================================

def test_node_metadata_is_preserved():

    builder = KnowledgeGraphBuilder()

    entity = make_entity(
        "KPI_1",
        "kpi",
        "yield",
        metadata={
            "primary_domain": "Manufacturing",
            "test_marker": "KPI_METADATA",
        },
    )

    statement = make_statement(
        "STATEMENT_1",
        [
            entity,
        ],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    node = builder.get_node(
        "KPI_1"
    )

    assert node is not None

    assert node.metadata[
        "test_marker"
    ] == "KPI_METADATA"

    assert node.domain == (
        "Manufacturing"
    )


# =====================================================================
# TEST 10
# EDGE METADATA
# =====================================================================

def test_edge_metadata_is_preserved():

    builder = KnowledgeGraphBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
        ),

        make_entity(
            "KPI_1",
            "kpi",
            "yield",
        ),

    ]

    relation = make_relation(
        "ACTION_1",
        "KPI_1",
        "AFFECTS",
        metadata={
            "origin": "semantic_relation_extractor",
        },
    )

    statement = make_statement(
        "STATEMENT_1",
        entities,
        [
            relation,
        ],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    edge = builder.get_edges()[0]

    assert edge.metadata[
        "origin"
    ] == "semantic_relation_extractor"


# =====================================================================
# TEST 11
# MULTIPLE STATEMENTS
# =====================================================================

def test_multiple_statements_are_built():

    builder = KnowledgeGraphBuilder()

    statement_1 = make_statement(

        "STATEMENT_1",

        [
            make_entity(
                "ACTION_1",
                "action",
                "improved",
                statement_id="STATEMENT_1",
            ),

            make_entity(
                "KPI_1",
                "kpi",
                "yield",
                statement_id="STATEMENT_1",
            ),
        ],

        [
            make_relation(
                "ACTION_1",
                "KPI_1",
                "AFFECTS",
            ),
        ],
    )

    statement_2 = make_statement(

        "STATEMENT_2",

        [
            make_entity(
                "ACTION_2",
                "action",
                "implemented",
                statement_id="STATEMENT_2",
            ),

            make_entity(
                "BKPI_2",
                "bkpi",
                "customer satisfaction",
                statement_id="STATEMENT_2",
            ),
        ],

        [
            make_relation(
                "ACTION_2",
                "BKPI_2",
                "AFFECTS",
            ),
        ],
    )

    resolution = MockSemanticResolution(
        [
            statement_1,
            statement_2,
        ]
    )

    builder.build(
        resolution
    )

    assert builder.node_count == 4

    assert builder.edge_count == 2


# =====================================================================
# TEST 12
# INVALID RELATION IS IGNORED
# =====================================================================

def test_invalid_relation_is_ignored():

    builder = KnowledgeGraphBuilder()

    action = make_entity(
        "ACTION_1",
        "action",
        "improved",
    )

    relation = make_relation(
        "ACTION_1",
        "DOES_NOT_EXIST",
        "AFFECTS",
    )

    statement = make_statement(
        "STATEMENT_1",
        [
            action,
        ],
        [
            relation,
        ],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    assert builder.node_count == 1

    assert builder.edge_count == 0


# =====================================================================
# TEST 13
# DUPLICATE NODE PROTECTION
# =====================================================================

def test_duplicate_nodes_are_not_created():

    builder = KnowledgeGraphBuilder()

    entity_1 = make_entity(
        "KPI_1",
        "kpi",
        "yield",
    )

    entity_2 = make_entity(
        "KPI_1",
        "kpi",
        "yield",
    )

    statement = make_statement(
        "STATEMENT_1",
        [
            entity_1,
            entity_2,
        ],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    assert builder.node_count == 1


# =====================================================================
# TEST 14
# DUPLICATE RELATION PROTECTION
# =====================================================================

def test_duplicate_edges_are_not_created():

    builder = KnowledgeGraphBuilder()

    entities = [

        make_entity(
            "ACTION_1",
            "action",
            "improved",
        ),

        make_entity(
            "KPI_1",
            "kpi",
            "yield",
        ),

    ]

    relation_1 = make_relation(
        "ACTION_1",
        "KPI_1",
        "AFFECTS",
    )

    relation_2 = make_relation(
        "ACTION_1",
        "KPI_1",
        "AFFECTS",
    )

    statement = make_statement(
        "STATEMENT_1",
        entities,
        [
            relation_1,
            relation_2,
        ],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    assert builder.edge_count == 1


# =====================================================================
# TEST 15
# EMPTY INPUT
# =====================================================================

def test_empty_input():

    builder = KnowledgeGraphBuilder()

    resolution = MockSemanticResolution(
        []
    )

    result = builder.build(
        resolution
    )

    assert result is not None

    assert result.graph is not None

    assert builder.node_count == 0

    assert builder.edge_count == 0


# =====================================================================
# TEST 16
# NONE INPUT
# =====================================================================

def test_none_input():

    builder = KnowledgeGraphBuilder()

    result = builder.build(
        None
    )

    assert result is not None

    assert result.graph is not None

    assert builder.node_count == 0

    assert builder.edge_count == 0


# =====================================================================
# TEST 17
# RESET
# =====================================================================

def test_reset():

    builder = KnowledgeGraphBuilder()

    entity = make_entity(
        "KPI_1",
        "kpi",
        "yield",
    )

    statement = make_statement(
        "STATEMENT_1",
        [
            entity,
        ],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    builder.build(
        resolution
    )

    assert builder.node_count == 1

    builder.reset()

    assert builder.node_count == 0

    assert builder.edge_count == 0

    assert builder.graph is None


# =====================================================================
# TEST 18
# OUTPUT CONTRACT
# =====================================================================

def test_output_contract():

    builder = KnowledgeGraphBuilder()

    entity = make_entity(
        "KPI_1",
        "kpi",
        "yield",
    )

    statement = make_statement(
        "STATEMENT_1",
        [
            entity,
        ],
    )

    resolution = MockSemanticResolution(
        [statement]
    )

    result = builder.build(
        resolution
    )

    # ---------------------------------------------------------------
    # Build result
    # ---------------------------------------------------------------

    assert hasattr(
        result,
        "graph",
    )

    assert result.graph is not None

    # ---------------------------------------------------------------
    # Builder API
    # ---------------------------------------------------------------

    assert hasattr(
        builder,
        "node_count",
    )

    assert hasattr(
        builder,
        "edge_count",
    )

    assert hasattr(
        builder,
        "summary",
    )

    assert hasattr(
        builder,
        "get_node",
    )

    assert hasattr(
        builder,
        "get_nodes",
    )

    assert hasattr(
        builder,
        "get_edges",
    )

    assert hasattr(
        builder,
        "reset",
    )


# =====================================================================
# MANUAL RUNNER
# =====================================================================

if __name__ == "__main__":

    tests = [

        test_basic_graph_creation,

        test_entities_become_graph_nodes,

        test_kpi_and_bkpi_remain_distinct,

        test_metric_remains_distinct,

        test_measurement_becomes_graph_node,

        test_statement_relation_becomes_graph_edge,

        test_edge_confidence_is_preserved,

        test_edge_reasoning_is_preserved,

        test_node_metadata_is_preserved,

        test_edge_metadata_is_preserved,

        test_multiple_statements_are_built,

        test_invalid_relation_is_ignored,

        test_duplicate_nodes_are_not_created,

        test_duplicate_edges_are_not_created,

        test_empty_input,

        test_none_input,

        test_reset,

        test_output_contract,

    ]

    passed = 0

    failed = 0

    print()

    print("=" * 70)

    print(
        "KNOWLEDGE GRAPH BUILDER REGRESSION TEST"
    )

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