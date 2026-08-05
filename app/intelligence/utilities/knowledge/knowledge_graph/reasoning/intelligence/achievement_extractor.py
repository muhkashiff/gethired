"""
Enterprise Achievement Extractor

Enterprise V6

Purpose
-------
Discovers achievement evidence from the
Knowledge Graph.

This component DOES NOT score.

It simply discovers relationships.

Input
-----

Knowledge Graph

Dependency Reasoning

Ontology Reasoning

Output
------

List[AchievementEvidence]
"""

from typing import Dict, List

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.achievement_models import (
    AchievementEvidence,
)


class AchievementExtractor:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        pass

    ####################################################################
    # PUBLIC API
    ####################################################################

    def extract(

        self,

        graph,

        dependency_reasoning,

        ontology_reasoning,

    ) -> List[AchievementEvidence]:

        """
        Discover achievement evidence.
        """

        achievements = []

        ###############################################################
        # Lookup Tables
        ###############################################################

        metric_lookup = self._metric_lookup(

            ontology_reasoning

        )

        measurement_lookup = self._measurement_lookup(

            ontology_reasoning

        )

        ###############################################################
        # Walk Actions
        ###############################################################

        for action in ontology_reasoning.actions:

            targets = (

                dependency_reasoning.action_targets.get(

                    action.entity_id,

                    [],

                )

            )

            for target in targets:

                evidence = self._build_evidence(

                    action,

                    target,

                    metric_lookup,

                    measurement_lookup,

                )

                if evidence:

                    achievements.append(

                        evidence

                    )

        return achievements

    ####################################################################
    # LOOKUP TABLES
    ####################################################################

    def _metric_lookup(

        self,

        ontology_reasoning,

    ) -> Dict:

        """
        Build Metric lookup.
        """

        return {

            metric.entity_id: metric

            for metric in ontology_reasoning.metrics

        }

    ####################################################################

    def _measurement_lookup(

        self,

        ontology_reasoning,

    ) -> Dict:

        """
        Build Measurement lookup.
        """

        return {

            measurement.entity_id: measurement

            for measurement in ontology_reasoning.measurements

        }

    ####################################################################
    # BUILD EVIDENCE
    ####################################################################

    def _build_evidence(

        self,

        action,

        target,

        metric_lookup,

        measurement_lookup,

    ):

        metric = metric_lookup.get(target)

        measurement = measurement_lookup.get(target)

        if metric is None and measurement is None:

            return None

        evidence = AchievementEvidence()

        evidence.action = action

        evidence.metric = metric

        evidence.measurement = measurement

        ###########################################################
        # Business Context
        ###########################################################

        if metric:

            evidence.business_area = getattr(

                metric,

                "business_area",

                "",

            )

            evidence.domain = getattr(

                metric,

                "domain",

                "",

            )

        ###########################################################
        # Confidence
        ###########################################################

        evidence.confidence = (

            self._calculate_confidence(

                action,

                metric,

                measurement,

            )

        )

        ###########################################################
        # Metadata
        ###########################################################

        evidence.metadata = {

            "metric_found": metric is not None,

            "measurement_found": measurement is not None,

        }

        return evidence

    ####################################################################
    # CONFIDENCE
    ####################################################################

    def _calculate_confidence(

        self,

        action,

        metric,

        measurement,

    ):

        confidence = 0.50

        if action:

            confidence += 0.15

        if metric:

            confidence += 0.15

        if measurement:

            confidence += 0.20

        return round(

            min(

                confidence,

                1.0,

            ),

            2,

        )