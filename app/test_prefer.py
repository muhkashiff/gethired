from app.intelligence.utilities.knowledge.jd_requirements.requirement_classifier import (
    JDRequirementClassifier,
)

classifier = JDRequirementClassifier()

text = (
    "Industry experience in restaurants, food manufacturing, "
    "or central production facilities is highly preferred."
)

priority = classifier._priority(
    text,
    statement={},
)

print("TEXT:")
print(text)

print()
print("PRIORITY:")
print(priority)

print()
print("PRIORITY VALUE:")
print(priority.value)