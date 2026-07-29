import sys
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.knowledge_pipeline import KnowledgePipeline

pipeline = KnowledgePipeline()

texts = [

    # Range
    "Increased Production Yield from 70% to 99% by leading cross-functional teams.",

    # Reduction
    "Reduced customer complaints from 35 to 10 per month.",

    # Cost savings
    "Generated cost savings of $2.5M through process optimization.",

    # Revenue increase
    "Increased annual revenue by 18%.",

    # Absolute KPI
    "Maintained 99.9% equipment availability.",

    # Food Safety
    "Implemented FSSC 22000 requirements across the manufacturing facility.",

    # Leadership
    "Led a team of 35 engineers to improve operational excellence.",

]

for idx, text in enumerate(texts, start=1):

    print("\n")
    print("="*100)
    print(f"TEST CASE {idx}")
    print("="*100)

    result = pipeline.process(text)

    document = result["knowledge_document"]
    graph_document = result["graph_document"]
    profile = result["knowledge_profile"]

    print("\nINPUT")
    print(text)

    print("\nDOCUMENT STATISTICS")
    pprint(document.statistics)

    print("\nGRAPH")
    pprint(graph_document.graph.summary())

    print("\nFACTS")

    for sentence in document.sentences:

        for fact in sentence.facts:

            print("-"*70)
            print(fact.text)

            measurement = fact.interpretation.measurement

            pprint(measurement.summary())

    print("\nPROFILE SUMMARY")
    pprint(profile["summary"])

    print("\nTOP ACHIEVEMENTS")
    pprint(profile["achievement"]["top_achievements"])

    print("\nTOP METRICS")
    pprint(profile["achievement"]["top_metrics"])