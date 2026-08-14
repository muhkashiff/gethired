from .base_non_ontology_extractor import BaseParserExtractor


class PublicationExtractor(BaseParserExtractor):

    def extract(self, lines):

        return self.clean(lines)