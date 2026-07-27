import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.knowledge_pipeline.knowledge_pipeline import KnowledgePipeline
from app.intelligence.utilities.knowledge.knowledge_graph.graph_builder import GraphBuilder
from app.intelligence.utilities.knowledge.knowledge_graph.graph_query import GraphQuery

pipeline = KnowledgePipeline()

doc = pipeline.process(

    "Implemented ISO 9001, trained staff and improved productivity by 25%."

)

graph = GraphBuilder().build(doc)

query = GraphQuery(graph)

query.print_graph()

print()

print(query.metrics())

print()

print(query.measurements())

print()

print(query.domains())

print()

print(query.actions_in_domain("quality"))

print()

print(query.metric_value("Productivity"))