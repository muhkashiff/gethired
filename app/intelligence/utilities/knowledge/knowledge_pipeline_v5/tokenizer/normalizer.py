"""
Enterprise Normalizer
Enterprise V5
"""

import re


class Normalizer:

    def normalize(self, phrase: str) -> str:

        if phrase is None:
            return ""

        text = phrase.lower().strip()

        # remove spaces between standard names

        text = re.sub(r"iso[\s\-]*9001", "iso9001", text)
        text = re.sub(r"iso[\s\-]*22000", "iso22000", text)
        text = re.sub(r"fssc[\s\-]*22000", "fssc22000", text)

        # remove spaces

        text = re.sub(r"\s+", "", text)

        return text