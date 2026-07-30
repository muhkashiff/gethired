"""
Metric Validator

Validates extracted KPI/Metric entities.

Purpose

Prevent false KPI detections.

Example

Food Safety

should NOT become KPI.

Production Yield

should remain KPI.
"""


class MetricValidator:

    """
    Removes invalid metrics and keeps only business KPIs.
    """

    def __init__(self):

        self.allowed_categories = {

            "quality",
            "production",
            "manufacturing",
            "operations",
            "financial",
            "leadership",
            "efficiency",
            "safety",

        }

    # -----------------------------------------------------

    def validate(self, resolution):

        valid_metrics = []

        for entity in resolution.entities:

            if entity.entity_type.lower() != "metric":

                valid_metrics.append(entity)

                continue

            category = entity.category.lower()

            if category in self.allowed_categories:

                valid_metrics.append(entity)

                continue

            # remove invalid KPI

            resolution.warnings.append(

                f"Removed invalid KPI: {entity.canonical}"

            )

        resolution.entities = valid_metrics

        return resolution