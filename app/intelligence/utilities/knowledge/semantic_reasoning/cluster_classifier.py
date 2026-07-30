"""
Advanced Cluster Classifier V2

Determines the semantic meaning of a business cluster.

This is where the engine decides whether something is

- Achievement
- Leadership
- Certification
- Responsibility
- Continuous Improvement
- Compliance
- Technical Skill
- Operations
- General Statement
"""

class ClusterClassifier:

    def classify(self, cluster):

        entity_types = {
            e.entity_type.lower()
            for e in cluster.entities
        }

        actions = [
            e.canonical.lower()
            for e in cluster.entities
            if e.entity_type.lower() == "action"
        ]

        standards = "standard" in entity_types
        methodologies = "methodology" in entity_types
        skills = "skill" in entity_types
        kpis = (
            "kpi" in entity_types
            or "metric" in entity_types
        )
        objects = "object" in entity_types
        domains = "domain" in entity_types

        semantic_type = "statement"

        # ----------------------------------------
        # Certification
        # ----------------------------------------

        if standards and any(
            a in (
                "implement",
                "certify",
                "develop",
            )
            for a in actions
        ):
            semantic_type = "certification"

        # ----------------------------------------
        # Continuous Improvement
        # ----------------------------------------

        elif methodologies and any(
            a in (
                "improve",
                "optimize",
                "reduce",
                "increase",
                "perform",
            )
            for a in actions
        ):
            semantic_type = "continuous_improvement"

        # ----------------------------------------
        # Leadership
        # ----------------------------------------

        elif any(
            a in (
                "lead",
                "manage",
                "supervise",
                "mentor",
            )
            for a in actions
        ):
            semantic_type = "leadership"

        # ----------------------------------------
        # Responsibility
        # ----------------------------------------

        elif objects and any(
            a in (
                "manage",
                "maintain",
                "monitor",
                "control",
                "implement",
                "develop",
            )
            for a in actions
        ):
            semantic_type = "responsibility"

        # ----------------------------------------
        # KPI Achievement
        # ----------------------------------------

        elif kpis:
            semantic_type = "achievement"

        # ----------------------------------------
        # Compliance
        # ----------------------------------------

        elif standards:
            semantic_type = "compliance"

        # ----------------------------------------
        # Technical Skill
        # ----------------------------------------

        elif skills:
            semantic_type = "technical_skill"

        # ----------------------------------------
        # Operations
        # ----------------------------------------

        elif domains:
            semantic_type = "operations"

        cluster.semantic_type = semantic_type

        cluster.label = self._label(cluster)

        return cluster

    # --------------------------------------------------

    def _label(self, cluster):

        actions = [
            e.original
            for e in cluster.entities
            if e.entity_type == "action"
        ]

        if actions:
            return actions[0]

        for entity in cluster.entities:
            return entity.original

        return "General"