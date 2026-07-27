"""
Ontology Validator

Validates ontology integrity.

Checks

✓ required fields
✓ duplicate IDs
✓ duplicate canonicals
✓ aliases
"""

from collections import Counter


class OntologyValidator:

    REQUIRED_FIELDS = [

        "id",

        "canonical",

        "aliases",

        "category",

        "business_area",

    ]

    # -------------------------------------------------

    def validate_entity(self, entity):

        errors = []

        for field in self.REQUIRED_FIELDS:

            if field not in entity:

                errors.append(f"Missing field : {field}")

        if "aliases" in entity:

            if not isinstance(entity["aliases"], list):

                errors.append("aliases must be list")

        return errors

    # -------------------------------------------------

    def validate_dictionary(self, dictionary):

        report = {}

        ids = []

        canonicals = []

        for key, entity in dictionary.items():

            report[key] = self.validate_entity(entity)

            if "id" in entity:

                ids.append(entity["id"])

            if "canonical" in entity:

                canonicals.append(entity["canonical"].lower())

        duplicate_ids = [

            item

            for item, count in Counter(ids).items()

            if count > 1

        ]

        duplicate_canonicals = [

            item

            for item, count in Counter(canonicals).items()

            if count > 1

        ]

        return {

            "entity_report": report,

            "duplicate_ids": duplicate_ids,

            "duplicate_canonicals": duplicate_canonicals,

        }