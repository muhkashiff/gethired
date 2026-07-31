"""
Advanced Cluster Classifier V4

Final semantic classifier.

BusinessStatement already resolved the intent.

Classifier only

• assigns label
• adjusts confidence

NOT semantic type.
"""

from collections import Counter


class ClusterClassifier:

    def classify(self, cluster):

        # semantic_type already assigned
        cluster.label = self._label(cluster)

        cluster.confidence = self._confidence(cluster)

        return cluster

    # ==========================================================
    # Label
    # ==========================================================

    def _label(self, cluster):

        action = self._action_entity(cluster)

        if action:

            return action.matched_text

        domains = self._entities(cluster, "domain")

        if domains:

            return domains[0].matched_text

        return cluster.cluster_id

    # ==========================================================
    # Confidence
    # ==========================================================

    def _confidence(self, cluster):

        score = cluster.confidence

        entity_types = Counter(

            entity.entity_type

            for entity in cluster.entities

        )

        if entity_types["action"]:
            score += 0.02

        if entity_types["object"]:
            score += 0.02

        if entity_types["standard"]:
            score += 0.02

        if entity_types["methodology"]:
            score += 0.01

        if entity_types["metric"]:
            score += 0.01

        return round(min(score, 0.99), 2)

    # ==========================================================
    # Helpers
    # ==========================================================

    def _entities(self, cluster, entity_type):

        return [

            entity

            for entity in cluster.entities

            if entity.entity_type == entity_type

        ]

    def _action_entity(self, cluster):

        actions = self._entities(cluster, "action")

        if actions:
            return actions[0]

        return None