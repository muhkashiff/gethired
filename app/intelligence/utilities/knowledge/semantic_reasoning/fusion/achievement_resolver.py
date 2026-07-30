"""
Achievement Resolver

Determines whether a semantic cluster represents

    Achievement
    Responsibility
    Task
    Contribution

instead of relying only on measurements.
"""


class AchievementResolver:

    """
    Classifies business statements.
    """

    def __init__(self):

        self.achievement_actions = {

            "implement",
            "improve",
            "increase",
            "reduce",
            "optimize",
            "develop",
            "establish",
            "design",
            "create",
            "certify",
            "launch",
            "deliver",

        }

        self.responsibility_actions = {

            "manage",
            "lead",
            "supervise",
            "coordinate",
            "direct",

        }

        self.task_actions = {

            "perform",
            "inspect",
            "monitor",
            "review",
            "prepare",
            "maintain",

        }

        self.support_actions = {

            "assist",
            "support",
            "help",

        }

    # -----------------------------------------------------

    def resolve(self, interpretation):

        action = interpretation.action.base.lower()

        if action in self.achievement_actions:

            interpretation.achievement = True

            interpretation.semantic_type = "achievement"

            return interpretation

        if action in self.responsibility_actions:

            interpretation.semantic_type = "responsibility"

            return interpretation

        if action in self.task_actions:

            interpretation.semantic_type = "task"

            return interpretation

        if action in self.support_actions:

            interpretation.semantic_type = "contribution"

            return interpretation

        interpretation.semantic_type = "statement"

        return interpretation