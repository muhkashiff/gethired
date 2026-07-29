import sys
from pathlib import Path
from pprint import pformat

# ------------------------------------------------------------
# Project Root
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.knowledge_pipeline.knowledge_pipeline import (
    KnowledgePipeline,
)

pipeline = KnowledgePipeline()

# ------------------------------------------------------------
# Output File
# ------------------------------------------------------------

OUTPUT_FILE = Path("pipeline_test_output.txt")
OUTPUT_FILE.write_text("", encoding="utf-8")


def log(text=""):
    """Print to console and write to file."""
    print(text)

    with OUTPUT_FILE.open("a", encoding="utf-8") as f:
        f.write(str(text))
        f.write("\n")


def dump(obj):
    """Pretty print object."""
    return pformat(obj, sort_dicts=False)


# ------------------------------------------------------------
# TEST CASES
# ------------------------------------------------------------

TEST_CASES = [

    "Increased Production Yield from 70% to 99% by leading cross-functional teams.",

    "Reduced customer complaints from 35 to 10 per month.",

    "Generated cost savings of $2.5M through process optimization.",

    "Increased annual revenue by 18%.",

    "Maintained 99.9% equipment availability.",

    "Implemented FSSC 22000 requirements across the manufacturing facility.",

    "Led a team of 35 engineers to improve operational excellence.",

    "Reduced downtime by implementing TPM.",

    "Improved OEE from 62% to 87% using Lean Manufacturing.",

    "Trained 120 operators on GMP and HACCP.",

    "Achieved zero customer complaints for six consecutive months.",

    "Reduced production waste from 12% to 4%.",

    "Improved inventory accuracy to 99.8%.",

    "Established ISO 9001 Quality Management System.",

    "Managed inventory worth $15M.",

]

# ------------------------------------------------------------
# PIPELINE TEST
# ------------------------------------------------------------

for i, text in enumerate(TEST_CASES, start=1):

    log("")
    log("=" * 110)
    log(f"TEST CASE {i}")
    log("=" * 110)

    result = pipeline.process(text)

    document = result["knowledge_document"]
    graph_document = result["graph_document"]
    graph = graph_document.graph
    profile = result["knowledge_profile"]

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    log("\nINPUT")
    log(text)

    # --------------------------------------------------------
    # DOCUMENT
    # --------------------------------------------------------

    log("\nDOCUMENT STATISTICS")
    log(dump(document.statistics))

    # --------------------------------------------------------
    # GRAPH
    # --------------------------------------------------------

    log("\nGRAPH SUMMARY")

    graph_summary = {
        "confidence": graph_document.confidence,
        "nodes": len(graph.nodes),
        "edges": len(graph.edges),
    }

    log(dump(graph_summary))

    # --------------------------------------------------------
    # FACTS
    # --------------------------------------------------------

    log("\nFACTS")

    for fact in document.facts:

        log("-" * 80)
        log(fact.text)

        m = fact.interpretation.measurement

        measurement = {

            "metric": m.metric,
            "value": m.value,
            "numeric_value": m.numeric_value,
            "unit": m.unit,

            "measurement_type": m.measurement_type,

            "from_value": m.from_value,
            "to_value": m.to_value,

            "change_value": m.change_value,
            "percent_change": m.percent_change,

            "direction": m.direction,
            "effect": m.effect,

            "confidence": m.confidence,

        }

        log(dump(measurement))

    # --------------------------------------------------------
    # GRAPH NODES
    # --------------------------------------------------------

    log("\nGRAPH NODES")

    for node in graph.nodes:

        log(
            f"{node.node_type:<15}"
            f"{node.label:<35}"
            f"{node.entity_id}"
        )

    # --------------------------------------------------------
    # GRAPH EDGES
    # --------------------------------------------------------

    log("\nGRAPH EDGES")

    for edge in graph.edges:

        log(
            f"{edge.relationship:<18}"
            f"{edge.source_node}"
            f" --> "
            f"{edge.target_node}"
        )

    # --------------------------------------------------------
    # PROFILE SUMMARY
    # --------------------------------------------------------

    log("\nPROFILE SUMMARY")

    summary = profile.summary

    summary_output = {

        "overall_score": summary.overall_score,
        "achievement_score": summary.achievement_score,
        "leadership_score": summary.leadership_score,
        "seniority_score": summary.seniority_score,
        "career_level": summary.career_level,

    }

    log(dump(summary_output))

    # --------------------------------------------------------
    # ACHIEVEMENT PROFILE
    # --------------------------------------------------------

    log("\nTOP ACHIEVEMENTS")
    log(dump(profile.achievement.top_achievements))

    log("\nTOP METRICS")
    log(dump(profile.achievement.top_metrics))

    log("\nACHIEVEMENT PROFILE")
    log(dump(profile.achievement))

    # --------------------------------------------------------
    # LEADERSHIP
    # --------------------------------------------------------

    log("\nLEADERSHIP PROFILE")
    log(dump(profile.leadership))

    # --------------------------------------------------------
    # SENIORITY
    # --------------------------------------------------------

    log("\nSENIORITY PROFILE")
    log(dump(profile.seniority))

    # --------------------------------------------------------
    # GRAPH STATS
    # --------------------------------------------------------

    log("\nGRAPH STATISTICS")
    log(dump(graph_document.statistics))

# ------------------------------------------------------------
# FINISHED
# ------------------------------------------------------------

log("")
log("=" * 110)
log("PIPELINE TEST COMPLETED")
log("=" * 110)

print(f"\nResults written to: {OUTPUT_FILE.resolve()}")