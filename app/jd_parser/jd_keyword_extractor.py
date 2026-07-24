import re
from collections import Counter


class JDKeywordExtractor:

    STOP_WORDS = {

        "the",
        "a",
        "an",
        "of",
        "to",
        "for",
        "with",
        "and",
        "or",
        "is",
        "are",
        "on",
        "in",
        "at",
        "as",
        "our",
        "your",
        "their",
        "will",
        "be"

    }

    def extract(self, text):

        words = re.findall(r"[A-Za-z][A-Za-z0-9+#.-]*", text.lower())

        words = [

            w

            for w in words

            if w not in self.STOP_WORDS

            and len(w) > 2

        ]

        return Counter(words).most_common(100)