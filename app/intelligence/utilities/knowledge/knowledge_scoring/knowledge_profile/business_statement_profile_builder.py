"""
Business Statement Profile Builder
Enterprise V14 - FIXED
"""

from __future__ import annotations

from typing import Any

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import (
    BusinessStatementProfile,
)


class BusinessStatementProfileBuilder:

    def build(
        self,
        statements: list = None,
        result: Any = None,
    ) -> BusinessStatementProfile:

        profile = BusinessStatementProfile()

        # Try multiple sources for business statements
        all_statements = []
        
        if statements:
            all_statements.extend(statements)
        
        if result:
            # Try different possible locations in result
            for attr in [
                "business_statements",
                "statements",
                "business_statement",
                "business_statement_list",
            ]:
                try:
                    stmts = getattr(result, attr, None)
                    if stmts:
                        if isinstance(stmts, list):
                            all_statements.extend(stmts)
                        else:
                            all_statements.append(stmts)
                except Exception:
                    pass

        if not all_statements:
            return profile

        for statement in all_statements:
            if isinstance(statement, dict):
                record = dict(statement)
            else:
                # Try to extract data from object
                record = {}
                
                # Get all attributes
                for key in dir(statement):
                    if not key.startswith("_"):
                        try:
                            value = getattr(statement, key)
                            if not callable(value):
                                record[key] = value
                        except Exception:
                            pass
                
                # If there's a to_dict method, use it
                if hasattr(statement, "to_dict"):
                    try:
                        record = statement.to_dict()
                    except Exception:
                        pass

            # Ensure required fields
            if "text" not in record:
                record["text"] = record.get("statement_text", "")
            if "type" not in record:
                record["type"] = record.get("statement_type", "general")

            profile.statements.append(record)

        profile.total_statements = len(profile.statements)

        return profile