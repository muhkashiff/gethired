from .base_extractor import BaseExtractor


class LanguageExtractor(BaseExtractor):

    def extract(self, lines):

        return self.clean(lines)