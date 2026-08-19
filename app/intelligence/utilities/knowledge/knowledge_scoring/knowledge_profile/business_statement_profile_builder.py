"""
Business Statement Profile Builder
Enterprise V14 - FIXED
"""

from __future__ import annotations

from typing import Any

from .profile_models import BusinessStatementProfile


class BusinessStatementProfileBuilder:

    def build(
        self,
        statements: list = None,
        result: Any = None,
    ) -> BusinessStatementProfile:

        profile = BusinessStatementProfile()

        # Try multiple sources for business statements
        all_statements = []
        
        # Source 1: Direct statements parameter
        if statements:
            all_statements.extend(self._as_list(statements))
            print(f"[DEBUG] Got {len(all_statements)} statements from parameter")
        
        # Source 2: From result object
        if result:
            # Try different attribute names
            for attr in [
                "business_statements",
                "statements",
                "business_statement",
                "business_statement_list",
                "business_statements_list",
            ]:
                try:
                    stmts = getattr(result, attr, None)
                    if stmts:
                        stmts_list = self._as_list(stmts)
                        if stmts_list:
                            all_statements.extend(stmts_list)
                            print(f"[DEBUG] Got {len(stmts_list)} statements from result.{attr}")
                            break
                except Exception as e:
                    print(f"[DEBUG] Error accessing result.{attr}: {e}")
            
            # If result is a dict
            if isinstance(result, dict):
                for key in [
                    "business_statements",
                    "statements",
                    "business_statement",
                ]:
                    if key in result:
                        stmts = result[key]
                        if stmts:
                            stmts_list = self._as_list(stmts)
                            if stmts_list:
                                all_statements.extend(stmts_list)
                                print(f"[DEBUG] Got {len(stmts_list)} statements from dict['{key}']")
                                break
        
        # Source 3: From knowledge document if available
        if result and hasattr(result, 'knowledge_document'):
            doc = result.knowledge_document
            if doc:
                if hasattr(doc, 'statements'):
                    stmts = self._as_list(doc.statements)
                    if stmts:
                        all_statements.extend(stmts)
                        print(f"[DEBUG] Got {len(stmts)} statements from document.statements")
                if hasattr(doc, 'business_statements'):
                    stmts = self._as_list(doc.business_statements)
                    if stmts:
                        all_statements.extend(stmts)
                        print(f"[DEBUG] Got {len(stmts)} statements from document.business_statements")

        # If no statements found, try to create from facts
        if not all_statements and result:
            if hasattr(result, 'facts'):
                facts = self._as_list(result.facts)
                if facts:
                    all_statements = self._create_statements_from_facts(facts)
                    print(f"[DEBUG] Created {len(all_statements)} statements from facts")

        # Build profile
        for statement in all_statements:
            if isinstance(statement, dict):
                record = dict(statement)
            else:
                # Try to extract data from object
                record = self._extract_statement_data(statement)
            
            # Ensure required fields
            if "text" not in record:
                record["text"] = record.get("statement_text", record.get("text", ""))
            if "type" not in record:
                record["type"] = record.get("statement_type", "general")
            if "achievement" not in record:
                record["achievement"] = record.get("is_achievement", False)
            if "quantified" not in record:
                record["quantified"] = record.get("is_quantified", False)
            if "confidence" not in record:
                record["confidence"] = record.get("confidence_score", 0.5)
            
            profile.statements.append(record)

        profile.total_statements = len(profile.statements)
        print(f"[DEBUG] Final profile has {profile.total_statements} statements")

        return profile

    def _as_list(self, value) -> list:
        """Convert to list safely."""
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, set):
            return list(value)
        return [value]

    def _extract_statement_data(self, statement) -> dict:
        """Extract data from statement object."""
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
                dict_data = statement.to_dict()
                if isinstance(dict_data, dict):
                    record.update(dict_data)
            except Exception:
                pass
        
        # If there's a __dict__ attribute
        if hasattr(statement, "__dict__"):
            try:
                record.update(statement.__dict__)
            except Exception:
                pass
        
        return record

    def _create_statements_from_facts(self, facts: list) -> list:
        """Create business statements from facts."""
        statements = []
        
        for fact in facts:
            if isinstance(fact, dict):
                # If fact has text field
                if 'text' in fact:
                    statements.append(fact)
                else:
                    # Create a statement from fact data
                    statement = {
                        'text': fact.get('statement', fact.get('content', str(fact))),
                        'achievement': fact.get('achievement', False),
                        'quantified': fact.get('quantified', False),
                        'confidence': fact.get('confidence', 0.5),
                    }
                    statements.append(statement)
            else:
                # Try to get text from object
                text = None
                if hasattr(fact, 'text'):
                    text = fact.text
                elif hasattr(fact, 'statement'):
                    text = fact.statement
                elif hasattr(fact, 'content'):
                    text = fact.content
                
                if text:
                    statements.append({
                        'text': text,
                        'achievement': getattr(fact, 'achievement', False),
                        'quantified': getattr(fact, 'quantified', False),
                        'confidence': getattr(fact, 'confidence', 0.5),
                    })
        
        return statements