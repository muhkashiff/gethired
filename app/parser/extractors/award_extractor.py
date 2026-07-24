from .base_extractor import BaseExtractor


class AwardExtractor(BaseExtractor):

    def extract(self, lines):

        return self.clean(lines)