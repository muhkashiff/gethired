"""
Enterprise Repository Surface Forms

Builds safe textual forms that may represent
a repository entity in natural language.
"""

from typing import List


class RepositorySurfaceForms:

    ############################################################
    # BUILD
    ############################################################

    @staticmethod
    def build(entity) -> List[str]:

        forms = []

        ########################################################
        # Canonical
        ########################################################

        canonical = (
            entity.canonical or ""
        ).strip()

        if canonical:
            forms.append(canonical)

        ########################################################
        # Aliases
        ########################################################

        for alias in entity.aliases:

            alias = (
                alias or ""
            ).strip()

            if alias:
                forms.append(alias)

        ########################################################
        # Vendor / brand prefix removal
        ########################################################
        #
        # Example:
        #
        # Microsoft Azure
        #       ↓
        # Azure
        #
        # Microsoft Power BI
        #       ↓
        # Power BI
        #
        # Microsoft Excel
        #       ↓
        # Excel
        #
        ########################################################

        words = canonical.split()

        if len(words) >= 2:

            first_word = words[0].casefold()

            vendor_words = {
                "microsoft",
                "amazon",
                "google",
                "ibm",
                "oracle",
                "sap",
            }

            if first_word in vendor_words:

                shortened = " ".join(
                    words[1:]
                )

                if shortened:
                    forms.append(shortened)

        ########################################################
        # Remove duplicates
        ########################################################

        unique = []

        seen = set()

        for form in forms:

            normalized = (
                form.casefold().strip()
            )

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(normalized)

            unique.append(normalized)

        return unique