from .normalize import TextNormalizer


class KnowledgeMatcher:

    def find_matches(self, text, knowledge):

        text = TextNormalizer.normalize(text)

        matches = []

        for item in knowledge:

            names = [item["name"]] + item.get("aliases", [])

            for candidate in names:

                candidate = TextNormalizer.normalize(candidate)

                if candidate in text:

                    matches.append(item["name"])

                    break

        return sorted(set(matches))