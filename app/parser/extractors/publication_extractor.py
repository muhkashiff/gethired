from .base_extractor import BaseExtractor


class PublicationExtractor(BaseExtractor):

    def extract(self, lines):

        return self.clean(lines)