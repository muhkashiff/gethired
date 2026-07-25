"""
GetHired

Production Achievement Detector

Extracts structured information from achievement statements.
"""

import re


class AchievementDetector:

    def __init__(self):

        # Common action verbs
        self.action_verbs = [

            "achieved",
            "improved",
            "increased",
            "reduced",
            "decreased",
            "developed",
            "implemented",
            "established",
            "created",
            "led",
            "managed",
            "optimized",
            "strengthened",
            "expanded",
            "delivered",
            "maintained",
            "introduced",
            "designed",
            "saved",
            "generated",
            "built",
            "launched",
            "enhanced",
            "performed",
            "obtained",
            "directed",
            "oversaw",
            "coordinated",
            "executed",
            "fostered",
            "governed",
            "utilized",
            "Sustained",
            "Delivered",
            "Maintained",
            "Generated",
            "Created",
            "Developed",
            "Managed",
            "Directed",
            "Executed",
            "Led",
            "Oversaw",
            "Produced",
            "Established",
            "Implemented",
            "Designed",
            "Built",
            "Increased",
            "Enhanced",
            "Reduced",
            "Optimized",
            "Strengthened"
        ]

    # =====================================================
    # Parse Achievement List
    # =====================================================

    def parse(self, achievement_lines):

        achievements = []

        for line in achievement_lines:

            line = line.strip()

            if not line:
                continue

            achievement = {

                "text": line,

                "action": self.detect_action(line),

                "metrics": self.extract_metrics(line),

                "category": self.detect_category(line),

                "business_area": self.detect_business_area(line)

            }

            achievements.append(achievement)

        return achievements

    # =====================================================
    # Detect Action Verb
    # =====================================================

    def detect_action(self, text):

        lower = text.lower()

        for verb in self.action_verbs:

            if lower.startswith(verb):

                return verb.title()

        return ""

    # =====================================================
    # Extract Metrics
    # =====================================================

    def extract_metrics(self, text):

        metrics = []

        # Percentages

        for value in re.findall(r"\d+(?:\.\d+)?\s*%[\+]?", text):

            metrics.append({

                "value": value,

                "type": "Percentage"

            })

        # Currency

        for value in re.findall(r"[$£€]\s?[\d,]+(?:\.\d+)?", text):

            metrics.append({

                "value": value,

                "type": "Currency"

            })

        # Large Numbers

        for value in re.findall(r"\b\d[\d,]*\b", text):

            if "%" not in value:

                metrics.append({

                    "value": value,

                    "type": "Number"

                })

        return metrics

    # =====================================================
    # Detect Category
    # =====================================================

    def detect_category(self, text):

        lower = text.lower()

        mapping = {

            "yield": "Yield Improvement",

            "quality": "Quality",

            "audit": "Audit",

            "food safety": "Food Safety",

            "training": "Training",

            "sales": "Sales",

            "profit": "Profitability",

            "cost": "Cost Reduction",

            "waste": "Waste Reduction",

            "downtime": "Productivity",

            "distribution": "Supply Chain",

            "customer": "Customer",

            "inventory": "Inventory",

            "supplier": "Procurement"

        }

        for keyword, category in mapping.items():

            if keyword in lower:

                return category

        return "General"

    # =====================================================
    # Detect Business Area
    # =====================================================

    def detect_business_area(self, text):

        lower = text.lower()

        mapping = {

            "production": "Manufacturing",

            "plant": "Manufacturing",

            "factory": "Manufacturing",

            "quality": "Quality",

            "food safety": "Food Safety",

            "audit": "Compliance",

            "warehouse": "Warehouse",

            "retail": "Retail",

            "sales": "Sales",

            "procurement": "Procurement",

            "inventory": "Inventory",

            "distribution": "Supply Chain",

            "customer": "Customer Service"

        }

        for keyword, area in mapping.items():

            if keyword in lower:

                return area

        return "Business"