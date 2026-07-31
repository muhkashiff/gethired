"""
Business Intent Resolver

Determines WHY a business statement exists.

Examples

Implemented ISO9001
        ↓
Compliance

Improved Production Yield
        ↓
Continuous Improvement

Reduced Customer Complaints
        ↓
Improvement

Managed Production Department
        ↓
Operations Management

Led Cross Functional Team
        ↓
Leadership

Performed Root Cause Analysis
        ↓
Problem Solving

Designed Dashboard
        ↓
Analytics
"""

from dataclasses import dataclass


# ==========================================================
# Intent Result
# ==========================================================

@dataclass
class IntentResult:

    intent: str = ""

    confidence: float = 0.0


# ==========================================================
# Resolver
# ==========================================================

class IntentResolver:

    def resolve(self, statement):

        action = ""

        if statement.action:

            action = statement.action.canonical.lower()

        standards = len(statement.standards)

        methodologies = len(statement.methods)

        skills = len(statement.skills)

        metrics = len(statement.metrics)

        domains = len(statement.domains)

        objects = len(statement.targets)

        # ------------------------------------------------

        if action in {

            "implement",
            "certify",
            "audit",
            "validate",

        } and standards:

            return IntentResult(

                intent="compliance",

                confidence=0.99,

            )

        # ------------------------------------------------

        if action in {

            "improve",
            "optimize",
            "reduce",
            "increase",

        }:

            return IntentResult(

                intent="continuous_improvement",

                confidence=0.99,

            )

        # ------------------------------------------------

        if action in {

            "lead",

        }:

            return IntentResult(

                intent="leadership",

                confidence=0.98,

            )

        # ------------------------------------------------

        if action in {

            "manage",

        }:

            if objects:

                return IntentResult(

                    intent="operations_management",

                    confidence=0.98,

                )

            return IntentResult(

                intent="leadership",

                confidence=0.94,

            )

        # ------------------------------------------------

        if action in {

            "perform",

        }:

            if methodologies:

                return IntentResult(

                    intent="problem_solving",

                    confidence=0.97,

                )

            return IntentResult(

                intent="execution",

                confidence=0.90,

            )

        # ------------------------------------------------

        if action in {

            "develop",

            "design",

            "build",

        }:

            if standards:

                return IntentResult(

                    intent="compliance",

                    confidence=0.96,

                )

            return IntentResult(

                intent="development",

                confidence=0.95,

            )

        # ------------------------------------------------

        if skills:

            return IntentResult(

                intent="technical_skill",

                confidence=0.93,

            )

        # ------------------------------------------------

        if metrics:

            return IntentResult(

                intent="performance",

                confidence=0.92,

            )

        # ------------------------------------------------

        if domains:

            return IntentResult(

                intent="operations",

                confidence=0.90,

            )

        return IntentResult(

            intent="statement",

            confidence=0.80,

        )