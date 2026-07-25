from collections import Counter


class SkillsAnalyzer:

    def analyze(self, skills):

        counter = Counter(skills)

        return {

            "skills": sorted(counter.keys()),

            "count": len(counter),

            "top": counter.most_common(20)

        }