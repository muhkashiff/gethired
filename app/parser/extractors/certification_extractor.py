from .base_extractor import BaseExtractor


class CertificationExtractor(BaseExtractor):

    def extract(self, lines):

        return self.clean(lines)