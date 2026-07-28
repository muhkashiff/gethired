import sys
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.knowledge_pipeline import (
    KnowledgePipeline,
)

pipeline = KnowledgePipeline()

result = pipeline.process(

    "Implemented FSSC 22000 requirements and increased Production Yield from 70% to 99% by leading cross-functional teams."

)

print("\n==============================")
print("PIPELINE RESULT TYPE")
print("==============================")
print(type(result))

print("\n==============================")
print("PIPELINE RESULT")
print("==============================")
pprint(result)

# ----------------------------------------
# If pipeline returns a dictionary
# ----------------------------------------

if isinstance(result, dict):

    print("\n==============================")
    print("KNOWLEDGE PROFILE")
    print("==============================")

    pprint(result.get("knowledge_profile"))

    print("\n==============================")
    print("GRAPH SUMMARY")
    print("==============================")

    graph_document = result.get("graph_document")

    if graph_document:

        pprint(graph_document.graph.summary())

        print("\nNodes :", graph_document.graph.node_count)
        print("Edges :", graph_document.graph.edge_count)

# ----------------------------------------
# If pipeline returns KnowledgeGraphDocument
# ----------------------------------------

else:

    print("\n==============================")
    print("GRAPH SUMMARY")
    print("==============================")

    pprint(result.graph.summary())