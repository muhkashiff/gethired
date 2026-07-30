import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

"""
Knowledge Pipeline Integration Test

Tests the complete pipeline:

Sentence
    ↓
Sentence Parser
    ↓
Knowledge Document
    ↓
Knowledge Graph
    ↓
Knowledge Profile
    ↓
Semantic Resolver

"""

from app.intelligence.utilities.knowledge.knowledge_pipeline.knowledge_pipeline import (
    KnowledgePipeline,
)


TEST_SENTENCES = [

    "Implemented FSSC22000 Quality Management System using Lean Manufacturing.",

    "Led cross functional team of 25 employees.",

    "Improved production yield from 70% to 99% using Six Sigma.",

    "Reduced customer complaints by 80%.",

    "Managed Water Treatment Plant operations.",

    "Certified facility against ISO 9001 and FSSC22000.",

    "Optimized production process through Kaizen methodology.",

    "Developed HACCP plans for beverage manufacturing.",

    "Performed Root Cause Analysis using Fishbone Diagram.",

    "Implemented GMP and Food Safety standards.",

]


def print_header(title):

    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def print_document(document):

    print("\nDOCUMENT")

    print("-" * 50)

    print(f"Sentences : {len(document.sentences)}")
    print(f"Facts     : {len(document.facts)}")
    print(f"Confidence: {document.confidence}")


def print_graph(graph_document):

    graph = graph_document.graph

    print("\nGRAPH")

    print("-" * 50)

    print(f"Nodes : {graph.node_count}")
    print(f"Edges : {graph.edge_count}")

    print("\nNode Types")

    counts = {}

    for node in graph.nodes:

        counts[node.node_type] = counts.get(node.node_type, 0) + 1

    for k, v in sorted(counts.items()):

        print(f"{k:15} : {v}")


def print_profile(profile):

    print("\nPROFILE")

    print("-" * 50)

    print(f"Overall Score      : {profile.summary.overall_score}")
    print(f"Seniority Score    : {profile.summary.seniority_score}")
    print(f"Leadership Score   : {profile.summary.leadership_score}")
    print(f"Achievement Score  : {profile.summary.achievement_score}")


def print_semantic(result):

    print("\nSEMANTIC")

    print("-" * 50)

    print(f"Entities      : {len(result.entities)}")
    print(f"Dependencies  : {len(result.dependencies)}")
    print(f"Clusters      : {len(result.clusters)}")
    print(f"Confidence    : {result.confidence}")

    print("\nMetadata")

    print(result.metadata)

    print("\nClusters")

    for cluster in result.clusters:

        print(
            f"{cluster.cluster_id}"
            f" | {cluster.semantic_type}"
            f" | {cluster.label}"
            f" | {cluster.confidence}"
        )

        for entity in cluster.entities:

            print(
                f"    └── "
                f"{entity.entity_type}"
                f" : {entity.canonical}"
            )

    print("\nDependencies")

    for dep in result.dependencies:

        print(

            f"{dep.source_entity}"

            f" -- {dep.relation} --> "

            f"{dep.target_entity}"

        )


def main():

    pipeline = KnowledgePipeline()

    for sentence in TEST_SENTENCES:

        print_header(sentence)

        result = pipeline.process(sentence)

        print_document(result.knowledge_document)

        print_graph(result.graph_document)

        print_profile(result.knowledge_profile)

        print_semantic(result.semantic_result)


if __name__ == "__main__":

    main()