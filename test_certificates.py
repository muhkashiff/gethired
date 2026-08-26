from app.intelligence.utilities.knowledge.jd_requirements.requirement_classifier import (
    JDRequirementClassifier,
)


def test_prefer_diagnostic():
    classifier = JDRequirementClassifier()

    text = (
        "Industry experience in restaurants, food manufacturing, "
        "or central production facilities is highly preferred."
    )

    print("\n" + "=" * 80)
    print("PREFERENCE DIAGNOSTIC")
    print("=" * 80)

    print("\nINPUT TEXT:")
    print(text)

    print("\nPREFERRED LANGUAGE:")
    print(
        classifier._contains_preferred_language(
            text.casefold()
        )
    )

    print("\nREQUIRED LANGUAGE:")
    print(
        classifier._contains_required_language(
            text.casefold()
        )
    )

    print("\nPRIORITY:")
    print(
        classifier._priority(
            text,
            {},
        )
    )

    print("\nPRIORITY VALUE:")
    print(
        classifier._priority(
            text,
            {},
        ).value
    )

    print("=" * 80)