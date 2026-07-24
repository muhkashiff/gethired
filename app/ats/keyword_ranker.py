from collections import Counter


class KeywordRanker:

    def rank(self, resume):

        text = " ".join(resume.experience)

        words = text.lower().split()

        return Counter(words).most_common(50)