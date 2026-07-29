"""
Metric Classifier

Infers business area and category
for temporary KPIs.
"""


class MetricClassifier:

    def __init__(self):

        self.rules = {

            "yield": ("operations", "operations"),

            "availability": ("operations", "operations"),

            "uptime": ("operations", "operations"),

            "downtime": ("operations", "operations"),

            "efficiency": ("operations", "operations"),

            "waste": ("operations", "operations"),

            "inventory": ("operations", "operations"),

            "stock": ("operations", "operations"),

            "complaint": ("quality", "quality"),

            "defect": ("quality", "quality"),

            "audit": ("quality", "quality"),

            "quality": ("quality", "quality"),

            "cost": ("finance", "finance"),

            "saving": ("finance", "finance"),

            "revenue": ("finance", "finance"),

            "profit": ("finance", "finance"),

            "team": ("leadership", "people"),

            "employee": ("leadership", "people"),

            "training": ("people", "people"),

            "safety": ("safety", "safety"),

        }

    def classify(self, metric_name):

        name = metric_name.lower()

        for keyword, values in self.rules.items():

            if keyword in name:

                return values

        return "unknown", "unknown"