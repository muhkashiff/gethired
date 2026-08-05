"""
Enterprise Business Breadth Analyzer

Calculates business breadth from clustered skills.

Business Breadth measures how widely the candidate
can operate across enterprise functions.

Examples

Manufacturing
Retail
Supply Chain
Quality
Food Safety

↓

Business Breadth
"""

from collections import Counter

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.skill_models import (
    BusinessBreadth,
)


class BusinessBreadthAnalyzer:

    def __init__(self):

        # Enterprise business area weights
        self.area_weights = {

            "manufacturing": 12,

            "quality": 12,

            "food_safety": 12,

            "retail": 10,

            "supply_chain": 10,

            "logistics": 9,

            "engineering": 9,

            "operations": 10,

            "project_management": 8,

            "digital": 8,

            "commercial": 7,

            "finance": 7,

            "leadership": 8,

        }

    # ----------------------------------------------------------

    def analyze(self, clusters):

        breadth = BusinessBreadth()

        counter = Counter()

        # ----------------------------------------
        # Count business areas represented
        # ----------------------------------------

        for cluster in clusters:

            for evidence in cluster.skills:

                area = (
                    evidence.business_area or ""
                ).lower()

                if area:

                    counter[area] += 1

        # ----------------------------------------
        # Convert frequency → weighted score
        # ----------------------------------------

        for area, count in counter.items():

            score = min(
                count * self.area_weights.get(area, 5),
                100,
            )

            if area == "manufacturing":
                breadth.manufacturing = score

            elif area == "retail":
                breadth.retail = score

            elif area == "logistics":
                breadth.logistics = score

            elif area == "quality":
                breadth.quality = score

            elif area == "food_safety":
                breadth.food_safety = score

            elif area == "engineering":
                breadth.engineering = score

            elif area == "project_management":
                breadth.management = score

            elif area == "digital":
                breadth.digital = score

            elif area == "operations":
                breadth.management = max(
                    breadth.management,
                    score,
                )

        # ----------------------------------------
        # Overall Breadth
        # ----------------------------------------

        values = [

            breadth.manufacturing,

            breadth.retail,

            breadth.logistics,

            breadth.quality,

            breadth.food_safety,

            breadth.engineering,

            breadth.management,

            breadth.digital,

        ]

        breadth.overall = round(

            sum(values) / len(values),

            2,

        )

        return breadth