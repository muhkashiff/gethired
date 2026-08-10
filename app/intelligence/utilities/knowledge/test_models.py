from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from app.intelligence.utilities.knowledge.repository_v5.repository import (
    Repository,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.domain_models import (
    DomainKnowledge,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.domain_extractor import (
    DomainExtractor,
)


####################################################################
# ASSERTION HELPERS
####################################################################

def check(
    condition,
    description,
):
    """
    Print PASS/FAIL for an individual assertion.
    """

    if condition:

        print(
            f"   PASS: {description}"
        )

        return True

    print(
        f"   FAIL: {description}"
    )

    return False


####################################################################
# RESULT DISPLAY
####################################################################

def print_result(
    test_number,
    sentence,
    result,
):

    print(
        "\n"
        + "=" * 80
    )

    print(
        f"TEST #{test_number}"
    )

    print(
        f"SENTENCE: {sentence}"
    )

    print(
        "\nResult object:"
    )

    print(
        result
    )

    print(
        "\nDomain:"
    )

    print(
        f"Found:              {result.found}"
    )

    print(
        f"Canonical:           {result.canonical}"
    )

    print(
        f"Entity ID:           {result.entity_id}"
    )

    print(
        f"Entity Type:         {result.entity_type}"
    )

    print(
        f"Ontology:            {result.ontology_name}"
    )

    print(
        f"Category:            {result.category}"
    )

    print(
        f"Business Area:       {result.business_area}"
    )

    print(
        f"Domain Family:       {result.domain_family}"
    )

    print(
        f"Parent Domain:       {result.parent_domain}"
    )

    print(
        f"Business Function:   {result.business_function}"
    )

    print(
        "\nClassification:"
    )

    print(
        f"Strategic:           {result.strategic}"
    )

    print(
        f"Operational:         {result.operational}"
    )

    print(
        f"Technical:           {result.technical}"
    )

    print(
        f"Compliance:          {result.compliance}"
    )

    print(
        f"Management:          {result.management}"
    )

    print(
        "\nEnterprise:"
    )

    print(
        f"Enterprise Level:    {result.enterprise_level}"
    )

    print(
        f"Criticality:         {result.criticality}"
    )

    print(
        "\nReasoning:"
    )

    print(
        f"Reasoning ID:        {result.reasoning_id}"
    )

    print(
        f"Reasoning Confidence:{result.reasoning_confidence}"
    )

    print(
        f"Primary Domain:      {result.primary_domain}"
    )

    print(
        f"Secondary Domains:   {result.secondary_domains}"
    )

    print(
        f"Trigger Actions:     {result.trigger_actions}"
    )

    print(
        f"Trigger Objects:     {result.trigger_objects}"
    )

    print(
        f"Trigger Skills:      {result.trigger_skills}"
    )

    print(
        f"Trigger Metrics:     {result.trigger_metrics}"
    )

    print(
        f"Trigger Certifications: {result.trigger_certifications}"
    )

    print(
        "\nResult:",
        "PASS" if result.found else "FAIL",
    )


####################################################################
# DOMAIN RESOLUTION TESTS
####################################################################

def test_domain_resolution(
    repository,
):

    print(
        "\n"
        + "=" * 80
    )

    print(
        "DOMAIN REPOSITORY RESOLUTION TESTS"
    )

    print(
        "=" * 80
    )

    tests = [

        (
            "Operations",
            "Operations",
            "DOMAIN_OPERATIONS",
        ),

        (
            "operations",
            "Operations",
            "DOMAIN_OPERATIONS",
        ),

        (
            "Manufacturing",
            "Manufacturing",
            "DOMAIN_MANUFACTURING",
        ),

        (
            "Food Safety",
            "Food Safety",
            "DOMAIN_FOOD_SAFETY",
        ),

        (
            "Quality Management",
            "Quality",
            "DOMAIN_QUALITY",
        ),

        (
            "Supply Chain",
            "Supply Chain",
            "DOMAIN_SUPPLY_CHAIN",
        ),

        (
            "Leadership",
            "Leadership",
            "DOMAIN_LEADERSHIP",
        ),

    ]

    passed = 0

    failed = 0

    for phrase, expected_canonical, expected_id in tests:

        entity = repository.find_entity(
            "domains",
            phrase,
        )

        if entity is None:

            print(
                f"   FAIL: {phrase} -> NOT FOUND"
            )

            failed += 1

            continue

        canonical_ok = (
            entity.canonical
            == expected_canonical
        )

        id_ok = (
            entity.entity_id
            == expected_id
        )

        if canonical_ok and id_ok:

            print(
                f"   PASS: {phrase} "
                f"-> {entity.canonical} "
                f"({entity.entity_id})"
            )

            passed += 1

        else:

            print(
                f"   FAIL: {phrase} "
                f"-> {entity.canonical} "
                f"({entity.entity_id})"
            )

            failed += 1

    print(
        "\nDomain repository tests:"
    )

    print(
        f"   Passed: {passed}"
    )

    print(
        f"   Failed: {failed}"
    )

    return passed, failed


####################################################################
# DOMAIN EXTRACTION TESTS
####################################################################

def test_domain_extraction(
    extractor,
):

    print(
        "\n"
        + "=" * 80
    )

    print(
        "DOMAIN EXTRACTION TESTS"
    )

    print(
        "=" * 80
    )

    tests = [

        (
            1,
            "Operations",
        ),

        (
            2,
            "Manufacturing",
        ),

        (
            3,
            "Food Safety",
        ),

        (
            4,
            "Quality Management",
        ),

        (
            5,
            "Supply Chain",
        ),

        (
            6,
            "Leadership",
        ),

    ]

    passed = 0

    failed = 0

    for test_number, sentence in tests:

        result = extractor.extract(
            sentence
        )

        print_result(
            test_number,
            sentence,
            result,
        )

        if result.found:

            passed += 1

        else:

            failed += 1

    print(
        "\nDomain extraction tests:"
    )

    print(
        f"   Passed: {passed}"
    )

    print(
        f"   Failed: {failed}"
    )

    return passed, failed


####################################################################
# ALIAS TESTS
####################################################################

def test_domain_aliases(
    repository,
    extractor,
):

    print(
        "\n"
        + "=" * 80
    )

    print(
        "DOMAIN ALIAS TESTS"
    )

    print(
        "=" * 80
    )

    tests = [

        (
            "quality management",
            "DOMAIN_QUALITY",
        ),

        (
            "quality management system",
            "DOMAIN_QUALITY",
        ),

        (
            "qms",
            "DOMAIN_QUALITY",
        ),

        (
            "food-safety",
            "DOMAIN_FOOD_SAFETY",
        ),

        (
            "supply-chain",
            "DOMAIN_SUPPLY_CHAIN",
        ),

    ]

    passed = 0

    failed = 0

    for phrase, expected_id in tests:

        entity = repository.find_entity(
            "domains",
            phrase,
        )

        if entity is not None:

            if entity.entity_id == expected_id:

                print(
                    f"   PASS: {phrase} "
                    f"-> {entity.canonical} "
                    f"({entity.entity_id})"
                )

                passed += 1

            else:

                print(
                    f"   FAIL: {phrase} "
                    f"-> WRONG ENTITY "
                    f"({entity.entity_id})"
                )

                failed += 1

        else:

            print(
                f"   FAIL: {phrase} "
                f"-> NOT FOUND"
            )

            failed += 1

    print(
        "\nDomain alias tests:"
    )

    print(
        f"   Passed: {passed}"
    )

    print(
        f"   Failed: {failed}"
    )

    return passed, failed


####################################################################
# NEGATIVE TESTS
####################################################################

def test_negative_cases(
    repository,
    extractor,
):

    print(
        "\n"
        + "=" * 80
    )

    print(
        "NEGATIVE DOMAIN TESTS"
    )

    print(
        "=" * 80
    )

    tests = [

        None,

        "",

        "This domain does not exist",

        "Random XYZ domain",

    ]

    passed = 0

    failed = 0

    for phrase in tests:

        result = extractor.extract(
            phrase
        )

        if not result.found:

            print(
                f"   PASS: {phrase!r} "
                "-> correctly not found"
            )

            passed += 1

        else:

            print(
                f"   FAIL: {phrase!r} "
                "-> unexpected domain found"
            )

            failed += 1

    print(
        "\nNegative tests:"
    )

    print(
        f"   Passed: {passed}"
    )

    print(
        f"   Failed: {failed}"
    )

    return passed, failed


####################################################################
# DOMAIN REASONING TEST
####################################################################

def test_leadership_reasoning(
    extractor,
):

    print(
        "\n"
        + "=" * 80
    )

    print(
        "DOMAIN REASONING TEST"
    )

    print(
        "=" * 80
    )

    result = extractor.extract(
        "Leadership"
    )

    passed = 0

    failed = 0

    ################################################################
    # BASIC DOMAIN
    ################################################################

    print(
        "\n1. Basic Domain"
    )

    checks = [

        (
            result.found,
            "Leadership domain found",
        ),

        (
            result.canonical == "Leadership",
            "Canonical = Leadership",
        ),

        (
            result.entity_id
            == "DOMAIN_LEADERSHIP",
            "Entity ID = DOMAIN_LEADERSHIP",
        ),

        (
            result.entity_type == "domain",
            "Entity type = domain",
        ),

        (
            result.ontology_name == "domains",
            "Ontology = domains",
        ),

    ]

    for condition, description in checks:

        if check(
            condition,
            description,
        ):

            passed += 1

        else:

            failed += 1

    ################################################################
    # REASONING ID
    ################################################################

    print(
        "\n2. Reasoning Identity"
    )

    checks = [

        (
            result.reasoning_id
            == "REASON_LEADERSHIP",
            "Reasoning ID = REASON_LEADERSHIP",
        ),

        (
            result.reasoning_confidence
            == 0.99,
            "Reasoning confidence = 0.99",
        ),

        (
            result.reasoning_object
            is not None,
            "Reasoning object exists",
        ),

    ]

    for condition, description in checks:

        if check(
            condition,
            description,
        ):

            passed += 1

        else:

            failed += 1

    ################################################################
    # PRIMARY / SECONDARY DOMAINS
    ################################################################

    print(
        "\n3. Domain Relationships"
    )

    checks = [

        (
            result.primary_domain
            == "leadership",
            "Primary domain = leadership",
        ),

        (
            result.secondary_domains
            == [
                "people_management",
                "operations_management",
                "strategic_management",
            ],
            "Secondary domains are correct",
        ),

    ]

    for condition, description in checks:

        if check(
            condition,
            description,
        ):

            passed += 1

        else:

            failed += 1

    ################################################################
    # TRIGGER ACTIONS
    ################################################################

    print(
        "\n4. Trigger Actions"
    )

    expected_actions = [

        "ACT_LEAD",
        "ACT_DIRECT",
        "ACT_MANAGE",
        "ACT_SUPERVISE",
        "ACT_GUIDE",
        "ACT_MENTOR",
        "ACT_COACH",
        "ACT_DELEGATE",

    ]

    if check(
        result.trigger_actions
        == expected_actions,
        "All leadership trigger actions are correct",
    ):

        passed += 1

    else:

        failed += 1

    ################################################################
    # TRIGGER OBJECTS
    ################################################################

    print(
        "\n5. Trigger Objects"
    )

    expected_objects = [

        "OBJ_TEAM",
        "OBJ_EMPLOYEES",
        "OBJ_ENGINEERS",
        "OBJ_OPERATORS",
        "OBJ_DEPARTMENT",

    ]

    if check(
        result.trigger_objects
        == expected_objects,
        "All leadership trigger objects are correct",
    ):

        passed += 1

    else:

        failed += 1

    ################################################################
    # TRIGGER SKILLS
    ################################################################

    print(
        "\n6. Trigger Skills"
    )

    expected_skills = [

        "SKILL_LEADERSHIP",
        "SKILL_TEAM_BUILDING",
        "SKILL_COACHING",
        "SKILL_MENTORING",
        "SKILL_STAKEHOLDER_MANAGEMENT",

    ]

    if check(
        result.trigger_skills
        == expected_skills,
        "All leadership trigger skills are correct",
    ):

        passed += 1

    else:

        failed += 1

    ################################################################
    # TRIGGER METRICS
    ################################################################

    print(
        "\n7. Trigger Metrics"
    )

    expected_metrics = [

        "KPI_EMPLOYEE_ENGAGEMENT",
        "KPI_PRODUCTIVITY",
        "KPI_TRAINING",
        "KPI_RETENTION",

    ]

    if check(
        result.trigger_metrics
        == expected_metrics,
        "All leadership trigger metrics are correct",
    ):

        passed += 1

    else:

        failed += 1

    ################################################################
    # TRIGGER CERTIFICATIONS
    ################################################################

    print(
        "\n8. Trigger Certifications"
    )

    if check(
        result.trigger_certifications == [],
        "Leadership certifications list is empty",
    ):

        passed += 1

    else:

        failed += 1

    ################################################################
    # REASONING SUMMARY
    ################################################################

    print(
        "\nReasoning test:"
    )

    print(
        f"   Passed: {passed}"
    )

    print(
        f"   Failed: {failed}"
    )

    return passed, failed


####################################################################
# MAIN
####################################################################

def main():

    print(
        "\nStarting test_domain.py..."
    )

    ################################################################
    # 1. LOAD REPOSITORY
    ################################################################

    print(
        "\n1. Loading repository..."
    )

    repository = Repository()

    print(
        "   Repository initialized successfully"
    )

    ################################################################
    # 2. CREATE EXTRACTOR
    ################################################################

    print(
        "\n2. Creating DomainExtractor..."
    )

    extractor = DomainExtractor(
        repository=repository
    )

    print(
        "   DomainExtractor created"
    )

    ################################################################
    # 3. DOMAIN RESOLUTION
    ################################################################

    repository_passed, repository_failed = (
        test_domain_resolution(
            repository
        )
    )

    ################################################################
    # 4. DOMAIN EXTRACTION
    ################################################################

    extraction_passed, extraction_failed = (
        test_domain_extraction(
            extractor
        )
    )

    ################################################################
    # 5. ALIAS TESTS
    ################################################################

    alias_passed, alias_failed = (
        test_domain_aliases(
            repository,
            extractor,
        )
    )

    ################################################################
    # 6. NEGATIVE TESTS
    ################################################################

    negative_passed, negative_failed = (
        test_negative_cases(
            repository,
            extractor,
        )
    )

    ################################################################
    # 7. REASONING TEST
    ################################################################

    reasoning_passed, reasoning_failed = (
        test_leadership_reasoning(
            extractor
        )
    )

    ################################################################
    # 8. FINAL SUMMARY
    ################################################################

    total_passed = (
        repository_passed
        + extraction_passed
        + alias_passed
        + negative_passed
        + reasoning_passed
    )

    total_failed = (
        repository_failed
        + extraction_failed
        + alias_failed
        + negative_failed
        + reasoning_failed
    )

    total_tests = (
        total_passed
        + total_failed
    )

    print(
        "\n"
        + "=" * 80
    )

    print(
        "FINAL DOMAIN TEST SUMMARY"
    )

    print(
        "=" * 80
    )

    print(
        f"Total assertions:   {total_tests}"
    )

    print(
        f"Passed:             {total_passed}"
    )

    print(
        f"Failed:             {total_failed}"
    )

    print(
        "=" * 80
    )

    if total_failed == 0:

        print(
            "\nALL DOMAIN TESTS PASSED"
        )

        print(
            "Domain resolution:       PASS"
        )

        print(
            "Domain extraction:       PASS"
        )

        print(
            "Domain aliases:          PASS"
        )

        print(
            "Negative handling:       PASS"
        )

        print(
            "Domain reasoning:        PASS"
        )

    else:

        print(
            "\nSOME DOMAIN TESTS FAILED"
        )

        print(
            "\nReview the FAIL lines above."
        )


####################################################################
# ENTRY POINT
####################################################################

if __name__ == "__main__":

    main()