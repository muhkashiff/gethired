from .base_extractor import BaseExtractor


class ExperienceExtractor(BaseExtractor):

    def extract(self, lines):

        return self.clean(lines)