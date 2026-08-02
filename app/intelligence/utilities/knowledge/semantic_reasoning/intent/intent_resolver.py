"""
Enterprise Intent Resolver

Determines WHY a business statement exists.

Enterprise V5
"""

from .intent_models import (

    IntentContext,

    IntentResult,

)

from .intent_rules import INTENT_RULES


class IntentResolver:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        pass

    ####################################################################
    # MAIN ENTRY
    ####################################################################

    def resolve(

        self,

        statement,

    ) -> IntentResult:

        """
        Resolve the business intent
        from a ParsedStatement.
        """

        context = self.build_context(

            statement

        )

        ################################################################
        # Evaluate Rules
        ################################################################

        for rule in INTENT_RULES:

            if not self.matches_rule(

                context,

                rule,

            ):

                continue

            result = self.build_result(

                rule,

                context,

            )

            if result.confidence >= 0.90:

                return result

        ################################################################
        # Default
        ################################################################

        return IntentResult(

            intent="statement",

            semantic_type="statement",

            primary_domain=context.primary_domain or "General",

            business_area=context.business_area or "General",

            achievement=False,

            confidence=0.80,

            matched_rule="default",

            reasoning="No intent rule matched.",

            trigger_entities=[],

        )
    ####################################################################
    # BUILD INTENT CONTEXT
    ####################################################################

    def build_context(

        self,

        statement,

    ) -> IntentContext:

        """
        Converts ParsedStatement into a lightweight
        IntentContext used by the rule engine.
        """

        context = IntentContext()

        # ==========================================================
        # ACTION
        # ==========================================================

        if statement.action and statement.action.found:

            context.action = (

                statement.action.base

                or statement.action.canonical

                or statement.action.original

            ).lower()

            context.action_category = (

                statement.action.category

            )

        # ==========================================================
        # ENTITY COUNTS
        # ==========================================================

        context.object_count = len(

            statement.targets

        )

        context.standard_count = len(

            statement.standards

        )

        context.methodology_count = len(

            statement.methods

        )

        context.metric_count = len(

            statement.metrics

        )

        context.measurement_count = len(

            getattr(

                statement,

                "measurements",

                []

            )

        )

        context.domain_count = len(

            statement.domains

        )

        context.skill_count = len(

            statement.skills

        )

        context.technology_count = len(

            getattr(

                statement,

                "technologies",

                []

            )

        )

        context.certification_count = len(

            getattr(

                statement,

                "certifications",

                []

            )

        )

        # ==========================================================
        # ENTITY NAMES
        # ==========================================================

        context.objects = [

            entity.canonical

            for entity in statement.targets

            if entity.found

        ]

        context.standards = [

            entity.canonical

            for entity in statement.standards

            if entity.found

        ]

        context.methodologies = [

            entity.canonical

            for entity in statement.methods

            if entity.found

        ]

        context.metrics = [

            entity.canonical

            for entity in statement.metrics

            if entity.found

        ]

        context.domains = [

            entity.canonical

            for entity in statement.domains

            if entity.found

        ]

        context.skills = [

            skill.name

            for skill in statement.skills

        ]

        context.technologies = [

            entity.canonical

            for entity in getattr(

                statement,

                "technologies",

                []

            )

            if entity.found

        ]

        context.certifications = [

            entity.canonical

            for entity in getattr(

                statement,

                "certifications",

                []

            )

            if entity.found

        ]

        # ==========================================================
        # PRIMARY DOMAIN
        # ==========================================================

        if statement.domains:

            context.primary_domain = (

                statement.domains[0].canonical

            )

            context.business_area = (

                statement.domains[0].business_area

            )

        return context
    ####################################################################
    # RULE MATCHER
    ####################################################################

    def matches_rule(

        self,

        context: IntentContext,

        rule: dict,

    ) -> bool:

        """
        Determines whether a rule matches the
        current IntentContext.
        """

        # ==========================================================
        # ACTION
        # ==========================================================

        if context.action not in rule.get(

            "actions",

            []

        ):

            return False

        # ==========================================================
        # ENTITY COUNT LOOKUP
        # ==========================================================

        entity_counts = {

            "objects": context.object_count,

            "standards": context.standard_count,

            "methodologies": context.methodology_count,

            "metrics": context.metric_count,

            "measurements": context.measurement_count,

            "domains": context.domain_count,

            "skills": context.skill_count,

            "technologies": context.technology_count,

            "certifications": context.certification_count,

        }

        # ==========================================================
        # REQUIRED ENTITY TYPES
        # ==========================================================

        for requirement in rule.get(

            "requires",

            []

        ):

            if entity_counts.get(

                requirement,

                0

            ) == 0:

                return False

        # ==========================================================
        # OPTIONAL ENTITY VALUE MATCHING
        #
        # Future-proof:
        # A rule can require specific ontology values.
        #
        # Example:
        #
        # "objects":["FSSC 22000","HACCP"]
        #
        # ==========================================================

        entity_lists = {

            "objects": context.objects,

            "standards": context.standards,

            "methodologies": context.methodologies,

            "metrics": context.metrics,

            "domains": context.domains,

            "skills": context.skills,

            "technologies": context.technologies,

            "certifications": context.certifications,

        }

        for entity_type in entity_lists.keys():

            expected = rule.get(entity_type)

            if not expected:

                continue

            actual = entity_lists[entity_type]

            found = False

            for value in actual:

                if value.lower() in [

                    item.lower()

                    for item in expected

                ]:

                    found = True

                    break

            if not found:

                return False

        # ==========================================================
        # PASSED
        # ==========================================================

        return True
    ####################################################################
    # BUILD RESULT
    ####################################################################

    def build_result(

        self,

        rule: dict,

        context: IntentContext,

    ) -> IntentResult:

        """
        Builds a standardized IntentResult
        from a matched rule.
        """

        # ------------------------------------------------------------
        # Collect trigger entities
        # ------------------------------------------------------------

        trigger_entities = [

            context.action,

            *context.objects,

            *context.standards,

            *context.methodologies,

            *context.metrics,

            *context.skills,

            *context.domains,

            *context.technologies,

            *context.certifications,

        ]

        # ------------------------------------------------------------
        # Remove duplicates while preserving order
        # ------------------------------------------------------------

        trigger_entities = list(

            dict.fromkeys(

                entity

                for entity in trigger_entities

                if entity

            )

        )

        # ------------------------------------------------------------
        # Build result
        # ------------------------------------------------------------

        return IntentResult(

            # ----------------------------------------------------
            # Intent
            # ----------------------------------------------------

            intent=rule.get(

                "intent",

                "statement",

            ),

            semantic_type=rule.get(

                "intent",

                "statement",

            ),

            confidence=rule.get(

                "confidence",

                0.80,

            ),

            # ----------------------------------------------------
            # Business
            # ----------------------------------------------------

            primary_domain=rule.get(

                "primary_domain",

                context.primary_domain or "General",

            ),

            business_area=rule.get(

                "business_area",

                context.business_area or "General",

            ),

            achievement=rule.get(

                "achievement",

                False,

            ),

            # ----------------------------------------------------
            # Explainability
            # ----------------------------------------------------

            matched_rule=rule.get(

                "id",

                "",

            ),

            reasoning=(

                f"Matched intent rule "

                f"'{rule.get('id','unknown')}'."

            ),

            trigger_entities=trigger_entities,

            # ----------------------------------------------------
            # Metadata
            # ----------------------------------------------------

            metadata={

                "action": context.action,

                "action_category": context.action_category,

                "objects": context.objects,

                "standards": context.standards,

                "methodologies": context.methodologies,

                "metrics": context.metrics,

                "domains": context.domains,

                "skills": context.skills,

                "technologies": context.technologies,

                "certifications": context.certifications,

            }

        )
        ####################################################################
    # RESOLVE FROM CONTEXT
    ####################################################################

    def resolve_from_context(

        self,

        context: IntentContext,

    ) -> IntentResult:

        """
        Allows future AI modules to resolve
        intents without requiring a ParsedStatement.

        Example

            Knowledge Graph

            Narrative Builder

            AI Resume Generator

        """

        for rule in INTENT_RULES:

            if not self.matches_rule(

                context,

                rule,

            ):

                continue

            result = self.build_result(

                rule,

                context,

            )

            if result.confidence >= 0.90:

                return result

        return IntentResult(

            intent="statement",

            semantic_type="statement",

            primary_domain=context.primary_domain or "General",

            business_area=context.business_area or "General",

            achievement=False,

            confidence=0.80,

            matched_rule="default",

            reasoning="No intent rule matched.",

            trigger_entities=[],

        )