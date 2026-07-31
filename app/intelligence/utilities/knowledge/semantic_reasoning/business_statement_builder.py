"""
Business Statement Builder V2

Creates fully interpreted business statements.

Pipeline

Entities
        ↓
Dependencies
        ↓
BusinessStatement
        ↓
Intent Resolution
        ↓
Business Intelligence
        ↓
Semantic Cluster
"""

import uuid

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    BusinessStatement,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.intent_resolver import (
    IntentResolver,
)


class BusinessStatementBuilder:

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(self):

        self.intent_resolver = IntentResolver()

    # ==========================================================
    # Main Builder
    # ==========================================================

    def build(self, entities, dependencies):

        statements = []

        actions = [

            entity

            for entity in entities

            if entity.entity_type == "action"

        ]

        # ------------------------------------------------------
        # One Business Statement per Action
        # ------------------------------------------------------

        for action in actions:

            statement = BusinessStatement()

            statement.statement_id = (

                "STATEMENT_"

                + uuid.uuid4().hex[:8].upper()

            )

            statement.action = action

            # --------------------------------------------------
            # Collect every connected semantic entity
            # --------------------------------------------------

            self._collect_entities(

                statement,

                entities,

                dependencies,

            )

            # --------------------------------------------------
            # Resolve Business Intent
            # --------------------------------------------------

            statement.intent = (

                self.intent_resolver.resolve(

                    statement

                )

            )

            # --------------------------------------------------
            # Copy Intent Information
            # --------------------------------------------------

            if statement.intent:

                statement.semantic_type = (

                    statement.intent.intent

                )

                statement.primary_domain = (

                    statement.intent.primary_domain

                )

                statement.primary_business_area = (

                    statement.intent.business_area

                )

            # --------------------------------------------------
            # Build Human Label
            # --------------------------------------------------

            statement.label = (

                self._build_label(

                    statement

                )

            )

            # --------------------------------------------------
            # Apply Intelligence Flags
            # --------------------------------------------------

            self._apply_flags(

                statement

            )

            # --------------------------------------------------
            # Confidence
            # --------------------------------------------------

            statement.confidence = (

                self._confidence(

                    statement

                )

            )

            statements.append(

                statement

            )

        return statements

    # ==========================================================
    # Collect Every Related Entity
    # ==========================================================

    def _collect_entities(

        self,

        statement,

        entities,

        dependencies,

    ):

        # -----------------------------------------
        # Action
        # -----------------------------------------

        statement.entities.append(

            statement.action

        )

        # -----------------------------------------
        # Related Dependencies
        # -----------------------------------------

        related = [

            dependency

            for dependency in dependencies

            if dependency.source_entity

            == statement.action.entity_id

        ]

        statement.dependencies = related

        # -----------------------------------------
        # Resolve Target Entities
        # -----------------------------------------

        for dependency in related:

            entity = next(

                (

                    item

                    for item in entities

                    if item.entity_id

                    == dependency.target_entity

                ),

                None,

            )

            if entity is None:

                continue

            statement.entities.append(

                entity

            )

            # -------------------------------------

            if entity.entity_type == "object":

                statement.targets.append(

                    entity

                )

                continue

            # -------------------------------------

            if entity.entity_type == "standard":

                statement.standards.append(

                    entity

                )

                continue

            # -------------------------------------

            if entity.entity_type == "methodology":

                statement.methods.append(

                    entity

                )

                continue

            # -------------------------------------

            if entity.entity_type in (

                "metric",

                "kpi",

            ):

                statement.metrics.append(

                    entity

                )

                continue

            # -------------------------------------

            if entity.entity_type == "skill":

                statement.skills.append(

                    entity

                )

                continue

            # -------------------------------------

            if entity.entity_type == "domain":

                statement.domains.append(

                    entity

                )

                continue


# ==========================================================
# Build Human Readable Label
# ==========================================================

    def _build_label(

        self,

        statement,

    ):

        pieces = []

        # -------------------------------------
        # Action
        # -------------------------------------

        if statement.action:

            action = (

                statement.action.matched_text

                or statement.action.original

                or statement.action.canonical

            )

            pieces.append(

                action.capitalize()

            )

        # -------------------------------------
        # Target
        # -------------------------------------

        if statement.targets:

            target = statement.targets[0]

            pieces.append(

                target.matched_text

                or target.original

                or target.canonical

            )

        # -------------------------------------
        # Standard
        # -------------------------------------

        if statement.standards:

            names = [

                standard.matched_text

                or standard.original

                or standard.canonical

                for standard in statement.standards

            ]

            pieces.append(

                "("

                + ", ".join(names)

                + ")"

            )

        # -------------------------------------
        # Methodology
        # -------------------------------------

        if statement.methods:

            method = statement.methods[0]

            pieces.append(

                "using"

            )

            pieces.append(

                method.matched_text

                or method.original

                or method.canonical

            )

        # -------------------------------------
        # Metric
        # -------------------------------------

        elif statement.metrics:

            metric = statement.metrics[0]

            pieces.append(

                metric.matched_text

                or metric.original

                or metric.canonical

            )

        return " ".join(pieces).strip()
    # ==========================================================
    # Apply Intelligence Flags
    # ==========================================================

    def _apply_flags(

        self,

        statement,

    ):

        if statement.intent is None:

            return

        intent = (

            statement.intent.intent

            or ""

        ).lower()

        statement.achievement = (

            statement.intent.achievement

        )

        if intent == "leadership":

            statement.leadership = True

        elif intent == "certification":

            statement.certification = True

        elif intent == "continuous_improvement":

            statement.continuous_improvement = True

        elif intent == "technical_skill":

            statement.technical_skill = True

        elif intent == "responsibility":

            statement.responsibility = True

        # ---------------------------------------------
        # Quantified Statement
        # ---------------------------------------------

        statement.quantified = (

            len(statement.metrics) > 0

        )


# ==========================================================
# Semantic Completeness Confidence
# ==========================================================

    def _confidence(

        self,

        statement,

    ):

        score = 0.50

        # ---------------------------------------------

        if statement.action:

            score += 0.10

        if statement.targets:

            score += 0.10

        if statement.methods:

            score += 0.08

        if statement.standards:

            score += 0.08

        if statement.metrics:

            score += 0.06

        if statement.skills:

            score += 0.05

        if statement.domains:

            score += 0.04

        # ---------------------------------------------
        # Intent confidence
        # ---------------------------------------------

        if statement.intent:

            score += 0.05

            if getattr(statement.intent, "primary_domain", ""):

                score += 0.02

            if getattr(statement.intent, "business_area", ""):

                score += 0.02

        # ---------------------------------------------
        # Achievement bonus
        # ---------------------------------------------

        if statement.achievement:

            score += 0.03

        # ---------------------------------------------
        # Quantified statement
        # ---------------------------------------------

        if statement.quantified:

            score += 0.02

        return round(

            min(score, 0.99),

            2,

        )