import sys
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from pprint import pprint

from app.intelligence.utilities.knowledge.knowledge_pipeline import (
    KnowledgePipeline,
)

from app.intelligence.utilities.knowledge.knowledge_graph.knowledge_graph_builder import (
    KnowledgeGraphBuilder,
)

from app.intelligence.utilities.knowledge.knowledge_graph.graph_query_engine import (
    GraphQueryEngine,
)

pipeline = KnowledgePipeline()

document = pipeline.process(
    "Implemented FSSC 22000 requirements and increased Production Yield from 70% to 99% by leading cross-functional teams."
)

builder = KnowledgeGraphBuilder()

graph_document = builder.build(document)

graph = graph_document.graph

print("\n====================")
print("NODES")
print("====================")

for node in graph.nodes:
    pprint(node)

print("\n====================")
print("EDGES")
print("====================")

for edge in graph.edges:
    pprint(edge)

query = GraphQueryEngine(graph)

print("\n====================")
print("ACTIONS")
print("====================")

for node in query.actions():
    print(node.label)

print("\n====================")
print("OBJECTS")
print("====================")

for node in query.objects():
    print(node.label)

print("\n====================")
print("METRICS")
print("====================")

for node in query.metrics():
    print(node.label)

print("\n====================")
print("DOMAINS")
print("====================")

for node in query.domains():
    print(node.label)

print("\n====================")
print("MEASUREMENTS")
print("====================")

for node in query.measurements():
    print(node.label)

print("\n====================")
print("GRAPH SUMMARY")
print("====================")

print("Nodes :", len(graph.nodes))
print("Edges :", len(graph.edges))