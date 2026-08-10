"""
Enterprise Metric Extractor

Repository compatible.

Responsibilities:

1. Detect metric entity.
2. Convert repository metric into MetricKnowledge.
3. Preserve ontology metadata.
4. Provide higher-is-better business direction.
5. Provide measurement expectations.

Enterprise V3
"""

from app.intelligence.utilities.knowledge.repository_v5.repository import (
    Repository,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.metric_models import (
    MetricKnowledge,
)


class MetricExtractor:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self, repository=None):

        self.repository = repository or Repository()

    ####################################################################
    # MAIN
    ####################################################################

    def extract(self, sentence):

        """
        Extract a metric from a sentence.

        Expected repository behaviour:

            repository.search(...)
            
        The exact repository lookup should remain compatible with
        the existing repository implementation.
        """

        if not sentence:

            return MetricKnowledge()

        ################################################################
        # Repository lookup
        ################################################################

        result = self.repository.search(
            ontology="metrics",
            text=sentence,
        )

        if not result:

            return MetricKnowledge()

        ################################################################
        # Select metric entity
        ################################################################

        metric = result[0] if isinstance(result, list) else result

        if metric is None:

            return MetricKnowledge()

        ################################################################
        # Metadata
        ################################################################

        metadata = getattr(metric, "metadata", None)

        if metadata is None:

            metadata = {}

        ################################################################
        # Direction
        ################################################################

        higher_is_better = metadata.get(
            "higher_is_better",
            getattr(metric, "higher_is_better", True),
        )

        ################################################################
        # Target
        ################################################################

        target_value = metadata.get(
            "target_value",
            0.0,
        )

        ################################################################
        # Build knowledge object
        ################################################################

        return MetricKnowledge(

            ################################################################
            # Detection
            ################################################################

            found=True,

            confidence=getattr(
                metric,
                "confidence",
                0.99,
            ),

            phrase=getattr(
                metric,
                "phrase",
                "",
            ),

            alias_match=getattr(
                metric,
                "alias_match",
                False,
            ),

            ################################################################
            # Identity
            ################################################################

            metric_family=metadata.get(
                "metric_family",
                "",
            ),

            metric_group=metadata.get(
                "metric_group",
                "",
            ),

            canonical=getattr(
                metric,
                "canonical",
                "",
            ),

            unit=metadata.get(
                "unit",
                "",
            ),

            ################################################################
            # Classification
            ################################################################

            category=getattr(
                metric,
                "category",
                metadata.get("category", ""),
            ),

            business_area=getattr(
                metric,
                "business_area",
                metadata.get("business_area", ""),
            ),

            ################################################################
            # Direction
            ################################################################

            higher_is_better=bool(
                higher_is_better
            ),

            lower_is_better=not bool(
                higher_is_better
            ),

            ################################################################
            # Metric type
            ################################################################

            percentage_metric=metadata.get(
                "percentage_metric",
                False,
            ),

            financial_metric=metadata.get(
                "financial_metric",
                False,
            ),

            quality_metric=metadata.get(
                "quality_metric",
                False,
            ),

            productivity_metric=metadata.get(
                "productivity_metric",
                False,
            ),

            operational_metric=metadata.get(
                "operational_metric",
                False,
            ),

            ################################################################
            # KPI
            ################################################################

            kpi=metadata.get(
                "kpi",
                False,
            ),

            benchmark_available=metadata.get(
                "benchmark_available",
                False,
            ),

            target_value=target_value,

            ################################################################
            # Measurement
            ################################################################

            measurement_expected=metadata.get(
                "measurement_expected",
                True,
            ),

            ################################################################
            # Business
            ################################################################

            impact_weight=getattr(
                metric,
                "impact_weight",
                metadata.get("impact_weight", 0.0),
            ),

            ################################################################
            # Source
            ################################################################

            source=getattr(
                metric,
                "source",
                "",
            ),

            ################################################################
            # Description
            ################################################################

            description=metadata.get(
                "description",
                "",
            ),

            ################################################################
            # Metadata
            ################################################################

            metadata=metadata,
        )