from resume_intelligence.core.relation_matcher import RelationMatcher


class DependencyParser:

    def __init__(self):

        self.matcher = RelationMatcher()

    def parse(self, sentence, entities):

        edges = self.matcher.build_edges(entities)

        return {

            "sentence": sentence,

            "edges": edges,

            "confidence": round(

                sum(e.confidence for e in edges) /

                max(len(edges), 1),

                2,

            ),

        }