"""
Metadata Builder V3

Aggregates metadata from Business Statements.

Business Statements are now the primary
semantic objects.

Clusters are only visualization groups.
"""

from collections import Counter

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (

    SemanticMetadata,

    SemanticStatistics,

)


class MetadataBuilder:

    def build(self, semantic_result):

        metadata = SemanticMetadata()

        statistics = SemanticStatistics()

        entities = semantic_result.entities

        dependencies = semantic_result.dependencies

        clusters = semantic_result.clusters

        statements = semantic_result.business_statements

        # ===================================================
        # Statistics
        # ===================================================

        statistics.entities = len(entities)

        statistics.dependencies = len(dependencies)

        statistics.clusters = len(clusters)

        statistics.actions = sum(

            1

            for entity in entities

            if entity.entity_type == "action"

        )

        statistics.objects = sum(

            1

            for entity in entities

            if entity.entity_type == "object"

        )

        statistics.domains = sum(

            1

            for entity in entities

            if entity.entity_type == "domain"

        )

        statistics.metrics = sum(

            1

            for entity in entities

            if entity.entity_type in ("metric", "kpi")

        )

        statistics.measurements = sum(

            1

            for entity in entities

            if entity.entity_type == "measurement"

        )

        statistics.methodologies = sum(

            1

            for entity in entities

            if entity.entity_type == "methodology"

        )

        statistics.standards = sum(

            1

            for entity in entities

            if entity.entity_type == "standard"

        )

        metadata.statistics = statistics

        # ===================================================
        # Primary Semantic Type
        # ===================================================

        intents = [

            statement.intent.intent

            for statement in statements

            if statement.intent

        ]

        if intents:

            metadata.semantic_type = (

                Counter(intents)

                .most_common(1)[0][0]

            )

        # ===================================================
        # Primary Domain
        # ===================================================

        domains = [

            statement.intent.primary_domain

            for statement in statements

            if statement.intent

            and statement.intent.primary_domain

        ]

        if domains:

            metadata.primary_domain = (

                Counter(domains)

                .most_common(1)[0][0]

            )

        # ===================================================
        # Primary Business Area
        # ===================================================

        business_areas = [

            statement.intent.business_area

            for statement in statements

            if statement.intent

            and statement.intent.business_area

        ]

        if business_areas:

            metadata.primary_business_area = (

                Counter(business_areas)

                .most_common(1)[0][0]

            )

        # ===================================================
        # Achievement
        # ===================================================

        metadata.achievement = any(

            statement.intent.achievement

            for statement in statements

            if statement.intent

        )

        return metadata