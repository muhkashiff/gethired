"""
Business Statement Profile Builder
Enterprise V14
"""

from __future__ import annotations

from typing import Any

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import (
    BusinessStatementProfile,
)


class BusinessStatementProfileBuilder:

    def build(
        self,
        statements=None,
    ) -> BusinessStatementProfile:

        profile = (
            BusinessStatementProfile()
        )

        if statements is None:
            return profile

        for statement in statements:

            if isinstance(
                statement,
                dict,
            ):

                record = dict(
                    statement
                )

            else:

                record = dict(
                    getattr(
                        statement,
                        "__dict__",
                        {},
                    )
                )

            profile.statements.append(
                record
            )

        profile.total_statements = len(
            profile.statements
        )

        return profile