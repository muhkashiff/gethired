def test_prefer_is_not_classified_as_responsibility(self):
    profile = make_document_profile(
        statements=[
            {
                "statement_id": "PREFER-1",
                "text": (
                    "Industry experience in restaurants, "
                    "food manufacturing, or central production "
                    "facilities is highly preferred."
                ),
            }
        ],
        entities=[
            {
                "entity_id": "P1",
                "statement_id": "PREFER-1",
                "entity_type": "action",
                "canonical": "Prefer",
                "confidence": 0.95,
            },
            {
                "entity_id": "P2",
                "statement_id": "PREFER-1",
                "entity_type": "domain",
                "canonical": "Food Manufacturing",
                "confidence": 0.90,
            },
        ],
    )

    result = self.classifier.process(profile)

    prefer_requirements = [
        requirement
        for requirement in result.requirements
        if requirement.subject.casefold() == "prefer"
    ]

    assert prefer_requirements == []

    responsibility_requirements = [
        requirement
        for requirement in result.requirements
        if requirement.requirement_type
        == RequirementType.RESPONSIBILITY
    ]

    assert all(
        requirement.subject.casefold() != "prefer"
        for requirement in responsibility_requirements
    )