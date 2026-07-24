from app.knowledge.loader import KnowledgeLoader
from app.knowledge.matcher import KnowledgeMatcher

loader = KnowledgeLoader()

skills = loader.skills()

matcher = KnowledgeMatcher()

text = """
Experienced Quality Assurance professional with QA, HACCP,
CGMP, Food Safety Management System, SAP Quality Management,
Power BI and Python Programming.
"""

print(matcher.find_matches(text, skills))