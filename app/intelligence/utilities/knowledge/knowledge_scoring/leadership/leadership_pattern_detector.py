"""
Leadership Pattern Detector
"""

from app.intelligence.eng_models.leadership_pattern import LeadershipPattern

from app.intelligence.eng_knowledge.leadership_loader import LeadershipKnowledge


class LeadershipPatternDetector:

    def __init__(self):

        self.knowledge = LeadershipKnowledge()

    def detect(self, sentence):

        sentence_lower = sentence.lower()

        patterns = []

        for rule in self.knowledge.get_patterns():

            matched = []

            for keyword in rule["keywords"]:

                if keyword.lower() in sentence_lower:

                    matched.append(keyword)

            if matched:

                pattern = LeadershipPattern(

                    text=sentence,

                    dimensions=rule["dimensions"],

                    weight=rule["base_weight"],

                    matched_keywords=matched

                )

                patterns.append(pattern)

        return patterns