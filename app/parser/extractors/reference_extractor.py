"""
Reference Extractor
"""

from app.parser.models import Reference


class ReferenceExtractor:

    def extract(self, lines):

        if not lines:
            return []

        text = " ".join(lines).lower()

        if "available upon request" in text:
            return [
                Reference(
                    available_on_request=True
                )
            ]

        references = []

        current = Reference()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if current.name == "":
                current.name = line

            elif current.designation == "":
                current.designation = line

            else:
                current.notes += line + " "

        references.append(current)

        return references