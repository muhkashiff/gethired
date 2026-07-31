"""
Business Intent Resolver

Determines WHY a business statement exists.
"""

from dataclasses import dataclass


# ==========================================================
# Intent Result
# ==========================================================

@dataclass
class IntentResult:

    # Main semantic classification
    intent: str = ""

    # Backward compatibility
    semantic_type: str = ""

    # Enterprise metadata
    primary_domain: str = ""

    business_area: str = ""

    achievement: bool = False

    confidence: float = 0.0

    def __post_init__(self):
        # Keep both names synchronized
        if not self.semantic_type:
            self.semantic_type = self.intent


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

        # =====================================================
        # Compliance
        # =====================================================

        if action in {
            "implement",
            "certify",
            "audit",
            "validate",
        } and standards:

            return IntentResult(
                intent="compliance",
                primary_domain="Quality",
                business_area="Food Safety",
                achievement=True,
                confidence=0.99,
            )

        # =====================================================
        # Continuous Improvement
        # =====================================================

        if action in {
            "improve",
            "optimize",
            "reduce",
            "increase",
        }:

            return IntentResult(
                intent="continuous_improvement",
                primary_domain="Operations",
                business_area="Continuous Improvement",
                achievement=True,
                confidence=0.99,
            )

        # =====================================================
        # Leadership
        # =====================================================

        if action == "lead":

            return IntentResult(
                intent="leadership",
                primary_domain="Management",
                business_area="Leadership",
                achievement=False,
                confidence=0.98,
            )

        # =====================================================
        # Operations Management
        # =====================================================

        if action == "manage":

            if objects:

                return IntentResult(
                    intent="operations_management",
                    primary_domain="Operations",
                    business_area="Operations",
                    achievement=False,
                    confidence=0.98,
                )

            return IntentResult(
                intent="leadership",
                primary_domain="Management",
                business_area="Leadership",
                achievement=False,
                confidence=0.94,
            )

        # =====================================================
        # Problem Solving
        # =====================================================

        if action == "perform":

            if methodologies:

                return IntentResult(
                    intent="problem_solving",
                    primary_domain="Quality",
                    business_area="Root Cause Analysis",
                    achievement=False,
                    confidence=0.97,
                )

            return IntentResult(
                intent="execution",
                primary_domain="Operations",
                business_area="Execution",
                achievement=False,
                confidence=0.90,
            )

        # =====================================================
        # Development
        # =====================================================

        if action in {
            "develop",
            "design",
            "build",
        }:

            if standards:

                return IntentResult(
                    intent="compliance",
                    primary_domain="Quality",
                    business_area="Food Safety",
                    achievement=True,
                    confidence=0.96,
                )

            return IntentResult(
                intent="development",
                primary_domain="Engineering",
                business_area="Development",
                achievement=False,
                confidence=0.95,
            )

        # =====================================================
        # Technical Skills
        # =====================================================

        if skills:

            return IntentResult(
                intent="technical_skill",
                primary_domain="Technical",
                business_area="Technical Skills",
                achievement=False,
                confidence=0.93,
            )

        # =====================================================
        # Performance
        # =====================================================

        if metrics:

            return IntentResult(
                intent="performance",
                primary_domain="Operations",
                business_area="Performance",
                achievement=True,
                confidence=0.92,
            )

        # =====================================================
        # Operations
        # =====================================================

        if domains:

            domain_name = statement.domains[0].canonical if statement.domains else "Operations"

            return IntentResult(
                intent="operations",
                primary_domain=domain_name,
                business_area=statement.domains[0].business_area if statement.domains else "Operations",
                achievement=False,
                confidence=0.90,
            )

        # =====================================================
        # Default
        # =====================================================

        return IntentResult(
            intent="statement",
            primary_domain="General",
            business_area="General",
            achievement=False,
            confidence=0.80,
        )