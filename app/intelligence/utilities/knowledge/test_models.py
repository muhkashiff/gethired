import sys
from pathlib import Path
from pprint import pprint

# ==========================================================
# Project Root
# ==========================================================

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

"""
Enterprise Pipeline Integration Test

KnowledgePipeline
        ↓
KnowledgeDocument
        ↓
SemanticResult
        ↓
GraphDocument
        ↓
KnowledgeProfile
        ↓
GraphQuery
"""

# ==========================================================
# Pipeline
# ==========================================================

from app.intelligence.utilities.knowledge.knowledge_pipeline import (
    KnowledgePipeline,
)

# ==========================================================
# Graph Query
# ==========================================================

from app.intelligence.utilities.knowledge.knowledge_graph.graph_query import (
    GraphQuery,
)

# ==========================================================
# TEST SENTENCE
# ==========================================================

TEST_SENTENCE = (
    "Implemented FSSC 22000 requirements "
    "and increased Yield from 70% to 99% "
    "using Root Cause Analysis."
)


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 80)
    print("GETHIRED ENTERPRISE PIPELINE TEST")
    print("=" * 80)

    # ------------------------------------------------------
    # Pipeline
    # ------------------------------------------------------

    pipeline = KnowledgePipeline()

    result = pipeline.process(TEST_SENTENCE)

    print("\nPIPELINE EXECUTED")

    # ------------------------------------------------------
    # Pipeline Result
    # ------------------------------------------------------

    print("\nKnowledge Document")
    pprint(result.knowledge_document)

    print("\nSemantic Result")
    pprint(result.semantic_result)

    print("\nKnowledge Profile")
    pprint(result.knowledge_profile)

    # ------------------------------------------------------
    # Graph
    # ------------------------------------------------------



    # ------------------------------------------------------
    # IMPORTANT
    # ------------------------------------------------------
    # Change this if your GraphDocument attribute
    # is named differently.
    # ------------------------------------------------------

    graph = result.graph_document

    print("\nKnowledge Graph Created")

    print(f"Nodes : {graph.statistics.node_count}")
    print(f"Edges : {graph.statistics.edge_count}")

    # ------------------------------------------------------
    # Query Engine
    # ------------------------------------------------------

    query = GraphQuery(graph)

    # ------------------------------------------------------
    # Nodes
    # ------------------------------------------------------

    print("\n---------------------------")
    print("ALL NODES")
    print("---------------------------")

    for node in graph.get_nodes():

        print(
            f"{node.entity_type:<18}"
            f"{node.canonical}"
        )

    # ------------------------------------------------------
    # Edges
    # ------------------------------------------------------

    print("\n---------------------------")
    print("ALL RELATIONS")
    print("---------------------------")

    for edge in graph.get_edges():

        print(edge.reasoning)

    # ------------------------------------------------------
    # Query Example
    # ------------------------------------------------------

    print("\n---------------------------")
    print("QUERY : Standards")
    print("---------------------------")

    standards = query.find_nodes(
        entity_type="standard"
    )

    for standard in standards:

        print(standard.canonical)

    # ------------------------------------------------------

    print("\n---------------------------")
    print("QUERY : acts_on")
    print("---------------------------")

    relations = query.find_by_relation(
        relation="acts_on"
    )

    for relation in relations:

        print(relation["reasoning"])

    # ------------------------------------------------------

    print("\nPIPELINE TEST COMPLETED")


# ==========================================================

if __name__ == "__main__":

    main()